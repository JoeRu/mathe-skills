---
name: kopfrechnen
description: >
  Dieser Skill wird verwendet, wenn der Nutzer ein Kopfrechenblatt, Kopfrechentest,
  Rechentraining oder Einmaleins-Blatt erstellen möchte — etwa "Kopfrechnen für
  Freitag", "Kopfrechenblatt mit negativen Zahlen", "40 Aufgaben zum Einmaleins",
  "Rechentraining für die 7", "Kopfrechnen mit Lösung" oder "neues Blatt wie
  letzte Woche, andere Zahlen". Erzeugt datierte Blätter mit garantiert korrektem
  Lösungsblatt aus einem Python-Generator.
metadata:
  version: "0.8.0"
---

# Kopfrechenblatt erzeugen

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` und
`${CLAUDE_PLUGIN_ROOT}/references/dokumente.md` lesen.

Ordner: `Mathematik/Kopfrechnen/` (alle Stufen, alle Kurse). Generatoren:
`Mathematik/Kopfrechnen/generator/Kopfrechnen_generator.py` (gemischtes Blatt) und
`Kopfrechnen_quadratzahlen_generator.py`. **Erst den vorhandenen Generator
benutzen** (`python Kopfrechnen_generator.py TT.MM.JJJJ [Zielordner] [Variante]`),
nur für neue Aufgabentypen erweitern — dann als neue Datei `…_v2.py`, der alte
Generator bleibt lauffähig.

## Format des Blattes

Etabliertes Muster (siehe `Mathematik/Kopfrechnen/`):

- Überschrift `Kopfrechnen`, **zentriert** und mit deutlichem Abstand darunter
- Zeile `Name: ______________________` und `Datum: TT.MM.JJJJ`
- ca. **40 Aufgaben**, mehrspaltig gesetzt, jede in der Form `7 x 8 = _____`
- **Keine Aufgabennummerierung.** Die Klasse verwechselt sonst die laufende
  Nummer mit den Zahlen der Aufgabe. Kein `1)`, kein `\begin{enumerate}` —
  die Aufgaben stehen als eigenständige Zeilen untereinander.
- Passt auf **eine Seite**, wird in wenigen Minuten zu Stundenbeginn geschrieben
- **Großzügiger vertikaler Abstand** — nach der Namenszeile und zwischen den
  Aufgaben, siehe Abschnitt „Vertikaler Platz" in `references/dokumente.md`.
  Bewährt: LaTeX 3 Spalten mit `itemsep 2.6em`, Word Tabelle 10 × 4 mit
  Zeilenhöhe 2,05 cm.
- Zweite Fassung mit eingetragenen Lösungen, Dateiname mit `_Lösung`
  (ältere Blätter heißen noch `_Mit_lösung`)

Dateiname für neue Blätter: `Kopfrechnen-JJJJ-MM-TT[-Schwerpunkt].docx` (Datum =
Einsatztag des ersten Einsatzes), so erzeugt es der Generator. Ältere Blätter heißen
`Kopfrechnen_TT.MM.JJJJ.docx` und werden nicht umbenannt. Ablage in `Mathematik/Kopfrechnen/`.

Vor dem Erzeugen mit `kurs.py material --kurs <Kurs> --thema Kopfrechnen` nachsehen,
welche Blätter der Kurs schon geschrieben hat — die Variante (3. Argument) so
wählen, dass kein Blatt doppelt kommt.

Parallelkurse (`kurs.py parallel`): Ob sie dasselbe Blatt schreiben, wird gefragt. Schreibt ein
zweiter Kurs es an einem anderen Tag, wird es für ihn mit seinem Datum neu erzeugt (Dateiname mit
Zusatz `-<Kurzname>`), damit das gedruckte Datum stimmt; jeder Kurs bekommt seine Zeile in
`ausgeteilt.csv`.

## Aufgabenmischung

Wenn der Nutzer keinen Schwerpunkt nennt, die bewährte Mischung verwenden:

| Anteil    | Typ                                                       |
| --------- | --------------------------------------------------------- |
| ~35 %     | kleines Einmaleins (2–10)                                 |
| ~15 %     | großes Einmaleins (11–15, Quadratzahlen bis 15²)          |
| ~15 %     | Multiplikation mit 10, 100, 1000                          |
| ~15 %     | Division, auch mit Ergebnis < 1 (z. B. 90 : 100 = 0,9)    |
| ~12 %     | Verkettungen (2 x 2 x 2), Vielfache runder Zahlen         |
| **≥ 1**   | **Brüche — auf jedem Blatt, ohne Ausnahme**               |

**Bruchaufgaben sind Pflicht.** Mindestens eine pro Blatt, bewährt sind drei.
Bruchrechnung verkümmert sonst zwischen den Themenblöcken; das Kopfrechenblatt
hält sie wach. Geeignete Typen:

- Anteil einer Größe: `1/4 von 60` (Zähler so wählen, dass das Ergebnis ganzzahlig wird)
- gleichnamige Addition: `1/5 + 2/5`
- Vielfaches eines Stammbruchs: `3 x 1/4`
- Bruch als Dezimalzahl: `1/4 als Dezimalzahl`

Lösungen von Bruchaufgaben als **Bruch** setzen, nicht als Dezimalzahl — außer die
Aufgabe fragt ausdrücklich nach der Dezimalschreibweise. In LaTeX `\dfrac`
verwenden, nicht `\frac`: inline gesetzte Brüche werden sonst so klein, dass sie
neben den übrigen Aufgaben unlesbar sind.

Bei Themenschwerpunkt (negative Zahlen, Prozente, Terme) die Mischung entsprechend
verschieben, aber immer ein Drittel Grundlagen und die Bruchaufgaben beibehalten —
das Blatt soll auch der Wiederholung dienen.

Aufgaben nicht in Blöcken sortieren, sondern durchmischen. Keine Aufgabe doppelt.

## Generator statt Handarbeit

Ein Python-Skript schreiben, das Aufgaben **und** Lösungen in einem Durchgang
erzeugt. Die Lösung entsteht aus derselben Rechnung wie die Aufgabe — dadurch
können sie nicht auseinanderlaufen.

```python
import random
random.seed(<Datum als Zahl>)   # reproduzierbar
aufgaben = []                    # Liste von (text, ergebnis)
```

Danach eine **unabhängige Prüfung** laufen lassen: jeden Aufgabentext parsen und
neu auswerten, mit dem gespeicherten Ergebnis vergleichen, bei Abweichung abbrechen.
Die Prüfung zählt außerdem die Bruchaufgaben und bricht ab, wenn keine dabei ist.

Das ist keine Formalie. In den vorhandenen Blättern stehen falsche Lösungen
(`4 x 8 = 48`, `14 x 4 = 52`). Ein Blatt mit falscher Lösung ist schlimmer als
kein Blatt.

Dezimalergebnisse mit Komma setzen: `0,9` statt `0.9`.

## Ausgabe

`.docx`, `.tex` und `.pdf` — je einmal ohne und einmal mit Lösungen. Der Generator
schreibt `.docx` und `.tex`; das PDF entsteht mit `pdflatex` aus der `.tex`
(Ausnahme von der LaTeX-Regel in `dokumente.md`: hier wird die `.docx` immer
mit erzeugt, weil Blätter oft in Word nachbearbeitet werden). LaTeX-Präambeln:
`$SCHULPAKET/vorlagen/LaTeX/`.

Zum Schluss dem Nutzer die Dateipfade nennen und bestätigen, dass die Lösungen
maschinell gegengeprüft wurden. Nach dem Test das Blatt als `art: test` in
`ausgeteilt.csv` des Kurses eintragen (Skill `kurs`).
