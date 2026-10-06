#!/usr/bin/env python3

"""
PokePawn Automatic Product Discovery

Runs independently from monitor.py.

Purpose:
- Search for products belonging to known/current Pokémon TCG sets.
- Ignore unwanted retailers such as GameStop.
- Save newly discovered products for monitor.py.
- Avoid modifying config.py.
"""

import asyncio
import json
import random
from pathlib import Path

import discover


# ---------------------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------------------

DATA_DIR = Path("data")
DISCOVERED_FILE = DATA_DIR / "discovered_products.json"

BLOCKED_RETAILERS = {
    "gamestop",
}

SEARCH_RETAILERS = [
    "pokemon_center",
    "target",
    "walmart",
    "bestbuy",
]

# Sets/products we currently care about discovering.
#
# Later we'll make this list automatically update from a release feed.
WATCH_SETS = [
    "30th Anniversary",
    "30th Celebration",
    "Pokemon Day 2026",
    "Delta Reign",
    "Mega Evolution Delta Reign",
]

PRODUCT_TYPES = [
    "Elite Trainer Box",
    "ETB",
    "Booster Box",
    "Booster Bundle",
    "Ultra Premium Collection",
    "UPC",
    "Super Premium Collection",
    "SPC",
]


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def load_existing() -> list[dict]:
    if not DISCOVERED_FILE.exists():
        return []

    try:
        data = json.loads(DISCOVERED_FILE.read_text())

        if isinstance(data, list):
            return data

    except Exception as e:
        print(f"⚠️ Could not read {DISCOVERED_FILE}: {e}")

    return []


def product_key(product: dict) -> tuple:
    return (
        product.get("retailer", "").strip().lower(),
        product.get("url", "").strip().lower(),
    )


def allowed_product(product: dict) -> bool:
    retailer = product.get("retailer", "").lower()

    if retailer in BLOCKED_RETAILERS:
        return False

    name = product.get("name", "").lower()
    url = product.get("url", "").lower()

    # Basic Pokémon sanity check.
    haystack = f"{name} {url}"

    if "pokemon" not in haystack and "pokémon" not in haystack:
        return False

    return True


# ---------------------------------------------------------------------------
# SEARCH
# ---------------------------------------------------------------------------

async def search_query(session, query: str) -> list[dict]:
    print(f"\n🔎 {query}")

    tasks = []

    for retailer in SEARCH_RETAILERS:
        search_function = discover.SEARCH_FUNCTIONS.get(retailer)

        if not search_function:
            continue

        tasks.append(
            asyncio.create_task(
                search_function(session, query)
            )
        )

    results = []

    for task in asyncio.as_completed(tasks):
        try:
            found = await task

            for product in found:
                if allowed_product(product):
                    results.append(product)

        except Exception as e:
            print(
                f"   ⚠️ Search failure: "
                f"{type(e).__name__}: {e}"
            )

    return results


async def run_discovery():
    print("=" * 64)
    print("🔎 PokePawn Automatic Product Discovery")
    print("=" * 64)

    existing = load_existing()

    known = {
        product_key(product)
        for product in existing
    }

    discovered = []

    timeout = __import__("aiohttp").ClientTimeout(total=12)

    import aiohttp

    async with aiohttp.ClientSession(timeout=timeout) as session:

        # Search set names first.
        queries = list(WATCH_SETS)

        # Then search high-value product combinations.
        for set_name in WATCH_SETS:
            for product_type in PRODUCT_TYPES:
                queries.append(
                    f"Pokemon TCG {set_name} {product_type}"
                )

        # Remove duplicate queries while preserving order.
        queries = list(dict.fromkeys(queries))

        print(f"Searching {len(queries)} queries...")

        for query in queries:
            try:
                products = await search_query(session, query)

                for product in products:
                    key = product_key(product)

                    if key in known:
                        continue

                    known.add(key)
                    discovered.append(product)

                # Don't hammer retailer search endpoints.
                await asyncio.sleep(
                    random.uniform(2.0, 4.0)
                )

            except Exception as e:
                print(
                    f"⚠️ Query failed: {query}: "
                    f"{type(e).__name__}: {e}"
                )

    print()
    print("=" * 64)

    if not discovered:
        print("ℹ️ No new products discovered.")
        return

    print(f"🎯 Found {len(discovered)} NEW product(s):")

    for product in discovered:
        print()
        print(f"   {product['name']}")
        print(f"   Retailer: {product['retailer']}")
        print(f"   URL: {product['url']}")

    print()
    print("NOTE: Test mode — nothing was automatically saved.")
    print("=" * 64)


if __name__ == "__main__":
    asyncio.run(run_discovery())
