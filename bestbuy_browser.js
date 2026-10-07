const { chromium } = require('playwright');
const readline = require('readline');

const MAX_CONCURRENT = 3;

let browser = null;
let context = null;
let browserPromise = null;
let active = 0;
const queue = [];

async function ensureBrowser() {
    if (browser && context) {
        return;
    }

    if (!browserPromise) {
        browserPromise = (async () => {
            browser = await chromium.launch({
                headless: true
            });

            context = await browser.newContext({
                locale: 'en-US'
            });
        })().finally(() => {
            browserPromise = null;
        });
    }

    await browserPromise;
}

async function acquireSlot() {
    if (active < MAX_CONCURRENT) {
        active++;
        return;
    }

    await new Promise(resolve => queue.push(resolve));
    active++;
}

function releaseSlot() {
    active--;

    const next = queue.shift();
    if (next) {
        next();
    }
}

async function checkBestBuy(url) {
    await acquireSlot();

    const started = Date.now();
    let page = null;

    try {
        await ensureBrowser();

        page = await context.newPage();

        // Best Buy product pages contain a large amount of media and
        // third-party content that is irrelevant to stock detection.
        // Keep scripts/XHR/fetch enabled because the purchase controls
        // depend on them.
        await page.route('**/*', async route => {
            const request = route.request();
            const type = request.resourceType();

            if (
                type === 'image' ||
                type === 'font' ||
                type === 'media'
            ) {
                await route.abort();
                return;
            }

            await route.continue();
        });

        let response;
        let navigationMs = null;
        let controlWaitMs = null;

        try {
            const navStarted = Date.now();

            response = await page.goto(url, {
                waitUntil: 'domcontentloaded',
                timeout: 35000
            });

            navigationMs = Date.now() - navStarted;
        } catch (firstErr) {
            const firstMessage = String(
                firstErr && firstErr.message
                    ? firstErr.message
                    : ''
            );

            const retryable =
                firstErr?.name === 'TimeoutError' ||
                firstMessage.includes('ERR_HTTP2_PROTOCOL_ERROR');

            if (!retryable) {
                return {
                    ok: false,
                    stock: null,
                    price: null,
                    state: 'BROWSER_NAV_ERROR',
                    detail: `${firstErr?.name || 'Error'}: ${firstMessage || 'navigation error'}`,
                    elapsed: (Date.now() - started) / 1000,
                    navigation: navigationMs === null
                        ? null
                        : navigationMs / 1000,
                    controlWait: null
                };
            }

            try {
                // Stop the failed navigation before retrying.
                await page.evaluate(() => window.stop())
                    .catch(() => {});

                const retryStarted = Date.now();

                response = await page.goto(url, {
                    waitUntil: 'commit',
                    timeout: 20000
                });

                navigationMs = Date.now() - retryStarted;
            } catch (retryErr) {
                const retryMessage = String(
                    retryErr && retryErr.message
                        ? retryErr.message
                        : ''
                );

                const retryIsTimeout =
                    retryErr?.name === 'TimeoutError' ||
                    retryMessage
                        .toLowerCase()
                        .includes('timeout');

                return {
                    ok: false,
                    stock: null,
                    price: null,
                    state: retryIsTimeout
                        ? 'BROWSER_TIMEOUT'
                        : 'BROWSER_NAV_ERROR',
                    detail:
                        `initial: ${firstErr?.name || 'Error'}: ` +
                        `${firstMessage || 'navigation error'}; ` +
                        `retry: ${retryErr?.name || 'Error'}: ` +
                        `${retryMessage || 'navigation error'}`,
                    elapsed: (Date.now() - started) / 1000,
                    navigation: navigationMs === null
                        ? null
                        : navigationMs / 1000,
                    controlWait: null
                };
            }
        }

        const status = response ? response.status() : null;

        if (status !== 200) {
            return {
                ok: false,
                stock: null,
                price: null,
                state: `HTTP_${status}`,
                detail: 'Best Buy browser HTTP error',
                elapsed: (Date.now() - started) / 1000,
                navigation: navigationMs === null ? null : navigationMs / 1000,
                controlWait: controlWaitMs === null ? null : controlWaitMs / 1000
            };
        }

        // Wait for a purchase-state button instead of sleeping a
        // fixed eight seconds. Continue after the timeout because the
        // page may still contain useful availability information.
        const controlStarted = Date.now();

        try {
            await page.waitForFunction(() => {
                const labels = Array.from(
                    document.querySelectorAll('button')
                ).map(
                    el => (el.innerText || '').trim().toLowerCase()
                );

                return labels.some(text =>
                    text === 'add to cart' ||
                    text === 'unavailable' ||
                    text === 'sold out' ||
                    text === 'coming soon' ||
                    text === 'pre-order' ||
                    text === 'preorder'
                );
            }, {
                timeout: 12000
            });
        } catch (_) {}

        controlWaitMs = Date.now() - controlStarted;

        const title = await page.title().catch(() => '');
        const body = await page.locator('body').innerText()
            .catch(() => '');

        const bodyLower = body.toLowerCase();

        const challengeSignals = [
            'access denied',
            'verify you are a human',
            'are you a human',
            'captcha',
            'unusual traffic'
        ];

        if (challengeSignals.some(x => bodyLower.includes(x))) {
            return {
                ok: false,
                stock: null,
                price: null,
                state: 'CHALLENGE',
                detail: 'Best Buy browser challenge',
                title,
                elapsed: (Date.now() - started) / 1000,
                navigation: navigationMs === null ? null : navigationMs / 1000,
                controlWait: controlWaitMs === null ? null : controlWaitMs / 1000
            };
        }

        const buttons = await page.locator('button').allInnerTexts()
            .catch(() => []);

        const normalizedButtons = buttons
            .map(x => x.trim())
            .filter(Boolean);

        const findButton = regex =>
            normalizedButtons.find(x => regex.test(x));

        const addToCart = findButton(/^add to cart$/i);
        const soldOut = findButton(/^sold out$/i);
        const unavailable = findButton(/^unavailable$/i);
        const comingSoon = findButton(/^coming soon$/i);
        const preorder = findButton(/^pre[- ]?order$/i);

        let price = null;

        const priceMatch = body.match(/\$([\d,]+\.\d{2})/);

        if (priceMatch) {
            price = `$${priceMatch[1]}`;
        }

        if (addToCart) {
            // ---------------------------------------------------------
            // SELLER VERIFICATION
            //
            // Best Buy embeds information about multiple offers in the
            // page, so script/JSON seller fields alone are NOT enough.
            //
            // We verify the seller currently rendered in the active
            // purchase area.
            // ---------------------------------------------------------

            const sellerInfo = await page.evaluate(() => {
                const bodyText =
                    document.body?.innerText || '';

                // Match the rendered:
                //
                // Sold & shipped by
                // Best Buy
                //
                // or a Marketplace seller.
                const sellerMatch = bodyText.match(
                    /Sold\s*&\s*shipped\s*by\s*\n?\s*([^\n]+)/i
                );

                let seller = null;

                if (sellerMatch && sellerMatch[1]) {
                    seller = sellerMatch[1].trim();
                }

                const marketplace =
                    /More options from Marketplace sellers/i
                        .test(bodyText);

                return {
                    seller,
                    marketplace
                };
            });

            const seller =
                sellerInfo &&
                sellerInfo.seller
                    ? sellerInfo.seller.trim()
                    : null;

            const normalizedSeller =
                seller
                    ? seller
                        .toLowerCase()
                        .replace(/[^a-z0-9]/g, '')
                    : '';

            const isBestBuySeller =
                normalizedSeller === 'bestbuy';

            if (isBestBuySeller) {
                return {
                    ok: true,
                    stock: true,
                    price,
                    state: 'ADD_TO_CART_BESTBUY',
                    seller,
                    detail:
                        'Add to Cart rendered; sold & shipped by Best Buy',
                    title,
                    elapsed: (Date.now() - started) / 1000,
                    navigation:
                        navigationMs === null
                            ? null
                            : navigationMs / 1000,
                    controlWait:
                        controlWaitMs === null
                            ? null
                            : controlWaitMs / 1000
                };
            }

            if (seller) {
                return {
                    ok: true,
                    stock: false,
                    price,
                    state: 'MARKETPLACE',
                    seller,
                    detail:
                        `Marketplace seller: ${seller}`,
                    title,
                    elapsed: (Date.now() - started) / 1000,
                    navigation:
                        navigationMs === null
                            ? null
                            : navigationMs / 1000,
                    controlWait:
                        controlWaitMs === null
                            ? null
                            : controlWaitMs / 1000
                };
            }

            // Add to Cart without a readable active seller remains
            // neutral. Never generate a restock alert from it.
            return {
                ok: true,
                stock: null,
                price,
                state: 'ADD_TO_CART_UNVERIFIED',
                seller: null,
                detail:
                    'Add to Cart rendered; active seller unknown',
                title,
                elapsed: (Date.now() - started) / 1000,
                navigation:
                    navigationMs === null
                        ? null
                        : navigationMs / 1000,
                controlWait:
                    controlWaitMs === null
                        ? null
                        : controlWaitMs / 1000
            };
        }

        if (unavailable) {
            return {
                ok: true,
                stock: false,
                price,
                state: 'UNAVAILABLE',
                detail: 'Unavailable purchase button',
                title,
                elapsed: (Date.now() - started) / 1000,
                navigation: navigationMs === null ? null : navigationMs / 1000,
                controlWait: controlWaitMs === null ? null : controlWaitMs / 1000
            };
        }

        if (soldOut) {
            return {
                ok: true,
                stock: false,
                price,
                state: 'SOLD_OUT',
                detail: 'Sold Out purchase button',
                title,
                elapsed: (Date.now() - started) / 1000,
                navigation: navigationMs === null ? null : navigationMs / 1000,
                controlWait: controlWaitMs === null ? null : controlWaitMs / 1000
            };
        }

        if (comingSoon) {
            return {
                ok: true,
                stock: false,
                price,
                state: 'COMING_SOON',
                detail: 'Coming Soon purchase button',
                title,
                elapsed: (Date.now() - started) / 1000,
                navigation: navigationMs === null ? null : navigationMs / 1000,
                controlWait: controlWaitMs === null ? null : controlWaitMs / 1000
            };
        }

        if (preorder) {
            return {
                ok: true,
                stock: null,
                price,
                state: 'PRE_ORDER_UNVERIFIED',
                detail: 'Pre-order rendered; seller verification required',
                title,
                elapsed: (Date.now() - started) / 1000,
                navigation: navigationMs === null ? null : navigationMs / 1000,
                controlWait: controlWaitMs === null ? null : controlWaitMs / 1000
            };
        }

        return {
            ok: false,
            stock: null,
            price,
            state: 'UNKNOWN',
            detail: 'No recognized Best Buy purchase control',
            title,
            elapsed: (Date.now() - started) / 1000
        };

    } catch (err) {
        return {
            ok: false,
            stock: null,
            price: null,
            state: 'BROWSER_ERROR',
            detail: `${err.name || 'Error'}: ${err.message}`,
            elapsed: (Date.now() - started) / 1000
        };
    } finally {
        if (page) {
            try {
                await page.close();
            } catch (_) {}
        }

        releaseSlot();
    }
}

