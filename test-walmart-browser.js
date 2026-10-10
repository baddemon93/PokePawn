const { chromium } = require("playwright");

(async () => {
  const url = process.argv[2];

  if (!url) {
    console.error("Usage: node test-walmart-browser.js <url>");
    process.exit(1);
  }

  const browser = await chromium.launch({
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    locale: "en-US"
  });

  const page = await context.newPage();

  const interesting = [];

  page.on("response", async response => {
    const u = response.url();

    if (
      /inventory|fulfillment|pickup|delivery|shipping|store|availability/i.test(u)
    ) {
      let body = "";

      try {
        const ct = response.headers()["content-type"] || "";

        if (
          ct.includes("json") ||
          ct.includes("text")
        ) {
          body = await response.text();
          body = body.slice(0, 1500);
        }
      } catch {}

      interesting.push({
        status: response.status(),
        method: response.request().method(),
        type: response.request().resourceType(),
        url: u,
        body
      });
    }
  });

  try {
    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 35000
    });

    console.log("HTTP:", response?.status());
    console.log("Final URL:", page.url());

    await page.waitForTimeout(10000);

    const result = await page.evaluate(() => {
      const body = document.body?.innerText || "";

      const buttons = [...document.querySelectorAll("button")]
        .map(b => ({
          text: (b.innerText || "").trim(),
          aria: b.getAttribute("aria-label"),
          disabled: b.disabled
        }))
        .filter(x =>
          /cart|pickup|shipping|delivery|store/i.test(
            `${x.text} ${x.aria || ""}`
          )
        );

      return {
        title: document.title,
        bodyLength: body.length,

        challenge:
          /verify your identity|robot|captcha|blocked|access denied/i
            .test(body),

        addToCart:
          buttons.some(x =>
            /add to cart/i.test(`${x.text} ${x.aria || ""}`) &&
            !x.disabled
          ),

        pickup:
          buttons.some(x =>
            /pickup/i.test(`${x.text} ${x.aria || ""}`)
          ),

        shipping:
          buttons.some(x =>
            /shipping|delivery/i.test(`${x.text} ${x.aria || ""}`)
          ),

        outOfStock:
          /out of stock/i.test(body),

        buttons
      };
    });

    console.log("\n===== DOM =====");
    console.log(JSON.stringify(result, null, 2));

    console.log("\n===== INTERESTING NETWORK =====");

    for (const item of interesting) {
      console.log("\n---");
      console.log("STATUS:", item.status);
      console.log("METHOD:", item.method);
      console.log("TYPE:", item.type);
      console.log("URL:", item.url);

      if (item.body) {
        console.log("BODY:");
        console.log(item.body);
      }
    }

  } catch (err) {
    console.error("ERROR:", err.message);
  }

  await browser.close();
})();
