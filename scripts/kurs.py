#!/usr/bin/env python3
"""Kurse lesen und fortschreiben (references/kurse.md).

    python kurs.py liste                                   alle Kurse mit Status
    python kurs.py aktiv                                   der einzige aktive Kurs (sonst Fehler mit Liste)
    python kurs.py stand      --kurs 2026-27_KURSID        Steckbrief, Themenfolge, letzte Einträge
    python kurs.py material   --kurs 2026-27_KURSID --thema Zuordnungen
                                                           Material des Themas (<Fach des Kurses>/<Thema>/): hatte der Kurs es schon?
                                                           (docx/pdf/tex mit gleichem Namen zählen zusammen)
    python kurs.py eingefroren "Mathematik/Zuordnungen/Arbeitsblätter/AB-….pdf"
    python kurs.py pruefen    --kurs 2026-27_KURSID        existieren alle Dateien aus ausgeteilt.csv?
    python kurs.py eintragen  --kurs 2026-27_KURSID --datum 2026-09-25 --thema Zuordnungen \\
                              --art ausgeteilt --datei "Mathematik/Zuordnungen/…pdf" --notiz "…" [--probe]
    python kurs.py parallel   --kurs K --thema Zuordnungen  Parallelkurse (gleiche Stufe und Niveau, Thema in der Themenfolge)
    python kurs.py pfad       --kurs K --thema Zuordnungen --art scan|korrektur|bettermarks|auswertung \\
                              [--arbeit Arbeit|Wiederholung|Nachschreiben|Test --datum JJJJ-MM-TT --version 2] [--anlegen]
                                                           Ablage unter Kurse/<K>/_intern/<Thema>/ (Namen, Punkte, Scans)

--kurs wird geprüft (kein Tippfehler legt etwas an). Lesende Befehle nehmen ohne --kurs den einzigen aktiven
Kurs, bei mehreren brechen sie ab; `eintragen` verlangt --kurs immer.

Wurzel: --wurzel, sonst der Schulordner mit `einstellungen.md` (siehe schulordner.py). Dateipfade werden Unicode-normalisiert
verglichen (OneDrive speichert Umlaute teils zerlegt).
"""
from __future__ import annotations
import argparse, csv, datetime as dt, os, re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import schulordner as so  # noqa: E402

ARTEN = {"ausgeteilt", "hausaufgabe", "arbeit", "test", "tafelbild", "bettermarks", "buch"}
FELDER = ["datum", "thema", "datei", "art", "quelle", "notiz"]
MATERIAL = {".pdf", ".docx", ".doc", ".tex", ".ggb", ".png", ".jpg", ".pptx", ".xlsx"}


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s.replace("\\", "/"))


def stamm(pfad: str) -> str:
    """Pfad ohne Endung: Word, PDF und LaTeX derselben Fassung gelten gemeinsam."""
    p = nfc(pfad)
    return p.rsplit(".", 1)[0] if "." in p.rsplit("/", 1)[-1] else p