const rl = readline.createInterface({
    input: process.stdin,
    crlfDelay: Infinity
});

rl.on('line', line => {
    line = line.trim();

    if (!line) {
        return;
    }

    let request;

    try {
        request = JSON.parse(line);
    } catch (_) {
        process.stdout.write(JSON.stringify({
            ok: false,
            stock: null,
            state: 'BAD_REQUEST',
            detail: 'Invalid JSON'
        }) + '\n');

        return;
    }

    const id = request.id ?? null;
    const url = request.url;

    if (!url) {
        process.stdout.write(JSON.stringify({
            id,
            ok: false,
            stock: null,
            state: 'BAD_REQUEST',
            detail: 'Missing URL'
        }) + '\n');

        return;
    }

    checkBestBuy(url)
        .then(result => {
            result.id = id;
            process.stdout.write(JSON.stringify(result) + '\n');
        })
        .catch(err => {
            process.stdout.write(JSON.stringify({
                id,
                ok: false,
                stock: null,
                state: 'BROWSER_ERROR',
                detail: err.message
            }) + '\n');
        });
});

async function shutdown() {
    try {
        if (context) {
            await context.close();
        }
    } catch (_) {}

    try {
        if (browser) {
            await browser.close();
        }
    } catch (_) {}

    process.exit(0);
}

rl.on('close', shutdown);
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
