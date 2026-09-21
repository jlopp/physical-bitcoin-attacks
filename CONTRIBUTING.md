# Contributing

Thank you for helping keep this list of physical attacks against crypto owners up to date! This document explains what kinds of incidents belong here and how to add them.

## What counts as an appropriate attack

This list tracks **physical ("meatspace") attacks targeting people or entities because of their cryptocurrency holdings or activities**. To be included, an attack should meet all of the following criteria:

1. **Physical world component** — the attack happened in person, not purely online. Online hacks, phishing, exchange breaches, etc. are out of scope.
2. **Crypto-related motive or target** — the victim was targeted because they were known or believed to hold crypto assets, were involved in the crypto industry, or the attackers demanded payment in cryptocurrency.

### In scope

- **Home invasions / armed robberies** where attackers demanded crypto transfers, seed phrases, or hardware wallets
- **Kidnappings for crypto ransom**, including of family members of crypto holders
- **In-person trade robberies** — ambushes during face-to-face buys/sells of crypto for cash
- **SWATting and extortion** with a crypto demand, when the victim was targeted for their crypto involvement
- **Violent attacks on crypto businesses** (exchanges, BTM operators, mining farms)
- **Impersonation attacks** (fake police, fake delivery drivers, fake rideshare) used to gain physical access for crypto theft
- **Torture or coercion** to force victims to transfer crypto or reveal keys
- **Theft of mining hardware** in physical raids

### Out of scope

- Purely digital incidents (exchange hacks, SIM swaps, phishing) with no physical-world attack
- Ordinary street crime where crypto was coincidental (e.g., a phone stolen that happened to have a wallet app, with no evidence of targeting)
- Fraud/scams that did not involve physical force or threat (e.g., romance scams executed entirely online)
- Verbal threats or online harassment with no physical action
- **Unverified or purely rumored incidents** — we require at least one credible published source (news article, police report, court document)

### Privacy considerations

- Do not publish victims' **full home addresses** or other information that could enable future targeting
- If the victim is a private individual who has not been publicly named, keep them **unidentified** in the entry (e.g., "39 y/o man")
- Link to reputable sources; prefer archive links ([archive.is](https://archive.is), [web.archive.org](https://web.archive.org)) so entries don't rot

## How to update the data

Attack entries live in two places that must be kept in sync:

1. **`README.md`** — the human-readable table (the canonical list)
2. **`attacks.json`** — the machine-readable data powering [the dashboard](./index.html)

### Adding an attack to README.md

Add a new row to the table in `README.md`, in chronological order:

```
| January 15, 2027 | Victim Name | City, Region, Country | [Short description of the attack](https://archive.is/example) [(original link)](https://www.example.com/article) |
```

- **Date**: as precise as known. Use `Month Day, Year` when known; `Month, Year` or `?, Year` when partially known.
- **Victim**: name if publicly reported; otherwise a short anonymous descriptor (`Unidentified`, `34 y/o man`, etc.)
- **Location**: `City, Region/State, Country` where possible. The country must be last.
- **Description**: one concise sentence with the incident and outcome, as markdown links.

### Adding the attack to attacks.json

Each entry in `attacks.json` mirrors a README row:

```json
{
  "date": { "raw": "January 15, 2027", "year": 2027 },
  "victim": "Victim Name",
  "location": "City, Region, Country",
  "description": "Short description of the attack",
  "links": [
    { "label": "Short description of the attack", "url": "https://archive.is/example" },
    { "label": "(original link)", "url": "https://www.example.com/article" }
  ],
  "city": "City",
  "region": "Region",
  "country": "Country",
  "country_code": "XX",
  "lat": 12.34,
  "lng": 56.78
}
```

Field requirements:

| Field | Notes |
| :--- | :--- |
| `date.year` | Integer, required. Extracted from `date.raw`. |
| `location` | Must **exactly match** the README's Location cell (the parser keys off this). |
| `country_code` | Two-letter ISO 3166-1 alpha-2 code (e.g., `US`, `FR`, `HK`). |
| `lat` / `lng` | Decimal degrees for the city (or country centroid if only the country is known). Be precise — this drives the dashboard map. |

### Regenerating attacks.json (recommended)

Rather than hand-editing `attacks.json`, you can regenerate it from the README:

```bash
python3 tools/parse_readme.py   # README table -> tools/raw_attacks.json
python3 tools/geocode.py        # adds coordinates + country codes -> attacks.json
```

`geocode.py` contains a lookup table of known locations. **If your new attack's location isn't in the table yet**, the script will fail with a `MISSING GEO` listing — add the new location to the `GEO` dictionary in `tools/geocode.py` following the existing pattern:

```python
"City, Region, Country": ("City", "Region", "Country", "XX", 12.34, 56.78),
```

Then re-run `geocode.py` and commit the updated `attacks.json`.

### Submitting

1. Open a pull request with both the README row and the `attacks.json` entry (or regenerated file)
2. Include a source link for the incident in your PR description
3. Maintainers may ask for additional sources if the incident is not widely reported

Thank you for contributing — every verified entry helps the community understand and defend against these attacks.
