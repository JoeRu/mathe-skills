# Dokumenterstellung

Konventionen für alle Materialien dieses Plugins.

## Ausgabeformate

Jedes Unterrichtsmaterial wird in drei Formaten erzeugt:

1. **`.docx`** — zum Nachbearbeiten. Das ist das Arbeitsformat.
2. **`.pdf`** — zum Austeilen und Drucken.
3. **`.tex`** — LaTeX-Quelle, wenn das Material rechnerisch erzeugt wurde
   (Kopfrechnen, Aufgabengeneratoren). Für rein textliche Materialien entfällt sie.

Alle liegen nebeneinander im selben Unterordner des Themenordners
(`Klassenarbeiten/`, `Arbeitsblätter/`, `Tafelbilder/` — siehe `grundlagen.md`),
mit identischem Basisnamen nach der Namenskonvention in `grundlagen.md`.
Eine geänderte Fassung einer vorhandenen Datei heißt `…_v2` — vorher mit
`kurs.py eingefroren` prüfen, ob das Original schon ausgeteilt ist.

## Word erzeugen

Das `docx`-Skill nutzen (Read auf dessen SKILL.md), bevor eine .docx-Datei gebaut
wird. Für Dokumente, die einem bestehenden Muster folgen sollen (Elternbriefe,
Klassenarbeiten im Layout der Schule), immer die vorhandene Datei kopieren und den Text
ersetzen — nie ein leeres Dokument von Grund auf aufbauen. Der Briefkopf, die
Fußzeile und die Formatvorlagen gehen sonst verloren.

## PDF erzeugen

Auf dem Gerät des Nutzers steht LibreOffice meist zur Verfügung:

```bash
soffice --headless --convert-to pdf --outdir "<Zielordner>" "<Datei.docx>"
```

Vorher mit `which soffice libreoffice` prüfen. Wenn nicht vorhanden: die .docx
in den Cloud-Workspace übertragen, dort konvertieren und das PDF zurückschreiben.

Für LaTeX-erzeugte Materialien direkt `pdflatex` bzw. `lualatex` nutzen — dann ist
die .tex die Quelle und das PDF das Original. Die .docx entsteht nur, wenn der
Generator sie ohnehin schreibt (Kopfrechnen, `Mathematik/Zuordnungen/generator/`) oder
die Lehrkraft sie ausdrücklich will.

## LaTeX-Konvention

Vorlagen liegen in `$SCHULPAKET/vorlagen/LaTeX/` (`exam.tex`, `Matheblatt.tex`,
`generate_test.py`), lauffähige Generatoren in `Mathematik/Kopfrechnen/generator/` und
`Mathematik/Zuordnungen/generator/`. Diese Dateien vor dem Schreiben einer neuen
.tex lesen und Präambel sowie Seitenlayout übernehmen.

Immer `\usepackage[ngerman]{babel}` und UTF-8-Eingabe verwenden.

**Wenn `ngerman.ldf` fehlt** (`kpsewhich ngerman.ldf` leer — so in der Linux-VM der
Desktop-App seit 13.11.2026, dort ohne Root-Rechte nicht nachinstallierbar): nicht ohne
babel ausliefern, sondern im Cloud-Workspace setzen — dort einmal je Sitzung
`apt-get update && apt-get install -y --no-install-recommends texlive-lang-german`,
Generator bzw. .tex dorthin übertragen, bauen und die PDFs zurückschreiben. Dezimaltrennzeichen
ist das **Komma**, nicht der Punkt — in Fließtext, Tabellen und Lösungen.

## Aufgaben rechnen lassen, nicht schätzen

**Jede** Zahl in einer Lösung wird programmatisch berechnet (Python), nie im Kopf
geschrieben. In den vorhandenen Kopfrechenblättern stehen nachweislich falsche
Lösungen (z. B. „4 x 8 = 48", „14 x 4 = 52") — genau das darf nicht passieren.

Vorgehen: Aufgaben und Lösungen in einem Python-Skript zusammen erzeugen, das
Ergebnis direkt aus der Rechnung übernehmen, und vor dem Setzen des Dokuments
alle Werte durch eine unabhängige Nachrechnung prüfen. Bei Textaufgaben die
Rechnung Schritt für Schritt hinschreiben und die Probe machen.

## Layout-Gewohnheiten

- Überschrift zentriert, mit klarem Abstand zur Namenszeile darunter
- Kopfzeile mit `Name: ______________________` und `Datum: TT.MM.JJJJ`
- Punktzahl pro Aufgabe in Klammern am rechten Rand
- Bei Klassenarbeiten: Punktetabelle am Ende, Notenschlüssel darunter
- Geometrische Abbildungen als PNG einbetten oder als GeoGebra-Datei danebenlegen

## Vertikaler Platz

Schülerinnen und Schüler schreiben **auf** das Blatt. Zu eng gesetzte Blätter sind
unbrauchbar, auch wenn sie ordentlich aussehen. Deshalb:

- Nach der Namenszeile mindestens **3 em** (LaTeX) bzw. **28 pt Absatzabstand**
  (Word) Abstand, bevor die erste Aufgabe kommt. Der Name wird handschriftlich
  eingetragen und braucht Höhe, nicht nur Linienlänge.
- Zwischen den Aufgaben mindestens **2,6 em** (LaTeX) bzw. **2,05 cm Zeilenhöhe**
  in Tabellen (Word). Bei Aufgaben mit Rechenweg deutlich mehr.
- Die Namenslinie mindestens 6 cm lang.

## Aufgabennummern

Nummerierung nur dort, wo sie gebraucht wird — bei Klassenarbeiten und
Arbeitsblättern, auf die sich Korrektur, Lösung oder Unterrichtsgespräch beziehen.

**Bei reinen Rechenblättern weglassen** (Kopfrechnen, Rechentraining,
Einmaleins-Blätter). Die Lernenden verwechseln die laufende Nummer sonst mit den
Zahlen der Aufgabe: `12) 3 x 4 =` wird als Rechnung mit der 12 gelesen. Auf
solchen Blättern stehen die Aufgaben ohne Nummer untereinander.

Lieber die Aufgabenzahl reduzieren als den Abstand. Ein Blatt mit 30 luftigen
Aufgaben ist besser als eines mit 40 gedrängten.

**Immer prüfen, dass das Ergebnis auf eine Seite passt** und keine Aufgabe
umbricht: PDF erzeugen, Seitenzahl prüfen, Blatt ansehen. Ein Umbruch mitten in
einer Aufgabe wird nicht ausgeliefert.

## Wohin nicht

Nichts mit Namen, Schülercodes und Punkten in `Arbeitsblätter/`, `Klassenarbeiten/`
oder `Tafelbilder/` — dafür gibt es `Kurse/<Kurs>/_intern/<Thema>/` und `Personenbezogenes/`.
Zwischenstände, Prüfbilder und Ausschnitte für Rückfragen entstehen im
Arbeitsverzeichnis außerhalb des Schulordners, nicht im Themenordner.
