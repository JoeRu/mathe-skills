---
name: korrektur
description: >
  Dieser Skill wird verwendet, wenn der Nutzer geschriebene Arbeiten korrigieren
  lassen möchte — etwa "korrigier die Arbeit von S11", "die Scans im Ordner
  Scan_Arbeit_2026-09-16 durchgehen", "Punkte für die Zuordnungen-Arbeit vergeben",
  "mach mir die Korrektur-PDF", "wie viele Punkte hat das Kind", "Stärken und
  Schwächen aus der Arbeit" oder "Punkte ins Schulportal übertragen". Liest die
  eingescannten Arbeiten seitenweise, vergibt Punkte nach dem Erwartungshorizont,
  legt unklare Handschrift zur Entscheidung vor und erzeugt eine kommentierte
  Korrektur-PDF mit Punktetabelle, Note und Kurzanalyse.
metadata:
  version: "0.8.0"
---

# Korrektur gescannter Arbeiten

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md`, `${CLAUDE_PLUGIN_ROOT}/references/notenschluessel.md` (Notenschlüssel,
Ordnerstruktur, Datenschutz) und `${CLAUDE_PLUGIN_ROOT}/references/dokumente.md`
(Rechenkontrolle) lesen.

## 0. Kurs und Arbeit bestimmen

Vor dem ersten Scan: **Kurs** nach `grundlagen.md` (*Kurswahl*) bestimmen und nennen. Der Kurs wird
nie aus dem Schülercode, dem Scanordner oder dem Material erschlossen — `S11` gibt es in jedem Kurs.
Dazu **Art und Termin** der Arbeit (`Arbeit`, `Wiederholung`, `Nachschreiben`, `Test`; Datum aus
`themenfolge.csv` bzw. dem Aufdruck der Arbeit). Daraus entstehen alle Pfade:

```
python3 $SKILLS/scripts/kurs.py pfad --kurs <Kurs> --thema <Thema> --art scan|korrektur \
    --arbeit <Art> --datum <JJJJ-MM-TT> [--version 2] --anlegen
