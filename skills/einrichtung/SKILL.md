---
name: einrichtung
description: >
  Dieser Skill wird verwendet, wenn ein Schulordner neu eingerichtet oder auf eine
  neue Fassung der Skills umgestellt wird — etwa "richte den Ordner ein", "erster
  Start", "Einrichtung", "ich bin neu hier", "einstellungen anlegen", "leg meine
  Kurse an", "übernimm mein altes Material", "Schulpaket verbinden" oder
  "Strukturversion passt nicht" — und immer dann, wenn ein anderer Skill keine
  einstellungen.md findet oder dort Platzhalter stehen. Prüft die Werkzeuge,
  stellt die Einrichtungsfragen (darunter die unterrichteten Fächer), schreibt
  einstellungen.md, legt die Fachordner an, verbindet Skills und Schulpaket, legt
  Kurse aus dem Schulportal an und sortiert Material fachweise ein.
metadata:
  version: "1.1.0"
---

# Einrichtung und Umstellung

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` (drei Schichten, Pfade,
Ordnerstruktur) und `${CLAUDE_PLUGIN_ROOT}/references/kurse.md` lesen. Den
verbundenen Ordner mit `ls $HOME/mnt/` feststellen, nicht raten.

**Fällig, wenn:** im Schulordner keine `einstellungen.md` liegt, dort Platzhalter
`<<…>>` stehen, `schulordner.py --pruefen` Fehler meldet oder `Kurse/` nur das
Muster `Beispielkurs_…` enthält.

Die Einrichtung ist ein Gespräch, kein Formular: eine Frage nach der anderen, mit
Vorschlag, und erst schreiben, wenn die Antwort da ist. Was die Lehrkraft nicht
beantworten will, bleibt offen und wird am Ende genannt. Originale werden kopiert,
nie verschoben oder gelöscht.

## 1. Werkzeuge auf dem Rechner prüfen

In einem Durchgang auf dem Gerät:

```bash
python3 --version || python --version
python3 -c "import docx, openpyxl, jinja2, matplotlib, reportlab" 2>&1
which soffice libreoffice pdflatex lualatex git
```

Ergebnis als Tabelle (vorhanden / fehlt) mit dem, was ohne das Werkzeug nicht geht.
Fehlende Python-Pakete auf Wunsch installieren
(`pip install python-docx openpyxl jinja2 matplotlib reportlab`). LibreOffice,
LaTeX und Git nur nennen.

## 2. Skills und Schulpaket verbinden

Der Schulordner braucht zwei gemeinsame Ordner (siehe `grundlagen.md`):

| Ordner | Woher | Eintrag in `einstellungen.md` |
|---|---|---|
| **Skills** (`mathe-skills/`) | freigegebener OneDrive-Ordner der Person, die die Skills pflegt, oder Git-Klon | `skills:` |
| **Schulpaket** (z. B. `schule-xyz/`) | freigegebener Ordner der Fachschaft, oder aus `$SKILLS/vorlagen/schulpaket/` neu | `schulpaket:` |

Freigegebene OneDrive-Ordner über *Verknüpfung zu „Meine Dateien“ hinzufügen* in
den Schulordner holen — dann sind sie auf dem Gerät da und aktualisieren sich selbst.
Pfade relativ zum Schulordner eintragen. Gibt es noch kein Schulpaket, aus
`$SKILLS/vorlagen/schulpaket/` eines anlegen und mit der Lehrkraft `schule.md` und
`notenschluessel.md` ausfüllen (Schule, Kurssystem, Grenzen, Curricula, Vorlagen
mit Briefkopf).

## 3. Die Einrichtungsfragen

| Frage | Feld in `einstellungen.md` |
|---|---|
| **Wie heißt du, und wie soll ich dich ansprechen?** (Vorname, Du/Sie) | `lehrkraft:`, `anrede:` |
| **Wie unterschreibst du Briefe?** (vollständiger Name) | `lehrkraft_name:` |
| **Wie lautet dein Lehrerkürzel?** | `kuerzel:` |
| **Welche Fächer unterrichtest du?** (alle, auch wenn zunächst nur eines mit den Skills läuft) | `faecher:` — danach *Fachordner anlegen* unten |
| **In welchen Kursen unterrichtest du?** (je Kurs: Fach, Stufe, Niveau; gibt es Parallelkurse?) | Schritt 4 |
| **Bist du Klassenleitung?** (Klasse) | `klassenleitung:` (`nein` oder die Klasse) |
| **Stimmen Schule, Ort und Notenschlüssel im Schulpaket?** (Werte aus `schule.md` vorlesen) | bei Nein: Schulpaket anpassen — oder, wenn es nicht deines ist, der pflegenden Person melden |
| **Gibt es Regeln, die bei dir anders sind?** (z. B. bettermarks-Frist, Kürzel statt Name auf Blättern, Abzug bei Einheitenfehlern) | Abschnitt *Eigene Regeln* |
| **Soll ich im Schulportal nachsehen, welche Kurse du hast?** | Schritt 4 |
| **Hast du vorhandenes Material, das einsortiert werden soll?** | Schritt 5 |
| **Willst du Schülerdaten pseudonymisiert führen?** | Schritt 6 |
| **Soll der Ordner ein Git-Repository werden?** | `git init`; `.gitignore` liegt bei; `git status` vor dem ersten Push lesen |

`einstellungen.md` aus dem Muster `$SKILLS/vorlagen/einstellungen.md` schreiben, dann
`python3 $SKILLS/scripts/schulordner.py --pruefen` — muss „ok“ melden.

### Fachordner anlegen

Die Themen sind fachspezifisch, deshalb liegt jedes Thema im Ordner seines Fachs
(`grundlagen.md`, *Fächer*). Nach der Fächerfrage:

1. Die Fächer so schreiben, wie die Ordner heißen sollen (`Mathematik`, `Physik`, `Deutsch` —
   ausgeschrieben, keine Kürzel), und als `faecher: [Mathematik, Physik]` eintragen.
2. Je Fach einen Ordner `<Fach>/` im Schulordner anlegen. Die Vorlage bringt `Mathematik/` mit
   (`Beispielthema/`, `Kopfrechnen/`, `Mathewettbewerb/`). Unterrichtet die Lehrkraft keine
   Mathematik, das sagen und fragen, ob der Ordner weg soll — nicht selbst löschen.
3. Gibt es im Schulpaket einen Themenplan des Fachs (`$SCHULPAKET/curricula/<Fach>/themenplan-<Stufe>.csv`),
   die Themenordner der unterrichteten Stufen mit den vier Unterordnern (`Arbeitsblätter/`,
   `Klassenarbeiten/`, `Tafelbilder/`, `generator/`) anbieten. Fehlt er, bleiben die Fachordner
   leer; Themenordner entstehen, wenn das erste Material kommt. Keine Themen erfinden.
4. Für andere Fächer als Mathematik sagen, was die Skills können: Ablage, Kurse, Wochenplanung,
   Notenauswertung und Elternbriefe sinngemäß; `kopfrechnen`, `bettermarks`, `buchaufgaben` und
   Mathewettbewerb nur für Mathematik.

## 4. Kurse und Stundenplan aus dem Schulportal

Nur nach Ja. Vorher sagen: „Ich öffne jetzt das Schulportal; melde dich bitte
selbst an.“ Bedienung und Grundregeln: `references/schulportal.md`.

1. **Kursmappen:** *Mein Unterricht → Eigene Kursmappen*: Bezeichnung, Kurskennung,
   `schulportal_id` aus dem Link. Keine Schülernamen, keine Spalte „Weiteres“;
   die Schülerzahl nur als Zahl.
2. **Stundenplan:** Startseite → *Stundenplan*: je Tag und Stunde die Kurskennung;
   aufeinanderfolgende Stunden zur Doppelstunde zusammenfassen. Als Tabelle
   *Kurs → Tag, Stunden, Minuten* zeigen und bestätigen lassen.
3. Was das Portal nicht hergibt, erfragen: Fach (wenn es aus der Bezeichnung nicht eindeutig hervorgeht), Stufe, Niveau, Halbjahr, bettermarks-Klasse
   und -Testklasse, einen **Kurznamen** (eindeutig unter den Kursen) und, wenn die Kinder
   aus mehreren Stammklassen kommen, die Stammklassen (`klassen:`). Der Kursschlüssel bleibt das
   ganze Schuljahr gleich.
4. Je Kurs nach `references/kurse.md`, *Neuer Kurs*: `Kurse/<Schuljahr>_<Kurs-ID>/`
   mit `kurs.md` (mit `fach:`), `themenfolge.csv` aus `$SCHULPAKET/curricula/<Fach>/themenplan-<Stufe>.csv`
   (nur Themen des Niveaus), leere `ausgeteilt.csv`.
5. Anbieten, die Historie des Halbjahrs einzulesen (Skill `kurs`) — eigener Schritt.

Ohne Portalzugang: Kurse aus den Antworten anlegen, `schulportal_id` leer lassen.

## 5. Vorhandenes Material einsortieren

Nur nach Ja und nur **kopieren**.

1. Quelle sichten (Dateitypen, Ordnernamen, Anzahl); Überblick je erkanntem Thema.
2. Zuordnung vorschlagen: **zuerst das Fach, dann das Thema** → `<Fach>/<Thema>/` (Themennamen
   aus dem Themenplan des Fachs). Ist das Fach einer Datei nicht erkennbar, wird gefragt oder
   sie geht nach `_Eingang/zu_sortieren/` — nicht raten.
   Arbeiten, Lösungen, Checklisten → `Klassenarbeiten/`; Arbeitsblätter,
   Verlagsmaterial → `Arbeitsblätter/`; Tafelbilder → `Tafelbilder/`;
   Kopfrechenblätter → `Mathematik/Kopfrechnen/`; leere Vorlagen → Schulpaket (Vorschlag).
3. **Alles mit Namen, Punkten oder Scans** → `Kurse/<Kurs>/_intern/<Thema>/` bzw.
   `Personenbezogenes/`. **Der Kurs wird belegt** (Arbeitstermin in `themenfolge.csv`, Zeitraum,
   Kursliste), nie aus dem Dateinamen geraten. Ist er nicht belegbar: `_Eingang/zu_sortieren/` und
   die Lehrkraft fragen. Inhalte nur so weit
   öffnen, wie für die Einordnung nötig, nichts davon im Chat wiedergeben.
4. Zuordnungstabelle zeigen, bestätigen lassen, kopieren. Nichts umbenennen oder
   überschreiben.
5. Protokoll `_Grundlagen/umzug-<JJJJ-MM-TT>.csv` (`quelle;ziel;thema;art;hinweis`).

## 6. Schülerliste und Kürzel-Mapping

Nur nach Ja **und** nachdem die Lehrkraft bestätigt, dass die Ablage
pseudonymisierter Schülerdaten mit Schulleitung bzw. Datenschutzbeauftragten
geklärt ist (`references/schuelerdaten.md`, Abschnitt *Was noch zu klären ist*).

1. Kursliste exportiert die Lehrkraft selbst (Kursmappe → Teilnehmerliste → Export)
   nach `Personenbezogenes/Kursliste_<Kurs>.xlsx`. Nicht öffnen.
2. `python3 $SKILLS/scripts/schuelerdaten/schluessel_anlegen.py --kurs <Kursschlüssel> --liste "Personenbezogenes/Kursliste_<Kurs>.xlsx"`
   — erzeugt Schlüsseldatei (nie öffnen), `kuerzel-map.csv` und leere Profile.
3. Kürzel gegen bettermarks abgleichen; Abweichungen korrigiert die Lehrkraft in
   `kuerzel-map.csv`.

## 7. Migration (Strukturversion)

Meldet `schulordner.py --pruefen` eine andere `struktur:` als die Skills erwarten:

1. `CHANGELOG.md` der Skills lesen — dort steht je Strukturversion, was sich ändert.
2. Die Änderungen als Liste zeigen (welche Ordner, Felder, Dateien), bestätigen lassen.
3. Ausführen: Ordner per `git mv` bzw. Kopie, Felder in `einstellungen.md` ergänzen,
   `struktur:` hochsetzen. Nichts löschen, was nicht ausdrücklich ersetzt wird.
4. `--pruefen` erneut, Ergebnis nennen.

**Struktur 1 → 2** (`<Thema>/_intern/` zieht in den Kursordner, `CHANGELOG.md`, *Migration*): Je Eintrag
den Kurs belegen und den Zielpfad mit `kurs.py pfad` bilden. Erst die Tabelle (Quelle, Ziel, Beleg,
offen) zeigen, nach Bestätigung verschieben. Ohne belegten Kurs bleibt der Eintrag liegen.

**Struktur 2 → 3** (Themenordner ziehen in den Fachordner, `CHANGELOG.md`, *Migration*):

1. Fächer erfragen und als `faecher:` eintragen; je Kurs `fach:` in `kurs.md` ergänzen.
2. Tabelle zeigen: jeder Themenordner an der Wurzel (dazu `Kopfrechnen/`, `Mathewettbewerb/`) →
   `<Fach>/<Ordner>/`. Bei einem Fach ist die Zuordnung eindeutig, bei mehreren je Ordner fragen.
3. Nach Bestätigung verschieben (`git mv` bzw. `mv`), dann die Pfade in jeder
   `Kurse/<Kurs>/ausgeteilt.csv` (Spalte `datei`) und `themenfolge.csv` (Spalte `checkliste`) um das
   Fach ergänzen — vorher Sicherungskopien nach `_Grundlagen/`, Protokoll
   `_Grundlagen/umzug-struktur3-<JJJJ-MM-TT>.csv`.
4. Liegt das Schulpaket in eigener Hand: `curricula/` und `lehrwerk/` je Fach in Unterordner legen.
5. `struktur: 3`, dann `schulordner.py --pruefen` und `kurs.py pruefen --kurs <K>` je Kurs.

## 8. Abschluss

- `schulordner.py --pruefen` und `noten.py --test` laufen lassen und nennen.
- Zusammenfassen: was eingetragen, angelegt, kopiert wurde; was offen bleibt
  (Schulpaket prüfen, Datenschutzklärung, Kurse ohne Portal-ID).
- Wie die Skills in den Assistenten kommen, steht in `$SKILLS/README.md`
  (Plugin, Skill-Uploads oder Ordner über `AGENTS.md`/`CLAUDE.md`).
