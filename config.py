"""
config.py — Drop Alert Master Edition
Rules:
  - MSRP only, no resellers
  - Walmart: shipped & sold by Walmart only (no marketplace sellers)
  - No preorders — in-stock alerts only
"""

CONFIG = {
    # ── Local Store Search ────────────────────────────────────────────────
    "location": {
        "zip": "80938",
        "state": "CO",
        "radius_miles": 25,
    },

    # ── Timing ────────────────────────────────────────────────────────────────
    "check_interval_seconds":  30,
    "alert_cooldown_seconds":  240,

    # ── Notifications ─────────────────────────────────────────────────────────
    "notifications": ["macos", "discord"],

    # ── Discord ───────────────────────────────────────────────────────────────
    "discord_webhook_url": "https://discord.com/api/webhooks/1556392517430415524/QQCZ0y4KV9-oW-sn0MEqFf4CDN0C-TYayubpvtDYA3EsfEawFnmKoBJgBxjFfSpUx1xW",
    "discord_ping_everyone": False,

    # ── Multi-channel Discord webhooks ────────────────────────────────────────
    # Leave empty ("") to route all alerts to discord_webhook_url above.
    # Fill with separate channel webhooks for organized Discord servers:
    "discord_webhooks": {
        "main":        "",   # online in-stock drops  → falls back to discord_webhook_url
        "in_store":    "",   # 🏪 local store alerts  → falls back to discord_webhook_url
        "price_drops": "",   # 💸 price drop alerts   → falls back to discord_webhook_url
        "heartbeat":   "",   # 💚 system status pings → falls back to discord_webhook_url
    },

    # ── Twilio SMS ────────────────────────────────────────────────────────────
    "twilio": {
        "account_sid": "",
        "auth_token":  "",
        "from":        "",
        "to":          "+1XXXXXXXXXX",
    },

    # ── Stock filter ──────────────────────────────────────────────────────────
    # Allow pre-orders — alert on PRE_ORDER status for high-resell products
    "skip_preorder": False,

    # Walmart: only alert if sold & shipped by Walmart (not marketplace)
    "walmart_first_party_only": True,

    # ── Local stores (your local area) ───────────────────────────────────────
    # Used by *_instore retailer checkers to monitor local physical stores.
    # Target store IDs: 1826 = Capital Blvd, 1080 = Hwy 70 (Grove Barton Rd)
    # Walmart store IDs: 1751 = Glenwood Ave, 2058 = New Hope Church Rd,
    #                    4484 = Town Dr, 1372 = Fayetteville Rd,
    #                    5292 = New Bern Ave, 5118 = Tryon Rd
    # Best Buy store IDs: 299 = Glenwood Ave, 821 = Capital Blvd
    "local_stores": {
        "target":  ["1826", "1080"],
        "walmart": ["1751", "2058", "4484", "1372", "5292", "5118"],
        "bestbuy": ["299", "821"],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# PRODUCT TIERS
# Tier 1 → 5s polling (highest value, must-have)
# Tier 2 → 10s polling (high value, strong margin)
# Tier 3 → 30s polling (standard / older sets)
# Patterns are matched by substring (case-insensitive) against product names.
# First match wins, so put more specific patterns first.
# ═══════════════════════════════════════════════════════════════════════════════

PRODUCT_TIERS = {
    1: [
        # PC exclusives, UPCs, SPCs — highest demand, check every 5s
        "30th Celebration",
        "30th Anniversary",
        "Delta Reign",
        "Prismatic Evolutions ETB",
        "Prismatic Evolutions Super Premium",
        "Ascended Heroes PC ETB",
        "Perfect Order PC ETB",
        "Chaos Rising PC ETB",                   # releasing May 22 2026
        "Storm Emerald PC ETB",                  # releasing Sep 2026
        "Mega Charizard X ex UPC",
        "Team Rocket's Moltres ex UPC",
        "Celebrations Ultra Premium",
        "Enhanced Booster Box",                  # Enhanced boxes = strong margins
        "Journey Together Enhanced",
        "Pokemon Day 2026",
        "Pokemon 151 Mew ex UPC",               # Mew UPC — top resale
        "Surging Sparks Super Premium",         # Pikachu ex SPC
        "Paldean Fates Shiny Charizard",        # Shiny Charizard ex — high demand
    ],
    2: [
        # Mass-retail ETBs, Booster Boxes, high-demand SPCs — check every 10s
        "ETB",
        "Booster Box",
        "UPC",
        "Lucario ex Figure Collection",
        "Unova Victini",
        "Blooming Waters",
        "Mega Lucario",
        "Surging Sparks Iron Thorns",
        "Surging Sparks Eevee Grove",
        "Stellar Crown Terapagos",
        "Shrouded Fable Pecharunt",
        "Temporal Forces Iron Crown",
        "Paradox Rift Roaring Moon",
        "Paradox Rift Iron Valiant",
        "Obsidian Flames Charizard ex SPC",
    ],
    3: [
        # Standard booster bundles & older/slower-moving products
        "Booster Bundle",
        "Surprise Box",
        "Costco",
        "Lucario ex & Tyranitar",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
# RELEASE CALENDAR
# Format: "YYYY-MM-DD": "Set Name"  or  "YYYY-MM-DD": ["Set A", "Set B"]
# Used to activate BLITZ mode (3s) on release day and
# LAUNCH WINDOW mode (5s) in the ±7-day window around each release.
# ═══════════════════════════════════════════════════════════════════════════════

RELEASE_CALENDAR = {
    "2025-01-17": "Prismatic Evolutions",          # released
    "2025-03-28": "Journey Together",              # released
    "2025-05-02": "Destined Rivals",               # released
    "2025-08-01": ["Black Bolt", "White Flare"],   # released
    "2025-11-07": "Phantasmal Flames",             # released
    "2026-01-30": "Ascended Heroes",               # released
    "2026-03-27": "Perfect Order",                 # just released — BLITZ ACTIVE
    "2026-05-22": "Chaos Rising",                  # UPCOMING — Mega Greninja ex
    "2026-09-05": "Storm Emerald",                 # UPCOMING — Mega Rayquaza ex (est.)
}

# ═══════════════════════════════════════════════════════════════════════════════
# PRODUCTS
# Online keys:    pokemon_center · target · walmart · costco · sams_club
#                gamestop · bestbuy · other_pokemon · jp_pokemon · tcg_supplies
# In-store keys: target_instore · walmart_instore · bestbuy_instore
#                (checks local your city, ST stores defined in local_stores above)
# ═══════════════════════════════════════════════════════════════════════════════

PRODUCTS = [

    # ══════════════════════════════════════════════════════════════════════════
    # PRISMATIC EVOLUTIONS (Jan 2025)  ·  PC ETB ~$50 → $390+ resale
    # ══════════════════════════════════════════════════════════════════════════

    # -- ETBs --
    {"name": "Prismatic Evolutions ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/en-us/product/scarlet-violet-prismatic-evolutions-etb/290-85589"},
    {"name": "Prismatic Evolutions ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-Scarlet-Violet-Prismatic-Evolutions-Elite-Trainer-Box/13816151308"},
    {"name": "Prismatic Evolutions ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-elite-trainer-box/JJG2TLCW3L"},
    {"name": "Prismatic Evolutions ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/pokemon-tcg-scarlet-violet-prismatic-evolutions"},

    # -- Booster Bundles --
    {"name": "Prismatic Evolutions Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-prismatic-evolutions-booster-bundle/-/A-93954446"},
    {"name": "Prismatic Evolutions Booster Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/POKEMON-SV8-5-PRISMATIC-EVO-BST-BUNDLE/14803962651"},
    {"name": "Prismatic Evolutions Booster Bundle - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-booster-bundle/JJG2TL23JK"},
    {"name": "Prismatic Evolutions Booster Bundle - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-prismatic-evolutions-booster-bundle/20018824.html"},

    # -- Surprise Box --
    {"name": "Prismatic Evolutions Surprise Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/100-10096/pokemon-tcg-scarlet-and-violet-prismatic-evolutions-surprise-box"},
    {"name": "Prismatic Evolutions Surprise Box - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/2025-pokemon-scarlet-violet-s8-5-prismatic-evolutions-surprise-box/-/A-94336414"},
    {"name": "Prismatic Evolutions Surprise Box - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-Trading-Card-Games-Scarlett-Violet-8-5-Prismatic-Evolutions-Surprise-Box/14148473268"},
    {"name": "Prismatic Evolutions Surprise Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-surprise-box/JJG2TLCK6H"},
    {"name": "Prismatic Evolutions Surprise Box - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-prismatic-evolutions-surprise-box-styles-may-vary/20018748.html"},

    # -- Super Premium Collection --
    {"name": "Prismatic Evolutions Super Premium Collection - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-prismatic-evolutions-super-premium-collection/-/A-94300072"},
    {"name": "Prismatic Evolutions Super Premium Collection - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pok-mon-TCG-Scarlet-Violet-8-5-Prismatic-Evolutions-Super-Premium-Collection/15494520186"},
    {"name": "Prismatic Evolutions Super Premium Collection - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-super-premium-collection/JJG2TL23CW"},
    {"name": "Prismatic Evolutions Super Premium Collection - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-prismatic-evolutions-super-premium-collection/20020881.html"},

    # -- Lucario ex & Tyranitar ex Premium Collection (Sam's Club exclusive) --
    {"name": "Prismatic Evolutions Lucario ex & Tyranitar ex Collection - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pokemon-tcg-scarlet-violet-prismatic-evolutions-lucario-ex-tyranitar-ex-premium-collection-box-14-packs/-/A-1005879863"},
    {"name": "Prismatic Evolutions Lucario ex & Tyranitar ex Collection - Sam's Club",
     "retailer": "sams_club",
     "url": "https://www.samsclub.com/ip/Pokemon-Lucario-Ex-Tyranitar-Ex-Premium-Collection/17295401081"},

    # -- Costco 2-Pack Bundle --
    {"name": "Prismatic Evolutions Costco 2-Pack ETB+Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-Prismatic-Evolutions-Elite-Trainer-Box-Booster-Bundle/16817304907"},


    # ══════════════════════════════════════════════════════════════════════════
    # TWILIGHT MASQUERADE (May 2024)  ·  ETB ~$50 → $75+ resale
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Twilight Masquerade PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/189-85799/pokemon-tcg-scarlet-and-violet-twilight-masquerade-pokemon-center-elite-trainer-box"},
    {"name": "Twilight Masquerade ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-twilight-masquerade-elite-trainer-box/-/A-91619960"},
    {"name": "Twilight Masquerade ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-Trading-Card-Games-SV6-Twilight-Masquerade-Elite-Trainer-Box/5558569421"},
    {"name": "Twilight Masquerade ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-twilight-masquerade-elite-trainer-box/J3YSYH8XK6"},
    {"name": "Twilight Masquerade ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-twilight-masquerade-elite-trainer-box/20011215.html"},
    {"name": "Twilight Masquerade Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/699-86340/pokemon-tcg-scarlet-and-violet-twilight-masquerade-booster-display-box-36-packs"},
    {"name": "Twilight Masquerade Booster Box - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Twilight-Masquerade-Booster-Box-36-Packs/5736034613"},
    {"name": "Twilight Masquerade Booster Box - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-twilight-masquerade-36-booster-pack-box-styles-may-vary/20011255.html"},


    # ══════════════════════════════════════════════════════════════════════════
    # DESTINED RIVALS (May 2025)  ·  PC ETB ~$50 → $414+ resale
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Destined Rivals PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/100-10653/pokemon-tcg-scarlet-and-violet-destined-rivals-pokemon-center-elite-trainer-box"},
    {"name": "Destined Rivals ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Destined-Rivals-Elite-Trainer-Box-ETB/16728861909"},
    {"name": "Destined Rivals PC ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pok-mon-TCG-Scarlet-Violet-Destined-Rivals-Pok-mon-Center-Elite-Trainer-Box/15718673510"},
    {"name": "Destined Rivals ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-destined-rivals-elite-trainer-box/JJG2TL22PF"},
    {"name": "Destined Rivals ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-destined-rivals-elite-trainer-box/20021586.html"},
    {"name": "Destined Rivals Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10157-101/pokemon-tcg-scarlet-and-violet-destined-rivals-booster-display-box-36-packs"},
    {"name": "Destined Rivals Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-destined-rivals-booster-box-36-packs/JJG2TL25CG"},
    {"name": "Destined Rivals Booster Box - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-destined-rivals-booster-box/20021587.html"},
    {"name": "Destined Rivals Booster Bundle - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-destined-rivals-booster-bundle/20021585.html"},


    # ══════════════════════════════════════════════════════════════════════════
    # JOURNEY TOGETHER (Mar 2025)  ·  Enhanced Box $248+ resale
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Journey Together PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/100-10356/pokemon-tcg-scarlet-and-violet-journey-together-pokemon-center-elite-trainer-box"},
    {"name": "Journey Together Enhanced Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10125-102/pokemon-tcg-scarlet-and-violet-journey-together-enhanced-booster-display-box-36-packs-and-1-promo-card"},
    {"name": "Journey Together ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/2025-pok-233-mon-scarlet-violet-s9-elite-trainer-box/-/A-93803439"},
    {"name": "Journey Together Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-journey-together-booster-bundle/-/A-94300074"},
    {"name": "Journey Together ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-Trading-Card-Game-Scarlet-Violet-9-Journey-Together-Elite-Trainer-Box/15156564532"},
    {"name": "Journey Together Enhanced Booster Box - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pok-mon-TCG-Scarlet-Violet-9-Journey-Together-Enhanced-Booster-Display/15053563608"},
    {"name": "Journey Together ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-scarlet-and-violet-journey-together-elite-trainer-box/20019414.html"},
    {"name": "Journey Together Enhanced Booster Box - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-scarlet-and-violet-journey-together-booster-box-36-count/20019550.html"},
    {"name": "Journey Together Enhanced Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-journey-together-booster-box-36-packs/JJG2TL2QS8"},
    {"name": "Journey Together Booster Bundle - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-trading-card-game-scarlet-violet-journey-together-booster-bundle-6-pk/6614264.p?skuId=6614264"},


    # ══════════════════════════════════════════════════════════════════════════
    # BLACK BOLT & WHITE FLARE (Aug 2025)  ·  PC ETB $145–178 resale
    # ══════════════════════════════════════════════════════════════════════════

    # -- White Flare --
    {"name": "White Flare PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10037-117/pokemon-tcg-scarlet-and-violet-white-flare-pokemon-center-elite-trainer-box"},
    {"name": "White Flare ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-white-flare-elite-trainer-box/-/A-94636860"},
    {"name": "White Flare ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-10-5-White-Flare-Elite-Trainer-Box-9-Packs-Promo-Card/16446322202"},
    {"name": "White Flare ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-white-flare-elite-trainer-box/JJG2TL28KK"},
    {"name": "White Flare ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-white-flare-elite-trainer-box/20021658.html"},
    {"name": "White Flare Booster Bundle - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10035-115/pokemon-tcg-scarlet-and-violet-white-flare-booster-bundle-6-packs"},

    # -- Black Bolt --
    {"name": "Black Bolt PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10037-118/pokemon-tcg-scarlet-and-violet-black-bolt-pokemon-center-elite-trainer-box"},
    {"name": "Black Bolt ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Black-Bolt-Elite-Trainer-Box-ETB/17317016821"},
    {"name": "Black Bolt ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-black-bolt-elite-trainer-box/20021662.html"},
    {"name": "Black Bolt Booster Bundle - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10115-113/pokemon-tcg-scarlet-and-violet-black-bolt-booster-bundle-6-packs"},
    {"name": "Black Bolt Booster Bundle - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-trading-card-game-scarlet-violet-black-bolt-booster-bundle/6632402.p?skuId=6632402"},
    {"name": "Black Bolt Booster Bundle - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-black-bolt-booster-bundle/20021649.html"},

    # -- Unova Victini Illustration Collection (Black Bolt set) --
    {"name": "Unova Victini Illustration Collection - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10029-102/pokemon-tcg-unova-victini-illustration-collection"},
    {"name": "Unova Victini Illustration Collection - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-unova-victini-illustration-collection/-/A-94636866"},
    {"name": "Unova Victini Illustration Collection - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-10-5-Unova-Victini-Illustration-Collection-4-Packs/16454274271"},
    {"name": "Unova Victini Illustration Collection - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-unova-victini-illustration-collection/JJG2TL232V"},
    {"name": "Unova Victini Illustration Collection - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-unova-victini-illustration-collection/20021655.html"},


    # ══════════════════════════════════════════════════════════════════════════
    # MEGA EVOLUTION — PHANTASMAL FLAMES (Nov 2025)  ·  Booster Box $324+ resale
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Phantasmal Flames PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10186-109/pokemon-tcg-mega-evolution-phantasmal-flames-pokemon-center-elite-trainer-box"},
    {"name": "Phantasmal Flames ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-mega-evolution-8212-phantasmal-flames-elite-trainer-box/-/A-94860231"},
    {"name": "Phantasmal Flames ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-phantasmal-flames-elite-trainer-box/JJG2TL2VT6"},
    {"name": "Phantasmal Flames ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-phantasmal-flames-elite-trainer-box/20027391.html"},
    {"name": "Phantasmal Flames Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-phantasmal-flames-booster-box-36-packs/JJG2TL3XYR"},
    {"name": "Phantasmal Flames Booster Box - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-phantasmal-flames-booster-box/20027387.html"},
    {"name": "Phantasmal Flames Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-mega-evolution-8212-phantasmal-flames-booster-bundle/-/A-94884496"},
    {"name": "Phantasmal Flames Booster Bundle - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-phantasmal-flames-6pk-booster-bundle/JJG2TL3XY4"},
    {"name": "Phantasmal Flames Booster Bundle - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-phantasmal-flames-booster-bundle/20027390.html"},


    # ══════════════════════════════════════════════════════════════════════════
    # MEGA EVOLUTION — ASCENDED HEROES (Jan 2026)  ·  PC ETB $267+ resale
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Ascended Heroes PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10315-108/pokemon-tcg-mega-evolution-ascended-heroes-pokemon-center-elite-trainer-box"},
    {"name": "Ascended Heroes PC ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pokemon-tcg-mega-evolution-ascended-heroes-pokemon-center-elite-trainer-box/-/A-1009871732"},
    {"name": "Ascended Heroes ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/2025-pok-me-2-5-elite-trainer-box/-/A-95082118"},
    {"name": "Ascended Heroes ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pok-mon-Trading-Card-Game-Mega-Evolution-Ascended-Heroes-Elite-Trainer-Box/18710966734"},
    {"name": "Ascended Heroes ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-ascended-heroes-elite-trainer-box/JJG2TLXSFV"},
    {"name": "Ascended Heroes ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-ascended-heroes-elite-trainer-box/20030564.html"},
    {"name": "Ascended Heroes Booster Bundle - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10311-114/pokemon-tcg-mega-evolution-ascended-heroes-booster-bundle-6-packs"},
    {"name": "Ascended Heroes Booster Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pok-mon-TCG-Mega-Evolution-Ascended-Heroes-Booster-Bundle-6-Packs/18728422476"},
    {"name": "Ascended Heroes Booster Bundle - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-ascended-heroes-booster-bundle/JJG2TL3JP8"},
    {"name": "Ascended Heroes Booster Bundle - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-ascended-heroes-booster-bundle/20030569.html"},


    # ══════════════════════════════════════════════════════════════════════════
    # MEGA EVOLUTION — PERFECT ORDER (Mar 2026)  ·  PC ETB $247+ resale
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Perfect Order PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10372-109/pokemon-tcg-mega-evolution-perfect-order-pokemon-center-elite-trainer-box"},
    {"name": "Perfect Order ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-mega-evolution-s3-perfect-order-elite-trainer-box/-/A-95230445"},
    {"name": "Perfect Order ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-perfect-order-elite-trainer-box/JJG2TL3W86"},
    {"name": "Perfect Order ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-perfect-order-elite-trainer-box/20031957.html"},
    {"name": "Perfect Order Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10380-119/pokemon-tcg-mega-evolution-perfect-order-booster-display-box-36-packs"},
    {"name": "Perfect Order Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-perfect-order-booster-box-36-packs/JJG2TL3QWS"},
    {"name": "Perfect Order Booster Bundle - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10377-109"},
    {"name": "Perfect Order Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-mega-evolution-s3-perfect-order-booster-bundle-box/-/A-95230447"},
    {"name": "Perfect Order Booster Bundle - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-perfect-order-booster-bundle/JJG2TL3QK2"},


    # ══════════════════════════════════════════════════════════════════════════
    # MEGA EVOLUTION — ENHANCED BOOSTER BOX  ·  $268+ resale
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Mega Evolution Enhanced Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10057-127/pokemon-tcg-mega-evolution-enhanced-booster-display-box-36-packs-and-1-promo-card"},
    {"name": "Mega Evolution Enhanced Booster Box - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pokemon-tcg-mega-evolution-enhanced-booster-display-box-36-packs-box-topper/-/A-1006274804"},
    {"name": "Mega Evolution Enhanced Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-mega-evolution-booster-box-enhanced-version/JJG2TLXTZK"},
    {"name": "Mega Evolution Enhanced Booster Box - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-mega-evolution-booster-box/20023801.html"},


    # ══════════════════════════════════════════════════════════════════════════
    # ULTRA PREMIUM COLLECTIONS
    # ══════════════════════════════════════════════════════════════════════════

    # -- Mega Charizard X ex UPC  ~$185 resale --
    {"name": "Mega Charizard X ex UPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10065-109/pokemon-tcg-mega-charizard-x-ex-ultra-premium-collection"},
    {"name": "Mega Charizard X ex UPC - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Mega-Charizard-X-ex-Ultra-Premium-Collection-UPC/18553766405"},
    {"name": "Mega Charizard X ex UPC - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-charizard-x-ex-ultra-premium-collection/JJG2TLXYCP"},
    {"name": "Mega Charizard X ex UPC - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-mega-charizard-x-ex-ultra-premium-collection/20026985.html"},

    # -- Team Rocket's Moltres ex UPC  ~$218 resale --
    {"name": "Team Rocket's Moltres ex UPC - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pokemon-tcg-team-rocket-s-moltres-ex-ultra-premium-collection/-/A-1007482805"},
    {"name": "Team Rocket's Moltres ex UPC - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-Team-Rocket-s-Moltres-ex-Ultra-Premium-Collection/18515010372"},
    {"name": "Team Rocket's Moltres ex UPC - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-pokemon-team-rockets-moltres-ex-ultra-premium-collection-english/JJG2TLXG4V"},
    {"name": "Team Rocket's Moltres ex UPC - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-team-rocket-moltres-ex-ultra-premium-collection/20026508.html"},

    # -- Mega Lucario ex Figure Collection  ~$42 resale --
    {"name": "Mega Lucario ex Figure Collection - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-lucario-ex-figure-collection/JJG2TLXQG2"},
    {"name": "Mega Lucario ex Figure Collection - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-ME1-Mega-Evolution-Lucario-Figure-Collection/17918917897"},

    # -- Celebrations UPC  ~$950 resale (2021, watch for restocks) --
    {"name": "Celebrations Ultra Premium Collection - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pok-mon-Trading-Card-Games-25th-Anniversary-Celebrations-Ultra-Premium-Collection/718429382"},
    {"name": "Celebrations Ultra Premium Collection - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-celebrations-ultra-premium-collection/11150628.html"},
    {"name": "Celebrations Ultra Premium Collection - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-trading-card-game-celebrations-ultra-premium-collection/6473336.p?skuId=6473336"},


    # ══════════════════════════════════════════════════════════════════════════
    # BLOOMING WATERS 151 PREMIUM COLLECTION
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Blooming Waters Premium Collection - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-blooming-waters-premium-collection/-/A-94724987"},
    {"name": "Blooming Waters Premium Collection - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pok-mon-TCG-Blooming-Waters-Premium-Collection/15130366484"},
    {"name": "Blooming Waters Premium Collection - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-blooming-waters-premium-collection/JJG2TL25QK"},
    {"name": "Blooming Waters Premium Collection - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-blooming-waters-premium-collection/20018822.html"},


    # ══════════════════════════════════════════════════════════════════════════
    # 30TH CELEBRATION — PRIORITY PRODUCTS
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "30th Celebration ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/-/A-1010892076"},

    {"name": "30th Celebration ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-30th-celebration-elite-trainer-box/JJG2TL8XCJ/sku/6685559"},

    {"name": "30th Celebration UPC Day or Night - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-30th-celebration-ultra-premium-collection-day-or-night-1-ultra-premium-collection-per-order-styles-may-vary/JJG2TL8254/sku/6685563"},


    # ══════════════════════════════════════════════════════════════════════════
    # POKÉMON DAY 2026 COLLECTION  (30th Anniversary)
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Pokemon Day 2026 Collection - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/10-10394-108/pokemon-tcg-pokemon-day-2026-collection"},
    {"name": "Pokemon Day 2026 Collection - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/2025-pok-pokemon-day/-/A-95082138"},
    {"name": "Pokemon Day 2026 Collection - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/POKEMON-PIKACHU-POKEMON-DAY-COLLECTION-BOX/18981958891"},
    {"name": "Pokemon Day 2026 Collection - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-pokemon-day-2026-collection/JJG2TL3JS9"},
    {"name": "Pokemon Day 2026 Collection - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/toys-games/trading-cards/products/pokemon-trading-card-game-pokemon-day-2026-collection/20030148.html"},


    # ══════════════════════════════════════════════════════════════════════════
    # 🏪 IN-STORE STOCK — your local area stores
    # Alerts fire when the product hits shelves at a local Target, Walmart,
    # or Best Buy so you can drive there and grab it at MSRP.
    # ══════════════════════════════════════════════════════════════════════════

    # -- Prismatic Evolutions (still restocking) --
    {"name": "Prismatic Evolutions ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-prismatic-evolutions-elite-trainer-box/-/A-93954444"},
    {"name": "Prismatic Evolutions ETB - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pokemon-Scarlet-Violet-Prismatic-Evolutions-Elite-Trainer-Box/13816151308"},
    {"name": "Prismatic Evolutions ETB - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-elite-trainer-box/JJG2TLCW3L"},

    {"name": "Prismatic Evolutions Booster Bundle - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-prismatic-evolutions-booster-bundle/-/A-93954446"},
    {"name": "Prismatic Evolutions Booster Bundle - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/POKEMON-SV8-5-PRISMATIC-EVO-BST-BUNDLE/14803962651"},
    {"name": "Prismatic Evolutions Booster Bundle - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-booster-bundle/JJG2TL23JK"},

    {"name": "Prismatic Evolutions Super Premium Collection - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-prismatic-evolutions-super-premium-collection/-/A-94300072"},
    {"name": "Prismatic Evolutions Super Premium Collection - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pok-mon-TCG-Scarlet-Violet-8-5-Prismatic-Evolutions-Super-Premium-Collection/15494520186"},
    {"name": "Prismatic Evolutions Super Premium Collection - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-super-premium-collection/JJG2TL23CW"},

    # -- Ascended Heroes (newest ME set, high resale) --
    {"name": "Ascended Heroes ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/2025-pok-me-2-5-elite-trainer-box/-/A-95082118"},
    {"name": "Ascended Heroes ETB - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pok-mon-Trading-Card-Game-Mega-Evolution-Ascended-Heroes-Elite-Trainer-Box/18710966734"},
    {"name": "Ascended Heroes ETB - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-ascended-heroes-elite-trainer-box/JJG2TLXSFV"},

    {"name": "Ascended Heroes Booster Bundle - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pok-mon-TCG-Mega-Evolution-Ascended-Heroes-Booster-Bundle-6-Packs/18728422476"},
    {"name": "Ascended Heroes Booster Bundle - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-ascended-heroes-booster-bundle/JJG2TL3JP8"},

    # -- Perfect Order (just released) --
    {"name": "Perfect Order ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-mega-evolution-s3-perfect-order-elite-trainer-box/-/A-95230445"},
    {"name": "Perfect Order ETB - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-perfect-order-elite-trainer-box/JJG2TL3W86"},

    {"name": "Perfect Order Booster Bundle - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-233-mon-mega-evolution-s3-perfect-order-booster-bundle-box/-/A-95230447"},
    {"name": "Perfect Order Booster Bundle - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-perfect-order-booster-bundle/JJG2TL3QK2"},

    # -- Journey Together --
    {"name": "Journey Together ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/2025-pok-233-mon-scarlet-violet-s9-elite-trainer-box/-/A-93803439"},
    {"name": "Journey Together ETB - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pokemon-Trading-Card-Game-Scarlet-Violet-9-Journey-Together-Elite-Trainer-Box/15156564532"},
    {"name": "Journey Together ETB - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-journey-together-booster-box-36-packs/JJG2TL2QS8"},

    # -- Destined Rivals --
    {"name": "Destined Rivals ETB - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Destined-Rivals-Elite-Trainer-Box-ETB/16728861909"},
    {"name": "Destined Rivals ETB - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-destined-rivals-elite-trainer-box/JJG2TL22PF"},

    # -- Ultra Premium Collections (high value — worth driving for) --
    {"name": "Mega Charizard X ex UPC - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Mega-Charizard-X-ex-Ultra-Premium-Collection-UPC/18553766405"},
    {"name": "Mega Charizard X ex UPC - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-charizard-x-ex-ultra-premium-collection/JJG2TLXYCP"},

    {"name": "Team Rocket's Moltres ex UPC - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pokemon-tcg-team-rocket-s-moltres-ex-ultra-premium-collection/-/A-1007482805"},
    {"name": "Team Rocket's Moltres ex UPC - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pokemon-Team-Rocket-s-Moltres-ex-Ultra-Premium-Collection/18515010372"},
    {"name": "Team Rocket's Moltres ex UPC - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-pokemon-team-rockets-moltres-ex-ultra-premium-collection-english/JJG2TLXG4V"},

    # -- Pokemon Day 2026 Collection --
    {"name": "Pokemon Day 2026 Collection - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/2025-pok-pokemon-day/-/A-95082138"},
    {"name": "Pokemon Day 2026 Collection - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/POKEMON-PIKACHU-POKEMON-DAY-COLLECTION-BOX/18981958891"},
    {"name": "Pokemon Day 2026 Collection - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-pokemon-day-2026-collection/JJG2TL3JS9"},

    # -- Phantasmal Flames --
    {"name": "Phantasmal Flames ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-233-mon-trading-card-game-mega-evolution-8212-phantasmal-flames-elite-trainer-box/-/A-94860231"},
    {"name": "Phantasmal Flames ETB - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-phantasmal-flames-elite-trainer-box/JJG2TL2VT6"},


    # ══════════════════════════════════════════════════════════════════════════
    # CHAOS RISING — May 22 2026  ·  Mega Greninja ex  ·  UPCOMING
    # Monitor starts BLITZ mode (3s) on release day.
    # URLs below are pre-release stubs — will activate on launch day.
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Chaos Rising PC ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/pokemon-tcg-mega-evolution-chaos-rising-pokemon-center-elite-trainer-box"},
    {"name": "Chaos Rising ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=chaos+rising+elite+trainer+box"},
    {"name": "Chaos Rising ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=chaos+rising+elite+trainer+box"},
    {"name": "Chaos Rising ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/searchpage.jsp?st=chaos+rising+elite+trainer+box"},
    {"name": "Chaos Rising ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=chaos+rising+elite+trainer+box&t=product"},
    {"name": "Chaos Rising Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/pokemon-tcg-mega-evolution-chaos-rising-booster-display-box"},
    {"name": "Chaos Rising Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=chaos+rising+booster+bundle"},

    # -- Chaos Rising In-Store (launch day = drive there immediately) --
    {"name": "Chaos Rising ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/s?searchTerm=chaos+rising+elite+trainer+box"},
    {"name": "Chaos Rising ETB - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/search?q=chaos+rising+elite+trainer+box"},
    {"name": "Chaos Rising ETB - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/site/searchpage.jsp?st=chaos+rising+elite+trainer+box"},




    # ══════════════════════════════════════════════════════════════════════════
    # SURGING SPARKS (SV8) — Nov 8 2024  ·  Pikachu ex / Iron Crown ex
    # ══════════════════════════════════════════════════════════════════════════

    # -- ETBs --
    {"name": "Surging Sparks ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87386/pokemon-tcg-scarlet-violet-surging-sparks-elite-trainer-box"},
    {"name": "Surging Sparks ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-surging-sparks-elite-trainer-box/-/A-92396126"},
    {"name": "Surging Sparks ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Surging-Sparks-Elite-Trainer-Box/13476694424"},
    {"name": "Surging Sparks ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-surging-sparks-elite-trainer-box/6596534.p"},
    {"name": "Surging Sparks ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=surging+sparks+elite+trainer+box&t=product"},
    {"name": "Surging Sparks ETB - Sam's Club",
     "retailer": "sams_club",
     "url": "https://www.samsclub.com/s/surging%20sparks%20elite%20trainer%20box"},

    # -- Booster Box --
    {"name": "Surging Sparks Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87385/pokemon-tcg-scarlet-violet-surging-sparks-booster-display-box"},
    {"name": "Surging Sparks Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-surging-sparks-booster-display-box/6596536.p"},
    {"name": "Surging Sparks Booster Box - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=surging+sparks+booster+display+box&t=product"},

    # -- Booster Bundle --
    {"name": "Surging Sparks Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=surging+sparks+booster+bundle"},
    {"name": "Surging Sparks Booster Bundle - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/searchpage.jsp?st=surging+sparks+booster+bundle"},
    {"name": "Surging Sparks Booster Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=surging+sparks+booster+bundle"},

    # -- Special Collections --
    {"name": "Surging Sparks Super Premium Collection - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87388/pokemon-tcg-scarlet-violet-surging-sparks-super-premium-collection"},
    {"name": "Surging Sparks Super Premium Collection - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=surging+sparks+super+premium+collection"},
    {"name": "Surging Sparks Iron Thorns ex SPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87390/pokemon-tcg-scarlet-violet-surging-sparks-iron-thorns-ex-special-collection"},
    {"name": "Surging Sparks Eevee Grove SPC - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=surging+sparks+eevee+grove+special+collection"},

    # -- In-Store --
    {"name": "Surging Sparks ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-surging-sparks-elite-trainer-box/-/A-92396126"},
    {"name": "Surging Sparks ETB - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Surging-Sparks-Elite-Trainer-Box/13476694424"},
    {"name": "Surging Sparks ETB - Best Buy (In-Store)",
     "retailer": "bestbuy_instore",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-surging-sparks-elite-trainer-box/6596534.p"},


    # ══════════════════════════════════════════════════════════════════════════
    # STELLAR CROWN (SV7) — Sep 13 2024  ·  Terapagos ex
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Stellar Crown ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87185/pokemon-tcg-scarlet-violet-stellar-crown-elite-trainer-box"},
    {"name": "Stellar Crown ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-stellar-crown-elite-trainer-box/-/A-91718064"},
    {"name": "Stellar Crown ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Stellar-Crown-Elite-Trainer-Box/8041793882"},
    {"name": "Stellar Crown ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-stellar-crown-elite-trainer-box/6586671.p"},
    {"name": "Stellar Crown ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=stellar+crown+elite+trainer+box&t=product"},
    {"name": "Stellar Crown Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87183/pokemon-tcg-scarlet-violet-stellar-crown-booster-display-box"},
    {"name": "Stellar Crown Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-stellar-crown-booster-display-box/6586673.p"},
    {"name": "Stellar Crown Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=stellar+crown+booster+bundle"},
    {"name": "Stellar Crown Booster Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=stellar+crown+booster+bundle"},
    {"name": "Stellar Crown Terapagos ex SPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87188/pokemon-tcg-scarlet-violet-stellar-crown-terapagos-ex-special-collection"},
    # -- In-Store --
    {"name": "Stellar Crown ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-stellar-crown-elite-trainer-box/-/A-91718064"},
    {"name": "Stellar Crown ETB - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Stellar-Crown-Elite-Trainer-Box/8041793882"},


    # ══════════════════════════════════════════════════════════════════════════
    # SHROUDED FABLE (SV6.5) — Aug 2 2024  ·  Pecharunt ex · Ogerpon ex
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Shrouded Fable ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87036/pokemon-tcg-scarlet-violet-shrouded-fable-elite-trainer-box"},
    {"name": "Shrouded Fable ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-shrouded-fable-elite-trainer-box/-/A-91193088"},
    {"name": "Shrouded Fable ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-shrouded-fable-elite-trainer-box/6585398.p"},
    {"name": "Shrouded Fable ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=shrouded+fable+elite+trainer+box"},
    {"name": "Shrouded Fable ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=shrouded+fable+elite+trainer+box&t=product"},
    {"name": "Shrouded Fable Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87034/pokemon-tcg-scarlet-violet-shrouded-fable-booster-display-box"},
    {"name": "Shrouded Fable Pecharunt ex SPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-87039/pokemon-tcg-scarlet-violet-shrouded-fable-pecharunt-ex-special-collection"},


    # ══════════════════════════════════════════════════════════════════════════
    # TEMPORAL FORCES (SV5) — Mar 22 2024  ·  Iron Crown ex / Walking Wake ex
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Temporal Forces ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-86581/pokemon-tcg-scarlet-violet-temporal-forces-elite-trainer-box"},
    {"name": "Temporal Forces ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-temporal-forces-elite-trainer-box/-/A-89756694"},
    {"name": "Temporal Forces ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Temporal-Forces-Elite-Trainer-Box/5261819700"},
    {"name": "Temporal Forces ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-temporal-forces-elite-trainer-box/6570616.p"},
    {"name": "Temporal Forces ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=temporal+forces+elite+trainer+box&t=product"},
    {"name": "Temporal Forces Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-86579/pokemon-tcg-scarlet-violet-temporal-forces-booster-display-box"},
    {"name": "Temporal Forces Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-temporal-forces-booster-display-box/6570618.p"},
    {"name": "Temporal Forces Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=temporal+forces+booster+bundle"},
    {"name": "Temporal Forces Booster Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=temporal+forces+booster+bundle"},
    {"name": "Temporal Forces Iron Crown ex SPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-86584/pokemon-tcg-scarlet-violet-temporal-forces-iron-crown-ex-special-collection"},
    # -- In-Store --
    {"name": "Temporal Forces ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-temporal-forces-elite-trainer-box/-/A-89756694"},
    {"name": "Temporal Forces ETB - Walmart (In-Store)",
     "retailer": "walmart_instore",
     "url": "https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Temporal-Forces-Elite-Trainer-Box/5261819700"},


    # ══════════════════════════════════════════════════════════════════════════
    # PALDEAN FATES (SV4.5) — Jan 26 2024  ·  Shiny Charizard ex  ·  HIGH DEMAND
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Paldean Fates ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-86175/pokemon-tcg-scarlet-violet-paldean-fates-elite-trainer-box"},
    {"name": "Paldean Fates ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=paldean+fates+elite+trainer+box"},
    {"name": "Paldean Fates ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=paldean+fates+elite+trainer+box"},
    {"name": "Paldean Fates ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-paldean-fates-elite-trainer-box/6569612.p"},
    {"name": "Paldean Fates ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=paldean+fates+elite+trainer+box&t=product"},
    {"name": "Paldean Fates Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-86173/pokemon-tcg-scarlet-violet-paldean-fates-booster-display-box"},
    {"name": "Paldean Fates Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=paldean+fates+booster+bundle"},
    {"name": "Paldean Fates Booster Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=paldean+fates+booster+bundle"},
    # -- Shiny Charizard ex Premium Collection (T2 special) --
    {"name": "Paldean Fates Shiny Charizard ex Premium Collection - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-86176/pokemon-tcg-scarlet-violet-paldean-fates-shiny-charizard-ex-premium-collection"},
    {"name": "Paldean Fates Shiny Charizard ex Premium Collection - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=paldean+fates+shiny+charizard+ex+premium+collection"},
    {"name": "Paldean Fates Shiny Charizard ex Premium Collection - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=paldean+fates+shiny+charizard+ex+premium+collection"},
    {"name": "Paldean Fates Shiny Charizard ex Premium Collection - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/searchpage.jsp?st=paldean+fates+shiny+charizard+ex+premium+collection"},
    # -- In-Store --
    {"name": "Paldean Fates ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/s?searchTerm=paldean+fates+elite+trainer+box"},
    {"name": "Paldean Fates Shiny Charizard ex Premium Collection - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/s?searchTerm=paldean+fates+shiny+charizard+ex+premium+collection"},


    # ══════════════════════════════════════════════════════════════════════════
    # POKEMON 151 (SV3.5) — Sep 22 2023  ·  Mew ex UPC  ·  TOP RESALE VALUE
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Pokemon 151 ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85242/pokemon-tcg-scarlet-violet-151-elite-trainer-box"},
    {"name": "Pokemon 151 ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pokemon-trading-card-game-scarlet-violet-151-elite-trainer-box/-/A-88753499"},
    {"name": "Pokemon 151 ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=pokemon+151+elite+trainer+box"},
    {"name": "Pokemon 151 ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-151-elite-trainer-box/6556966.p"},
    {"name": "Pokemon 151 ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=pokemon+151+elite+trainer+box&t=product"},
    {"name": "Pokemon 151 Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85240/pokemon-tcg-scarlet-violet-151-booster-display-box"},
    {"name": "Pokemon 151 Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-151-booster-display-box/6556968.p"},
    {"name": "Pokemon 151 Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=pokemon+151+booster+bundle"},
    {"name": "Pokemon 151 Booster Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=pokemon+151+booster+bundle"},
    # -- Mew ex Ultra Premium Collection (T1 — extremely high resale) --
    {"name": "Pokemon 151 Mew ex UPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85244/pokemon-tcg-scarlet-violet-151-mew-ex-ultra-premium-collection"},
    {"name": "Pokemon 151 Mew ex UPC - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=pokemon+151+mew+ultra+premium+collection"},
    {"name": "Pokemon 151 Mew ex UPC - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=pokemon+151+mew+ultra+premium+collection"},
    {"name": "Pokemon 151 Mew ex UPC - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+151+mew+ex+ultra+premium+collection"},
    # -- In-Store --
    {"name": "Pokemon 151 ETB - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/p/pokemon-trading-card-game-scarlet-violet-151-elite-trainer-box/-/A-88753499"},
    {"name": "Pokemon 151 Mew ex UPC - Target (In-Store)",
     "retailer": "target_instore",
     "url": "https://www.target.com/s?searchTerm=pokemon+151+mew+ultra+premium+collection"},


    # ══════════════════════════════════════════════════════════════════════════
    # PARADOX RIFT (SV4) — Nov 3 2023  ·  Roaring Moon ex / Iron Valiant ex
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Paradox Rift ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85620/pokemon-tcg-scarlet-violet-paradox-rift-elite-trainer-box"},
    {"name": "Paradox Rift ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-paradox-rift-elite-trainer-box/-/A-88821898"},
    {"name": "Paradox Rift ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=paradox+rift+elite+trainer+box"},
    {"name": "Paradox Rift ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-paradox-rift-elite-trainer-box/6562793.p"},
    {"name": "Paradox Rift ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=paradox+rift+elite+trainer+box&t=product"},
    {"name": "Paradox Rift Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85618/pokemon-tcg-scarlet-violet-paradox-rift-booster-display-box"},
    {"name": "Paradox Rift Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-paradox-rift-booster-display-box/6562795.p"},
    {"name": "Paradox Rift Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=paradox+rift+booster+bundle"},
    {"name": "Paradox Rift Roaring Moon ex SPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85623/pokemon-tcg-scarlet-violet-paradox-rift-roaring-moon-ex-special-collection"},
    {"name": "Paradox Rift Iron Valiant ex SPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85624/pokemon-tcg-scarlet-violet-paradox-rift-iron-valiant-ex-special-collection"},


    # ══════════════════════════════════════════════════════════════════════════
    # OBSIDIAN FLAMES (SV3) — Aug 11 2023  ·  Charizard ex / Tyranitar ex
    # ══════════════════════════════════════════════════════════════════════════

    {"name": "Obsidian Flames ETB - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85062/pokemon-tcg-scarlet-violet-obsidian-flames-elite-trainer-box"},
    {"name": "Obsidian Flames ETB - Target",
     "retailer": "target",
     "url": "https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-obsidian-flames-elite-trainer-box/-/A-88459342"},
    {"name": "Obsidian Flames ETB - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=obsidian+flames+elite+trainer+box"},
    {"name": "Obsidian Flames ETB - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-obsidian-flames-elite-trainer-box/6554891.p"},
    {"name": "Obsidian Flames ETB - GameStop",
     "retailer": "gamestop",
     "url": "https://www.gamestop.com/search#q=obsidian+flames+elite+trainer+box&t=product"},
    {"name": "Obsidian Flames Booster Box - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85060/pokemon-tcg-scarlet-violet-obsidian-flames-booster-display-box"},
    {"name": "Obsidian Flames Booster Box - Best Buy",
     "retailer": "bestbuy",
     "url": "https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-obsidian-flames-booster-display-box/6554893.p"},
    {"name": "Obsidian Flames Booster Bundle - Target",
     "retailer": "target",
     "url": "https://www.target.com/s?searchTerm=obsidian+flames+booster+bundle"},
    {"name": "Obsidian Flames Booster Bundle - Walmart",
     "retailer": "walmart",
     "url": "https://www.walmart.com/search?q=obsidian+flames+booster+bundle"},
    {"name": "Obsidian Flames Charizard ex SPC - Pokemon Center",
     "retailer": "pokemon_center",
     "url": "https://www.pokemoncenter.com/product/290-85065/pokemon-tcg-scarlet-violet-obsidian-flames-charizard-ex-special-collection"},


    # Costco
    {
        "name": 'Charizard ex Super-Premium Collection - Costco',
        "retailer": 'costco',
        "url": 'https://www.costco.com/p/-/pokmon-tcg-charizard-ex-super-premium-collection/4000313298',
    },
    {
        "name": 'Unova Heavy Hitters Premium Collection 2-Pack - Costco',
        "retailer": 'costco',
        "url": 'https://www.costco.com/CompareProductsDisplay?partNumbers=1943158',
    },
    {
        "name": 'Mega Charizard X ex UPC 2-Pack - Costco',
        "retailer": 'costco',
        "url": 'https://www.costco.com/CompareProductsDisplay?partNumbers=4000433058',
    },
    {
        "name": 'Charizard ex Super-Premium Collection - Costco Warehouse',
        "retailer": 'costco_instore',
        "url": 'https://www.costco.com/p/-/pokmon-tcg-charizard-ex-super-premium-collection/4000313298',
    },
    {
        "name": 'Unova Heavy Hitters Premium Collection 2-Pack - Costco Warehouse',
        "retailer": 'costco_instore',
        "url": 'https://www.costco.com/CompareProductsDisplay?partNumbers=1943158',
    },
    {
        "name": 'Mega Charizard X ex UPC 2-Pack - Costco Warehouse',
        "retailer": 'costco_instore',
        "url": 'https://www.costco.com/CompareProductsDisplay?partNumbers=4000433058',
    },

    # AUTO-GENERATED IN-STORE MIRRORS
    {
        "name": 'Prismatic Evolutions Surprise Box - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/2025-pokemon-scarlet-violet-s8-5-prismatic-evolutions-surprise-box/-/A-94336414',
    },
    {
        "name": 'Prismatic Evolutions Surprise Box - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pokemon-Trading-Card-Games-Scarlett-Violet-8-5-Prismatic-Evolutions-Surprise-Box/14148473268',
    },
    {
        "name": 'Prismatic Evolutions Surprise Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-surprise-box/JJG2TLCK6H',
    },
    {
        "name": 'Prismatic Evolutions Lucario ex & Tyranitar ex Collection - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pokemon-tcg-scarlet-violet-prismatic-evolutions-lucario-ex-tyranitar-ex-premium-collection-box-14-packs/-/A-1005879863',
    },
    {
        "name": 'Prismatic Evolutions Costco 2-Pack ETB+Bundle - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pokemon-Prismatic-Evolutions-Elite-Trainer-Box-Booster-Bundle/16817304907',
    },
    {
        "name": 'Twilight Masquerade ETB - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-twilight-masquerade-elite-trainer-box/-/A-91619960',
    },
    {
        "name": 'Twilight Masquerade ETB - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pokemon-Trading-Card-Games-SV6-Twilight-Masquerade-Elite-Trainer-Box/5558569421',
    },
    {
        "name": 'Twilight Masquerade ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-twilight-masquerade-elite-trainer-box/J3YSYH8XK6',
    },
    {
        "name": 'Twilight Masquerade Booster Box - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pokemon-TCG-Twilight-Masquerade-Booster-Box-36-Packs/5736034613',
    },
    {
        "name": 'Destined Rivals PC ETB - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pok-mon-TCG-Scarlet-Violet-Destined-Rivals-Pok-mon-Center-Elite-Trainer-Box/15718673510',
    },
    {
        "name": 'Destined Rivals Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-destined-rivals-booster-box-36-packs/JJG2TL25CG',
    },
    {
        "name": 'Journey Together Booster Bundle - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-journey-together-booster-bundle/-/A-94300074',
    },
    {
        "name": 'Journey Together Enhanced Booster Box - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pok-mon-TCG-Scarlet-Violet-9-Journey-Together-Enhanced-Booster-Display/15053563608',
    },
    {
        "name": 'Journey Together Booster Bundle - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-trading-card-game-scarlet-violet-journey-together-booster-bundle-6-pk/6614264.p?skuId=6614264',
    },
    {
        "name": 'White Flare ETB - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-white-flare-elite-trainer-box/-/A-94636860',
    },
    {
        "name": 'White Flare ETB - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-10-5-White-Flare-Elite-Trainer-Box-9-Packs-Promo-Card/16446322202',
    },
    {
        "name": 'White Flare ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-scarlet-violet-white-flare-elite-trainer-box/JJG2TL28KK',
    },
    {
        "name": 'Black Bolt ETB - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-Black-Bolt-Elite-Trainer-Box-ETB/17317016821',
    },
    {
        "name": 'Black Bolt Booster Bundle - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-trading-card-game-scarlet-violet-black-bolt-booster-bundle/6632402.p?skuId=6632402',
    },
    {
        "name": 'Unova Victini Illustration Collection - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-233-mon-trading-card-game-unova-victini-illustration-collection/-/A-94636866',
    },
    {
        "name": 'Unova Victini Illustration Collection - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pokemon-TCG-Scarlet-Violet-10-5-Unova-Victini-Illustration-Collection-4-Packs/16454274271',
    },
    {
        "name": 'Unova Victini Illustration Collection - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-unova-victini-illustration-collection/JJG2TL232V',
    },
    {
        "name": 'Phantasmal Flames Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-phantasmal-flames-booster-box-36-packs/JJG2TL3XYR',
    },
    {
        "name": 'Phantasmal Flames Booster Bundle - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-233-mon-trading-card-game-mega-evolution-8212-phantasmal-flames-booster-bundle/-/A-94884496',
    },
    {
        "name": 'Phantasmal Flames Booster Bundle - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-phantasmal-flames-6pk-booster-bundle/JJG2TL3XY4',
    },
    {
        "name": 'Ascended Heroes PC ETB - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pokemon-tcg-mega-evolution-ascended-heroes-pokemon-center-elite-trainer-box/-/A-1009871732',
    },
    {
        "name": 'Perfect Order Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-mega-evolution-perfect-order-booster-box-36-packs/JJG2TL3QWS',
    },
    {
        "name": 'Mega Evolution Enhanced Booster Box - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pokemon-tcg-mega-evolution-enhanced-booster-display-box-36-packs-box-topper/-/A-1006274804',
    },
    {
        "name": 'Mega Evolution Enhanced Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-mega-evolution-booster-box-enhanced-version/JJG2TLXTZK',
    },
    {
        "name": 'Mega Lucario ex Figure Collection - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-mega-lucario-ex-figure-collection/JJG2TLXQG2',
    },
    {
        "name": 'Mega Lucario ex Figure Collection - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pokemon-ME1-Mega-Evolution-Lucario-Figure-Collection/17918917897',
    },
    {
        "name": 'Celebrations Ultra Premium Collection - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pok-mon-Trading-Card-Games-25th-Anniversary-Celebrations-Ultra-Premium-Collection/718429382',
    },
    {
        "name": 'Celebrations Ultra Premium Collection - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-trading-card-game-celebrations-ultra-premium-collection/6473336.p?skuId=6473336',
    },
    {
        "name": 'Blooming Waters Premium Collection - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-233-mon-trading-card-game-blooming-waters-premium-collection/-/A-94724987',
    },
    {
        "name": 'Blooming Waters Premium Collection - Walmart (In-Store)',
        "retailer": 'walmart_instore',
        "url": 'https://www.walmart.com/ip/Pok-mon-TCG-Blooming-Waters-Premium-Collection/15130366484',
    },
    {
        "name": 'Blooming Waters Premium Collection - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-blooming-waters-premium-collection/JJG2TL25QK',
    },
    {
        "name": '30th Celebration ETB - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/-/A-1010892076',
    },
    {
        "name": '30th Celebration ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-30th-celebration-elite-trainer-box/JJG2TL8XCJ/sku/6685559',
    },
    {
        "name": '30th Celebration UPC Day or Night - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/product/pokemon-trading-card-game-30th-celebration-ultra-premium-collection-day-or-night-1-ultra-premium-collection-per-order-styles-may-vary/JJG2TL8254/sku/6685563',
    },
    {
        "name": 'Surging Sparks Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-surging-sparks-booster-display-box/6596536.p',
    },
    {
        "name": 'Stellar Crown ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-stellar-crown-elite-trainer-box/6586671.p',
    },
    {
        "name": 'Stellar Crown Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-stellar-crown-booster-display-box/6586673.p',
    },
    {
        "name": 'Shrouded Fable ETB - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-shrouded-fable-elite-trainer-box/-/A-91193088',
    },
    {
        "name": 'Shrouded Fable ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-shrouded-fable-elite-trainer-box/6585398.p',
    },
    {
        "name": 'Temporal Forces ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-temporal-forces-elite-trainer-box/6570616.p',
    },
    {
        "name": 'Temporal Forces Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-temporal-forces-booster-display-box/6570618.p',
    },
    {
        "name": 'Paldean Fates ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-paldean-fates-elite-trainer-box/6569612.p',
    },
    {
        "name": 'Pokemon 151 ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-151-elite-trainer-box/6556966.p',
    },
    {
        "name": 'Pokemon 151 Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-151-booster-display-box/6556968.p',
    },
    {
        "name": 'Paradox Rift ETB - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-paradox-rift-elite-trainer-box/-/A-88821898',
    },
    {
        "name": 'Paradox Rift ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-paradox-rift-elite-trainer-box/6562793.p',
    },
    {
        "name": 'Paradox Rift Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-paradox-rift-booster-display-box/6562795.p',
    },
    {
        "name": 'Obsidian Flames ETB - Target (In-Store)',
        "retailer": 'target_instore',
        "url": 'https://www.target.com/p/pok-mon-trading-card-game-scarlet-violet-obsidian-flames-elite-trainer-box/-/A-88459342',
    },
    {
        "name": 'Obsidian Flames ETB - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-obsidian-flames-elite-trainer-box/6554891.p',
    },
    {
        "name": 'Obsidian Flames Booster Box - Best Buy (In-Store)',
        "retailer": 'bestbuy_instore',
        "url": 'https://www.bestbuy.com/site/pokemon-tcg-scarlet-violet-obsidian-flames-booster-display-box/6554893.p',
    },
]
