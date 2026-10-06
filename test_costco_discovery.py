#!/usr/bin/env python3

import asyncio
import aiohttp
import re

SEARCH_URL = "https://www.costco.com/s?keyword=pokemon"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


async def main():
    timeout = aiohttp.ClientTimeout(
        total=20,
        connect=7,
        sock_read=15,
    )

    connector = aiohttp.TCPConnector(limit=2)

    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector,
    ) as session:

        print("=" * 65)
        print("PokePawn Costco Pokémon Discovery Test")
        print("=" * 65)
        print("URL:", SEARCH_URL)
        print()

        try:
            async with session.get(
                SEARCH_URL,
                headers=HEADERS,
                allow_redirects=True,
            ) as r:

                print("HTTP:", r.status)
                print("FINAL URL:", r.url)
                print("CONTENT-TYPE:", r.headers.get("Content-Type"))
                print()

                text = await r.text(errors="ignore")

                print("Downloaded:", len(text), "characters")

                if r.status != 200:
                    print()
                    print("Costco did not return a normal search page.")
                    return

                lower = text.lower()

                if "captcha" in lower or "access denied" in lower:
                    print()
                    print("⚠️ Costco challenge/block detected")
                    return

                # Find Costco product URLs.
                urls = set()

                patterns = (
                    r'href="([^"]*pokemon[^"]*\.product\.[^"]*\.html[^"]*)"',
                    r'href="([^"]*\.product\.\d+\.html[^"]*)"',
                )

                for pattern in patterns:
                    for match in re.findall(
                        pattern,
                        text,
                        re.IGNORECASE,
                    ):
                        match = (
                            match
                            .replace("&amp;", "&")
                            .strip()
                        )

                        if match.startswith("/"):
                            match = "https://www.costco.com" + match

                        if match.startswith("http"):
                            urls.add(match)

                print()
                print("Potential product URLs:", len(urls))
                print("-" * 65)

                for url in sorted(urls):
                    print(url)

                print()

                # Useful diagnostics if Costco changed its site.
                signals = {
                    "pokemon": lower.count("pokemon"),
                    "product": lower.count("product"),
                    "add to cart": lower.count("add to cart"),
                    "warehouse": lower.count("warehouse"),
                    "out of stock": lower.count("out of stock"),
                }

                print("Page signals:")
                for key, value in signals.items():
                    print(f"  {key:15}: {value}")

        except asyncio.TimeoutError:
            print("❌ Costco request timed out")

        except aiohttp.ClientError as e:
            print(
                "❌ Costco network error:",
                type(e).__name__,
                repr(e),
            )


asyncio.run(main())
