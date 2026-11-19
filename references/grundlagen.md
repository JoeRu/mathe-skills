# Grundlagen — bei jedem Skill zuerst lesen

Die Skills sind für alle Lehrkräfte gleich. Was sich je Person und je Schule
unterscheidet, steht **nicht** hier, sondern wird zur Laufzeit gelesen:

| Schicht | Wo | Inhalt |
|---|---|---|
| **Skills** (dieses Paket) | installiertes Plugin bzw. Ordner `mathe-skills/` | Abläufe, allgemeine Referenzen, Werkzeuge |
| **Schulpaket** | Ordner laut `schulpaket:` in `einstellungen.md` | `schule.md` (Schule, Kurssystem, Curricula, Lehrwerk), `notenschluessel.md` (Grenzen), `curricula/`, `vorlagen/`, `lehrwerk/` |
| **Schulordner** der Lehrkraft | verbundener Ordner mit `einstellungen.md` | Einstellungen, Kurse, Material, Schülerdaten |

## Erster Schritt jedes Skills

1. **Schulordner finden:** der verbundene Ordner, der `einstellungen.md` enthält
   (auf dem Gerät `$HOME/mnt/<Ordner>`, mit `ls $HOME/mnt/*/einstellungen.md`
   feststellen, nicht raten). Fehlt die Datei oder stehen dort noch Platzhalter
   `<<…>>`: Skill `einrichtung`.
2. **`einstellungen.md` lesen:** Name und Anrede der Lehrkraft, Kürzel, Pfade zu
   Schulpaket und Skills, und unter *Eigene Regeln* die Abweichungen von den
   Standards dieser Skills. **Eigene Regeln gehen vor.**
3. **`<Schulpaket>/schule.md` lesen:** Schule, Kurssystem, Fachcurriculum, Lehrwerk,
   Vorlagen. Was dort steht, wird nicht erfragt.
4. Prüfen, dass `struktur:` in `einstellungen.md` zu diesen Skills passt
   (`python3 $SKILLS/scripts/schulordner.py --pruefen`). Passt sie nicht: nichts
   schreiben, Skill `einrichtung` (Migration) anbieten.
5. **Kurs bestimmen**, sobald die Aufgabe einen Kurs betrifft (Abschnitt *Kurswahl*).

In den Skills bedeuten:

| Kürzel | Pfad |
|---|---|
| `$SCHULORDNER` | Schulordner auf dem Gerät, z. B. `$HOME/mnt/Schule_XYZ` |
| `$SCHULPAKET` | `$SCHULORDNER/<schulpaket aus einstellungen.md>` |
| `$SKILLS` | `$SCHULORDNER/<skills aus einstellungen.md>` — die lokale Kopie dieser Skills |
| *die Lehrkraft* | die Person aus `einstellungen.md` (`lehrkraft:`), angesprochen wie dort unter `anrede:` |

## Werkzeuge — wo sie laufen

Alle Werkzeuge lesen oder schreiben Dateien im Schulordner und laufen deshalb **auf
dem Gerät** aus der lokalen Kopie `$SKILLS/scripts/`. `${CLAUDE_PLUGIN_ROOT}` ist die
installierte Kopie im Cloud-Workspace — dort liegen dieselben Texte zum Lesen, aber
der Schulordner ist von dort nicht erreichbar.

| Werkzeug | Aufruf |
|---|---|
| Schulordner prüfen | `python3 $SKILLS/scripts/schulordner.py --pruefen` |
| Kurse, Pfade, Parallelkurse | `python3 $SKILLS/scripts/kurs.py …` (`liste`, `aktiv`, `pfad`, `parallel`, …) |
| Noten | `python3 $SKILLS/scripts/noten.py …` (Grenzen aus dem Schulpaket) |
| Schülerdaten | `python3 $SKILLS/scripts/schuelerdaten/<werkzeug>.py …` |

Die Werkzeuge finden den Schulordner selbst (Umgebungsvariable `SCHULORDNER`, sonst
über `einstellungen.md`). Kurzformen wie `kurs.py material …` in den Skills meinen
diese Aufrufe.

Ohne Claude (Codex, andere Agenten über `AGENTS.md`): `${CLAUDE_PLUGIN_ROOT}` ist
`$SKILLS`, die lokale Shell ersetzt `device_bash`, Browser-Schritte erledigt die
Lehrkraft, wenn kein Browserwerkzeug da ist.

## Fächer — Material liegt je Fach

Welche Fächer die Lehrkraft unterrichtet, steht in `einstellungen.md` (`faecher:`), gefragt wird
einmal bei der Einrichtung. Jedes Fach hat einen gleichnamigen Ordner im Schulordner, und **alle
Themenordner liegen darin**: `<Fach>/<Thema>/`, z. B. `Mathematik/Prozentrechnung/`. An der Wurzel
liegt kein Themenordner — auch nicht bei nur einem Fach.

