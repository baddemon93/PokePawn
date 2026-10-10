const { chromium } = require("playwright");

const url = process.argv[2];

if (!url) {
  console.error("Usage: node test-target-hydration.js <url>");
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch({
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });

  const page = await context.newPage();

  try {
    console.log("Loading:");
    console.log(url);
    console.log();

    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 35000
    });

    console.log("HTTP:", response?.status());
    console.log("Title:", await page.title());
    console.log();

    let previous = "";

    for (let seconds = 0; seconds <= 30; seconds += 2) {
      if (seconds)
        await page.waitForTimeout(2000);

      const state = await page.evaluate(() => {
        function get(id) {
          const el = document.getElementById(id);

          if (!el)
            return null;

          return {
            text: (el.innerText || "").trim(),
            aria: el.getAttribute("aria-label"),
            disabled: !!el.disabled,
            className: String(el.className || ""),
            html: el.innerHTML.slice(0, 1000)
          };
        }

        const buttons = [...document.querySelectorAll("button")]
          .map(b => ({
            text: (b.innerText || "").trim(),
            aria: b.getAttribute("aria-label"),
            disabled: !!b.disabled
          }))
          .filter(x =>
            /add to cart|ship it|notify|out of stock/i.test(
              `${x.text} ${x.aria || ""}`
            )
          );

        return {
          pickup: get("PICKUP"),
          delivery: get("DELIVERY"),
          shipping: get("SHIPPING"),
          purchaseButtons: buttons
        };
      });

      const serialized = JSON.stringify(state);

      if (serialized !== previous) {
        console.log(`===== ${seconds}s =====`);

        console.log(JSON.stringify({
          pickup: state.pickup && {
            text: state.pickup.text,
            aria: state.pickup.aria,
            className: state.pickup.className
          },

          delivery: state.delivery && {
            text: state.delivery.text,
            aria: state.delivery.aria,
            className: state.delivery.className
          },

          shipping: state.shipping && {
            text: state.shipping.text,
            aria: state.shipping.aria,
            className: state.shipping.className
          },

          purchaseButtons: state.purchaseButtons
        }, null, 2));

        previous = serialized;
      }
    }

    console.log();
    console.log("Hydration test complete.");

  } catch (e) {
    console.error("ERROR:", e.name, e.message);
  } finally {
    await browser.close();
  }
})();
