#!/usr/bin/env python3
"""Wertet das Ereignisprotokoll aus. Rechnet, zählt nicht aus dem Gedächtnis.

    python auswerten.py --kurs 2026-27_KURSID                  Überblick
    python auswerten.py --kurs 2026-27_KURSID --briefe         nur die 3x-Regel
    python auswerten.py --kurs 2026-27_KURSID --wer MaMu       ein Kind im Verlauf
    python auswerten.py --kurs 2026-27_KURSID --klarnamen      Kürzel statt Pseudonym

Die 3x-Regel: gezählt werden Ereignisse art=hausaufgabe mit wert=fehlt, und
zwar **seit dem letzten Elternkontakt mit Grund Hausaufgaben**. Danach beginnt
die Zählung von vorn. 'entschuldigt' und 'nachgereicht' zählen nicht mit.

--klarnamen zeigt die bettermarks-Kürzel aus kuerzel-map.csv. Echte Namen
stehen nur in der Schlüsseldatei und werden hier nie gelesen.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from schulordner import wurzel, schulpaket, einstellungen, kurs_ordner, kurse  # noqa: E402
WURZEL = wurzel()
SCHWELLE = 3


def korrekturen_anwenden(saetze):
    """Ein hausaufgabe-Satz mit notiz "Korrektur: ..." ersetzt alle früher erfassten
    Sätze desselben Kindes, Datums und derselben Quelle (append-only bleibt erhalten)."""
    out = []
    for s in saetze:
        if s.get("art") == "hausaufgabe" and s.get("notiz", "").lower().startswith("korrektur"):
            schl = (s.get("pseudonym"), s.get("datum"), s.get("art"), s.get("quelle"))
            out = [t for t in out if (t.get("pseudonym"), t.get("datum"), t.get("art"), t.get("quelle")) != schl]
        out.append(s)
    return out


def laden(kurs: str) -> list[dict]:
    pfad = WURZEL / "Schuelerdaten" / kurs / "ereignisse.jsonl"
    if not pfad.exists():
        return []
    sätze = []
    for nr, zeile in enumerate(pfad.read_text(encoding="utf-8").splitlines(), 1):
        zeile = zeile.strip()
        if not zeile:
            continue
        try:
            sätze.append(json.loads(zeile))
        except json.JSONDecodeError as e:
            print(f"  ! Zeile {nr} in ereignisse.jsonl ist kein gültiges JSON: {e}")
    sätze = korrekturen_anwenden(sätze)
    return sorted(sätze, key=lambda s: (s.get("datum", ""), s.get("pseudonym", "")))


def kuerzel_map(kurs: str) -> dict[str, str]:
    pfad = WURZEL / "Schuelerdaten" / kurs / "kuerzel-map.csv"
    if not pfad.exists():
        return {}
    with pfad.open(encoding="utf-8", newline="") as f:
        return {r["pseudonym"]: r["kuerzel"] for r in csv.DictReader(f, delimiter=";")}


def offene_versaeumnisse(sätze: list[dict]) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Zwei Zählungen pro Kind.

    offen    -> Daten der fehlenden Hausaufgaben **seit der letzten
                Rücksetzung** (Elternbrief oder anerkannte Nacharbeit).
                Das ist die Grundlage für die 3x-Regel.
    gesamt   -> alle Daten fehlender Hausaufgaben im ganzen Zeitraum.
                Das bleibt für die Note stehen und wird nie zurückgesetzt.
    """
    offen: dict[str, list[str]] = defaultdict(list)
    gesamt: dict[str, list[str]] = defaultdict(list)
    for s in sätze:
        p = s.get("pseudonym")
        if not p:
            continue
        art, wert = s.get("art"), s.get("wert")
        text = (s.get("thema", "") + " " + s.get("notiz", "")).lower()
        if art == "elternkontakt" and "hausaufgab" in text:
            offen[p] = []                      # Brief ist raus
        elif art == "hausaufgabe" and wert == "nachgearbeitet":
            offen[p] = []                      # Nacharbeit anerkannt
        elif art == "hausaufgabe" and wert == "fehlt":
            offen[p].append(s["datum"])
            gesamt[p].append(s["datum"])
    return offen, gesamt