- Jeder Kurs gehört zu genau einem Fach (`fach:` in `kurs.md`). Der Themenordner eines Kurses ist
  `<Fach des Kurses>/<Thema>/`; `thema` in `themenfolge.csv` und in den Werkzeugen bleibt der bloße
  Themenname.
- Dateipfade in `ausgeteilt.csv` und `themenfolge.csv` sind relativ zum Schulordner und beginnen
  mit dem Fach (`Mathematik/Zuordnungen/Arbeitsblätter/…`).
- Das Schulpaket führt Curricula und Lehrwerk je Fach: `$SCHULPAKET/curricula/<Fach>/`,
  `$SCHULPAKET/lehrwerk/<Fach>/`.
- Kommt ein Fach dazu: in `faecher:` ergänzen, Fachordner anlegen (Skill `einrichtung`).
- Diese Skills sind für Mathematik geschrieben. Für andere Fächer gelten Ablage, Kurse,
  Wochenplanung, Notenauswertung und Elternbriefe sinngemäß; `kopfrechnen`, `bettermarks`,
  `buchaufgaben` und der Mathewettbewerb sind reine Mathematik-Skills. Das wird gesagt, statt ein
  Mathe-Verfahren auf ein anderes Fach zu übertragen.

## Kurse — immer zuerst klären, um welchen Kurs es geht

Material gehört zu einem **Thema**, Unterricht zu einem **Kurs**. Jeder Kurs hat einen
eigenen Ordner `Kurse/<Schuljahr>_<Kurs-ID>/` (z. B. `Kurse/2026-27_KURSID/`) mit Niveau,
Wochenrhythmus, Portal- und bettermarks-Kennungen, Themenfolge, der Liste des Ausgeteilten
und allem, was Namen, Punkte oder Scans enthält (`_intern/`). Aufbau und Regeln:
`references/kurse.md`.

**Die Ebenenregel.** Im Themenordner liegt nur, was **keinen Kurs und keine Person**
betrifft (Arbeit, Lösung, Checkliste, Arbeitsblatt, Tafelbild, Generator). Alles andere
gehört in den Kursordner, und der Kursschlüssel steht dann im **Pfad**, nicht nur im
Dateinamen. Pfade unter `_intern/` werden nicht von Hand gebaut, sondern mit
`python3 $SKILLS/scripts/kurs.py pfad …` erzeugt.

### Kurswahl — gilt für jeden Skill

- Niveau, Stufe, Rhythmus und Regeln des Kurses stehen in `kurs.md` — **dort lesen, nicht erfragen**.
- Nennt der Auftrag einen Kurs (Kursschlüssel, Kurzname, „die 7 B“), wird er mit `kurs.py liste`
  gegen die vorhandenen Kurse geprüft. Passt nichts eindeutig, wird gefragt.
- Nennt der Auftrag keinen: **genau ein aktiver Kurs** → er ist gemeint, wird aber im Ergebnis
  genannt. **Mehrere aktive Kurse** → einmal fragen (mit den Kurznamen als Auswahl) und nicht aus
  Dateinamen, Scans, Codes oder dem zuletzt bearbeiteten Kurs schließen.
- Jede Antwort, die einen Kurs betrifft, beginnt mit `Kurs: <Kurzname> (<Kursschlüssel>)`.
  Schreibende Schritte (Ausgeteiltes, Ereignisse, Portal, Briefe) nennen den Kurs im Vorschlag,
  bevor sie ausgeführt werden.
- Betrifft ein Auftrag mehrere Kurse („Wochenabschluss“ ohne Kursangabe, „alle Kurse“), gibt es
  **einen Block je Kurs**, und Freigaben gelten je Kurs.
- **Codes sind nur innerhalb eines Kurses eindeutig.** Pseudonym (`S08`) und bettermarks-Kürzel
  (`MaMu`) können in zwei Kursen vorkommen. Bei mehr als einem aktiven Kurs werden sie mit Kurs
  genannt (`<Kurzname>/S08`); Tabellen mit Codes tragen eine Spalte `kurs`.
- **Der Kurs bleibt im Schuljahr derselbe**, auch wenn Kinder kommen, gehen oder wechseln, und auch
  über das Halbjahr (`references/kurse.md`, *Zu- und Abgänge*).
- **Kurs ≠ Klasse.** Der Kurs ist die Lerngruppe im Unterricht und kann Kinder aus mehreren
  Stammklassen enthalten (`klassen:` in `kurs.md`). Wo ein Dokument die Klasse verlangt (z. B. ein
  Elternbrief), ist die **Stammklasse des Kindes** gemeint, nicht der Kurs. Ist sie nicht bekannt,
  wird gefragt.
