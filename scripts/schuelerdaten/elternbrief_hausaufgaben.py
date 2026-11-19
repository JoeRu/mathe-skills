# -*- coding: utf-8 -*-
"""Füllt die Vorlage '3x Keine Hausaufgaben' des Schulpakets für Kinder, bei denen die
3x-Regel greift: Name (aus der Schlüsseldatei, nur lokal), Datum, Ankreuzfeld
und die Liste der offenen Versäumnisse aus ereignisse.jsonl.

Klarnamen werden nur in die .docx geschrieben, nie auf die Konsole.

    python elternbrief_hausaufgaben.py --kurs 2026-27_KURSID --datum TT.MM.JJJJ MaMu S99
"""
import argparse, csv, json, shutil, subprocess, sys
from pathlib import Path
import docx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from schulordner import wurzel, schulpaket, einstellungen, kurs_ordner, kurse  # noqa: E402
WURZEL = wurzel()
VORLAGE = schulpaket(WURZEL) / "vorlagen" / "Elternbriefe" / "3x Keine Hausaufgaben-template.docx"
UNTERSCHRIFT = str(einstellungen(WURZEL).get("lehrkraft_name") or einstellungen(WURZEL).get("lehrkraft", ""))


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

def offene(ereignisse, pseudo):
    """Versäumnisse seit der letzten Rücksetzung (wie auswerten.py)."""
    ev = sorted([e for e in ereignisse if e.get("pseudonym") == pseudo], key=lambda e: (e["datum"], e.get("erfasst", "")))
    liste = []
    for e in ev:
        txt = (e.get("thema", "") + " " + e.get("notiz", "")).lower()
        if e["art"] == "elternkontakt" and "hausaufgab" in txt:
            liste = []
        elif e["art"] == "hausaufgabe" and e["wert"] == "nachgearbeitet":
            liste = []
        elif e["art"] == "hausaufgabe" and e["wert"] == "fehlt":
            liste.append(e)
    return liste

def datum_de(iso):
    j, m, t = iso.split("-")
    return f"{t}.{m}."

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--kurs", required=True)
    p.add_argument("--datum", required=True, help="Briefdatum TT.MM.JJJJ")
    p.add_argument("--version", default="", help="nur fuer eine zweite Fassung am selben Tag, z. B. v2")
    p.add_argument("kuerzel", nargs="+")
    a = p.parse_args()
    kurs_ordner(a.kurs, WURZEL)
    kursordner = WURZEL / "Schuelerdaten" / a.kurs
    ereignisse = korrekturen_anwenden([json.loads(z) for z in (kursordner / "ereignisse.jsonl").open(encoding="utf-8") if z.strip()])
    schluessel = {}
    # Ablage: Personenbezogenes/<Kurs>/ (seit Nov. 2026) oder flach Personenbezogenes/
    pb_kurs = WURZEL / "Personenbezogenes" / a.kurs
    pb = pb_kurs if (pb_kurs / f"schluessel-{a.kurs}.csv").exists() else WURZEL / "Personenbezogenes"
    with (pb / f"schluessel-{a.kurs}.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            schluessel[r["kuerzel"].lower()] = r
    ziel = (pb_kurs / "Elternbriefe") if pb == pb_kurs else WURZEL / "Personenbezogenes" / "Elternbriefe" / a.kurs
    ziel.mkdir(parents=True, exist_ok=True)
    for k in a.kuerzel:
        r = schluessel.get(k.lower())
        if not r:
            print(f"{k}: nicht in der Schlüsseldatei"); continue
        liste = offene(ereignisse, r["pseudonym"])
        if len(liste) < 3:
            print(f"{k}: nur {len(liste)} offene Versäumnisse, kein Brief"); continue
        # je Datum zusammenfassen: Buch und bettermarks am selben Tag in einer Angabe
        tage = {}
        for e in liste:
            ist_bm = "bettermarks" in (e.get("thema", "") + " " + e.get("quelle", "")).lower()
            tage.setdefault(e["datum"], []).append("bettermarks" if ist_bm else "Buch")
        daten = []
        for iso, arten in sorted(tage.items()):
            j, m, t = iso.split("-")
            d = f"{t}.{m}.{j}"
            if "bettermarks" in arten:
                d += " (Buch und bettermarks)" if "Buch" in arten else " (bettermarks)"
            daten.append(d)
        aufz = "; ".join(daten)
        iso_brief = f"{a.datum[6:]}-{a.datum[3:5]}-{a.datum[:2]}"
        out = ziel / f"3x Keine Hausaufgaben_{iso_brief}_{k}{'_' + a.version if a.version else ''}.docx"
        if out.exists():
            print(f"{k}: {out.name} existiert schon, nichts überschrieben"); continue
        d = docx.Document(VORLAGE); P = d.paragraphs
        P[9].runs[1].text = a.datum
        name = f"{r['vorname']} {r['nachname']}"
        P[13].runs[0].text = P[13].runs[0].text.replace("__________________", name, 1)
        P[14].runs[0].text = "☒"
        P[14].runs[1].text = f" Mehrfach wurden die Hausaufgaben nicht erledigt ({len(liste)}-mal). Gefehlt haben sie zu den Stunden am: {aufz}."
        if any("bettermarks" in v for v in tage.values()):
            P[14].runs[1].text += (" Die mit „bettermarks“ gekennzeichneten Hausaufgaben waren Aufgaben auf der"
                                   " Lernplattform bettermarks (Zugang über das Schulportal Hessen). Sie zählen"
                                   " wie Hausaufgaben im Heft; das angegebene Datum ist dort die Abgabefrist.")
        for run in P[19].runs: run.text = ""
        P[21].runs[3].text = " " + UNTERSCHRIFT
        d.save(out)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(ziel), str(out)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"{k}: Brief erstellt ({len(liste)} Versäumnisse: {', '.join(daten)})")

if __name__ == "__main__":
    main()
