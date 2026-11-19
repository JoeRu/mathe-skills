#!/usr/bin/env python3
"""Schulordner, Einstellungen und Schulpaket finden — gemeinsam für alle Werkzeuge.

Der Schulordner ist der Ordner, der `einstellungen.md` enthält. Gesucht wird in
dieser Reihenfolge:

1. Umgebungsvariable SCHULORDNER
2. das aktuelle Verzeichnis und seine Eltern
3. der Ordner dieses Skripts und seine Eltern (Skills liegen im Schulordner)
4. $HOME/mnt/*/einstellungen.md (verbundener Ordner in Claude Cowork), wenn genau einer

    python schulordner.py            zeigt Schulordner, Einstellungen, Schulpaket
    python schulordner.py --pruefen  prüft Strukturversion und Pfade (Exit 1 bei Fehlern),
                                     meldet Hinweise (mehrere aktive Kurse, Altbestand)

Die Werkzeuge importieren `wurzel()`, `einstellungen()`, `schulpaket()`,
`skills_ordner()`, `notenschluessel()`, `faecher()` und für alles, was einen Kurs betrifft,
`kurse()`, `aktive_kurse()`, `kurs_ordner()`, `kurs_wahl()`, `kurs_fach()`, `thema_ordner()`
und `intern_pfad()`. Themenordner liegen unter `<Fach>/<Thema>/` (Struktur 3).
Grundsatz: ein Kursschlüssel wird geprüft, nie geraten und nie still angelegt.
"""
from __future__ import annotations

import datetime as dt
import os
import re
import sys
from pathlib import Path

STRUKTUR = 3                 # Version der Ordner-Schnittstelle, die diese Skills erwarten
DATEI = "einstellungen.md"
KURSE = "Kurse"
ARBEITEN = ("Arbeit", "Wiederholung", "Nachschreiben", "Test")
INTERN_ARTEN = ("scan", "korrektur", "bettermarks", "auswertung")
KEIN_FACH = {"Kurse", "Schuelerdaten", "Personenbezogenes", "Dienstliches", "Elternarbeit"}
THEMA_UNTERORDNER = ("Arbeitsblätter", "Klassenarbeiten", "Tafelbilder", "generator")
ALT_WURZEL = ("Kopfrechnen", "Mathewettbewerb")      # lagen bis Struktur 2 an der Wurzel


def _kandidaten(start: Path):
    p = start.resolve()
    yield p
    yield from p.parents


def wurzel(start: str | Path | None = None) -> Path:
    env = os.environ.get("SCHULORDNER")
    if env and (Path(env) / DATEI).is_file():
        return Path(env).resolve()
    for basis in ([Path(start)] if start else []) + [Path.cwd(), Path(__file__).parent]:
        for p in _kandidaten(basis):
            if (p / DATEI).is_file():
                return p
    mnt = Path(os.environ.get("HOME", "~")).expanduser() / "mnt"
    treffer = sorted(mnt.glob(f"*/{DATEI}")) if mnt.is_dir() else []
    if len(treffer) == 1:
        return treffer[0].parent
    raise SystemExit(
        f"Kein Schulordner gefunden (Datei {DATEI}). SCHULORDNER setzen oder im "
        f"Schulordner aufrufen. Neu aus der Vorlage? Dann zuerst den Skill `einrichtung`.")