def ausgetreten(sätze: list[dict]) -> dict[str, str]:
    """Pseudonym -> Datum des Austritts, wenn das letzte Ereignis `kurswechsel` ein Austritt ist."""
    letzter: dict[str, tuple[str, str]] = {}
    for s in sätze:
        if s.get("art") == "kurswechsel" and s.get("pseudonym"):
            letzter[s["pseudonym"]] = (s.get("wert", ""), s["datum"])
    return {p: d for p, (w, d) in letzter.items() if w == "austritt"}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kurs", required=True)
    p.add_argument("--briefe", action="store_true")
    p.add_argument("--wer")
    p.add_argument("--klarnamen", action="store_true",
                   help="bettermarks-Kürzel statt Pseudonym anzeigen")
    a = p.parse_args()
    kurs_ordner(a.kurs, WURZEL)

    sätze = laden(a.kurs)
    if not sätze:
        print(f"Keine Ereignisse für {a.kurs}.")
        return
    km = kuerzel_map(a.kurs) if a.klarnamen else {}

    def zeig(pseudo: str) -> str:
        return f"{pseudo} ({km[pseudo]})" if pseudo in km else pseudo

    if a.wer:
        ziel = a.wer.strip()
        rueck = {v: k for k, v in kuerzel_map(a.kurs).items()}
        ziel = rueck.get(ziel, ziel)
        eigene = [s for s in sätze if s.get("pseudonym") == ziel]
        if not eigene:
            print(f"Keine Ereignisse für {ziel}.")
            return
        print(f"Verlauf {zeig(ziel)} — {len(eigene)} Ereignisse\n")
        for s in eigene:
            zusatz = s.get("notiz") or s.get("thema") or ""
            print(f"  {s['datum']}  {s['art']:<14} {s['wert']:<14} {zusatz}")
        return

    offen, gesamt = offene_versaeumnisse(sätze)
    weg = ausgetreten(sätze)
    faellig = {k: v for k, v in offen.items() if len(v) >= SCHWELLE and k not in weg}

    print(f"Kurs {a.kurs} — {len(sätze)} Ereignisse, "
          f"{len({s.get('pseudonym') for s in sätze})} Kinder erfasst")
    print(f"Zeitraum {sätze[0]['datum']} bis {sätze[-1]['datum']}\n")

    print(f"Elternbrief fällig (>= {SCHWELLE}x offen seit letzter Rücksetzung):")
    if not faellig:
        print("  niemand")
    for pseudo, daten in sorted(faellig.items(), key=lambda t: -len(t[1])):
        print(f"  {zeig(pseudo):<14} {len(daten)}x   {', '.join(daten)}")

    if a.briefe:
        return

    knapp = {k: v for k, v in offen.items() if 0 < len(v) < SCHWELLE and k not in weg}
    print(f"\nDarunter (noch kein Brief fällig):")
    if not knapp:
        print("  niemand")
    for pseudo, daten in sorted(knapp.items(), key=lambda t: -len(t[1])):
        print(f"  {zeig(pseudo):<14} {len(daten)}x   {', '.join(daten)}")

    print("\nFür die Note — alle Versäumnisse, ohne Rücksetzung:")
    if not gesamt:
        print("  keine")
    for pseudo, daten in sorted(gesamt.items(), key=lambda t: -len(t[1])):
        zurueck = len(daten) - len(offen.get(pseudo, []))
        hinweis = f"   (davon {zurueck} bereits abgegolten)" if zurueck else ""
        print(f"  {zeig(pseudo):<14} {len(daten)}x   {', '.join(daten)}{hinweis}")

    if weg:
        print("\nNicht mehr im Kurs (letztes Ereignis kurswechsel=austritt), aus den Briefen ausgenommen:")
        for pseudo, datum in sorted(weg.items()):
            print(f"  {zeig(pseudo):<14} seit {datum}")

    offen = [s for s in sätze
             if s.get("art") == "sonderaufgabe" and s.get("wert") == "vereinbart"]
    erledigt = {(s["pseudonym"], s.get("thema", "")) for s in sätze
                if s.get("art") == "sonderaufgabe" and s.get("wert") == "erledigt"}
    noch_offen = [s for s in offen if (s["pseudonym"], s.get("thema", "")) not in erledigt]
    print("\nVereinbarte Sonderaufgaben, noch nicht als erledigt vermerkt:")
    if not noch_offen:
        print("  keine")
    for s in noch_offen:
        print(f"  {zeig(s['pseudonym']):<14} seit {s['datum']}   "
              f"{s.get('notiz') or s.get('thema') or ''}")


if __name__ == "__main__":
    main()