- **Parallelkurse** (gleiche Stufe, gleiches Niveau, gleiches Thema): Ob dieselbe Arbeit geschrieben
  wird, hängt vom Fall ab. `kurs.py parallel` zeigt sie an, die Lehrkraft entscheidet und wird
  **immer gefragt**.
- Kurs-IDs, Portal-IDs und Klassennamen stehen nur in `kurs.md`, nie in den Skills.

### Klassenleitung

Aufgaben der Klassenleitung (Stammklasse, nicht Mathekurs) sind **nicht Teil dieser Skills**. Steht in
`einstellungen.md` `klassenleitung:` mit einer Klasse oder nennt der Auftrag solche Aufgaben, übernimmt
der Platzhalter-Skill `klassenleitung`: Er fragt nach, was gebraucht wird, und erfindet kein Verfahren.

## Notenschlüssel

Grenzen und Gesamtnote stehen im Schulpaket (`$SCHULPAKET/notenschluessel.md`), die
Rechenregeln (Rundung, Tendenzen, bettermarks) in `references/notenschluessel.md`.
Gerechnet wird nur mit `noten.py`, nie per Hand.

## Ordnerstruktur des Schulordners (Struktur 3)

| Ordner | Inhalt | Git |
|---|---|---|
| `einstellungen.md` | Lehrkraft, Kürzel, Fächer, Pfade, eigene Regeln | ja |
| `<Schulpaket>/` bzw. `<Skills>/` | gemeinsam genutzte Ordner (oft als freigegebener Ordner verknüpft) | eigenes Repository |
| `_Grundlagen/` | eigene Grundlagen: `Punkte Prozent.xlsx`, Umzugsprotokolle | ja |
| `_Eingang/` | Chat-Ablagen, `zu_sortieren/` | nein |
| `<Fach>/` | ein Ordner je unterrichtetem Fach (`faecher:`), z. B. `Mathematik/` | ja |
| `<Fach>/<Thema>/` | Unterrichtsmaterial je Thema, ohne Kurs- und Personenbezug, siehe unten | ja |
| `Mathematik/Kopfrechnen/` | alle Kopfrechenblätter, `generator/` | ja |
| `Mathematik/Mathewettbewerb/` | `Aufgaben/`, `Übungsmaterial/`, `_intern/` | ja, außer `_intern/` |
| `Kurse/` | ein Ordner je Kurs und Schuljahr; darin `_intern/` für alles mit Namen, Punkten oder Scans | ja, außer `_intern/` |
| `Elternarbeit/` | Elternabend-Folien, allgemeine Elterninfos ohne Namen | ja |
| `Schuelerdaten/` | pseudonymisierter Bestand je Kurs | nur `README.md` |
| `Personenbezogenes/` | Klarnamen: Schlüssel, Listen, ausgefüllte Formulare, `Elternbriefe/<Kurs>/` | nein |
| `Dienstliches/` | eigene Personaldaten | nein |

Themenordner heißen wie die Themen des Fachcurriculums und liegen im Ordner ihres Fachs. Fehlt
ein Thema, einen neuen Ordner `<Fach>/<Themenname>/` anlegen (ohne Datum). An der Wurzel des
Schulordners liegt nur, was kein Fach hat (Kurse, Elternarbeit, Personenbezogenes …).

### Unterordner im Themenordner

| Unterordner | Inhalt |
|---|---|
| `Klassenarbeiten/` | Arbeiten, Übungs-, Nachschreib- und Wiederholungsarbeiten samt Lösungen und Erwartungshorizonten; Checklisten, Selbsttests |
| `Arbeitsblätter/` | eigene Arbeitsblätter mit Lösungen, Verlagsmaterial, lose Übungs-PDFs, Bildquellen |
| `Tafelbilder/` | Tafelbilder, ihre Bildquellen und Erzeugungsskripte |
| `generator/` | Python-Generatoren für Aufgaben und Arbeiten |

Direkt im Themenordner liegt nichts. Elterninfos mit Termin und Wochenpläne gehören in den
Kursordner; ältere Elterninfos im Themenordner bleiben, wo sie sind.

### Der Kursordner

