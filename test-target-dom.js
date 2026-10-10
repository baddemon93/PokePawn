const { chromium } = require("playwright");

(async () => {
  const url =
    "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-prismatic-evolutions-booster-bundle/-/A-93954446";

  const browser = await chromium.launch({ headless: true });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 }
  });

  const page = await context.newPage();

  try {
    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 35000
    });

    console.log("HTTP:", response?.status());

    await page.waitForTimeout(8000);

    const results = await page.evaluate(() => {
      const wanted = /^(Pickup|Delivery|Shipping)$/i;
      const found = [];

      for (const el of document.querySelectorAll("*")) {
        const text = (el.textContent || "").trim();

        if (!wanted.test(text))
          continue;

        // Only keep reasonably small elements instead of parent containers
        // containing half the page.
        if (el.children.length > 8)
          continue;

        found.push({
          text,
          tag: el.tagName,
          role: el.getAttribute("role"),
          ariaLabel: el.getAttribute("aria-label"),
          ariaSelected: el.getAttribute("aria-selected"),
          dataTest: el.getAttribute("data-test"),
          id: el.id || null,
          class: String(el.className || "").slice(0, 300),
          outerHTML: el.outerHTML.slice(0, 1500)
        });
      }

      return found.slice(0, 50);
    });

    console.log(JSON.stringify(results, null, 2));

  } catch (e) {
    console.error("ERROR:", e.name, e.message);
  } finally {
    await browser.close();
  }
})();