```

Schreiben zwei Kurse dieselbe Arbeit (`kurs.py parallel`), werden Scans, Korrekturen und
Punktetabellen **je Kurs getrennt** abgelegt und korrigiert; eine gemeinsame Auswertung gibt es nur
auf ausdrücklichen Wunsch.

## Zweck und Grenze

Der Skill **liest, rechnet und legt vor**. Er setzt keine Note fest. Jede
Punktzahl ist ein Vorschlag, bis die Lehrkraft sie bestätigt hat — auch in der
fertigen PDF steht sie als Korrekturvorschlag.

Zwei Dinge werden **nie** geraten: was auf dem Blatt steht und wie viele Punkte
eine strittige Antwort wert ist. Beides wird vorgelegt.

## 1. Bewertungsform klären

**Vor dem ersten Punkt** fragen, wie bewertet werden soll — die Antwort bestimmt,
was in der Korrektur-PDF, in der CSV und später im Schulportal steht:

> Wie möchtest du bewerten — ganze Noten (1 bis 6) oder Noten mit Tendenz
> (2+, 3−)?

Ohne Antwort gilt: **ganze Noten**, und das wird im Chat gesagt.

### Tendenzen, wenn gewünscht

Analog zum Schulportal (`schulportal-leistung`, Notenskala „Noten mit
Tendenzen", **Tendenzbereich 33**): Das Punktintervall einer Note wird
gedrittelt.

- oberes Drittel → **+**
- mittleres Drittel → glatte Note
- unteres Drittel → **−**

Die Note 1 bekommt kein „+", die Note 6 weder „+" noch „−" — eine 6 bleibt eine
6. Die Intervallgrenzen sind die Schwellen des Schlüssel der Schules; die obere Grenze
der 1 ist die Gesamtpunktzahl. Die Drittelgrenzen werden **nicht** gerundet,
sondern exakt gerechnet und mit der erreichten Punktzahl verglichen.

Beispiel, 38 Punkte:

| Note | Intervall | − | glatt | + |
|---|---|---|---|---|
| 1 | ab 36 | 36–36,67 | ab 36,67 | – |
| 2 | 30–36 | 30–32 | 32–34 | 34–36 |
| 3 | 24,5–30 | 24,5–26,33 | 26,33–28,17 | 28,17–30 |
| 4 | 19–24,5 | 19–20,83 | 20,83–22,67 | 22,67–24,5 |
| 5 | 9,5–19 | 9,5–12,67 | 12,67–15,83 | 15,83–19 |
| 6 | unter 9,5 | – | – | – |

Die Tendenz wird **zusätzlich** zur Note geführt, nie an ihrer Stelle: In der CSV
stehen beide Spalten (`note`, `tendenz`), auf der Anhangseite steht „Note 2−",
und die Gesamtnote rechnet weiterhin `notenauswertung`. Die im Portal
errechneten Tendenzgrenzen werden gegengeprüft, bevor dort etwas gespeichert
wird.

## 2. Bestand aufnehmen

Scans liegen unter `Kurse/<Kurs>/_intern/<Thema>/Scan_<Arbeit>_<JJJJ-MM-TT>/`, eine PDF je
Arbeit (Pfad: `kurs.py pfad`, Abschnitt 0). Alles, was hier entsteht, bleibt in
`Kurse/<Kurs>/_intern/` — dort ist es per Muster von Git ausgeschlossen.

1. **Version bestimmen.** Der gedruckte Text hat einen OCR-Textlayer:
   `pdftotext -f 1 -l 1 "<scan>" -` zeigt „Arbeit Nr. 1: Zuordnungen (A)".
   Dieser Layer taugt **nur** für den Druck — für Handschrift ist er unbrauchbar
   und wird dafür nie verwendet.
2. **Lösungsschlüssel zur Version holen.** Er liegt in
   `<Themenordner>/Klassenarbeiten/`. `<Arbeit> - Lösung.docx` enthält alle
   Versionen. Die Nachschreibearbeit (Version N) hat andere Zahlen als A und B —
   vor dem ersten Punkt prüfen, dass Schlüssel und Scan dieselbe Version sind,
   und die Zuordnung im Chat benennen.
3. **Schülercode lesen.** Oben rechts steht handschriftlich der Code (`S11`).
   Über alle Seiten vergleichen; weichen sie ab oder ist der Code unlesbar, wird
   der Ausschnitt vorgelegt. Der Klarname auf dem Blatt wird nicht gelesen, nicht
   genannt, nicht gespeichert. Der Code wird gegen `Schuelerdaten/<Kurs>/kuerzel-map.csv`
   geprüft: Ein Code, den es in diesem Kurs nicht gibt, wird vorgelegt, nicht zugeordnet.
4. **Vollständigkeit prüfen.** Seitenzahl gegen die Sollseiten der Arbeit,
   Zusatzblätter den Aufgaben zuordnen, angeschnittene oder fehlende Seiten
   melden statt zu ergänzen.

## 3. Lesen

```bash
pdftoppm -r 300 -png "<scan>" seite
```

Je Teilaufgabe den zugehörigen Bereich ausschneiden und im **Bild** lesen — nie
aus dem Textlayer. Erfasst wird pro Teilaufgabe:

| Feld | Inhalt |
|---|---|
| `antwort` | was dort steht, wörtlich |
| `sicherheit` | `sicher` oder `unklar` |
| `beleg` | Seite und Bereich, damit der Ausschnitt reproduzierbar ist |

Durchgestrichenes gilt als nicht geschrieben — es sei denn, daneben steht nichts
Neues; dann ist die Stelle `unklar`. Nebenrechnungen auf Zusatzblättern gehören
zu der Aufgabe, auf die sie sich erkennbar beziehen, und entscheiden mit, ob ein
Rechenweg vorliegt.

**Rechenwege werden großzügig anerkannt.** Ist der Ansatz irgendwo auf dem
Blattstapel erkennbar — auch verdreht notiert, auch auf dem Zusatzblatt —, gilt
der Rechenweg als vorhanden und die Kürzung auf die halbe Punktzahl entfällt.
Jede so anerkannte Nebenrechnung wird im Korrektur-PDF auf dem Zusatzblatt
markiert („→ Nebenrechnung Aufgabe 3a, anerkannt"), damit die Zuordnung später
nachvollziehbar ist.

## 4. Punkte vergeben

Verbindlich sind der Erwartungshorizont **und** die Bewertungshinweise am Anfang
des Lösungsdokuments, in der Regel:

- Folgefehler nur einmal abziehen
- **Einheitenfehler kosten 0,5 Punkte** (Standard; abweichende Regel in `einstellungen.md`): falsche
  Einheit („3,5 Liter" statt „3,5 min"), fehlende Einheit, vertauschte Größe im
  Antwortsatz („18 Tage" statt „18 Wanderer") und fehlerhafte Umrechnung
  (g statt kg, ml statt l, verschobenes Komma beim Dividieren). Kein zusätzlicher
  Abzug, wenn das Ergebnis ohnehin schon wegen eines Rechenfehlers falsch ist —
  dann trägt der Rechenfehler den Abzug allein
- Ergebnis richtig ohne erkennbaren Rechenweg: höchstens die Hälfte der Punkte
- Antwortsatz nur, wo er ausgewiesen ist
- im Zweifel zugunsten des Kindes entscheiden, besonders beim Anerkennen von
  Rechenwegen

Die Punkte kommen in eine Tabelle je Teilaufgabe und werden **programmatisch**
summiert (siehe `dokumente.md`). Solange etwas offen ist, werden **zwei** Summen
geführt: die sichere und die maximal erreichbare. Die Note wird erst nach der
letzten Entscheidung gebildet, mit `python3 $SKILLS/scripts/noten.py note <gesamt> <punkte> [--tendenz]`
— Prozentgrenzen auf halbe Punkte abgerundet, Tendenz nur wenn in Abschnitt 1
vereinbart. Nie eigene Grenzen rechnen.

## 5. Vorlegen — die Kernregel

Vorgelegt wird **jede Stelle, an der die Lesart über Punkte entscheidet**:

- der Bildausschnitt (ohne Namenszeile), so groß, dass der Kontext erkennbar ist
- die Lesarten, die in Frage kommen
- die Punktfolge je Lesart („0,75 → 1 P, 0,5 → 0 P")

Ist die Lesart eindeutig und nur die Bewertung strittig (Begründungen,
Teilpunkte), wird **nicht** blockiert: Der Skill schlägt eine Punktzahl vor,
markiert sie als Ermessen und nennt die Alternative. Alle offenen Stellen kommen
gebündelt, nicht einzeln nacheinander.

Formulierungen wie „vermutlich", „wahrscheinlich 3" oder „unleserlich, daher
0 Punkte" sind nicht zulässig.

## 6. Die Korrektur-PDF

Der Originalscan bleibt unverändert; die Anmerkungen liegen als Overlay darüber
(`reportlab` erzeugt die Ebene, `pypdf` legt sie auf die Scanseite). Die
Ankerpunkte für die Randkästchen kommen aus dem gedruckten Textlayer:
`pdftotext -bbox` liefert die Position von „/ 12", „/ 6", „/ 4" und der
Punktangaben — geraten wird nicht.

- **Punkte in die vorgedruckten Randkästchen** (`____ / 12`), rot
- **Zeichen neben jeder Teilaufgabe**, damit die Durchsicht schnell geht: grüner
  Haken bei voller Punktzahl, roter Haken mit Querstrich bei Teilpunkten, rotes
  Kreuz bei null. Daneben die vergebenen Punkte.
- **Die Ankerpunkte kommen von den Aufgabennummern** (`1.` bis `6.` am linken
  Rand) und den Teilaufgabenbuchstaben (`a)` bis `d)`), nicht von den gedruckten
  Punktangaben `(3 P)`: die erkennt die Texterkennung auf vielen Seiten nicht,
  und dann fehlen dort sämtliche Anmerkungen. Was auf einem Blatt nicht gefunden
  wird, kommt aus einem Layoutmodell — dem Median der Abstände über alle Arbeiten
  desselben Aufgabensatzes. Nach dem Lauf prüfen: steht auf **jeder** Seite zu
  **jeder** Teilaufgabe ein Zeichen?
- **Kurznotiz am Rand**, wo der Fehler benennbar ist („Einheit min, nicht Liter",
  „Grundgebühr fehlt"). Sachlich, an die Sache gerichtet, nie an die Person.
- Nichts über die Schülerschrift legen; freier Rand hat Vorrang

### Fünf Layoutregeln, die schon einmal schiefgegangen sind

1. **Jeder Text wird umgebrochen.** Kein `drawString` ohne vorherige Messung mit
   `stringWidth`: der rechte Rand des Scans ist bei x ≈ 476 zu Ende, es bleiben
   rund 126 pt, das sind drei bis vier Zeilen à 9 pt Zeilenabstand. Dasselbe gilt
   für die Spalte *Anmerkung* der Auswertungsseite (rund 288 pt) — dort wächst
   die Zeilenhöhe mit der Zahl der Zeilen.
2. **Gekürzt wird nur am Scanrand.** Die Randnotiz auf dem Scan hat physisch
   wenig Platz; dort darf ein Kommentar nach drei bis vier Zeilen enden, sichtbar
   mit „…". **Überall sonst wird nichts gekürzt** — nicht auf der Anhangseite,
   nicht in der CSV. Eine harte Zeichengrenze (`text[:120]`) beim Schreiben der
   Tabelle hat schon einmal jeden zweiten Kommentar mitten im Satz abgeschnitten
   („… multipliziert statt dividiert: 45 : 6"), ohne dass man es der Datei ansah.
   Wenn ein Kommentar für die Randnotiz zu lang ist, gehört er trotzdem
   ungekürzt in CSV und Anhangseite.
3. **Haken und Kreuze werden gezeichnet, nicht gesetzt.** Die Schriftart
   ZapfDingbats steht in der PDF-Ausgabe nicht zuverlässig zur Verfügung und
   erscheint als schwarze Kästchen. Zwei bzw. drei Linien mit `canvas.line`.
4. **Keine Gedankenstriche in Kommentaren.** Ein Strich zwischen zwei Satzteilen
   liest sich im Korrekturtext wie ein Minuszeichen. Stattdessen Doppelpunkt,
   oder Komma, wenn der Satz schon einen Doppelpunkt enthält.
5. **Deutsch mit Umlauten, Mathematik mit Malpunkt.** Kein `ae/oe/ue/ss` als
   Ersatzschreibung in Kommentaren, Stärken und Schwächen; Multiplikation als
   `·`, nicht als `*` oder `x`. Werden Kommentare maschinell nachbearbeitet,
   niemals über die rohe JSON-Datei ersetzen — die Schlüssel und Teilaufgaben-IDs
   werden sonst mitverändert.
### Die Anhangseite ist keine Seite

Sie wird als **Folge** von Seiten gebaut, nicht als eine. Reportlab zeichnet
klaglos unter den unteren Rand weiter — sichtbar wird der Verlust erst im
fertigen PDF, wo die Liste „Daran musst du noch arbeiten" mitten im Satz endet
oder ganz fehlt. Deshalb:

- Vor **jedem** Block prüfen, ob die benötigte Höhe noch bis rund 60 pt über dem
  Seitenende passt; sonst `showPage()` und auf der neuen Seite weiter.
- Die neue Seite bekommt Kopfzeile und Schülercode wieder, mit dem Zusatz
  „(Fortsetzung)", und bei einer laufenden Tabelle auch die Spaltenüberschriften.
- Eine Überschrift steht **nie allein** am Seitenende: „Das kannst du schon" und
  „Daran musst du noch arbeiten" brauchen zusammen mit ihrem ersten Eintrag
  Platz, sonst wandern sie gemeinsam auf die nächste Seite.
- Am Ende werden **alle** Seiten des Puffers angehängt (`for seite in
  PdfReader(buf).pages`), nicht nur `pages[0]` — sonst verschwindet die
  Fortsetzung wieder.
- Die Zeilenhöhe einer Tabellenzeile richtet sich nach der Zahl der
  umgebrochenen Kommentarzeilen, nicht nach einem festen Wert.

Zwei Auswertungsseiten sind in Ordnung. Ein abgeschnittener Satz ist es nicht.

- **Zusatzblätter** bekommen je Block eine Zuordnungsnotiz („→ Fortsetzung
  Aufgabe 2", „→ Nebenrechnung Aufgabe 3a, anerkannt")
- **Anhangseite** am Ende: Punktetabelle je Teilaufgabe, Summe, Prozent, Note
  (mit Tendenz, wenn so vereinbart), Notenspiegel der Arbeit und der Abstand zur
  nächstbesseren Note; darunter **Stärken und Schwächen** in drei bis fünf
  Sätzen, ausschließlich aus den Teilaufgaben abgeleitet („Wertetabellen
  antiproportional sicher, proportional unsicher"), keine Sätze über Charakter,
  Fleiß oder Begabung.

**Solange die Lehrkraft die Korrektur nicht durchgesehen hat**, tragen die Blätter in
der Fußzeile „Korrekturvorschlag, zu prüfen von <Kürzel aus einstellungen.md>" und offene Lesarten ein
Sternchen. **Nach der Freigabe** wird beides entfernt und die Fußzeile lautet
`Korrektur <Kürzel> · TT.MM.JJJJ · <Kurzname>/<Code> · Version <A/B>`. Die freigegebene
Fassung kommt in einen eigenen Ordner (`Korrektur_<Arbeit>_<JJJJ-MM-TT>_v2`, `_v3`, …), damit ein
laufender Durchgang nicht unter den Händen wegbricht. `_vN` bedeutet nur das; eine weitere Arbeit
bekommt ihren eigenen Termin im Ordnernamen.

Ablage, ohne den Scanordner zu verändern:

```
Kurse/<Kurs>/_intern/<Thema>/Korrektur_<Arbeit>_<JJJJ-MM-TT>/<Code>_<Version>_korrigiert.pdf
```

Bestehende Dateien nie überschreiben — neue Version mit Datum daneben.

## 7. Nebenprodukte

- `Kurse/<Kurs>/_intern/<Thema>/Korrektur_<Arbeit>_<JJJJ-MM-TT>/punkte_<arbeit>.csv` — eine Zeile
  je Code × Teilaufgabe, **erste Spalte `kurs`** (damit die Tabelle auch außerhalb ihres Ordners
  eindeutig bleibt), mit Punkten, Maximum, Status (`ok`, `falsch`, `ermessen`) und dem
  **vollständigen** Kommentar, dazu die Summenzeile mit Prozent, Notenvorschlag
  und — wenn so vereinbart — der Tendenz. Das ist die Eingabe für
  `notenauswertung`. In dieser Datei wird kein Text gekürzt: Sie ist der Ort, an
  dem die Begründung nachlesbar sein muss.
- **Gesamtleistung je Kind**: an `notenauswertung` übergeben (50 % mündlich,
  50 % schriftlich) — dieser Skill rechnet die Arbeit, nicht das Zeugnis.
- **Schulportal**: Übergabe an `schulportal-leistung` — dort stehen der Weg
  (Mein Unterricht → Leistungen → + Leistung), die Feldbelegung, die
  Punkteverteilung je Aufgabe und die Berechnungsfaktoren. Geschrieben wird nur
  nach ausdrücklichem „passt"; die Zuordnung Code → Name passiert im Browser.
- Sind mehrere Arbeiten korrigiert: **Fehlerübersicht je Teilaufgabe** über den
  **Kurs** (kursübergreifend nur auf Wunsch) — Grundlage für die Rückgabestunde.

## 8. Gegenprüfung vor der Abgabe

1. Summe der Teilpunkte unabhängig nachrechnen, gegen die Maximalpunktzahl prüfen
2. Note mit `noten.py` gegenprüfen und nennen, wie viele Punkte zur nächsten
   Note fehlen
3. Die erzeugte PDF ansehen: sitzen die Anmerkungen an der richtigen Stelle,
   verdecken sie nichts, und ist die **letzte** Seite vollständig — Stärken,
   Schwächen und Quellenangabe bis zum Schlusspunkt sichtbar?
4. Die CSV stichprobenartig öffnen: endet jeder Kommentar mit einem Satzzeichen
   oder zumindest mit einem vollständigen Wort? Ein „…" darf dort nicht stehen,
   außer es gehört zur Zahl (1,33…).
5. Zwei Teilaufgaben blind neu lesen und mit der Tabelle vergleichen

## Datenschutz

Die Scans enthalten Klarnamen. Es gilt `grundlagen.md`, zusätzlich:

- In den Cloud-Workspace kommt nur, was zum Lesen nötig ist; Ausschnitte für
  Rückfragen werden so geschnitten, dass die Namenszeile nicht mitkommt.
- Im Chat, in CSV und in Dateinamen steht der Code, nie der Name.
- Korrektur-PDFs und Punktetabellen kommen nicht ins Repository und nicht in
  Artefakte.

## Übergaben

| Bedarf | Skill |
|---|---|
| Noten, Notenspiegel, Zeugnisnote | `notenauswertung` |
| Punkte ins Schulportal eintragen | `schulportal-leistung` |
| Auffälligkeiten zu einem Kind festhalten | `schuelerdaten` |
| Brief an die Eltern nach schwacher Arbeit | `elternbrief` |
| Übungsmaterial zu den Schwächen | `arbeitsblatt`, `bettermarks` |
| Rückgabestunde planen | `wochenplanung` |
