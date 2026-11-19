# Changelog mathe-skills (bis 0.9.1: mathe-ars)

## 1.2.2 — 2026-11-19 · Sperrliste lokal

- `build.py`: Die Begriffe der Leck-Prüfung (Schule, Ort, Person, Klassenkürzel) stehen
  nicht mehr im Code, sondern in der lokalen Datei `.sperrliste` neben `build.py`
  (git-ignoriert). Vorbereitung für das öffentliche Repository `mathe-skills`.

## 1.2.1 — 2026-11-19 · bettermarks: Bestand vor dem Austeilen

- `bettermarks`: Vor jedem Austeilen die Reiter *Aktuell* **und** *Geplant* lesen
  und je Kürzel die vorhandenen Übungs-IDs festhalten; keine Doppelzuweisung,
  Überschneidungen stehen in der Bestätigungsbox (`Bestand:`). Anlass 19.11.2026:
  vier Kinder waren kurzzeitig doppelt belegt, weil *Geplant* nicht geprüft wurde.
- Löschregel präzisiert: „Auftrag löschen“ löscht sofort ohne Rückfrage; nur ein
  selbst angelegter, noch nicht gestarteter Doppel-Auftrag wird nach Rückmeldung
  zurückgenommen, Aufträge der Lehrkraft nie.
- Begriffe an die Oberfläche angepasst (Zuweisung = *Auftrag*).

## 1.2.0 — 2026-11-16 · Struktur 3 (Fächer) und Rückschau in der Wochenplanung

Themen sind fachspezifisch. Wer den Ordner übernimmt, unterrichtet meist mehr als ein Fach —
deshalb fragt die Einrichtung die Fächer ab, und alle Themen liegen im Ordner ihres Fachs.

- **Ablage je Fach:** `<Fach>/<Thema>/` statt `<Thema>/` an der Wurzel, immer (auch bei einem Fach).
  `Kopfrechnen/` und `Mathewettbewerb/` liegen in `Mathematik/`.
- **`einstellungen.md`:** neues Feld `faecher: [Mathematik, …]`; **`kurs.md`:** neues Feld `fach:`.
- **Schulpaket je Fach:** `curricula/<Fach>/`, `lehrwerk/<Fach>/`.
- **`einrichtung`:** Frage „Welche Fächer unterrichtest du?", Abschnitt *Fachordner anlegen*,
  Einsortieren erst nach Fach, dann nach Thema; Migration 2 → 3.
- **Werkzeuge:** `schulordner.py` (`faecher`, `kurs_fach`, `thema_ordner`; `--pruefen` verlangt
  `faecher:` und Fachordner, meldet Themenordner an der Wurzel), `kurs.py material` sucht im
  Fachordner des Kurses, `kurs.py liste` zeigt das Fach.
- Die Skills bleiben Mathematik-Skills; für andere Fächer gelten Ablage, Kurse, Wochenplanung,
  Notenauswertung und Elternbriefe sinngemäß (`grundlagen.md`, *Fächer*).
