const { chromium } = require("playwright");

const url = process.argv[2];

if (!url) {
  console.error("Usage: node test-target-network.js <url>");
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

  const interesting =
    /fulfill|inventory|stock|availability|pickup|shipping|delivery|redsky|location|store/i;

  page.on("response", async response => {
    const req = response.request();
    const reqUrl = response.url();

    if (!interesting.test(reqUrl))
      return;

    console.log("\n===== NETWORK =====");
    console.log("STATUS:", response.status());
    console.log("METHOD:", req.method());
    console.log("TYPE:", req.resourceType());
    console.log("URL:", reqUrl);

    try {
      const ct =
        (await response.allHeaders())["content-type"] || "";

      console.log("CONTENT-TYPE:", ct);

      if (
        ct.includes("json") ||
        ct.includes("text")
      ) {
        const body = await response.text();

        console.log(
          "BODY:",
          body.slice(0, 2000)
        );
      }
    } catch (e) {
      console.log(
        "BODY ERROR:",
        e.message
      );
    }
  });

  try {
    console.log("Loading:");
    console.log(url);

    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 35000
    });

    console.log("\nPAGE HTTP:", response?.status());

    await page.waitForTimeout(15000);

    console.log("\n===== FINAL DOM =====");

    const state = await page.evaluate(() => {
      function get(id) {
        const el = document.getElementById(id);

        if (!el)
          return null;

        return {
          text: (el.innerText || "").trim(),
          aria: el.getAttribute("aria-label"),
          className: String(el.className || "")
        };
      }

      return {
        pickup: get("PICKUP"),
        delivery: get("DELIVERY"),
        shipping: get("SHIPPING")
      };
    });

    console.log(
      JSON.stringify(state, null, 2)
    );

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