def _frontmatter(pfad: Path) -> dict:
    """Liest den YAML-Kopf zwischen --- und --- (flach, eine Ebene Einrückung)."""
    text = pfad.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return {}
    daten: dict = {}
    aktuell: str | None = None
    for zeile in m.group(1).splitlines():
        if not zeile.strip() or zeile.lstrip().startswith("#"):
            continue
        zeile = re.sub(r"\s+#.*$", "", zeile)
        eingerueckt = zeile[:1] in (" ", "\t")
        if ":" not in zeile:
            continue
        k, v = zeile.split(":", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if eingerueckt and aktuell is not None:
            if not isinstance(daten.get(aktuell), dict):
                daten[aktuell] = {}
            daten[aktuell][k] = _wert(v)
        else:
            aktuell = k
            daten[k] = _wert(v) if v else {}
    return daten


def _wert(v: str):
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+[.,]\d+", v):
        return float(v.replace(",", "."))
    return v


def einstellungen(w: Path | None = None) -> dict:
    w = w or wurzel()
    return _frontmatter(w / DATEI)


def _pfad(w: Path, wert: str | None, vorgabe: str) -> Path:
    p = Path(os.path.expandvars(os.path.expanduser(wert or vorgabe)))
    return p if p.is_absolute() else (w / p)


def schulpaket(w: Path | None = None) -> Path:
    w = w or wurzel()
    return _pfad(w, einstellungen(w).get("schulpaket"), "schulpaket").resolve()


def skills_ordner(w: Path | None = None) -> Path:
    w = w or wurzel()
    return _pfad(w, einstellungen(w).get("skills"), "mathe-skills").resolve()


def notenschluessel(w: Path | None = None) -> dict:
    """Grenzen in Prozent je Note aus <Schulpaket>/notenschluessel.md."""
    d = _frontmatter(schulpaket(w) / "notenschluessel.md")
    g = d.get("grenzen") or {}
    grenzen = {int(k): float(v) / 100 for k, v in g.items()}
    if not grenzen:
        raise SystemExit("Notenschlüssel ohne Feld `grenzen:` im Schulpaket.")
    return {"grenzen": grenzen,
            "tendenzbereich": float(d.get("tendenzbereich", 33)),
            "muendlich": float(d.get("gesamt_muendlich", 50)) / 100}


def faecher(w: Path | None = None) -> list[str]:
    """Unterrichtete Fächer aus `faecher:` in einstellungen.md, z. B. [Mathematik, Physik].
    Jedes Fach hat einen gleichnamigen Ordner im Schulordner; darin liegen die Themenordner."""
    w = w or wurzel()
    roh = einstellungen(w).get("faecher") or ""
    if isinstance(roh, dict):
        return []
    return [f.strip().strip('"').strip("'") for f in str(roh).strip("[]").split(",") if f.strip()]


# --- Kurse: prüfen, nie raten, nie still anlegen -------------------------------------

def kurse(w: Path | None = None) -> dict[str, dict]:
    """Kursschlüssel -> Kopf von kurs.md (nur Ordner, die eine kurs.md haben)."""
    w = w or wurzel()
    ordner = w / KURSE
    if not ordner.is_dir():
        return {}
    return {k.name: _frontmatter(k / "kurs.md")
            for k in sorted(ordner.iterdir()) if (k / "kurs.md").is_file()}


def aktive_kurse(w: Path | None = None) -> list[str]:
    return [k for k, d in kurse(w).items() if str(d.get("status", "")).strip() == "aktiv"]


def _kursliste(w: Path) -> str:
    z = [f"  {k:30} {str(d.get('kurzname', '')):10} {d.get('status', '?')}" for k, d in kurse(w).items()]
    return "\n".join(z) or "  (keine Kurse angelegt)"


def kurs_ordner(kurs: str, w: Path | None = None) -> Path:
    """Prüft, dass der Kurs existiert. Ein Tippfehler im Kursschlüssel bricht ab,
    statt einen zweiten Kurs mit eigenem Protokoll anzulegen."""
    w = w or wurzel()
    p = w / KURSE / kurs
    if not (p / "kurs.md").is_file():
        sys.exit(f"Kurs '{kurs}' gibt es nicht (kein {KURSE}/{kurs}/kurs.md). Vorhanden:\n{_kursliste(w)}")
    return p


def kurs_wahl(arg: str | None, w: Path | None = None, nur_ausdruecklich: bool = False) -> str:
    """Kursschlüssel aus --kurs prüfen. Ohne Angabe nur lesend und nur, wenn genau ein
    Kurs aktiv ist; schreibende Werkzeuge (nur_ausdruecklich) verlangen immer die Angabe."""
    w = w or wurzel()
    if arg:
        kurs_ordner(arg, w)
        return arg
    if nur_ausdruecklich:
        sys.exit("--kurs fehlt. Dieses Werkzeug schreibt und rät nie; Kursschlüssel angeben:\n" + _kursliste(w))
    aktiv = aktive_kurse(w)
    if len(aktiv) == 1:
        return aktiv[0]
    sys.exit(("Mehr als ein aktiver Kurs" if aktiv else "Kein aktiver Kurs")
             + ", bitte --kurs angeben (die Lehrkraft fragen, nicht raten):\n" + _kursliste(w))


def kurs_fach(kurs: str, w: Path | None = None) -> str:
    """Fach des Kurses: `fach:` in kurs.md; fehlt es, das einzige Fach der Lehrkraft."""
    w = w or wurzel()
    kurs_ordner(kurs, w)
    alle = faecher(w)
    fach = kurse(w)[kurs].get("fach") or ""
    fach = "" if isinstance(fach, dict) else str(fach).strip()
    if not fach:
        if len(alle) == 1:
            return alle[0]
        sys.exit(f"Kurs '{kurs}': Feld `fach:` fehlt in kurs.md "
                 f"(Fächer laut {DATEI}: {', '.join(alle) or 'keine eingetragen'}).")
    if alle and fach not in alle:
        sys.exit(f"Kurs '{kurs}': Fach '{fach}' steht nicht unter `faecher:` in {DATEI} ({', '.join(alle)}).")
    return fach


def thema_ordner(kurs: str, thema: str, w: Path | None = None) -> Path:
    """<Schulordner>/<Fach des Kurses>/<Thema>/ — geprüft, nie angelegt."""
    w = w or wurzel()
    fach = kurs_fach(kurs, w)
    p = w / fach / thema
    if thema.startswith(("_", ".")) or not p.is_dir():
        sys.exit(f"Themenordner '{fach}/{thema}' gibt es nicht.")
    return p


def intern_pfad(kurs: str, thema: str, art: str, arbeit: str | None = None,
                datum: str | None = None, version: str | None = None,
                w: Path | None = None) -> Path:
    """Ablage für alles mit Namen, Punkten oder Scans: Kurse/<Kurs>/_intern/<Thema>/…

    scan        Scan_<Arbeit>_<JJJJ-MM-TT>/
    korrektur   Korrektur_<Arbeit>_<JJJJ-MM-TT>[_vN]/   (_vN = freigegebene Fassung)
    bettermarks bettermarks/
    auswertung  das Themenverzeichnis selbst
    <Arbeit> ist Arbeit | Wiederholung | Nachschreiben | Test, das Datum der Termin."""
    w = w or wurzel()
    if art not in INTERN_ARTEN:
        sys.exit(f"Art '{art}' unbekannt. Erlaubt: {', '.join(INTERN_ARTEN)}")
    thema_ordner(kurs, thema, w)
    basis = kurs_ordner(kurs, w) / "_intern" / thema
    if art == "bettermarks":
        return basis / "bettermarks"
    if art == "auswertung":
        return basis
    if arbeit not in ARBEITEN:
        sys.exit(f"--arbeit angeben: {', '.join(ARBEITEN)}")
    try:
        dt.date.fromisoformat(datum or "")
    except ValueError:
        sys.exit("--datum angeben (JJJJ-MM-TT, der Termin der Arbeit)")
    name = f"{'Scan' if art == 'scan' else 'Korrektur'}_{arbeit}_{datum}"
    if art == "korrektur" and version:
        name += f"_v{int(str(version).lstrip('vV'))}"
    return basis / name


def pruefen() -> int:
    fehler = []
    w = wurzel()
    e = einstellungen(w)
    if int(e.get("struktur", 0)) != STRUKTUR:
        fehler.append(f"struktur: {e.get('struktur')} in {DATEI}, die Skills erwarten {STRUKTUR} "
                      f"(Skill `einrichtung`, Abschnitt Migration)")
    for feld in ("lehrkraft", "kuerzel", "schulpaket", "skills"):
        if not e.get(feld) or "<<" in str(e.get(feld)):
            fehler.append(f"Feld `{feld}` fehlt oder ist Platzhalter")
    sp = schulpaket(w)
    for datei in ("schule.md", "notenschluessel.md"):
        if not (sp / datei).is_file():
            fehler.append(f"Schulpaket: {sp / datei} fehlt")
    if not (skills_ordner(w) / "scripts" / "schulordner.py").is_file():
        fehler.append(f"Skills-Ordner {skills_ordner(w)} enthält keine Werkzeuge")
    alle = faecher(w)
    if not alle:
        fehler.append(f"Feld `faecher` fehlt in {DATEI} (z. B. `faecher: [Mathematik]`) — Skill `einrichtung`")
    for f in alle:
        if not (w / f).is_dir():
            fehler.append(f"Fachordner {f}/ fehlt (Themenordner liegen unter <Fach>/<Thema>/)")
    hinweise = []
    aktiv = aktive_kurse(w)
    for k in aktiv:
        f = kurse(w)[k].get("fach") or ""
        f = "" if isinstance(f, dict) else str(f).strip()
        if not f and len(alle) != 1:
            fehler.append(f"Kurs {k}: Feld `fach:` fehlt in kurs.md")
        elif f and alle and f not in alle:
            fehler.append(f"Kurs {k}: Fach '{f}' steht nicht unter `faecher:`")
    for x in sorted(p for p in w.iterdir() if p.is_dir()):
        if x.name in alle or x.name in KEIN_FACH or x.name.startswith(("_", ".")):
            continue
        if x.name in ALT_WURZEL or any((x / u).is_dir() for u in THEMA_UNTERORDNER):
            hinweise.append(f"Themenordner {x.name}/ liegt an der Wurzel (Struktur 2): gehört nach "
                            f"<Fach>/{x.name}/ (Skill `einrichtung`, Migration)")
    if len(aktiv) > 1:
        hinweise.append(f"{len(aktiv)} aktive Kurse: Skills fragen nach dem Kurs, wenn der Auftrag keinen nennt")
    for k in aktiv:
        if not (w / "Schuelerdaten" / k).is_dir():
            hinweise.append(f"Kurs {k}: kein Bestand in Schuelerdaten/ (nur nötig, wenn Schülerdaten geführt werden)")
    orte = [w] + [w / f for f in alle if (w / f).is_dir()]
    for t in sorted(x for o in orte for x in o.iterdir() if x.is_dir() and (x / "_intern").is_dir()):
        if t.name != "Mathewettbewerb" and any((t / "_intern").iterdir()):
            hinweise.append(f"Altbestand in {t.relative_to(w)}/_intern/ (Struktur 1): gehört nach "
                            f"{KURSE}/<Kurs>/_intern/{t.name}/ (Skill `einrichtung`, Migration)")
    print(f"Schulordner: {w}\nSchulpaket:  {sp}\nSkills:      {skills_ordner(w)}\nFächer:      {', '.join(alle) or '–'}")
    for h in hinweise:
        print("HINWEIS:", h)
    for f in fehler:
        print("FEHLER:", f)
    print("ok" if not fehler else f"{len(fehler)} Fehler")
    return 1 if fehler else 0


if __name__ == "__main__":
    if "--pruefen" in sys.argv:
        sys.exit(pruefen())
    w = wurzel()
    print(f"Schulordner: {w}")
    for k, v in einstellungen(w).items():
        print(f"  {k}: {v}")
    print(f"Schulpaket:  {schulpaket(w)}")
    print(f"Skills:      {skills_ordner(w)}")
