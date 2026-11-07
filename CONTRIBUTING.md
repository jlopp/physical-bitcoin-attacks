# Contributing

Thank you for helping keep this list of physical attacks against crypto owners up to date! This document explains what kinds of incidents belong here and how to add them.

## What counts as an appropriate attack

This list tracks **physical ("meatspace") attacks targeting people or entities because of their cryptocurrency holdings or activities**. To be included, an attack should meet all of the following criteria:

1. **Physical world component** — the attack happened in person, not purely online. Online hacks, phishing, exchange breaches, etc. are out of scope.
2. **Crypto-related motive or target** — the victim was targeted because they were known or believed to hold crypto assets, were involved in the crypto industry, or the attackers demanded payment in cryptocurrency.

### In scope

- **Home invasions / armed robberies** where attackers demanded crypto transfers, seed phrases, or hardware wallets
- **Kidnappings for crypto ransom** only if the victim or family members are crypto holders
- **In-person trade robberies** — ambushes during face-to-face buys/sells of crypto for cash
- **SWATting and extortion** with a crypto demand, when the victim was targeted for their crypto involvement
- **Violent attacks on crypto businesses** (exchanges, BTM operators, mining farms)
- **Impersonation attacks** (fake police, fake delivery drivers, fake rideshare) used to gain physical access for crypto theft
- **Torture or coercion** to force victims to transfer crypto or reveal keys
- **Theft of mining hardware** in physical raids

### Out of scope

- Purely digital incidents (exchange hacks, SIM swaps, phishing) with no physical-world attack
- Kidnappings / ransom of wealthy people with no connection to crypto where it just happens to be the demanded payment method
- Fraud/scams that did not involve physical force or threat (e.g., romance scams executed entirely online)
- Verbal threats or online harassment with no physical action
- **Unverified or purely rumored incidents** — we require at least one credible published source (news article, police report, court document)

### Privacy considerations

- Do not publish victims' **full home addresses** or other information that could enable future targeting
- If the victim is a private individual who has not been publicly named, keep them **unidentified** in the entry (e.g., "39 y/o man")
- Link to reputable sources; prefer archive links ([archive.is](https://archive.is), [web.archive.org](https://web.archive.org)) so entries don't rot

## How to update the data

Attack entries live in two places:

1. **`README.md`** — the human-readable table. **This is the only file you edit by hand.**
2. **`attacks.json`** — the machine-readable data powering [the dashboard](https://jlopp.github.io/physical-bitcoin-attacks/). This is a **build artifact**.

### Adding an attack to README.md

Add a new row to the table in `README.md`, in chronological order, this format:

```
| January 15 2027 | Victim Name | City, Region, Country | [Short description of the attack](https://archive.is/example) [(original link)](https://www.example.com/article) |
```

- **Date**: as precise as known. Use `Month Day Year` when known; `Month Year` or `Year` when partially known. If a granular part of the date is unknown, position the new row at the top of the entries for that month or year.
- **Victim**: name if publicly reported; otherwise a short generic descriptor (`Unidentified`, `34 y/o man`, "Couple", "Brothers", "Teenagers", etc.)
- **Location**: `City, Region/State, Country` where possible. The country must be last.
- **Description**: one concise sentence with the incident and outcome, as markdown links.

### Regenerating attacks.json (should not be necessary)

**`attacks.json` is generated. Do not hand-edit it.** The GitHub workflow
(`.github/workflows/static.yml`) re-runs the pipeline on every push to `master`
and deploys the result, so any manual change to `attacks.json` is silently
overwritten. If a coordinate is wrong, fix `tools/geocode.py` — that is the
source of truth. The PR check (`validate.yml`) fails if `attacks.json` is out
of sync with the generators.

To regenerate locally from the README:

```bash
python3 tools/parse_readme.py   # README table -> tools/raw_attacks.json
python3 tools/autofill_geo.py   # (optional) geocode locations missing from GEO
python3 tools/geocode.py        # adds coordinates + country codes -> attacks.json
```

`geocode.py` contains a lookup table of known locations. **If your new attack's location isn't in the table yet**, the script will fail with a `MISSING GEO` listing — add the new location to the `GEO` dictionary in `tools/geocode.py` following the existing pattern:

**Watch the sign on latitude:** it is negative in the southern hemisphere
(`-23.55` for São Paulo, not `23.55`). A dropped minus sign still looks
plausible and used to go unnoticed, so `audit_coords.py` now verifies every
point against country polygons and fails the build if one lands in the wrong
hemisphere.

```python
"City, Region, Country": ("City", "Region", "Country", "XX", 12.34, 56.78),
```

Then re-run `geocode.py` and commit both `tools/geocode.py` and `attacks.json`.

### Auditing coordinates

```bash
python3 tools/audit_coords.py           # report only, always exits 0
python3 tools/audit_coords.py --gate    # exit 1 if anything is misplaced (used in CI)
python3 tools/audit_coords.py --fix     # repair geocode.py in place, then regenerate
```

`--fix` patches the `GEO` dict in `geocode.py`, **not** `attacks.json`, so the
repair survives regeneration and shows up in review. Review the diff it
produces before committing. Polygons are vendored in
`tools/ne_10m_admin_0_countries.min.json` so the check runs offline.

### Submitting

1. Open a pull request with a new README.md row
2. Include a source link for the incident in your PR description
3. Maintainers may ask for additional sources if the incident is not widely reported

Thank you for contributing — every verified entry helps the community understand and defend against these attacks.
