#!/usr/bin/env python3

import asyncio
import aiohttp
import json
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET

from pathlib import Path
from urllib.parse import quote_plus, urlsplit, urlunsplit

from config import CONFIG


DISCOVERED_FILE = Path("data/discovered_products.json")
STATE_FILE = Path("data/costco_30th_watch_state.json")

SEARCH_TERMS = [
    'site:costco.com Pokemon "30th Celebration"',
    'site:costco.com Pokemon "30th Anniversary"',
    'site:costco.com "Pokemon TCG" 30th Costco',
    'site:costco.com Pokemon 30th "Elite Trainer Box"',
    'site:costco.com Pokemon 30th "Booster Bundle"',
]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/154.0.0.0 Safari/537.36"
)


def canonicalize(url: str) -> str:
    """Remove tracking/query fragments while preserving the Costco product URL."""
    parts = urlsplit(url)

    return urlunsplit((
        parts.scheme or "https",
        parts.netloc,
        parts.path,
        "",
        "",
    ))


def is_valid_match(title: str, description: str, url: str) -> bool:
    combined = f"{title} {description} {url}".lower()

    if "costco.com" not in url.lower():
        return False

    if not any(x in combined for x in ("pokemon", "pokémon")):
        return False

    # Require an actual 30th reference so old Celebrations/25th pages
    # don't get accidentally added.
    if "30th" not in combined:
        return False

    # Prefer TCG/product language.
    product_terms = (
        "tcg",
        "trading card",
        "elite trainer",
        "etb",
        "booster",
        "collection",
        "bundle",
        "ultra-premium",
        "ultra premium",
    )

    return any(term in combined for term in product_terms)


async def bing_rss_search(session, query: str) -> list[dict]:
    """
    Use Bing's public RSS search output rather than scraping Costco's
    anti-bot-protected search page.
    """

    url = (
        "https://www.bing.com/search"
        f"?q={quote_plus(query)}&format=rss"
    )

    try:
        async with session.get(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/rss+xml,application/xml,text/xml,*/*",
            },
            timeout=aiohttp.ClientTimeout(total=20),
        ) as r:

            if r.status != 200:
                print(f"Search HTTP {r.status}: {query}")
                return []

            body = await r.text(errors="ignore")

    except Exception as e:
        print(f"Search error ({query}): {type(e).__name__}: {e}")
        return []

    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print(f"RSS parse error: {e}")
        return []

    results = []

    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = (item.findtext("description") or "").strip()

        if link:
            results.append({
                "title": title,
                "url": link,
                "description": desc,
            })

    return results


def load_discovered() -> list:
    if not DISCOVERED_FILE.exists():
        return []

    try:
        data = json.loads(DISCOVERED_FILE.read_text())
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_discovered(products: list):
    DISCOVERED_FILE.parent.mkdir(parents=True, exist_ok=True)

    DISCOVERED_FILE.write_text(
        json.dumps(products, indent=2, ensure_ascii=False) + "\n"
    )


def load_state() -> dict:
    if not STATE_FILE.exists():
        return {"seen_urls": []}

    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {"seen_urls": []}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    STATE_FILE.write_text(
        json.dumps(state, indent=2) + "\n"
    )


async def notify_discord(session, title: str, url: str):
    webhook = CONFIG.get("discord_webhook_url", "")

    if not webhook or "YOUR_WEBHOOK" in webhook:
        return

    payload = {
        "embeds": [
            {
                "title": "🎉 NEW COSTCO 30TH LISTING DISCOVERED",
                "description": title,
                "url": url,
                "color": 0xE31837,
                "fields": [
                    {
                        "name": "🏪 Retailer",
                        "value": "Costco",
                        "inline": True,
                    },
                    {
                        "name": "🔎 Status",
                        "value": "Added to PokePawn monitoring",
                        "inline": True,
                    },
                    {
                        "name": "🔗 Product",
                        "value": f"[Open Costco listing]({url})",
                        "inline": False,
                    },
                ],
                "footer": {
                    "text": "PokePawn • Costco 30th Discovery Watch"
                },
            }
        ]
    }

    try:
        async with session.post(
            webhook,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=10),
        ):
            pass
    except Exception:
        pass


def clean_title(title: str) -> str:
    title = re.sub(r"\s*\|\s*Costco.*$", "", title, flags=re.I)
    title = re.sub(r"\s+", " ", title).strip()

    if not title:
        title = "Pokemon TCG 30th Anniversary"

    return title


def restart_pokepawn():
    try:
        uid = os.getuid()

        subprocess.run(
            [
                "launchctl",
                "kickstart",
                "-k",
                f"gui/{uid}/com.pokepawn.monitor",
            ],
            check=False,
            timeout=15,
        )

        print("Restarted PokePawn to load new Costco product.")

    except Exception as e:
        print(
            "Could not automatically restart PokePawn:",
            type(e).__name__,
            e,
        )


async def main():
    print("=" * 68)
    print("🎉 PokePawn Costco 30th Discovery Watch")
    print("=" * 68)

    products = load_discovered()
    state = load_state()

    known_urls = {
        canonicalize(str(p.get("url", ""))).lower()
        for p in products
        if p.get("url")
    }

    seen_urls = set(
        str(x).lower()
        for x in state.get("seen_urls", [])
    )

    found = {}

    connector = aiohttp.TCPConnector(limit=2)

    async with aiohttp.ClientSession(
        connector=connector,
    ) as session:

        for query in SEARCH_TERMS:
            print(f"Searching: {query}")

            results = await bing_rss_search(session, query)

            for result in results:
                raw_url = result["url"]

                if not is_valid_match(
                    result["title"],
                    result["description"],
                    raw_url,
                ):
                    continue

                url = canonicalize(raw_url)

                found[url.lower()] = {
                    "title": clean_title(result["title"]),
                    "url": url,
                }

        if not found:
            print("No Costco 30th listing discovered yet.")
            return

        added = 0

        for key, result in found.items():
            url = result["url"]
            base_title = result["title"]

            print()
            print("FOUND:", base_title)
            print("URL:  ", url)

            if key in known_urls:
                print("Already monitored.")
                seen_urls.add(key)
                continue

            online = {
                "name": f"{base_title} - Costco",
                "retailer": "costco",
                "url": url,
            }

            warehouse = {
                "name": f"{base_title} - Costco Warehouse",
                "retailer": "costco_instore",
                "url": url,
            }

            products.append(online)
            products.append(warehouse)

            known_urls.add(key)
            seen_urls.add(key)

            added += 2

            print("ADDED online + warehouse monitoring.")

            await notify_discord(
                session,
                base_title,
                url,
            )

    if added:
        save_discovered(products)

        state["seen_urls"] = sorted(seen_urls)
        state["last_found"] = int(time.time())
        save_state(state)

        print()
        print(f"Added {added} monitor entries.")

        restart_pokepawn()

    else:
        state["seen_urls"] = sorted(seen_urls)
        save_state(state)

        print("No new products needed.")


if __name__ == "__main__":
    asyncio.run(main())
