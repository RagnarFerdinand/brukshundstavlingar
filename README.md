# Brukshundstävlingar

Tävlingar i svenska brukshundklubbar. Webbapp i `docs/` (GitHub Pages), skrapare i `scraper/`
och en nattlig GitHub Action (`.github/workflows/uppdatera.yml`) som sparar `docs/data/tavlingar.json`.

## Data
- `docs/data/klubbar.json`: 277 lokalklubbar i 18 distrikt, från SBK:s verksamhetsberättelse 2025 (sid 6–7). Bara ortsnamn, inga webbadresser än.
- `docs/data/tavlingar.json`: kommande tävlingar från SBK Tävling (`POST https://brukshundklubben.se/api/search_competition`, ett anrop ger alla). Uppdateras nattligen av `scraper/scrape.py`.

## Öppet
- Arrangörsnamnen i API:t matchar bara delvis klubblistan (t.ex. "Ulricehamns Brukshundklubb" mot "Ulricehamn"). Dessutom finns rasklubbar och Schäfer-distrikt i datan.
- Klubbarnas webbadresser.