- Schulportal: Hinweis zur kurzen Sitzung präzisiert (einmal „zurück" frischt sie oft auf).
- Personennamen aus Referenzen und Changelog entfernt.

### Migration von Struktur 2

1. `faecher:` in `einstellungen.md`, `fach:` in jeder `kurs.md`, `struktur: 3`.
2. Fachordner anlegen, Themenordner (und `Kopfrechnen/`, `Mathewettbewerb/`) hineinverschieben.
3. Pfade in `ausgeteilt.csv` (`datei`) und `themenfolge.csv` (`checkliste`) um das Fach ergänzen.
   `Kurse/<Kurs>/_intern/<Thema>/` bleibt, wie es ist.
4. Schulpaket: `curricula/` und `lehrwerk/` je Fach in Unterordner.
5. `schulordner.py --pruefen`, `kurs.py pruefen` je Kurs.

### Rückschau

- **`wochenplanung` beginnt mit einer Rückschau:** Plan der Vorwoche (Soll) gegen das, was die
  Lehrkraft erfasst hat (Schulportal-Historie nach der Ist-Korrektur, erfasste Leistungen,
  Ausfälle, `ausgeteilt.csv`, Ergebnis des Wochenabschlusses). Befund je Block (*wie geplant,
  geändert, nicht geschafft, ausgefallen, zusätzlich, Eintrag unverändert*), gezielte Rückfragen
  „Was ist anders gelaufen als geplant?" und Folgen für den neuen Plan. Geplant wird erst nach
  den Antworten.
- **Der bestätigte Wochenplan wird immer gespeichert:**
  `Kurse/<Kurs>/Wochenplan-<Kurzname>-KW<NN>-<JJJJ>.md` ist das Soll für die nächste Rückschau
  (bisher nur auf Wunsch als .docx). Keine Strukturänderung, keine Migration.
- `wochenabschluss` übergibt seine Diagnose als Ist an die Rückschau.

## 1.1.0 — 2026-11-07 · Struktur 2 (mehrere Kurse)

Die Ablage war themenbezogen und ging von einem Kurs aus. Sie ist jetzt kursbezogen, und kein
Werkzeug und kein Skill ratet mehr, welcher Kurs gemeint ist.

- **Ablage je Kurs (Variante B):** `Kurse/<Kurs>/_intern/<Thema>/{Scan_<Arbeit>_<JJJJ-MM-TT>/,
  Korrektur_<Arbeit>_<JJJJ-MM-TT>[_vN]/, Auswertung-….docx, bettermarks/}`. `<Arbeit>` ist `Arbeit`,
  `Wiederholung`, `Nachschreiben` oder `Test`; `_vN` bedeutet nur die freigegebene Korrekturfassung.
  Der Themenordner enthält nur noch Material ohne Kurs- und Personenbezug.
- **Kurswahl-Regel** (`grundlagen.md`): ein aktiver Kurs → benutzt und genannt; mehrere → einmal
  fragen; Ausgabe mit Kopf `Kurs: <Kurzname> (<Kursschlüssel>)`; Freigaben und Zusammenfassungen je Kurs.
  Schülercodes und Kürzel gelten nur im Kurs (`<Kurzname>/S08`).
- **Kurs ≠ Klasse:** `klassen:` in `kurs.md`; Briefe nutzen die Stammklasse des Kindes.
- **Parallelkurse:** `kurs.py parallel`; ob dieselbe Arbeit geschrieben wird, wird **immer gefragt**.
- **Zu- und Abgänge:** Der Kursschlüssel bleibt im Schuljahr gleich; Ereignis `kurswechsel`
  (`eintritt`/`austritt`), Pseudonyme werden nie neu vergeben, Ausgetretene bekommen keine Briefe mehr.
- **Werkzeuge:** `schulordner.py` (`kurs_ordner`, `kurs_wahl`, `intern_pfad`; Hinweise in `--pruefen`),
  `kurs.py` (`aktiv`, `pfad`, `parallel`; `--kurs` wird geprüft, kein Traceback), Schülerdaten-Werkzeuge
  legen **nie still** einen Kurs an (ein Tippfehler erzeugte bisher einen Phantom-Kursordner).
- **Neuer Skill `klassenleitung`:** Platzhalter, der nachfragt und kein Verfahren erfindet.
- Skills `korrektur`, `klassenarbeit`, `notenauswertung`, `schulportal-leistung`, `bettermarks`,
  `wochenabschluss`, `wochenplanung`, `elternbrief`, `einrichtung`, `kurs`, `schuelerdaten`, `kopfrechnen`
  auf die Kursablage umgestellt; Schulportal- und bettermarks-Klasse werden vor dem Schreiben gegen
  `kurs.md` geprüft.
- Vorlage: `kurs.md` mit `kurzname`, `klassen`, `## Regeln`; `einstellungen.md` mit `klassenleitung:`;
  `.gitignore` mit `**/Scan_*/`, `**/Korrektur_*/`, `Klassenleitung/`.

### Migration von Struktur 1

1. `struktur: 2` in `einstellungen.md`, `klassenleitung:` ergänzen.
2. In jeder `kurs.md` `kurzname` (eindeutig) und bei gemischten Klassen `klassen:` ergänzen.
3. `<Thema>/_intern/…` je Eintrag einem Kurs zuordnen und nach `Kurse/<Kurs>/_intern/<Thema>/`
   verschieben; Zielpfade liefert `kurs.py pfad`. Ordnernamen `…_<JJJJ.MM>` werden zu
   `…_<Arbeit>_<JJJJ-MM-TT>`. Ohne belegten Kurs bleibt der Eintrag liegen (Skill `einrichtung`
   zeigt vorher eine Tabelle).
4. `Personenbezogenes/Noten_<Jahr>_<Halbjahr>.xlsx` → `Noten_<Kursschlüssel>_<Halbjahr>.xlsx`;
   Elternbriefe in `Personenbezogenes/Elternbriefe/<Kurs>/`.
5. `.gitignore` aus dem Template übernehmen; `schulordner.py --pruefen` meldet Altbestand.

## 1.0.0 — 2026-10-30 · Struktur 1

Aus dem persönlichen Plugin `mathe-ars` werden allgemeine Skills für alle Lehrkräfte.

- **Drei Schichten:** Skills (dieser Ordner) · Schulpaket (`schule.md`,
  `notenschluessel.md`, Curricula, Vorlagen, Lehrwerk) · Schulordner mit
  `einstellungen.md`. Keine Platzhalter mehr in den Skills.
- `references/grundlagen.md` ersetzt `ars-kontext.md`; Schulspezifisches
  (Schule, Kurssystem, Curricula, Lehrwerk, Notengrenzen) liegt im Schulpaket.
- `scripts/schulordner.py` findet Schulordner, Einstellungen und Schulpaket;
  `noten.py` liest die Grenzen aus dem Schulpaket (`--schluessel` zum Überschreiben);
  `kurs.py` und die Schülerdaten-Werkzeuge (jetzt `scripts/schuelerdaten/`) nutzen es.
- Elternbrief-Werkzeug: Vorlage aus dem Schulpaket, Unterschrift aus `einstellungen.md`.
- Persönliche Regeln (bettermarks-Frist, Einheitenfehler, Kürzel statt Name) sind
  Standards mit Verweis auf *Eigene Regeln* in `einstellungen.md`.
- Neuer Skill `einrichtung` (aus der Vorlage übernommen und umgebaut) mit Migration.
- `vorlagen/`: `einstellungen.md`, `schulpaket/`, `AGENTS.md`.
- `build.py`: Prüfungen und Ausgaben (Claude-Plugin, eigenständige Skill-Pakete).

### Migration von mathe-ars 0.9.x

1. `einstellungen.md` im Schulordner anlegen (`struktur: 1`).
2. Schulpaket anlegen: `_Grundlagen/` (Curricula, Themenpläne) → `<paket>/curricula/`,
   `_Vorlagen/` → `<paket>/vorlagen/`, `westermann-mh7.md` → `<paket>/lehrwerk/`.
3. `Schuelerdaten/werkzeuge/` entfällt (jetzt in den Skills).
4. Plugin `mathe-ars` deinstallieren, `mathe-skills` installieren.

## 0.9.1 — 2026-10-30

- Beschreibung von `kurs` ohne spitze Klammern (Upload-Validierung: keine XML-Tags in
  Skill-Beschreibungen); Paket mit Verzeichniseinträgen wie 0.7.0.

## 0.9.0 — 2026-10-30

- **Neuer Skill `wochenabschluss`:** Freitagsroutine in fester Reihenfolge — bettermarks-
  Auswertung, Hausaufgabenwertung, Ereignisse, 3×-Regel, Briefe, Kursdaten, Übergabe an
  die Wochenplanung; drei feste Freigabestellen.
- **Werkzeugpfade:** `kurs.py` und die Schülerdaten-Werkzeuge laufen aus der Quelle im
  verbundenen Ordner (`$HOME/mnt/Schule_ARS/…`), nicht aus `${CLAUDE_PLUGIN_ROOT}`;
  Tabelle *Werkzeuge* in `ars-kontext.md`.
- **bettermarks:** Zugang immer über die Schulportal-Kachel; Auswertungsdatei liegt in
  `<Thema>/_intern/`; Download über die Kachel geklärt; Fristen nachträglich ändern;
  Pflichtpaket für Kürzellisten; Abschnitt *Als Hausaufgabe werten* (gemacht / teilweise /
  fehlt, Können vs. Lust); Frist-Ausnahmen nur auf Ansage.
- **Notenschlüssel:** bettermarks-Schnitt darf als mündliche Leistung zählen, wenn die Lehrkraft
  es für ein Thema festlegt (Verfahren in `notenschluessel.md`).
- **schulportal-leistung:** Abschnitt *Mündliche Leistung* (1 Aufgabe × 100 Punkte, Tendenzen);
  Bedienung von Leistungsformular und Erfassungstabelle in `references/schulportal.md`.
- **elternbrief:** Werkzeug `elternbrief_hausaufgaben.py` beschrieben; es schreibt jetzt nach
  `Personenbezogenes/Elternbriefe/3x Keine Hausaufgaben_<JJJJ-MM-TT>_<Kürzel>`.
- **schuelerdaten / wochenplanung:** bettermarks-Hausaufgaben im Protokoll; Verweis auf
  `wochenabschluss`.
- **Datenschutz:** echte Kürzel aus `bettermarks-plattform.md` entfernt.

## 0.8.0 — 2026-09-22

- **Kurse:** neues Kursmodell (`references/kurse.md`, `Kurse/<Schuljahr>_<Kurs-ID>/`),
  neuer Skill `kurs`, Werkzeug `scripts/kurs.py`. „Ausgeteilt“ gilt je Kurs,
  „eingefroren“ je Datei. Kurs-IDs, Portal-ID, Rhythmus und bettermarks-Klassen
  stehen nur noch in `kurs.md`.
- **Wochenplanung** plant je Kurs: liest Themenfolge und Ausgeteiltes, entscheidet
  je Block zwischen vorhandenem und neuem Material. Portal-Details nach
  `references/schulportal.md` ausgelagert (inkl. vollständiger Historie und Archiv).
- **Notenschlüssel** zentral in `references/notenschluessel.md` und
  `scripts/noten.py` (mit Selbsttest); alle Skills rechnen damit.
- **Fachcurricula 2024** (Stufen 5–8) in `_Grundlagen/`; Themenplan Stufe 7 als
  `_Grundlagen/themenplan-7.csv`.
- **Ordnerstruktur:** `_Grundlagen/`, `_Vorlagen/`, `_Eingang/`, `Kopfrechnen/`,
  `Kurse/`, `Elternarbeit/`, `<Thema>/_intern/` für alles mit Namen, Punkten, Scans.
  Alle Themenordner in `Arbeitsblätter/`, `Klassenarbeiten/`, `Tafelbilder/` sortiert.
- **Dateinamen:** neue Dateien `<Typ>-<Thema>[-Variante]-JJJJ-MM-TT[_Lösung]`.
- **Datenschutz:** echte Namen und Kürzel aus Skill-Beispielen entfernt; Schlüsseldatei
  wird von Claude nie geöffnet (einheitlich in Skills und Einstellungen); Elternbriefe
  nach `Personenbezogenes/Elternbriefe/`; `.gitignore` per Muster statt Einzeldateien.
- **Referenzen fortschreiben** in der Quelle, nicht in der installierten Kopie.
- `kopfrechnen` nutzt die vorhandenen Generatoren; Lösungsfassung heißt `_Lösung`.
- `arbeitsblatt` erstellt auch Tafelbilder; `elternbrief` hängt nach dem Versand
  ein `elternkontakt`-Ereignis an.

## 0.7.0 — 2026-09-21

- Ordnerstruktur der Themenordner (Klassenarbeiten/Arbeitsblätter/Tafelbilder).
