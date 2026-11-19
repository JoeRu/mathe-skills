#!/usr/bin/env python3
"""Legt die Schlüsseldatei und die Profildateien für eine Lerngruppe an.

Läuft auf dem Rechner der Lehrkraft. Liest eine Kursliste (Schulportal-Export als .xlsx
oder .csv) und erzeugt:

  Personenbezogenes/schluessel-<KURS>.csv   Pseudonym <-> Klarname   (bleibt hier)
  Schuelerdaten/<KURS>/kuerzel-map.csv      Pseudonym <-> bettermarks-Kürzel
  Schuelerdaten/<KURS>/profile/S01.md ...   leere Profile

Die Schlüsseldatei wird nur von dir geöffnet. Claude liest sie nie.

Aufruf:
    python schluessel_anlegen.py --kurs 2026-27_KURSID --liste "..\\Personenbezogenes\\Kursliste_KURSID.xlsx"

Bestehende Dateien werden nicht überschrieben. Kommen später Kinder dazu,
denselben Aufruf wiederholen: neue Zeilen bekommen die nächsten freien Nummern.
"""
from __future__ import annotations

import argparse
import csv
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from schulordner import wurzel, schulpaket, einstellungen, kurs_ordner, kurse  # noqa: E402
WURZEL = wurzel()


def kuerzel(vorname: str, nachname: str) -> str:
    """Bildet das bettermarks-Kürzel: zwei Buchstaben Vorname + zwei Nachname."""
    def zwei(s: str) -> str:
        s = s.strip()
        if not s:
            return "??"
        s = s[:2]
        return s[0].upper() + s[1:].lower()
    return zwei(vorname) + zwei(nachname)


