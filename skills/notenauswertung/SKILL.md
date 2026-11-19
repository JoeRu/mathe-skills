---
name: notenauswertung
description: >
  Dieser Skill wird verwendet, wenn der Nutzer Punkte in Noten umrechnen, eine
  Klassenarbeit auswerten oder Zeugnisnoten bilden möchte — etwa "Punkte in Noten
  umrechnen", "Notenspiegel für die Arbeit", "Auswertung der Arbeit Zuordnungen",
  "Gesamtnote aus mündlich und schriftlich", "Zeugnisnoten für den B-Kurs",
  "wer steht auf der Kippe" oder "Notenschlüssel für 45 Punkte". Rechnet mit dem
  Notenskript und arbeitet direkt in den vorhandenen Excel-Listen.
metadata:
  version: "0.8.0"
---

# Notenauswertung

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` und
`${CLAUDE_PLUGIN_ROOT}/references/notenschluessel.md` lesen — dort stehen Schlüssel,
Rundung auf halbe Punkte, Tendenzen und Gesamtnote. **Gerechnet wird nur mit**
`python3 $SKILLS/scripts/noten.py` (bzw. `import noten` im eigenen
Skript), nie mit eigenen Formeln.

```
python noten.py schluessel 45 --tendenz      Grenzen für 45 Punkte
python noten.py note 45 31,5 --tendenz       Note und Abstand zur nächsten
python noten.py gesamt 2,4 3,0               Gesamtnote mündlich/schriftlich
```

## 1. Datenquelle finden

Zuerst den **Kurs** nach `grundlagen.md` (*Kurswahl*) bestimmen und nennen: Punkte, Listen und Noten
gelten je Kurs. Dann im verbundenen Ordner nachsehen, bevor etwas Neues angelegt wird:

| Datei | Ort | Inhalt |
|---|---|---|
| `punkte_<arbeit>.csv` | `Kurse/<Kurs>/_intern/<Thema>/Korrektur_<Arbeit>_<JJJJ-MM-TT>[_vN]/` | Punkte je Code × Teilaufgabe aus `korrektur` |
| `punkte arbeit.xlsx` | `Kurse/<Kurs>/_intern/<Thema>/` (Altbestand: `<Thema>/_intern/`, Struktur 1) | ältere Rohpunktlisten |
| `Noten_<Kursschlüssel>_<Halbjahr>.xlsx` | `Personenbezogenes/` | Gesamtnotenliste: `Tabelle1` je Kind mündlich/schriftlich und Einzelarbeiten, `Tabelle2` Zusammenfassung mit Kommentarspalten |
| `Kopfnoten-*.xlsx`, `Arbeitsverhalten-*.xlsx` | `Personenbezogenes/` | Arbeits- und Sozialverhalten |
| `Klassenbuch_*.xlsx`, `Anwesenheitsliste.xlsx` | `Personenbezogenes/` | Fehlzeiten |
| `Punkte Prozent.xlsx` | `_Grundlagen/` (falls vorhanden) | alter Schlüsselrechner (nur zum Vergleich) |

Diese Dateien auf dem Gerät mit `openpyxl` lesen und schreiben, nicht in den
Cloud-Workspace kopieren — sie enthalten Klarnamen. Listen, die Kinder mehrerer Kurse enthalten
können (Kopfnoten, Klassenbuch), tragen Kursschlüssel oder Stammklasse im Namen; ist unklar, zu
welchem Kurs eine Datei gehört, wird gefragt, bevor sie gelesen wird.

## 2. Rechnen

Bei jeder Auswertung:

- Punkte, Prozent, Note (mit Tendenz, wenn vereinbart) je Schülerin und Schüler
- **Notenspiegel**: Häufigkeit je Note, als Tabelle und Balkendiagramm
- Durchschnitt, Median, Anteil unter Note 4
- Auffälligkeiten: deutlich unter dem eigenen Vorlauf, Notenschwelle knapp verfehlt
  (< 1 Punkt), deutlich verbessert

Der letzte Punkt ist der eigentliche Nutzen. Zum Schluss den Notenspiegel
**unabhängig nachzählen** (zweiter Durchlauf über die Rohdaten).

## 3. Ergebnis liefern

In die vorhandene Excel-Datei zurückschreiben, Formeln und Formatierung erhalten,
neue Spalten anfügen statt bestehende zu überschreiben.

Auf Wunsch ein Auswertungsdokument `Auswertung-<Arbeit>-<JJJJ-MM-TT>.docx` in
`Kurse/<Kurs>/_intern/<Thema>/` mit Notenspiegel, Durchschnitt und einem Absatz zu den
Aufgaben, die besonders schlecht gelöst wurden (Grundlage der Rückgabestunde).
Ein Notenspiegel **ohne Namen** zum Aushang kann aus `$SCHULPAKET/vorlagen/Verwaltung/Notenspiegel.docx`
entstehen und darf dann in `Kurse/<Kurs>/` liegen (er gilt für einen Kurs; der Dateiname trägt den Kurznamen).

## 4. Gesamtnoten

- **je Kurs rechnen.** Ein Kind, das im Schuljahr den Kurs gewechselt hat (`kurswechsel`), wird nicht
  stillschweigend zusammengeführt, sondern der Lehrkraft vorgelegt.
- mündlich und schriftlich getrennt ausweisen, dann mit `noten.py gesamt` verrechnen
- die pädagogischen Kommentare der Liste (`Minus; C-Kurs`, `Förderplan ab 4−`,
  `A Kurs` / `Kein A Kurs`) mit anzeigen — sie sind Teil der Entscheidung
- Kurszuordnungsempfehlungen (A/B/C) getrennt vom Notenvorschlag benennen
- **keine** Note als endgültig darstellen; entschieden wird von der Lehrkraft

## Datenschutz

Namen, Noten und Förderhinweise bleiben in `Personenbezogenes/` und `Kurse/<Kurs>/_intern/`.
Nicht in Memory, nicht in Artefakte, im Chat nur so viel wie nötig — für einen
Notenspiegel reichen Zahlen ohne Namen.

## Übergaben

| Bedarf | Skill |
|---|---|
| Punkte ins Schulportal | `schulportal-leistung` |
| Brief nach schwacher Arbeit | `elternbrief` |
| Rückgabestunde planen | `wochenplanung` |