def wurzel(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    w = so.wurzel()
    if not (w / "Kurse").is_dir():
        sys.exit(f"{w} hat keinen Ordner Kurse/ — Skill `einrichtung`.")
    return w


def kopf(md: Path) -> dict:
    t = md.read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---", t, re.S)
    d = {}
    for z in (m.group(1).splitlines() if m else []):
        if re.match(r"^\w+:\s*\S", z):
            k, v = z.split(":", 1)
            d[k.strip()] = re.sub(r"\s+#.*$", "", v).strip()
    return d


def lesen(p: Path) -> list[dict]:
    if not p.exists():
        return []
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def alle_ausgeteilt(w: Path) -> dict[str, list[tuple[str, str]]]:
    """datei -> [(kurs, datum)] über alle Kurse."""
    r: dict[str, list[tuple[str, str]]] = {}
    for k in sorted((w / "Kurse").iterdir()):
        for z in lesen(k / "ausgeteilt.csv"):
            if z.get("datei"):
                r.setdefault(stamm(z["datei"]), []).append((k.name, z["datum"]))
    return r


def finde(w: Path, rel: str) -> Path | None:
    p = w / rel
    if p.exists():
        return p
    ziel = nfc(rel)
    ordner = w / Path(rel).parent
    kandidaten = [ordner] if ordner.is_dir() else []
    if not kandidaten:   # auch der Ordnername kann zerlegt gespeichert sein
        kandidaten = [q for q in (w / Path(rel).parts[0]).rglob("*") if q.is_dir()] if (w / Path(rel).parts[0]).exists() else []
    for o in kandidaten:
        for q in o.iterdir():
            if nfc(str(q.relative_to(w))) == ziel:
                return q
    return None


def cmd_liste(w, a):
    for k in sorted(x for x in (w / "Kurse").iterdir() if x.is_dir()):
        if (k / "kurs.md").exists():
            d = kopf(k / "kurs.md")
            print(f"{k.name:28} {str(d.get('kurzname', '')):8} {d.get('status', '?'):14} {d.get('fach', '–'):12} Stufe {d.get('stufe', '?')}, Niveau {d.get('niveau', '?')}")
        else:
            print(f"{k.name:28} (ohne kurs.md)")


def cmd_aktiv(w, a):
    print(so.kurs_wahl(None, w))


def cmd_pfad(w, a):
    if not a.thema or not a.art:
        sys.exit("--thema und --art (scan|korrektur|bettermarks|auswertung) angeben")
    pfad = so.intern_pfad(a.kurs, a.thema, a.art, a.arbeit, a.datum, a.version, w)
    if a.anlegen:
        pfad.mkdir(parents=True, exist_ok=True)
    print(pfad)


def cmd_parallel(w, a):
    if not a.thema:
        sys.exit("--thema angeben")
    alle = so.kurse(w)
    ich = alle[a.kurs]
    treffer = []
    for k in so.aktive_kurse(w):
        d = alle[k]
        if k == a.kurs or str(d.get("stufe")) != str(ich.get("stufe")) or str(d.get("niveau")) != str(ich.get("niveau")):
            continue
        zeile = next((z for z in lesen(w / "Kurse" / k / "themenfolge.csv") if z.get("thema") == a.thema), None)
        if zeile:
            treffer.append((k, d, zeile))
    if not treffer:
        print(f"Keine Parallelkurse zu {a.kurs} im Thema {a.thema} (gleiche Stufe und Niveau, aktiv).")
        return
    print(f"Parallelkurse zu {a.kurs} im Thema {a.thema}:")
    for k, d, z in treffer:
        print(f"  {k} ({d.get('kurzname', '')}) · Status {z.get('status') or '–'} · Arbeit am {z.get('arbeit_am') or '–'}")
    print("-> Die Lehrkraft fragen: dieselbe Arbeit oder getrennte Fassungen? Nicht annehmen.")


def cmd_stand(w, a):
    k = w / "Kurse" / a.kurs
    d = kopf(k / "kurs.md")
    print(f"Kurs {a.kurs}: {d.get('bezeichnung')} · Niveau {d.get('niveau')} · {d.get('status')}")
    print("\nThemenfolge:")
    for z in lesen(k / "themenfolge.csv"):
        print(f"  {z['nr']:>2}. {z['thema']:20} {z['status']:13} Soll {z.get('soll_wochen') or '–'} W · ist {z['ist_von'] or '–'} bis {z['ist_bis'] or '–'}"
              f"  Arbeit {z['arbeit_am'] or '–'}  {z['notiz']}")
    e = lesen(k / "ausgeteilt.csv")
    print(f"\nAusgeteilt: {len(e)} Einträge, letzte fünf:")
    for z in e[-5:]:
        print(f"  {z['datum']} {z['art']:11} {z['datei'] or z['notiz']}")


def cmd_material(w, a):
    t = so.thema_ordner(a.kurs, a.thema, w)
    aus = alle_ausgeteilt(w)
    print(f"Material {t.relative_to(w)} — Kurs {a.kurs}   [K] dieser Kurs hatte es  [e] eingefroren (anderer Kurs)")
    for p in sorted(t.rglob("*")):
        rel = p.relative_to(w)
        if not p.is_file() or p.suffix.lower() not in MATERIAL:
            continue
        if any(x in ("_intern", "generator", "__pycache__") for x in rel.parts):
            continue
        treffer = aus.get(stamm(str(rel)), [])
        diesr = [d for k, d in treffer if k == a.kurs]
        andere = [f"{k} {d}" for k, d in treffer if k != a.kurs]
        mark = "K" if diesr else ("e" if andere else " ")
        info = (" am " + ", ".join(diesr)) if diesr else (" (" + "; ".join(andere) + ")" if andere else "")
        print(f"  [{mark}] {p.relative_to(t)}{info}")


def cmd_eingefroren(w, a):
    t = alle_ausgeteilt(w).get(stamm(a.datei), [])
    if t:
        print("EINGEFROREN — ausgeteilt in: " + "; ".join(f"{k} am {d}" for k, d in t))
    else:
        print("nicht eingefroren — noch in keinem Kurs ausgeteilt")


def cmd_pruefen(w, a):
    fehler = 0
    for i, z in enumerate(lesen(w / "Kurse" / a.kurs / "ausgeteilt.csv"), start=2):
        if z["art"] not in ARTEN:
            print(f"Zeile {i}: unbekannte Art {z['art']}"); fehler += 1
        if None in z or len(z) != len(FELDER):
            print(f"Zeile {i}: falsche Spaltenzahl (Semikolon im Text?)"); fehler += 1
        try:
            dt.date.fromisoformat(z["datum"])
        except ValueError:
            print(f"Zeile {i}: Datum {z['datum']} nicht JJJJ-MM-TT"); fehler += 1
        if z["datei"] and not finde(w, z["datei"]):
            print(f"Zeile {i}: Datei fehlt: {z['datei']}"); fehler += 1
    print("ok" if not fehler else f"{fehler} Problem(e)")


def cmd_eintragen(w, a):
    if a.art not in ARTEN:
        sys.exit(f"Art muss eine von {sorted(ARTEN)} sein.")
    dt.date.fromisoformat(a.datum)
    if a.datei and not finde(w, a.datei):
        sys.exit(f"Datei nicht gefunden: {a.datei}")
    z = {"datum": a.datum, "thema": a.thema, "datei": nfc(a.datei or ""), "art": a.art,
         "quelle": a.quelle, "notiz": a.notiz or ""}
    ziel = w / "Kurse" / a.kurs / "ausgeteilt.csv"
    print(("PROBE: " if a.probe else "") + ";".join(z[f] for f in FELDER))
    if a.probe:
        return
    neu = not ziel.exists()
    with ziel.open("a", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, FELDER, delimiter=";")
        if neu:
            wr.writeheader()
        wr.writerow(z)
    print("angehängt")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("befehl", choices=["liste", "aktiv", "stand", "material", "eingefroren", "pruefen", "eintragen", "parallel", "pfad"])
    p.add_argument("datei_pos", nargs="?")
    p.add_argument("--wurzel"); p.add_argument("--kurs"); p.add_argument("--thema")
    p.add_argument("--datum"); p.add_argument("--art"); p.add_argument("--datei")
    p.add_argument("--arbeit"); p.add_argument("--version"); p.add_argument("--anlegen", action="store_true")
    p.add_argument("--quelle", default="claude"); p.add_argument("--notiz"); p.add_argument("--probe", action="store_true")
    a = p.parse_args()
    if a.befehl == "eingefroren":
        a.datei = a.datei or a.datei_pos
    w = wurzel(a.wurzel)
    if a.befehl in ("stand", "material", "pruefen", "parallel", "pfad"):
        a.kurs = so.kurs_wahl(a.kurs, w)
    elif a.befehl == "eintragen":
        a.kurs = so.kurs_wahl(a.kurs, w, nur_ausdruecklich=True)
    {"liste": cmd_liste, "aktiv": cmd_aktiv, "pfad": cmd_pfad, "parallel": cmd_parallel, "stand": cmd_stand, "material": cmd_material, "eingefroren": cmd_eingefroren,
     "pruefen": cmd_pruefen, "eintragen": cmd_eintragen}[a.befehl](w, a)


if __name__ == "__main__":
    main()
