---
name: kurs
description: >
  Dieser Skill wird verwendet, wenn es um den Stand oder die Stammdaten eines
  Mathekurses geht — etwa "wo steht der Kurs", "was hatte die 7 schon", "ist
  das Blatt schon ausgeteilt", "trag ein, dass wir heute das AB ausgeteilt
  haben", "Historie aus dem Schulportal nachtragen", "neuer Kurs im zweiten
  Halbjahr", "Arbeitstermin für Prozentrechnung eintragen", "liegen wir im
  Plan" oder "welches Material zu Dreiecken hatte der Kurs noch nicht". Liest
  und pflegt den Kursordner unter Kurse/ (kurs.md, themenfolge.csv, ausgeteilt.csv), gleicht
  mit dem Fachcurriculum und der Schulportal-Historie ab.
metadata:
  version: "0.8.0"
---

# Kurs: Stand, Themenfolge, Ausgeteiltes

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` und
`${CLAUDE_PLUGIN_ROOT}/references/kurse.md` lesen; für die Historie
`${CLAUDE_PLUGIN_ROOT}/references/schulportal.md`.

Werkzeug für alles: `python3 $SKILLS/scripts/kurs.py …` auf dem Gerät
(findet den Schulordner selbst, siehe `grundlagen.md`). Nicht selbst zählen oder abgleichen.

## Fragen beantworten

| Frage | Aufruf |
|---|---|
| Welche Kurse gibt es? | `kurs.py liste` |
| Wo steht der Kurs, liegt er im Plan? | `kurs.py stand --kurs <K>` — Soll-Wochen gegen Ist-Zeitraum vergleichen und in einem Satz bewerten |
| Was hatte der Kurs zu einem Thema schon, was noch nicht? | `kurs.py material --kurs <K> --thema <Thema>` |
| Darf ich die Datei noch ändern? | `kurs.py eingefroren "<Pfad>"` |
| Stimmen die Einträge? | `kurs.py pruefen --kurs <K>` |
| Welcher Kurs ist gemeint? | `kurs.py aktiv` (bei mehreren aktiven Kursen Fehler mit Liste — dann fragen) |
| Gibt es Parallelkurse im Thema? | `kurs.py parallel --kurs <K> --thema <T>` |
| Wohin mit Scans, Korrekturen, bettermarks-Dateien? | `kurs.py pfad --kurs <K> --thema <T> --art …` (Kursordner `_intern/`) |

Wochen im Plan: Ist-Wochen = Schulwochen zwischen `ist_von` und heute bzw.
`ist_bis`, Ferien abgezogen (Ferien nicht raten — im Schulportal-Kalender
nachsehen oder fragen).

## Ausgeteiltes eintragen

Eine Zeile kommt dazu, wenn etwas **tatsächlich im Kurs war**:

- die Lehrkraft sagt es („heute AB Dreisatz Basis ausgeteilt“),
- die Schulportal-Historie zeigt eine gehaltene Stunde mit Anhang oder Buchaufgabe,
- nach einer geschriebenen Arbeit oder einem Test.

```
python kurs.py eintragen --kurs <K> --datum JJJJ-MM-TT --thema <Thema> \
  --art ausgeteilt --datei "<Pfad relativ zum Schulordner>" --quelle lehrkraft --notiz "…" --probe
```

Erst mit `--probe` zeigen, bei mehr als drei Zeilen bestätigen lassen, dann ohne.
Buchaufgaben als `--art buch` ohne Datei, Seiten in `--notiz`; bettermarks-To-dos als
`--art bettermarks` mit den Übungs-IDs in `--notiz` — **nie mit Schülerkürzeln**.

## Historie aus dem Schulportal nachtragen

1. Kursmappe öffnen (`schulportal_id` aus `kurs.md`), die Lehrkraft meldet sich an.
2. Vollständige Historie über `meinunterricht.php?a=loadHistory&id=<id>` lesen und
   **nur** Datum, Thema, Inhalt/Hausaufgaben und Dateinamen der Anhänge übernehmen.
   Die Spalte „Weiteres“ enthält Klarnamen und wird nicht ausgewertet.
3. Nur gehaltene Stunden (Datum ≤ heute); Vorab-Einträge bleiben draußen.
4. Anhänge den Dateien im Themenordner zuordnen (`find` mit dem Dateinamen). Nicht
   eindeutig → Zeile ohne Datei, Beschreibung in der Notiz.
5. Schon vorhandene Zeilen (gleiches Datum, gleiche Datei) nicht doppelt eintragen.
6. Ist-Daten in `themenfolge.csv` nachziehen (Beginn eines Themas, Arbeitstermin).

## Themenfolge pflegen

- Neues Thema beginnt: `ist_von` und `status: läuft` setzen.
- Arbeit angesetzt: `arbeit_am` und `checkliste` eintragen — das ist die Quelle,
  aus der `wochenplanung` und `klassenarbeit` Termin und Stoff lesen.
- Thema abgeschlossen: `ist_bis`, `status: abgeschlossen`.
- Änderungen an `themenfolge.csv` per kurzem Python-Skript (csv-Modul, Trennzeichen
  `;`), nicht von Hand; Text mit Semikolon wird vom csv-Modul gequotet.

## Neuer Kurs

Nach `references/kurse.md`, Abschnitt *Neuer Kurs* (mit Kurznamen und Stammklassen; Zu- und Abgänge:
*Zu- und Abgänge*). Themenfolge aus
`$SCHULPAKET/curricula/<Fach>/themenplan-<Stufe>.csv`, nur die Themen für das Niveau des Kurses.
Fehlt der Themenplan der Stufe, aus dem Fachcurriculum-PDF in `$SCHULPAKET/curricula/<Fach>/`
ausziehen und der Lehrkraft zur Prüfung vorlegen (gehört dann ins Schulpaket).

## Datenschutz

Kursordner sind versioniert, außer `_intern/`. Außerhalb davon stehen **keine Namen, keine
Schülercodes und keine bettermarks-Kürzel**. Namen, Punkte und Scans liegen in
`Kurse/<Kurs>/_intern/`, Individuelles in `Schuelerdaten/` (Skill `schuelerdaten`).

## Übergaben

| Bedarf | Skill |
|---|---|
| Woche planen, Stunden ins Portal | `wochenplanung` |
| Material für den nächsten Schritt erstellen | `arbeitsblatt`, `klassenarbeit`, `kopfrechnen` |
| Einzelne Kinder, Hausaufgaben, 3×-Regel | `schuelerdaten` |
