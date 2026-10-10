"""Hämtar tävlingar och skriver docs/data/tavlingar.json.

Källan är inte kartlagd ännu (se README). Tills dess behåller skriptet
befintliga tävlingar och uppdaterar bara tidsstämpeln.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "docs" / "data"


def hamta_tavlingar():
    # TODO: implementera när källan är kartlagd. Returnera en lista med
    # {"datum", "typ", "klubb", "distrikt", "ort", "url"}.
    return None


def main():
    fil = DATA / "tavlingar.json"
    nuvarande = json.loads(fil.read_text(encoding="utf-8"))
    nya = hamta_tavlingar()
    if nya is not None:
        nuvarande["tavlingar"] = nya
        nuvarande["uppdaterad"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fil.write_text(json.dumps(nuvarande, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
