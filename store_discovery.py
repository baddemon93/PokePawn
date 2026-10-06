#!/usr/bin/env python3

"""
PokePawn local store discovery.

Store discovery is deliberately separated from monitor.py because retailer
store-locator endpoints may be slow, blocked, or change format.

Results are cached in:
    data/local_stores.json

If discovery fails, monitor.py can continue using CONFIG["local_stores"].
"""

import asyncio
import aiohttp
import json
import math
import re
from pathlib import Path

from config import CONFIG


CACHE_FILE = Path("data/local_stores.json")

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/154.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}


def haversine_miles(lat1, lon1, lat2, lon2):
    """Distance between two coordinates in miles."""
    r = 3958.8

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)

    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1)
        * math.cos(p2)
        * math.sin(dl / 2) ** 2
    )

    return 2 * r * math.asin(math.sqrt(a))


async def resolve_zip(session, zip_code):
    """
    Resolve a US ZIP code using Zippopotam's public ZIP lookup.
    """
    url = f"https://api.zippopotam.us/us/{zip_code}"

    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as r:

            if r.status != 200:
                return None

            data = await r.json()

            places = data.get("places", [])

            if not places:
                return None

            place = places[0]

            return {
                "zip": zip_code,
                "city": place.get("place name", ""),
                "state": place.get("state abbreviation", ""),
                "latitude": float(place["latitude"]),
                "longitude": float(place["longitude"]),
            }

    except Exception as e:
        print(f"ZIP lookup failed: {type(e).__name__}: {e}")
        return None


async def discover_bestbuy(session, location):
    """
    Best-effort Best Buy store discovery.

    This is allowed to fail. Existing config store IDs remain the fallback.
    """
    results = []

    zip_code = location["zip"]

    url = (
        "https://www.bestbuy.com/site/store-locator/"
        f"?location={zip_code}"
    )

    try:
        async with session.get(
            url,
            headers=HEADERS,
            timeout=aiohttp.ClientTimeout(total=12),
        ) as r:

            if r.status != 200:
                print(f"  Best Buy locator HTTP {r.status}")
                return results

            text = await r.text(errors="ignore")

            # Store IDs often appear in embedded page data.
            ids = set(
                re.findall(
                    r'"storeId"\s*:\s*"?(\\d+)"?',
                    text,
                    re.I,
                )
            )

            for store_id in ids:
                results.append({
                    "id": store_id,
                    "name": f"Best Buy #{store_id}",
                })

    except Exception as e:
        print(
            f"  Best Buy discovery unavailable: "
            f"{type(e).__name__}"
        )

    return results


async def discover_target(session, location):
    """
    Best-effort Target discovery.

    Target currently uses aggressive anti-bot protection, so failure here is
    expected and simply falls back to configured Target IDs.
    """
    return []


async def discover_walmart(session, location):
    """
    Best-effort Walmart discovery.

    Keep this conservative because Walmart frequently changes its web APIs.
    """
    return []


def configured_fallback():
    stores = CONFIG.get("local_stores", {})

    return {
        "target": [
            {"id": str(x), "name": f"Target #{x}"}
            for x in stores.get("target", [])
        ],
        "walmart": [
            {"id": str(x), "name": f"Walmart #{x}"}
            for x in stores.get("walmart", [])
        ],
        "bestbuy": [
            {"id": str(x), "name": f"Best Buy #{x}"}
            for x in stores.get("bestbuy", [])
        ],
    }


async def main():
    cfg = CONFIG.get("location", {})

    zip_code = str(cfg.get("zip", "80938"))
    radius = int(cfg.get("radius_miles", 25))

    print("=" * 64)
    print("PokePawn Local Store Discovery")
    print("=" * 64)
    print(f"ZIP:    {zip_code}")
    print(f"Radius: {radius} miles")
    print()

    fallback = configured_fallback()

    async with aiohttp.ClientSession() as session:
        location = await resolve_zip(session, zip_code)

        if not location:
            print("Could not resolve ZIP.")
            print("Keeping existing configured store IDs.")
            return

        print(
            f"Resolved: {location['city']}, {location['state']} "
            f"({location['latitude']}, {location['longitude']})"
        )
        print()

        discovered = {
            "bestbuy": await discover_bestbuy(session, location),
            "target": await discover_target(session, location),
            "walmart": await discover_walmart(session, location),
        }

    final = {}

    for retailer in ("target", "walmart", "bestbuy"):
        if discovered[retailer]:
            final[retailer] = discovered[retailer]
            source = "discovered"
        else:
            final[retailer] = fallback[retailer]
            source = "configured fallback"

        print(
            f"{retailer:8}: "
            f"{len(final[retailer])} stores "
            f"({source})"
        )

    payload = {
        "location": location,
        "radius_miles": radius,
        "stores": final,
    }

    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

    CACHE_FILE.write_text(
        json.dumps(payload, indent=2) + "\n"
    )

    print()
    print(f"Saved: {CACHE_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
