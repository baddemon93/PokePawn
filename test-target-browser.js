const { chromium } = require("playwright");

(async () => {
  const url =
    "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-prismatic-evolutions-booster-bundle/-/A-93954446";

  const browser = await chromium.launch({
    headless: true
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });

  const page = await context.newPage();

  try {
    console.log("Loading Target...");

    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 35000
    });

    console.log("HTTP:", response?.status());
    console.log("Final URL:", page.url());

    await page.waitForTimeout(8000);

    console.log("\n===== BEFORE CLICK =====");

    const before = await page.evaluate(() => {
      const body = document.body?.innerText || "";

      return {
        addToCart: /add to cart/i.test(body),
        shipIt: /\bship it\b/i.test(body),
        pickup: /\bpickup\b/i.test(body),
        outOfStock: /out of stock/i.test(body),
        soldOut: /sold out/i.test(body),
        unavailable: /\bunavailable\b/i.test(body),

        relevantText: body
          .split("\n")
          .map(x => x.trim())
          .filter(Boolean)
          .filter(x =>
            /pickup|shipping|ship it|delivery|stock|available|unavailable|cart|notify/i.test(x)
          )
          .slice(0, 80)
      };
    });

    console.log(JSON.stringify(before, null, 2));

    const pickup = page.getByRole("button", {
      name: /pickup/i
    }).first();

    if (await pickup.count()) {
      console.log("\nClicking Pickup...");

      await pickup.click({
        timeout: 10000
      });

      await page.waitForTimeout(5000);

      console.log("\n===== AFTER CLICK =====");

      const after = await page.evaluate(() => {
        const body = document.body?.innerText || "";

        const buttons = [...document.querySelectorAll("button")]
          .map(b => ({
            text: (b.innerText || "").trim(),
            aria: b.getAttribute("aria-label"),
            disabled: b.disabled
          }))
          .filter(x =>
            /pickup|cart|ship|store|notify/i.test(
              `${x.text} ${x.aria || ""}`
            )
          );

        return {
          addToCart: /add to cart/i.test(body),
          shipIt: /\bship it\b/i.test(body),
          outOfStock: /out of stock/i.test(body),
          soldOut: /sold out/i.test(body),
          unavailable: /\bunavailable\b/i.test(body),

          relevantText: body
            .split("\n")
            .map(x => x.trim())
            .filter(Boolean)
            .filter(x =>
              /pickup|shipping|ship it|delivery|stock|available|unavailable|cart|notify|store/i.test(x)
            )
            .slice(0, 120),

          buttons: buttons.slice(0, 40)
        };
      });

      console.log(JSON.stringify(after, null, 2));
    } else {
      console.log("No Pickup button found.");
    }

  } catch (e) {
    console.error(
      "ERROR:",
      e.name,
      e.message
    );
  } finally {
    await browser.close();
  }
})();
