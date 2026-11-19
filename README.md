# mathe-skills

Skills für den Mathematikunterricht — für jede Lehrkraft gleich. Was Person und
Schule unterscheidet, lesen die Skills zur Laufzeit:

| Schicht | Inhalt | Pflege |
|---|---|---|
| **mathe-skills** (dieser Ordner) | Abläufe (`skills/`), allgemeine Referenzen, Werkzeuge, Vorlagen für Einstellungen und Schulpaket | eine Person, für alle |
| **Schulpaket** (z. B. `schule-ars/`) | `schule.md`, `notenschluessel.md`, Curricula, Briefvorlagen, Lehrwerk-Verzeichnis | Fachschaft der Schule |
| **Schulordner** der Lehrkraft | `einstellungen.md`, Kurse, Material, Schülerdaten | jede Lehrkraft |

Schnittstelle zwischen den Schichten ist `einstellungen.md` im Schulordner
(Strukturversion `struktur: 3`, Muster in `vorlagen/einstellungen.md`) und das
Schulpaket mit `schule.md` und `notenschluessel.md` (Muster in `vorlagen/schulpaket/`).

## Skills

| Skill | Wofür |
|---|---|
| `einrichtung` | Schulordner einrichten, Skills und Schulpaket verbinden, Kurse anlegen, Migration |
| `arbeitsblatt` | Arbeits-, Übungs- und Lernblätter, Tafelbilder, differenziert |
| `kopfrechnen` | Kopfrechenblätter mit maschinell geprüftem Lösungsblatt |
| `klassenarbeit` | Arbeiten mit Parallelversion, Erwartungshorizont und Checkliste |
| `korrektur` | Gescannte Arbeiten korrigieren: Punkte, Korrektur-PDF, Stärken/Schwächen |
| `notenauswertung` | Punkte → Note, Notenspiegel, Gesamt- und Zeugnisnoten |
| `schulportal-leistung` | Arbeiten und mündliche Leistungen ins Schulportal |
| `elternbrief` | Elternschreiben und Verwaltungsdokumente aus den Vorlagen des Schulpakets |
| `wochenplanung` | Rückschau auf die Vorwoche (Soll/Ist, Rückfragen), Wochenplan je Stunde, Rückwärtsplanung vor Arbeiten, Schulportal-Einträge |
| `wochenabschluss` | Freitagsroutine: bettermarks, Hausaufgaben, 3×-Regel, Briefe, Kursdaten |
| `buchaufgaben` | Aufgaben im Lehrwerk finden, BiBox-Material laden |
| `bettermarks` | Auswerten, Aufgaben finden, Stunden planen, zuweisen |
| `schuelerdaten` | Hausaufgaben, Absprachen, Elternkontakte je Kind, 3×-Regel |
| `kurs` | Stand eines Kurses, Themenfolge, Ausgeteiltes |
| `klassenleitung` | Platzhalter für Aufgaben der Klassenleitung: fragt nach, erfindet kein Verfahren |

## Fächer

Themen sind fachspezifisch. Die Einrichtung fragt, welche Fächer die Lehrkraft unterrichtet
(`faecher:` in `einstellungen.md`), und alles Material liegt unter `<Fach>/<Thema>/`; jeder Kurs
nennt sein Fach in `kurs.md`. Die Skills selbst sind für Mathematik geschrieben — andere Fächer
bekommen dieselbe Ablage, Kurs- und Wochenplanung, aber keine eigenen Fach-Skills.

## Mehrere Kurse

Jede Aufgabe gehört zu genau einem Kurs; er wird nie erraten (`references/grundlagen.md`, *Kurswahl*).
Scans, Korrekturen, Punkte und bettermarks-Exporte liegen je Kurs unter
`Kurse/<Kurs>/_intern/<Thema>/`, Schülercodes gelten nur im Kurs (`<Kurzname>/S08`). Kurs und Klasse sind
verschiedene Dinge, und ob Parallelkurse dieselbe Arbeit schreiben, wird gefragt.

## Werkzeuge (`scripts/`)

Laufen auf dem Rechner der Lehrkraft aus der lokalen Kopie dieses Ordners und finden
den Schulordner über `einstellungen.md`:

- `schulordner.py` — Schulordner, Einstellungen, Schulpaket finden; `--pruefen`
- `noten.py` — Notenschlüssel (Grenzen aus dem Schulpaket), Tendenzen, Gesamtnote; `--test`
- `kurs.py` — Kurse, Themenfolge, Ausgeteiltes, Eingefroren-Prüfung; `aktiv`, `pfad` (Ablageort je Kurs), `parallel`
- `schuelerdaten/` — Schlüssel anlegen, Ereignisse, Auswertung (3×-Regel), Elternbrief

Benötigt Python 3.10+ mit `python-docx openpyxl` (Briefe, Excel), für einige Skills
LibreOffice und LaTeX (siehe Skill `einrichtung`).

## In den Assistenten bringen

| Weg | Für | Aktualisierung |
|---|---|---|
| **Ordner** (dieser Ordner im bzw. verknüpft mit dem Schulordner, dazu `vorlagen/AGENTS.md` als `CLAUDE.md`/`AGENTS.md`) | Claude Desktop/Cowork mit verbundenem Ordner, Claude Code, Codex | automatisch, wenn der Ordner ein freigegebener OneDrive-Ordner oder ein Git-Klon ist |
| **Claude-Plugin** `dist/mathe-skills-<version>.plugin` | Claude (Einstellungen → Plugins hochladen) | Upload je Version; Team/Enterprise: Sync aus GitHub |
| **Skill-Pakete** `dist/skills/<skill>-<version>.zip` | ChatGPT (Skills hochladen), Claude-Einzelskills, andere Agent-Skills-Clients | Upload je Version |

Die Werkzeuge brauchen in jedem Fall die lokale Kopie im Schulordner
(`skills:` in `einstellungen.md`) — Plugin und Skill-Pakete liefern nur die Texte.

## Bauen

```
python build.py --sperrliste <lokale Datei mit echten Kürzeln>
```

Prüft Frontmatter (Name, Beschreibung ≤ 1024 Zeichen, keine spitzen Klammern),
Verweise, Schul- und Personennamen, Python-Syntax und `noten.py --test`, und baut
dann Plugin und Skill-Pakete nach `dist/`. Vor jedem Bau die Version in
`.claude-plugin/plugin.json` und `CHANGELOG.md` erhöhen. Änderungen an der
Schnittstelle (Ordner, Felder in `einstellungen.md`) erhöhen `STRUKTUR` in
`scripts/schulordner.py` und bekommen im Changelog einen Abschnitt *Migration*.

## Datenschutz

Dieser Ordner enthält keine Schülerdaten, keine Namen und nichts Schulspezifisches —
er darf geteilt werden. Klarnamen, Noten und Förderhinweise bleiben im Schulordner der
Lehrkraft (`grundlagen.md`, Abschnitt *Datenschutz*).
