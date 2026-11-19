#!/usr/bin/env python3
"""Hängt Ereignisse an das Protokoll an — einzeln oder als Stapel.

Das Protokoll liegt in Schuelerdaten/<KURS>/ereignisse.jsonl und wird nur
ergänzt, nie überschrieben. Jede Zeile ist ein JSON-Objekt.

Pflichtfelder:  datum (TT.MM.JJJJ oder JJJJ-MM-TT), wer, art, wert
Optional:       fach, thema, quelle, notiz

Arten und die erlaubten Werte stehen in ../README.md.

Einzeln, mit Klarnamen (wird sofort in das Pseudonym übersetzt und nicht
gespeichert):

    python ereignis.py --kurs 2026-27_KURSID --datum 12.09.2026 \
        --wer "Tim Bulle" --art hausaufgabe --wert fehlt

Einzeln, mit Pseudonym oder bettermarks-Kürzel:

    python ereignis.py --kurs 2026-27_KURSID --datum 12.09.2026 \
        --wer MaMu --art sonderaufgabe --wert vereinbart \
        --notiz "P49B, 53VC, AB5B bis Montag"

Stapel aus einer Liste (eine Person pro Zeile, Klarname/Kürzel/Pseudonym):

    python ereignis.py --kurs 2026-27_KURSID --datum 12.09.2026 \
        --art hausaufgabe --wert fehlt --datei fehlende_ha.txt

Stapel mit verschiedenen Daten und Werten — eine Tabelle mit Semikolon,
Kopfzeile `datum;wer;art;wert;thema;quelle;notiz` (alles ab thema darf fehlen; notiz steht bewusst zuletzt,
damit ein Semikolon im Freitext nichts verschiebt).
Damit wird ein ganzer Zeitraum aus dem Schulportal auf einmal übertragen:

    python ereignis.py --kurs 2026-27_KURSID --quelle Schulportal \
        --tabelle uebertrag-schulportal-2026-09-13.csv --probe

Die Schlüsseldatei wird nur gelesen, wenn ein Klarname übersetzt werden muss.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from schulordner import wurzel, schulpaket, einstellungen, kurs_ordner, kurse  # noqa: E402
WURZEL = wurzel()

ARTEN = {
    "hausaufgabe":   {"gemacht", "fehlt", "teilweise", "entschuldigt",
                      "nachgereicht", "nachgearbeitet"},
    "sonderaufgabe": {"vereinbart", "erledigt", "nicht erledigt"},
    "elternkontakt": {"brief", "gespraech", "telefonat", "mail"},
    "beobachtung":   None,   # Freitext in --notiz
    "material":      {"dabei", "fehlt"},
    "test":          None,   # Wert = Punkte oder Prozent, Freitext erlaubt
    "kurswechsel":   {"eintritt", "austritt"},   # Zu- und Abgänge im Schuljahr
}


def entschaerfen(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.strip().lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def datum_normieren(s: str) -> str:
    s = s.strip()
    if s.lower() in ("heute", "today"):
        return date.today().isoformat()
    for muster in ("%d.%m.%Y", "%Y-%m-%d", "%d.%m.%y"):
        try:
            return datetime.strptime(s, muster).date().isoformat()
        except ValueError:
            continue
    sys.exit(f"Datum '{s}' nicht verstanden. Erlaubt: TT.MM.JJJJ, JJJJ-MM-TT, heute")


def aufloeser(kurs: str):
    """Liefert eine Funktion, die Klarname / Kürzel / Pseudonym -> Pseudonym macht."""
    tabelle: dict[str, str] = {}

    map_datei = WURZEL / "Schuelerdaten" / kurs / "kuerzel-map.csv"
    if map_datei.exists():
        with map_datei.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f, delimiter=";"):
                tabelle[entschaerfen(r["pseudonym"])] = r["pseudonym"]
                tabelle[entschaerfen(r["kuerzel"])] = r["pseudonym"]

    schluessel = WURZEL / "Personenbezogenes" / f"schluessel-{kurs}.csv"
    if schluessel.exists():
        with schluessel.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f, delimiter=";"):
                p = r["pseudonym"]
                vor, nach = r["vorname"], r["nachname"]
                for variante in (f"{vor} {nach}", f"{nach}, {vor}", vor, nach):
                    if variante.strip():
                        tabelle.setdefault(entschaerfen(variante), p)

    def aufloesen(wer: str) -> str:
        t = entschaerfen(wer)
        if t in tabelle:
            return tabelle[t]
        treffer = sorted({v for k, v in tabelle.items() if t and t in k})
        if len(treffer) == 1:
            return treffer[0]
        if len(treffer) > 1:
            sys.exit(f"'{wer}' ist mehrdeutig: {', '.join(treffer)}")
        sys.exit(
            f"'{wer}' nicht gefunden. Erst schluessel_anlegen.py laufen lassen, "
            f"oder das Pseudonym direkt angeben."
        )

    return aufloesen


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kurs", required=True)
    p.add_argument("--datum", help="TT.MM.JJJJ, JJJJ-MM-TT oder 'heute'")
    p.add_argument("--art", choices=sorted(ARTEN))
    p.add_argument("--wert")
    p.add_argument("--wer", help="Klarname, Kürzel oder Pseudonym")
    p.add_argument("--datei", help="Textdatei, eine Person pro Zeile")
    p.add_argument("--tabelle",
                   help="Semikolon-Tabelle: datum;wer;art;wert;thema;quelle;notiz")
    p.add_argument("--fach", default="Mathematik")
    p.add_argument("--thema", default="")
    p.add_argument("--quelle", default="haendisch",
                   help="z. B. Schulportal, bettermarks, haendisch")
    p.add_argument("--notiz", default="")
    p.add_argument("--probe", action="store_true",
                   help="nur zeigen, was geschrieben würde")
    a = p.parse_args()
    kurs_ordner(a.kurs, WURZEL)      # Tippfehler im Kursschlüssel bricht ab
    if not (WURZEL / "Schuelerdaten" / a.kurs).is_dir():
        sys.exit(f"Kein Schülerdaten-Bestand für {a.kurs}. Anlegen nur mit schluessel_anlegen.py (Skill `schuelerdaten`).")

    def pruefen(art: str, wert: str, wo: str = "") -> None:
        if art not in ARTEN:
            sys.exit(f"Art '{art}' gibt es nicht{wo}. "
                     f"Erlaubt: {', '.join(sorted(ARTEN))}")
        erlaubt = ARTEN[art]
        if erlaubt and wert not in erlaubt:
            sys.exit(f"Wert '{wert}' ist für art={art} nicht vorgesehen{wo}. "
                     f"Erlaubt: {', '.join(sorted(erlaubt))}")

    if a.tabelle and (a.wer or a.datei):
        sys.exit("--tabelle bringt die Personen schon mit; "
                 "--wer und --datei entfallen dann.")
    if not a.tabelle:
        for pflicht in ("datum", "art", "wert"):
            if not getattr(a, pflicht):
                sys.exit(f"--{pflicht} fehlt (oder stattdessen --tabelle angeben).")
        pruefen(a.art, a.wert)
        if not a.wer and not a.datei:
            sys.exit("Entweder --wer oder --datei angeben.")

    # (datum, wer, art, wert, thema, notiz, quelle) je Zeile
    posten: list[tuple[str, str, str, str, str, str, str]] = []

    if a.tabelle:
        roh = Path(a.tabelle).read_text(encoding="utf-8-sig").splitlines()
        leser = csv.DictReader((z for z in roh if z.strip()
                                and not z.lstrip().startswith("#")),
                               delimiter=";", restkey="__rest")
        pflicht = {"datum", "wer", "art", "wert"}
        if not leser.fieldnames or not pflicht <= {f.strip() for f in leser.fieldnames}:
            sys.exit("Kopfzeile der Tabelle muss datum;wer;art;wert "
                     "(optional ;thema;quelle;notiz) enthalten.")
        for nr, r in enumerate(leser, 2):
            art = (r.get("art") or "").strip()
            wert = (r.get("wert") or "").strip()
            pruefen(art, wert, f" (Zeile {nr})")
            notiz = (r.get("notiz") or "").strip()
            if r.get("__rest"):          # Semikolon im Freitext, wieder zusammensetzen
                notiz = "; ".join([notiz] + [x.strip() for x in r["__rest"] if x]).strip("; ")
            posten.append((
                (r.get("datum") or "").strip(), (r.get("wer") or "").strip(),
                art, wert,
                (r.get("thema") or "").strip(), notiz,
                (r.get("quelle") or "").strip() or a.quelle,
            ))
    else:
        namen = []
        if a.wer:
            namen.append(a.wer)
        if a.datei:
            namen += [z.strip() for z in
                      Path(a.datei).read_text(encoding="utf-8").splitlines()
                      if z.strip() and not z.lstrip().startswith("#")]
        posten = [(a.datum, n, a.art, a.wert, a.thema, a.notiz, a.quelle)
                  for n in namen]

    if not posten:
        sys.exit("Nichts einzutragen.")

    aufloesen = aufloeser(a.kurs)

    ziel = WURZEL / "Schuelerdaten" / a.kurs / "ereignisse.jsonl"

    zeilen = []
    for datum, wer, art, wert, thema, notiz, quelle in posten:
        satz = {
            "datum": datum_normieren(datum),
            "pseudonym": aufloesen(wer),
            "art": art,
            "wert": wert,
            "fach": a.fach,
            "erfasst": date.today().isoformat(),
            "quelle": quelle,
        }
        if thema:
            satz["thema"] = thema
        if notiz:
            satz["notiz"] = notiz
        zeilen.append(json.dumps(satz, ensure_ascii=False))

    # Ereignisse in der Zukunft sind fast immer ein Versehen — und ein
    # zurueckgesetzter Zaehler faellt sonst niemandem auf.
    heute = date.today().isoformat()
    kuenftig = [json.loads(z) for z in zeilen if json.loads(z)["datum"] > heute]
    if kuenftig:
        print(f"! Achtung: {len(kuenftig)} Ereignis(se) liegen in der Zukunft "
              f"(heute ist {heute}):")
        for s in kuenftig[:5]:
            print(f"!   {s['datum']}  {s['pseudonym']}  {s['art']}={s['wert']}")
        print("! Ein Datum in der Zukunft zaehlt trotzdem sofort mit und kann "
              "die 3x-Regel zuruecksetzen.")

    if a.probe:
        print("\n".join(zeilen))
        print(f"\n({len(zeilen)} Zeilen würden an {ziel} angehängt)")
        return

    with ziel.open("a", encoding="utf-8") as f:
        for z in zeilen:
            f.write(z + "\n")
    print(f"{len(zeilen)} Ereignis(se) angehängt an {ziel}")


if __name__ == "__main__":
    main()
