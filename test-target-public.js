const { chromium } = require("playwright");

(async () => {
  const url = process.argv[2];

  if (!url) {
    console.error("Usage: node test-target-public.js <url>");
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

  try {
    const response = await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: 35000
    });

    console.log("===== PAGE =====");
    console.log("HTTP:", response?.status());
    console.log("URL:", page.url());
    console.log("TITLE:", await page.title());

    const result = await page.evaluate(() => {
      const next = document.querySelector("#__NEXT_DATA__");

      let nextData = null;

      if (next?.textContent) {
        try {
          nextData = JSON.parse(next.textContent);
        } catch {}
      }

      const scripts = [...document.querySelectorAll("script")]
        .map(s => s.textContent || "")
        .filter(Boolean);

      const body = document.body?.innerText || "";

      function collect(obj, path = "", out = [], depth = 0) {
        if (
          obj === null ||
          obj === undefined ||
          depth > 12 ||
          out.length > 300
        ) {
          return out;
        }

        if (typeof obj !== "object") {
          const key = path.toLowerCase();

          if (
            /availability|inventory|fulfillment|shipping|pickup|delivery|stock/.test(key)
          ) {
            out.push({
              path,
              value:
                typeof obj === "string"
                  ? obj.slice(0, 300)
                  : obj
            });
          }

          return out;
        }

        if (Array.isArray(obj)) {
          for (let i = 0; i < Math.min(obj.length, 100); i++) {
            collect(
              obj[i],
              `${path}[${i}]`,
              out,
              depth + 1
            );
          }

          return out;
        }

        for (const [key, value] of Object.entries(obj)) {
          const newPath = path
            ? `${path}.${key}`
            : key;

          collect(
            value,
            newPath,
            out,
            depth + 1
          );
        }

        return out;
      }

      const interesting = nextData
        ? collect(nextData)
        : [];

      const scriptMatches = [];

      const patterns = [
        /availability.{0,150}/gi,
        /inventory.{0,150}/gi,
        /fulfillment.{0,150}/gi,
        /out.?of.?stock.{0,100}/gi,
        /in.?stock.{0,100}/gi
      ];

      for (const script of scripts) {
        for (const pattern of patterns) {
          const matches = script.match(pattern);

          if (matches) {
            for (const m of matches.slice(0, 20)) {
              scriptMatches.push(m.slice(0, 300));
            }
          }
        }

        if (scriptMatches.length > 100) {
          break;
        }
      }

      return {
        hasNextData: !!nextData,
        bodyLength: body.length,

        pageChallenge:
          /robot|captcha|access denied|verify your identity/i
            .test(body),

        interesting,
        scriptMatches
      };
    });

    console.log("\n===== RESULT =====");
    console.log(JSON.stringify(result, null, 2));

  } catch (err) {
    console.error("ERROR:", err.message);
  }

  await browser.close();
})();
