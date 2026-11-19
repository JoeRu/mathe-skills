#!/usr/bin/env python3
"""Baut die Ausgaben der Skills aus dieser einen Quelle und prüft sie vorher.

    python build.py                 prüfen und bauen (dist/)
    python build.py --nur-pruefen   nur prüfen
    python build.py --sperrliste DATEI   zusätzlich nach Begriffen aus DATEI suchen
                                    (eine Zeile je Begriff, z. B. echte Kürzel aus der
                                    kuerzel-map — die Datei bleibt lokal)

Ausgaben in dist/:
  mathe-skills-<version>.plugin     Claude-Plugin (Zip mit .claude-plugin/plugin.json)
  skills/<skill>-<version>.zip      je Skill ein eigenständiges Agent-Skills-Paket
                                    (SKILL.md + references/ + scripts/ im Skill-Ordner),
                                    für ChatGPT, Claude-Skill-Upload und andere Agenten

Prüfungen (Abbruch bei Fehler):
  - Frontmatter jeder SKILL.md: name = Ordnername, Kleinbuchstaben/Bindestrich,
    description vorhanden, höchstens 1024 Zeichen, keine spitzen Klammern
  - keine echten Namen/Kennungen aus der Sperrliste (--sperrliste DATEI und die lokale,
    nicht versionierte Datei .sperrliste neben build.py) in Texten und Skripten
  - jede in einer SKILL.md erwähnte references/ oder scripts/-Datei existiert
  - Python-Skripte kompilieren, noten.py --test läuft
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

QUELLE = Path(__file__).resolve().parent
DIST = QUELLE / "dist"
AUSGESCHLOSSEN = {"dist", "__pycache__", ".git"}
# Was nie in die gemeinsamen Skills gehört (Schule, Person, Kurs): die Begriffe stehen
# in der lokalen, nicht versionierten Datei .sperrliste (eine Zeile je Begriff, # = Kommentar).
# Fehlt sie, prüft build.py nur die Begriffe aus --sperrliste.
SPERRLISTE_LOKAL = QUELLE / ".sperrliste"


def muster_lokal() -> re.Pattern | None:
    if not SPERRLISTE_LOKAL.exists():
        return None
    begriffe = [z.strip() for z in SPERRLISTE_LOKAL.read_text(encoding="utf-8").splitlines()
                if z.strip() and not z.lstrip().startswith("#")]
    return re.compile("|".join(rf"\b{re.escape(b)}\b" for b in begriffe), re.I) if begriffe else None


MUSTER = muster_lokal()


def fehler(liste: list[str], text: str) -> None:
    liste.append(text)


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    d = re.search(r"^description:\s*(.*?)(?=^\w[\w-]*:|\Z)", fm, re.M | re.S)
    desc = re.sub(r"\s+", " ", d.group(1).lstrip(">|").strip()) if d else ""
    return {"name": name.group(1).strip() if name else "", "description": desc}


def dateien():
    for p in sorted(QUELLE.rglob("*")):
        if p.is_file() and not (set(p.relative_to(QUELLE).parts) & AUSGESCHLOSSEN) \
                and p.name != Path(__file__).name:
            yield p


def pruefen(sperrliste: list[str]) -> list[str]:
    f: list[str] = []
    skills = sorted((QUELLE / "skills").glob("*/SKILL.md"))
    for s in skills:
        t = s.read_text(encoding="utf-8")
        fm = frontmatter(t)
        ordner = s.parent.name
        if fm.get("name") != ordner:
            fehler(f, f"{ordner}: name '{fm.get('name')}' ≠ Ordnername")
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", ordner) or len(ordner) > 64:
            fehler(f, f"{ordner}: Name nur Kleinbuchstaben, Ziffern, Bindestrich, ≤ 64")
        d = fm.get("description", "")
        if not d:
            fehler(f, f"{ordner}: description fehlt")
        if len(d) > 1024:
            fehler(f, f"{ordner}: description {len(d)} Zeichen (> 1024)")
        if re.search(r"[<>]", d):
            fehler(f, f"{ordner}: description enthält spitze Klammern (gilt als XML-Tag)")
        for ref in set(re.findall(r"(?<![\w/$])(references|scripts)/([\w./-]+\.(?:md|py))", t)):
            if not (QUELLE / ref[0] / ref[1]).is_file():
                fehler(f, f"{ordner}: verweist auf {ref[0]}/{ref[1]}, gibt es nicht")
    sperr = [b for b in sperrliste if b.strip()]
    for p in dateien():
        if p.suffix not in (".md", ".py", ".json", ".csv", ".txt", ".tex"):
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        rel = p.relative_to(QUELLE)
        if MUSTER and rel.parts[0] not in ("CHANGELOG.md", ".claude-plugin") and (m := MUSTER.search(t)):
            fehler(f, f"{rel}: enthält '{m.group(0)}' (Schule oder Person gehört ins Schulpaket bzw. in einstellungen.md)")
        for b in sperr:
            if re.search(rf"\b{re.escape(b)}\b", t):
                fehler(f, f"{rel}: enthält einen Begriff aus der Sperrliste")
                break
    for py in QUELLE.rglob("*.py"):
        if set(py.relative_to(QUELLE).parts) & AUSGESCHLOSSEN:
            continue
        r = subprocess.run([sys.executable, "-m", "py_compile", str(py)], capture_output=True, text=True)
        if r.returncode:
            fehler(f, f"{py.relative_to(QUELLE)} kompiliert nicht: {r.stderr.strip()[:200]}")
    r = subprocess.run([sys.executable, str(QUELLE / "scripts" / "noten.py"), "--test"],
                       capture_output=True, text=True)
    if "Selbsttest ok" not in r.stdout:
        fehler(f, f"noten.py --test: {r.stdout.strip()} {r.stderr.strip()[:200]}")
    return f


def zip_ordner(z: zipfile.ZipFile, wurzel: Path, ziel: str = "") -> None:
    for p in sorted(wurzel.rglob("*")):
        rel = p.relative_to(wurzel)
        if set(rel.parts) & AUSGESCHLOSSEN:
            continue
        name = (Path(ziel) / rel).as_posix()
        if p.is_dir():
            z.writestr(name + "/", "")
        else:
            z.write(p, name)


def bauen() -> None:
    meta = json.loads((QUELLE / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    v = meta["version"]
    DIST.mkdir(exist_ok=True)
    plugin = DIST / f"mathe-skills-{v}.plugin"
    if plugin.exists():
        sys.exit(f"{plugin.name} gibt es schon — Version in plugin.json erhöhen.")
    with zipfile.ZipFile(plugin, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(QUELLE.iterdir()):
            if p.name in AUSGESCHLOSSEN or p.name == Path(__file__).name:
                continue
            if p.is_dir():
                z.writestr(p.name + "/", "")
                zip_ordner(z, p, p.name)
            else:
                z.write(p, p.name)
    (DIST / "skills").mkdir(exist_ok=True)
    for s in sorted((QUELLE / "skills").glob("*/SKILL.md")):
        name = s.parent.name
        ziel = DIST / "skills" / f"{name}-{v}.zip"
        t = s.read_text(encoding="utf-8")
        # eigenständig: Verweise auf ${CLAUDE_PLUGIN_ROOT}/references|scripts zeigen in den Skill-Ordner
        t2 = t.replace("${CLAUDE_PLUGIN_ROOT}/", "")
        with zipfile.ZipFile(ziel, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr(f"{name}/", "")
            z.writestr(f"{name}/SKILL.md", t2)
            for p in sorted(s.parent.iterdir()):
                if p.name != "SKILL.md":
                    zip_ordner(z, p, f"{name}/{p.name}") if p.is_dir() else z.write(p, f"{name}/{p.name}")
            z.writestr(f"{name}/references/", "")
            zip_ordner(z, QUELLE / "references", f"{name}/references")
            z.writestr(f"{name}/scripts/", "")
            zip_ordner(z, QUELLE / "scripts", f"{name}/scripts")
    print(f"gebaut: {plugin.name} und {len(list((DIST / 'skills').glob(f'*-{v}.zip')))} Skill-Pakete in dist/")


if __name__ == "__main__":
    a = sys.argv[1:]
    sperr: list[str] = []
    if "--sperrliste" in a:
        sperr = Path(a[a.index("--sperrliste") + 1]).read_text(encoding="utf-8").splitlines()
    f = pruefen(sperr)
    for x in f:
        print("FEHLER:", x)
    if f:
        sys.exit(f"{len(f)} Fehler — nichts gebaut.")
    print("Prüfung ok")
    if "--nur-pruefen" not in a:
        bauen()
