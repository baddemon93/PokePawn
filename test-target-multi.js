const { chromium } = require("playwright");
const fs = require("fs");

const urls = process.argv.slice(2);

if (!urls.length) {
  console.error("No URLs supplied");
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch({
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });

  for (const url of urls) {
    const page = await context.newPage();

    try {
      console.log("\n==================================================");
      console.log(url);

      const response = await page.goto(url, {
        waitUntil: "domcontentloaded",
        timeout: 35000
      });

      await page.waitForTimeout(8000);

      const result = await page.evaluate(() => {
        function fulfillment(id) {
          const el = document.getElementById(id);

          if (!el)
            return null;

          const cls = String(el.className || "");
          const text = (el.innerText || "").trim();

          return {
            id,
            text,
            disabled: !!el.disabled,
            ariaDisabled: el.getAttribute("aria-disabled"),
            ariaLabel: el.getAttribute("aria-label"),

            unavailable:
              /unavailablefulfillmentcell/i.test(cls),

            active:
              /activefulfillmentcell/i.test(cls) &&
              !/notactive/i.test(cls),

            className: cls
          };
        }

        const body = document.body?.innerText || "";

        return {
          title: document.title,

          challenge:
            /verify you are human|access denied|unusual traffic/i.test(body),

          addToCart:
            [...document.querySelectorAll("button")]
              .some(b =>
                /add to cart/i.test(
                  `${b.innerText || ""} ${b.getAttribute("aria-label") || ""}`
                ) && !b.disabled
              ),

          pickup: fulfillment("PICKUP"),
          delivery: fulfillment("DELIVERY"),
          shipping: fulfillment("SHIPPING")
        };
      });

      console.log(JSON.stringify(result, null, 2));

    } catch (e) {
      console.log(JSON.stringify({
        error: e.name,
        message: e.message
      }, null, 2));

    } finally {
      await page.close();
    }
  }

  await browser.close();
})();
