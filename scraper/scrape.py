"""Hämtar kommande tävlingar från SBK Tävling och skriver docs/data/tavlingar.json.

Källa: POST https://brukshundklubben.se/api/search_competition (samma anrop som
sidan https://brukshundklubben.se/sbktavling/prov-tavlingar/ gör). Ett anrop
returnerar alla kommande tävlingar.
"""
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://brukshundklubben.se/api/search_competition"
UT = Path(__file__).resolve().parent.parent / "docs" / "data" / "tavlingar.json"

DISTRIKT = {
    "SBK Värmland-Dals Distrikt": "Värmland-Dal",
    "SBK Skånes Distrikt": "Skåne",
    "SBK Västra Distriktet": "Västra",
    "SBK Smålands Distrikt": "Småland",
    "SBK Övre Norrlands Distrikt": "Övre Norrland",
    "SBK Blekinges Distrikt": "Blekinge",
    "SBK Gävleborgs Distrikt": "Gävleborg",
    "SBK Östergötlands Distrikt": "Östergötland",
    "SBK Västmanlands Distrikt": "Västmanland",
    "SBK Sörmlands Distrikt": "Sörmland",
    "SBK Upplandsdistrikt": "Uppland",
    "SBK Hallands Distrikt": "Halland",
    "SBK Stockholmsdistrikt": "Stockholm",
    "SBK Mellannorrlands Distrikt": "Mellannorrland",
    "SBK Dalarnas Distrikt": "Dalarna",
    "SBK Skaraborgs Distrikt": "Skaraborg",
    "SBK Närkes Distrikt": "Närke",
    "SBK Gotlandsdistriktet": "Gotland",
}


def datum(s):
    """'10/10/2026 00:00:00' (MM/DD/YYYY) -> '2026-10-10'."""
    return datetime.strptime(s.split()[0], "%m/%d/%Y").strftime("%Y-%m-%d")


def hamta():
    kropp = {
        "searchQuery": "", "types": [], "classes": [], "owners": [], "statuses": [],
        "categories": [], "earliestStartDate": "", "latestStartDate": "",
        "hidePassedDates": True, "selectedFacet": "",
    }
    req = urllib.request.Request(
        URL, data=json.dumps(kropp).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["results"]


def main():
    ut = []
    for rad in hamta():
        v = rad["values"]
        if not v.get("competitionStartDateRaw"):
            continue
        ut.append({
            "id": v["id"],
            "datum": datum(v["competitionStartDateRaw"]),
            "slutdatum": datum(v.get("competitionEndDateRaw") or v["competitionStartDateRaw"]),
            "typ": v.get("competitionType", "") or v.get("title", ""),
            "klubb": v.get("competitionOrganizer", ""),
            "distrikt": DISTRIKT.get(v.get("competitionDistrict", ""), v.get("competitionDistrict", "")),
            "status": v.get("status", ""),
            "anmalan_start": v.get("registration_start", ""),
            "anmalan_slut": v.get("registration_deadline", ""),
            "klasser": [k for k in v.get("competitionClasses", "").split(",") if k],
            "url": v.get("url", ""),
        })
    ut.sort(key=lambda t: (t["datum"], t["klubb"]))
    UT.write_text(json.dumps({
        "uppdaterad": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "tavlingar": ut,
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(ut)} tävlingar")


if __name__ == "__main__":
    main()