def entschaerfen(s: str) -> str:
    """Für den Vergleich: Umlaute und Groß/Klein vereinheitlichen."""
    s = unicodedata.normalize("NFKD", s.strip().lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def liste_lesen(pfad: Path) -> list[tuple[str, str]]:
    """Gibt [(vorname, nachname), ...] zurück. Akzeptiert .xlsx und .csv."""
    if pfad.suffix.lower() in (".csv", ".txt"):
        roh = pfad.read_text(encoding="utf-8-sig").splitlines()
        # Trennzeichen nehmen, das die meisten Spalten ergibt
        bestes, zeilen = None, []
        for trenner in (";", ",", "\t", "|"):
            versuch = [z for z in csv.reader(roh, delimiter=trenner)
                       if any(x.strip() for x in z)]
            breite = max((len(z) for z in versuch), default=0)
            if bestes is None or breite > bestes:
                bestes, zeilen = breite, versuch
    else:
        try:
            import openpyxl
        except ImportError:
            sys.exit(
                "Für .xlsx wird openpyxl gebraucht:  pip install openpyxl\n"
                "Alternativ die Kursliste in Excel als CSV speichern und die "
                "CSV angeben."
            )
        wb = openpyxl.load_workbook(pfad, data_only=True)
        ws = wb[wb.sheetnames[0]]
        zeilen = [
            ["" if v is None else str(v) for v in r]
            for r in ws.iter_rows(values_only=True)
            if any(v is not None and str(v).strip() for v in r)
        ]

    # Kopfzeile suchen: die Zeile, in der "name" vorkommt
    kopf_idx, sp_vor, sp_nach = None, None, None
    for i, z in enumerate(zeilen[:15]):
        klein = [entschaerfen(x) for x in z]
        for j, x in enumerate(klein):
            if x.startswith("vorname"):
                sp_vor = j
            elif x.startswith("nachname") or x == "name":
                sp_nach = j
        if sp_vor is not None and sp_nach is not None:
            kopf_idx = i
            break
    if kopf_idx is None:
        sys.exit(
            "In der Liste wurden keine Spalten 'Vorname' und 'Nachname' gefunden.\n"
            "Gefundene erste Zeilen:\n  " + "\n  ".join(str(z[:6]) for z in zeilen[:5])
        )

    leute = []
    for z in zeilen[kopf_idx + 1:]:
        vor = z[sp_vor].strip() if sp_vor < len(z) else ""
        nach = z[sp_nach].strip() if sp_nach < len(z) else ""
        if vor or nach:
            leute.append((vor, nach))
    return leute


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kurs", required=True, help="z. B. 2026-27_KURSID (Schuljahr_Kurs-ID)")
    p.add_argument("--liste", required=True, help="Kursliste als .xlsx oder .csv")
    a = p.parse_args()
    kurs_ordner(a.kurs, WURZEL)      # der Kurs wird zuerst angelegt (Skill `kurs`), nie hier nebenbei
    niveau = str(kurse(WURZEL)[a.kurs].get("niveau", ""))

    schluessel = WURZEL / "Personenbezogenes" / f"schluessel-{a.kurs}.csv"
    kursordner = WURZEL / "Schuelerdaten" / a.kurs
    map_datei = kursordner / "kuerzel-map.csv"
    profile = kursordner / "profile"
    profile.mkdir(parents=True, exist_ok=True)
    schluessel.parent.mkdir(parents=True, exist_ok=True)

    # Bestehende Zuordnung einlesen, damit Pseudonyme stabil bleiben
    bestand: dict[str, tuple[str, str, str]] = {}   # schluesselwort -> (pseudo, vor, nach)
    hoechste = 0
    if schluessel.exists():
        with schluessel.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f, delimiter=";"):
                key = entschaerfen(r["vorname"]) + "|" + entschaerfen(r["nachname"])
                bestand[key] = (r["pseudonym"], r["vorname"], r["nachname"])
                if r["pseudonym"].startswith("S") and r["pseudonym"][1:].isdigit():
                    hoechste = max(hoechste, int(r["pseudonym"][1:]))

    neu = 0
    gesehen: set[str] = set()
    for vor, nach in liste_lesen(Path(a.liste)):
        key = entschaerfen(vor) + "|" + entschaerfen(nach)
        gesehen.add(key)
        if key in bestand:
            continue
        hoechste += 1
        bestand[key] = (f"S{hoechste:02d}", vor, nach)
        neu += 1

    reihen = sorted(bestand.values(), key=lambda t: t[0])

    with schluessel.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["pseudonym", "vorname", "nachname", "kuerzel"])
        for pseudo, vor, nach in reihen:
            w.writerow([pseudo, vor, nach, kuerzel(vor, nach)])

    with map_datei.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["pseudonym", "kuerzel"])
        for pseudo, vor, nach in reihen:
            w.writerow([pseudo, kuerzel(vor, nach)])

    angelegt = 0
    for pseudo, vor, nach in reihen:
        ziel = profile / f"{pseudo}.md"
        if ziel.exists():
            continue
        ziel.write_text(
            f"---\npseudonym: {pseudo}\nkurs: {a.kurs}\n"
            f"kuerzel: {kuerzel(vor, nach)}\nniveau: {niveau}\n"
            "foerderbedarf: nein\nnachteilsausgleich: nein\n---\n\n"
            "## Beobachtungen\n\n",
            encoding="utf-8",
        )
        angelegt += 1

    print(f"Schlüsseldatei: {schluessel}   ({len(reihen)} Personen, {neu} neu)")
    print(f"Kürzel-Map:     {map_datei}")
    print(f"Profile:        {profile}   ({angelegt} neu angelegt)")
    weg = sorted(v[0] for k, v in bestand.items() if k not in gesehen)
    if weg:
        print(f"\nNicht mehr in der Liste: {', '.join(weg)} — bleiben im Bestand (Pseudonyme werden nie neu vergeben).")
        print("Austritt als Ereignis eintragen: ereignis.py --art kurswechsel --wert austritt --datum … --wer <Pseudonym>")
    print("\nDie Schlüsseldatei liegt in Personenbezogenes/ und ist git-ignoriert.")


if __name__ == "__main__":
    main()