```
Kurse/<Schuljahr>_<Kurs-ID>/
  kurs.md  themenfolge.csv  ausgeteilt.csv
  Wochenplan-<Kurzname>-KW<NN>-<JJJJ>.md        bestätigter Plan = Soll, mit Rückschau auf die Vorwoche (.docx auf Wunsch)
  Elterninfo-<Thema>-<JJJJ-MM-TT>.docx          ohne Namen, mit dem Termin dieses Kurses
  _intern/<Thema>/                              git-ignoriert
    Scan_<Arbeit>_<JJJJ-MM-TT>/                 eine PDF je Arbeit
    Korrektur_<Arbeit>_<JJJJ-MM-TT>[_vN]/       Korrektur-PDFs, punkte_<arbeit>.csv (_vN = freigegebene Fassung)
    Auswertung-<Arbeit>-<JJJJ-MM-TT>.docx
    bettermarks/                                Klassenaktivität …xlsx, schnitt_<JJJJ-MM-TT>.csv
```

`<Arbeit>` ist `Arbeit`, `Wiederholung`, `Nachschreiben` oder `Test`; das Datum ist der **Termin**,
nicht der Monat — so kollidieren zwei Arbeiten im selben Monat nicht.

**Regel:** Was einen Namen, einen Schülercode mit Punkten oder einen Scan enthält, kommt nach
`Kurse/<Kurs>/_intern/<Thema>/` bzw. `Personenbezogenes/` (dort mit Kursschlüssel im Pfad oder
Namen: `Elternbriefe/<Kurs>/`, `Noten_<Kurs>_<Halbjahr>.xlsx`) — nirgendwo sonst.

### Dateinamen

Für **neue** Dateien: `<Typ>-<Thema>[-<Variante>]-<JJJJ-MM-TT>[_Lösung].<ext>`,
z. B. `Mathematik/Zuordnungen/Arbeitsblätter/AB-Dreisatz-Basis-2026-10-06.docx`. Das Datum ist der Einsatztag (bei Arbeiten
der Termin), sonst der Erstellungstag. Word, PDF und LaTeX derselben Fassung tragen
denselben Basisnamen.

Bestehende Dateien werden nicht umbenannt und **nie überschrieben** — eine geänderte
Fassung bekommt `_v2`, `_v3` … an den Basisnamen.

Bei **Arbeiten** ist das Datum im Namen der Termin des ersten Einsatzes. Schreibt ein weiterer
Kurs dieselbe Arbeit, bleibt der Name; sein Termin steht in `themenfolge.csv` und
`ausgeteilt.csv` **dieses** Kurses.

## Ausgeteilt und eingefroren

- **Eingefroren** gilt für die Datei: Hat irgendein Kurs sie in der Hand, wird sie
  nicht mehr verändert. Verbesserungen entstehen als `_v2` daneben.
- **Ausgeteilt** gilt je Kurs und steht in `Kurse/<Kurs>/ausgeteilt.csv`. Vor dem
  Planen oder Erstellen dort nachsehen, was dieser Kurs schon hatte.

## Referenzen fortschreiben

Neu Gelerntes wird in der **Quelle** ergänzt, nie in `${CLAUDE_PLUGIN_ROOT}`:

| Was | Wohin |
|---|---|
| Plattformwissen (Schulportal, bettermarks, BiBox-Bedienung) | `$SKILLS/references/…` |
| Lehrwerk (Seiten, Aufgaben, Materialnummern) | `$SCHULPAKET/lehrwerk/<Fach>/…` |
| Schule (Termine, Kurssystem, Vorlagen) | `$SCHULPAKET/schule.md` |
| eigene Vorlieben und Absprachen der Lehrkraft | `einstellungen.md`, Abschnitt *Eigene Regeln* |

Liegen Skills oder Schulpaket in einem **freigegebenen Ordner einer anderen Person**
(nur lesbar), wird nichts dort geschrieben: Ergänzung als Vorschlag im Chat nennen.
Am Ende sagen, ob die Skills neu gebaut werden sollten (`$SKILLS/README.md`).

## Datenschutz

Der Schulordner enthält Klarnamen, Noten und Förderplanhinweise. Diese Daten:

- niemals in Zusammenfassungen oder Chat-Antworten breiter ausbreiten als nötig,
- niemals in Dateien schreiben, die den Schulordner verlassen (Repository, Artefakte,
  Projektwissen, Skills, Schulpaket — auch nicht als Beispiel),
- niemals in ein Memory oder Gedächtnis des Assistenten speichern.

Die Schlüsseldatei `Personenbezogenes/schluessel-<Kurs>.csv` wird **nie geöffnet**,
auch nicht lokal; nur die Werkzeuge in `$SKILLS/scripts/schuelerdaten/` benutzen sie.
Andere Dateien in `Personenbezogenes/` dürfen lokal gelesen werden, wenn die Aufgabe
es verlangt.

Ergebnisse mit Namen bleiben in `Personenbezogenes/` bzw. `Kurse/<Kurs>/_intern/`. Beispiele in
Skills, Referenzen und Schulpaket verwenden erfundene Codes (`S99`, `MaMu`).
