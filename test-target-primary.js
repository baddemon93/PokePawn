const { chromium } = require("playwright");

(async () => {
  const url = process.argv[2];

  const browser = await chromium.launch({
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    locale: "en-US"
  });

  const page = await context.newPage();

  const blocked = [];

  page.on("response", response => {
    if (
      response.status() === 435 ||
      response.status() === 429 ||
      response.status() === 403
    ) {
      blocked.push({
        status: response.status(),
        method: response.request().method(),
        url: response.url()
      });
    }
  });

  await page.goto(url, {
    waitUntil: "domcontentloaded",
    timeout: 35000
  });

  console.log("HTTP page loaded");
  console.log("TITLE:", await page.title());

  for (const seconds of [0, 2, 5, 10, 20, 30]) {
    if (seconds > 0) {
      const previous =
        seconds === 2 ? 0 :
        seconds === 5 ? 2 :
        seconds === 10 ? 5 :
        seconds === 20 ? 10 : 20;

      await page.waitForTimeout(
        (seconds - previous) * 1000
      );
    }

    const result = await page.evaluate(() => {
      const selectors = [
        '[data-test="shippingButton"]',
        '[data-test="pickupButton"]',
        '[data-test="deliveryButton"]',
        '[data-test="orderPickupButton"]',
        '[data-test="shipItButton"]',
        '[data-test="addToCartButton"]',
        '#PICKUP',
        '#DELIVERY',
        '#SHIPPING'
      ];

      const controls = [];

      for (const selector of selectors) {
        for (
          const el of document.querySelectorAll(selector)
        ) {
          controls.push({
            selector,
            text:
              (el.innerText || el.textContent || "")
                .trim()
                .slice(0, 300),
            aria: el.getAttribute("aria-label"),
            disabled:
              "disabled" in el
                ? el.disabled
                : null,
            class:
              (el.className || "")
                .toString()
                .slice(0, 300)
          });
        }
      }

      const buttons =
        [...document.querySelectorAll("button")]
          .map(el => ({
            text:
              (el.innerText || "")
                .trim()
                .slice(0, 200),
            aria: el.getAttribute("aria-label"),
            disabled: el.disabled
          }))
          .filter(x =>
            /add to cart|pickup|shipping|delivery|ship it/i
              .test(
                `${x.text} ${x.aria || ""}`
              )
          );

      return {
        controls,
        buttons
      };
    });

    console.log(
      `\n===== ${seconds}s =====`
    );

    console.log(
      JSON.stringify(result, null, 2)
    );
  }

  console.log("\n===== BLOCKED REQUESTS =====");

  for (const x of blocked) {
    console.log(
      `${x.status} ${x.method} ${x.url}`
    );
  }

  await browser.close();
})();
