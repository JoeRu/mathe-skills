# bettermarks — Plattform, Wege, Tücken

Aufgezeichnet ab 09.09.2026 in einer echten 7. Klasse und einer Testklasse
(Namen je Kurs in `kurs.md`). Was hier steht, wurde gesehen — nicht angenommen.
Was nicht geprüft ist, steht unter *Ungeprüft*.

## Zugang

Anmeldung über das **Schulportal Hessen** (Single Sign-on):

1. `https://start.schulportal.hessen.de` — **die Anmeldung macht der Nutzer
   selbst.** Zugangsdaten werden nie eingegeben und nie gespeichert.
2. Startseite → Kachel **bettermarks** (erste Kachel oben links)
3. Landet auf `https://apps.bettermarks.com/one/content/curricular/maths`

Die Sitzung hält über den Schulportal-Login. Ist sie abgelaufen, wird der
Nutzer gebeten, sich neu anzumelden, und gewartet.

**Freigabe im Browser-Panel:** `apps.bettermarks.com` wird pro Seitenaufruf
freigegeben. Jede `navigate`-Aktion braucht vorher ein `request_access`.
Klicks *innerhalb* der geöffneten Seite brauchen keine neue Freigabe — deshalb
lieber in der App navigieren (Seitenleiste, Reiter) als URLs anzuspringen.

## Klassen

| Klasse | Was sie ist |
|---|---|
| `bettermarks_klasse` aus `kurs.md` | die echte Lerngruppe |
| `bettermarks_testklasse` aus `kurs.md` | eine Klasse mit 1 Konto — **hier wird ausprobiert** |

Umgeschaltet wird über das Auswahlfeld **oben links in der Seitenleiste**.
Die Auswahl gilt **global** für Inhalte *und* Auswertung und bleibt bestehen,
bis sie geändert wird.

Lernende erscheinen in bettermarks nur als **vierstelliges Kürzel** (erfunden:
`MaMu`), Nachname leer. Die Zuordnung zu Klarnamen steht in den Listen im
Schulordner (`Schuelerdaten/<Kurs>/kuerzel-map.csv`), nicht hier. Kürzel bleiben trotzdem personenbezogen:
nicht ins Repository, nicht ins Memory, im Chat nur so weit wie nötig.

## Aufbau der Oberfläche

Seitenleiste (klappt unter etwa 1024 px Breite zum ☰-Menü zusammen):

| Eintrag | URL | Wofür |
|---|---|---|
| **To-dos & Ergebnisse** | `/one/tasks/maths/current` | Auswertung |
| **Mathematik** | `/one/content/curricular/maths` | Inhalte |
| **Lesezeichen** | `/one/learning-units` | gemerkte Lernpfade, eigene Arbeitsblätter |
| Übungscode | — | Startcode einer geschützten Aufgabe eingeben |
| Klassendetails | `/one/classes` | Klassenliste, Zugänge, Lizenzstatus |

## Inhalte

### Vier Einstiege

`/one/content/curricular/maths` mit den Reitern

- **Nach Klassenstufen** — Klasse 3-4, 5-6, 7-8, 9-10, 11-13, je Stufe die
  Themenbücher (`/one/content/curricular/maths`)
- **Nach Themen** — `/one/content/topic/maths`
- **Training** — `/one/content/training/maths`
- **Lernstandserhebungen** — `/one/content/diagnostic/maths`

Suchfeld **„Material durchsuchen …"** rechts oben. Es durchsucht die ganze
Bibliothek (Stand 09.09.2026: 502 Tafelbilder, 2937 Übungen, 327 Lernpfade)
und filtert nach dem gerade aktiven Reiter.

### Ein Themenbuch

`/one/content/curricular/maths/<Buch-ID>` mit drei Reitern, die sich auch
direkt ansteuern lassen:

```
…/<Buch-ID>?filterBy=Presentation   → Tafelbilder
…/<Buch-ID>?filterBy=Practice       → Übungen (nach Lernheften gruppiert)
…/<Buch-ID>?filterBy=LearningUnit   → Lernpfade
```

Eine einzelne Aufgabe adressiert sich als
`…/<Buch-ID>/<Lernheft-ID>#<Aufgaben-ID>`, z. B.
`…/bm_MathDE_78_Relations_de/21ab85#UV7E`.

**Bestätigte Buch-IDs (Klasse 7-8):**

| Thema | Buch-ID |
|---|---|
| Zuordnungen | `bm_MathDE_78_Relations_de` |
| Winkelbeziehungen | `bm_MathDE_78_AngRel_de` |
| Prozentrechnung | `bm_MathDE_78_Percentage_Interest_de` |
| Geometrische Konstruktionen | `bm_MathDE_78_GeoConst_de` |
| Terme und lineare Gleichungen | `bm_MathDE_78_Equations_de` |
| Zufall und Wahrscheinlichkeit | `bm_MathDE_78_ChanceProb_de` |
| Rechnen mit Termen | `bm_MathDE_78_Terms_de` |
| Flächeninhalte | `bm_MathDE_78_Areas_de` |
| Mehrstufige Zufallsexperimente | `bm_MathDE_78_ProbTrees_de` |
| Lineare Funktionen | `bm_MathDE_78_Functions_de` |
| Lineare Gleichungssysteme | `LMO_bm78_Linear_Equations_System_de` |
| Ähnlichkeit | `bm_MathDE_78_Similarity_de` |
| *(Klasse 5-6)* Anteile, Brüche und Prozent | `bm_MathDE_56_BRGL_de` |

Alle Buch-IDs der Stufe 7-8 am 19.10.2026 abgelesen. **Neu abgelesene IDs hier eintragen.**

### Inhaltsarten

Jeder Inhalt trägt eine **vierstellige ID** (`TF4B`, `3CXC`, `M1RE`) — sie ist
der kürzeste Weg, ihn wiederzufinden, und gehört in jede Empfehlung.

| Art | Wofür | Austeilbar |
|---|---|---|
| **Tafelbild** | interaktiv, für Einstieg und Erarbeitung an der Tafel | nein — wird *präsentiert* |
| **Wissenskasten** | Zusammenfassung zur Sicherung | nein |
| **Beispiel** | durchgerechnete Musteraufgabe | nein |
| **Übung** | Aufgabenpaket zum Üben | ja |
| **Test** | Aufgabenpaket zur Leistungsfeststellung | ja |
| **Lernpfad** | fertige Stundenfolge aus allem oben | Bestandteile einzeln |

### Übungen, Lernhefte, Schwierigkeitsgrad

Im Reiter *Übungen* sind die Aufgaben nach **Lernheften** gruppiert
(bei Zuordnungen: Vorwissen aktivieren · Einführung zu Zuordnungen · Graphen
von Zuordnungen · Einführung zu proportionalen Zuordnungen · Dreisatz für
proportionale Zuordnungen · Einführung zu antiproportionalen Zuordnungen ·
Dreisatz für antiproportionale Zuordnungen · Überprüfen).

Ein Lernheft aufklappen zeigt seine Übungen; eine Übung aufklappen zeigt

- **Umfang**: „5 Aufgaben · 9 Minuten"
- **Schwierigkeitsgrad**: **Standard / Einfach / Schwierig** — die
  Differenzierungsstellschraube. *Einfach* ≈ C-Kurs, *Standard* ≈ B-Kurs,
  *Schwierig* ≈ A-Kurs. Das ist eine Einschätzung, keine Zusicherung der
  Plattform; vor dem Austeilen eines abweichenden Grades die Vorschau ansehen.
- **Stift-Symbol** — eigene Auswahl einzelner Aufgaben; gespeichert landet sie
  unter *Lesezeichen → Arbeitsblätter* und ist dort als Test oder Übung
  austeilbar
- **Aufgabenpaket ansehen** — Vorschau
- Miniaturbilder der einzelnen Aufgaben

### Lernpfade

Ein Lernpfad ist eine fertige Stundenfolge („17 Materialien für 3
Unterrichtsstunden") mit Reitern **Überblick** und **Auswerten**.

Der Überblick nennt *Inhalt und Ziele*, *Neue Begriffe* und gliedert sich in
die Phasen:

1. **Vorwissen aktivieren**
2. **Tafelbilder zum Einsteigen und Erarbeiten**
3. **Tafelbilder zum Sichern** — Wissenskästen und Beispiele
4. **Üben** — Basisaufgaben, dann Weitere Aufgaben
5. **Überprüfen** — Test

Diese Phasenfolge deckt sich mit *Einstieg → Erarbeitung → Sicherung* der
Wochenplanung und ist deshalb die beste Vorlage für einen Stundenablauf.

**Als Lesezeichen merken** legt den Lernpfad für die Klasse ab
(`/one/learning-units`).

## Auswertung

`/one/tasks/maths/current`. Kopfzeile: **To-dos & Ergebnisse für
[Klasse] [Ganze Klasse ⌄]**. Der zweite Filter schaltet auf ein einzelnes
Kürzel um.

Reiter: **Aktuell** (laufende Fristen) · **Zurückliegend** (abgelaufene) ·
**Geplant** (noch nicht gestartete) · **Aktivitäten** (Verlauf, nur mit
ausgewähltem Kind).

### Die vier Kacheln

| Kachel | Inhalt |
|---|---|
| **Wissenslücken** | offene, von bettermarks erkannte Lücken. Klick öffnet *Offene Wissenslücken* mit den Reitern *Nach Wissenslücken* und *Nach Schüler:innen*. **Nicht löschen** — die Schaltfläche „Ausgewählte löschen" bleibt unberührt. |
| **Sterne** | Durchschnittliche Sterne je Kind |
| **Top 5 fehlerhafte Aufgaben** | die fünf am schlechtesten gelösten Einzelaufgaben mit Vorschaubild, Ø-Ergebnis und Anzahl der Bearbeitenden. Zeitfilter: Letzte 14 Tage · Letzte 7 Tage · Zu gestern · Zu heute · **In der Zukunft** |
| **Auswertung herunterladen** | Excel-Datei mit allen Prozentwerten (siehe unten) |

### Die To-do-Liste

Gruppiert nach Frist („in 6 Tagen · 15.09.26, 23:45"). Je Zeile: Titel, Art
(*Übung* / *Test*), Herkunft („aus <Lernheft>"), **bearbeitet N/21** und ein
Ampelbalken (rot / gelb / grün / grau = noch nicht bearbeitet).

Der Schalter **„Nur offene anzeigen"** blendet erledigte To-dos aus.

### Das ⋮-Menü einer Zeile

Zeigt oben das Bearbeitungsfenster (`08.09.26, 15:30 – 15.09.26, 23:45`) und

- **Details anzeigen** — klappt die Schülermatrix auf (siehe unten)
- **Ergebnisse anonymisieren** — Schalter
- **Datum ändern**
- **To-do beenden** (sobald Ergebnisse vorliegen) bzw.
  **To-do löschen** (solange niemand bearbeitet hat)

### Die Schülermatrix

Zeilen = Kürzel mit Gesamtprozent, Spalten = die einzelnen Aufgaben (1, 2, 3 …),
Zellen ampelfarben. Ein Kreispfeil mit Zahl hinter dem Kürzel heißt
**Wiederholungen** (`↻ 2`).

Sortierung über das Auswahlfeld links oben:
**Klassenliste** · **Erfolgreichste zuerst** · **Weniger Erfolgreiche zuerst**.

Legende: *Richtig* · *Teilweise richtig* · *Falsch* · *Keine Ergebnisse* ·
*Verspätete Abgabe*.

### Kompetenzfortschritt

Im Lernpfad, Reiter **Auswerten**: je Lernziel ein Balken von 0 % bis 100 %
mit Marken bei **60 %** und **90 %** und einem Punkt für die Klasse.
Die Marken sind bettermarks-Schwellen, **kein Notenschlüssel der Schule** — die
beiden nie gleichsetzen.

## Die Auswertungsdatei — der eigentliche Rechenweg

Die Kachel **Auswertung herunterladen** liefert eine `.xlsx` mit dem Namen

```
Klassenaktivität <Klasse> (<TT.MM.JJ> - <TT.MM.JJ>).xlsx
```

Der Zeitraum ist der Auswertungszeitraum, nicht das Erstelldatum. Die Datei
landet im Downloads-Ordner und wird von der Lehrkraft nach `Kurse/<Kurs>/_intern/<Thema>/bettermarks/` gelegt (git-ignoriert; ältere Exporte liegen in `_Eingang/`).

**Das ist die Quelle für jede Zahl.** Prozentwerte vom Bildschirm abzulesen
ist der Notweg, wenn keine Datei vorliegt.

### Blatt „Aktivitäten"

Zeile 1 der Titel, Zeile 2 `Aktivitäten`, danach **ein Block je Lernheft**,
durch Leerzeilen getrennt:

```
A: <Name des Lernhefts>
A:            C:            D..X: <Kürzel der Lernenden, alphabetisch>
A: Übung(en)  C: Übungscode
A: <Titel der Übung>   C: <ID>   D..X: <Prozentwert oder leer>
```

- Spalte **C** ist der **Übungscode** — dieselbe vierstellige ID wie in der
  Oberfläche und in der URL (`…#5R4B`). Über sie findet sich der Inhalt wieder,
  und über das Feld *Übungscode* in der Seitenleiste lässt er sich starten.
- Spalten ab **D** tragen die Kürzel in der Kopfzeile **jedes Blocks** — die
  Reihenfolge ist alphabetisch und wiederholt sich, trotzdem immer die Kopfzeile
  des jeweiligen Blocks lesen statt eine Reihenfolge anzunehmen.
- **Eine leere Zelle heißt zweierlei: „nicht bearbeitet" *oder* „0 %".**
  Nachgeprüft am 09.09.2026: die Datei exportiert ein Ergebnis von 0 % als
  leere Zelle. Bei `3M2C` zeigte der Bildschirm 18 Bearbeitende, davon drei
  mit 0 %; die Datei enthielt 15 Werte. Wer die Leeren einfach weglässt,
  rechnet den Schnitt zu gut (44,7 % statt 37,2 %).

  **Vorgehen:** die Zahl der Bearbeitenden (`N/21`) vom Bildschirm nehmen —
  Übersichtsliste oder Detailmatrix, dort steht 0 % ausgeschrieben. Die
  Differenz zwischen dieser Zahl und den Werten in der Datei sind
  Nullergebnisse und gehören mit 0 in den Schnitt. Ist der Bildschirmwert
  nicht verfügbar, wird der Schnitt **als Obergrenze** ausgewiesen und
  dazugesagt, dass Nullergebnisse fehlen könnten.
- Werte sind Fließkommazahlen (`94.44444…`). Zum Anzeigen auf ganze Prozent
  runden, zum Rechnen den Rohwert nehmen.
- Die Datei enthält **alle Aktivitäten des Zeitraums**, auch selbst gewählte
  Inhalte und Wissenslücken-Aufgaben außerhalb der ausgeteilten To-dos
  (erkennbar an Blöcken, die zu keinem To-do gehören).

### Blatt „Schülerinnen und Schüler"

Spalten `Kürzel`, `Vorname`, `Nachname`, `Zugangsname`. Der `Zugangsname` ist
eine UUID — ein Zugangsmerkmal. **Nie in eine Antwort, ein Dokument oder ein
Repository übernehmen.**

### Auswerten

Mit `openpyxl` auf dem Gerät des Nutzers lesen, nicht in die Cloud kopieren.
Blockweise parsen: Lernheft → Übungen → Kürzel → Wert. Daraus rechnen:

- Mittelwert und Median je Übung — über die Werte in der Datei **plus die
  Nullergebnisse**, die sich aus der Differenz zum Bildschirmwert ergeben
- Bearbeitungsquote je Übung (bearbeitet / Klassengröße), vom Bildschirm
- je Kind: Schnitt über die bearbeiteten Übungen, Zahl der offenen
- die Übungen unter 50 % Schnitt — das sind die Themen für die nächste Stunde
- die Kinder, die bei einem Thema deutlich unter ihrem eigenen Schnitt liegen

## Austeilen

1. In der Inhaltsansicht **Häkchen** vor den gewünschten Übungen oder Tests
   setzen. Ein Häkchen am Lernheft nimmt das ganze Heft.
2. Oben erscheint eine Leiste: *Anzahl · geschätzte Minuten · Zielklasse ·
   Frist*, mit **⚙** und **Austeilen**.
3. **⚙** öffnet das Panel *To-dos*:
   - **Austeilen an**: Klasse, darunter Empfänger — *Gesamte Klasse* oder
     einzelne Kürzel (mehrere möglich)
   - **Bearbeitungszeit festlegen**: `Heute` · `4 Tage` · `7 Tage` ·
     Kalender-Symbol für ein eigenes Fenster; darunter steht das Fenster im
     Klartext
   - **Weitere Einstellungen**:
     - *Werte für alle gleich* — ohne diesen Haken bekommt **jedes Kind eigene
       Zahlen**. Für gemeinsames Besprechen an der Tafel oder für eine
       Partnerkontrolle muss er gesetzt sein.
     - nur für Testmaterial: *Ergebnisanzeige deaktivieren*, *Wiederholen
       verbieten*, *Mit Startcode schützen*
   - Liste der gewählten Inhalte mit Papierkorb je Zeile
   - Fuß: „N Inhalte · Bearbeitungszeit gesamt: ca. M Minuten",
     **Verwerfen** / **Austeilen**
4. **Austeilen** → Bestätigung „Austeilen erfolgreich!" mit *Erneut austeilen*,
   *OK* und dem Link *To-dos ansehen*.

## Gesehene Übungscodes — Zuordnungen (`bm_MathDE_78_Relations_de`)

Stand 14.09.2026, alle in einer 7. Klasse (B-Kurs) ausgeteilt und ausgewertet.

| Code | Übung | Lernheft |
|---|---|---|
| `5R4B` | Zuordnungen und Wertepaare formell darstellen | Einführung zu Zuordnungen |
| `YLXD` | Liniendiagramme erstellen | Graphen von Zuordnungen |
| `UV7E` | Proportionale Zuordnungen grafisch darstellen | Einführung zu proportionalen Z. |
| `3M2C` | Proportionalität in Wertetabellen überprüfen, Proportionalitätsfaktor | Einführung zu proportionalen Z. |
| `AB5B` | Proportionale Zuordnungen erkennen | Einführung zu proportionalen Z. |
| `W7QP` | Proportionale Zuordnungen in Sachaufgaben anwenden | Einführung zu proportionalen Z. |
| `P49B` | Proportionalitätsfaktor zu Wertepaaren bestimmen | Einführung zu proportionalen Z. |
| `53VC` | Wertetabellen anhand proportionaler Zuordnungsvorschrift vervollständigen | Einführung zu proportionalen Z. |
| `3CXC` | Dreisatztabellen proportionaler Zuordnungen aufstellen | Dreisatz für proportionale Z. |
| `M1RE` | Mit dem Dreisatz Werte in Sachkontexten berechnen | Dreisatz für proportionale Z. |
| `V4AA` | Proportionalität überprüfen und Dreisatz berechnen | Dreisatz für proportionale Z. |
| `EYXQJ` | **Test** Werte proportionaler Zuordnungen mit dem Dreisatz berechnen | Dreisatz für proportionale Z. |
| `X7QR` | Antiproportionale Zuordnungen erkennen | Einführung zu antiproportionalen Z. |
| `R7QP` | Graphen antiproportionaler Zuordnungen erkennen | Einführung zu antiproportionalen Z. |
| `P22A` | Wertetabellen antiproportionaler Zuordnungen vervollständigen | Einführung zu antiproportionalen Z. |
| `CXTB` | Werte antiproportionaler Zuordnungen in Sachkontexten bestimmen | Einführung zu antiproportionalen Z. |
| `61R1A` | **Test** Mit antiproportionalen Zuordnungen umgehen | Einführung zu antiproportionalen Z. |
| `V66A` | Dreisatztabellen antiproportionaler Zuordnungen aufstellen | Dreisatz für antiproportionale Z. |
| `XQTE` | Zuordnungen mithilfe des Dreisatzes auf Antiproportionalität prüfen | Dreisatz für antiproportionale Z. |

### Ergänzung 24.09.2026 — vollständige Übungsliste und Bearbeitungsstand

Alle acht Lernhefte aufgeklappt und abgelesen (53 Übungen). Zahlen = bearbeitet
von 22. Fehlt die Zahl, hat der Kurs die Übung noch nie bekommen.

| Lernheft | Code | Übung | bearbeitet |
|---|---|---|---|
| Graphen von Zuordnungen | `V8BC` | Skizzierte Graphen im Sachkontext interpretieren | — |
| | `P2UD` | Liniendiagramme im Sachkontext interpretieren | — |
| | `YLXD` | Liniendiagramme erstellen | 21/22 |
| | `CRJC` | Daten aus Tabellen grafisch darstellen, Achsen skalieren | — |
| | `1TXC` | Diagramme zuordnen | — |
| | `FGAE` | Weg-Zeit-Diagramme erstellen | — |
| | `A7QC` | Weg-Zeit-Diagramme interpretieren | — |
| Einführung prop. | `UV7E` | Proportionale Zuordnungen grafisch darstellen | 21/22 |
| | `3M2C` | Proportionalität in Wertetabellen überprüfen, Faktor bestimmen | 20/22 |
| | `P49B` | Proportionalitätsfaktor zu Wertepaaren bestimmen | 1/22 |
| | `53VC` | Wertetabellen anhand prop. Zuordnungsvorschrift vervollständigen | 1/22 |
| | `AB5B` | Proportionale Zuordnungen erkennen | 19/22 |
| | `W7QP` | Proportionale Zuordnungen in Sachaufgaben anwenden | 20/22 |
| | `QR7E` | Proportionalitätsfaktor bestimmen und anwenden | — |
| Dreisatz prop. | `3CXC` | Dreisatztabellen prop. Zuordnungen aufstellen | 17/22 |
| | `V4AA` | Proportionalität überprüfen und Dreisatz berechnen | 1/22 |
| | `M1RE` | Mit dem Dreisatz Werte in Sachkontexten berechnen | 17/22 |
| | `F26C` | Ausgangswert bestimmen und Zweisatz anwenden | — |
| | `X4YB` | **Wählen geeigneter Zwischenwerte bei der Dreisatzberechnung** | — |
| | `B48C` | Proportionale Zuordnungen in Sachaufgaben anwenden | — |
| | `36AD` | Anwenden des doppelten Dreisatzes | — |
| Einführung antiprop. | `X7QR` | Antiproportionale Zuordnungen erkennen | 4/22 |
| | `R7QP` | Graphen antiproportionaler Zuordnungen erkennen | 3/22 |
| | `YGWD` | Antiprop. Zuordnungen erkennen und ihre Konstanten bestimmen | — |
| | `P22A` | Wertetabellen antiprop. Zuordnungen vervollständigen | 2/22 |
| | `CXTB` | Werte antiprop. Zuordnungen in Sachkontexten bestimmen | 1/22 |
| | `X7BY` | **Proportionale und antiproportionale Zuordnungen unterscheiden** | — |
| | `W9QP` | Prop. und antiprop. Zuordnungen in Sachaufgaben anwenden | — |
| Dreisatz antiprop. | `V66A` | Dreisatztabellen antiprop. Zuordnungen aufstellen | 17/22 |
| | `XQTE` | Zuordnungen mithilfe des Dreisatzes auf Antiproportionalität prüfen | 17/22 |
| | `9DVE` | Mit dem Dreisatz Werte in antiprop. Sachkontexten berechnen | — |
| | `PRCD` | Sachaufgaben zu antiprop. Zuordnungen schrittweise lösen | — |
| | `LRME` | Sachaufgaben zu komplexen antiprop. Zuordnungen lösen | — |
| | `TY1A` | Sachaufgaben zu veränderten antiprop. Zuordnungen lösen | — |
| | `PJUA` | Dreisatz bei prop. und antiprop. Zuordnungen anwenden | — |
| | `BXGA` | Prop. und antiprop. Zuordnungen in einem Sachzusammenhang anwenden | — |

**Der ganze antiproportionale Teil ist praktisch unbearbeitet** (höchstens 4 von
22) — während der proportionale Teil bei 17 bis 21 liegt. Das deckt sich mit dem
Befund der ersten Arbeit.

Zwei Übungen am 24.09.2026 in der Vorschau angesehen:

- **`X4YB`** (3 Aufgaben, 7 min 40 s) — die Dreisatztabelle hat eine eigene
  **Zwischenzeile**; Aufgabe 1 rechnet von 10 Personen über den Zwischenwert auf
  6 Personen. Das ist die einzige Übung des Kapitels, die die Zwischengröße
  ausdrücklich zum Thema macht.
- **`X7BY`** (2 min 37 s) — Multiple Choice mit den drei Antworten
  „antiproportional", „weder proportional noch antiproportional",
  „proportional". Damit die einzige Übung, die **„weder noch"** als Antwort
  anbietet.

**Zum Tarif mit Grundgebühr gibt es im Buch Zuordnungen keine eigene Übung.**
Am nächsten kommt `X7BY`, weil dort „weder noch" vorkommt.

### Tücke: Der Knopf *Austeilen* lässt sich nicht fernsteuern (24.09.2026)

Auswahl, Empfänger und Frist lassen sich vollständig vorbereiten — der letzte
Klick auf **Austeilen** aber nicht. Weder ein Klick über die Bildschirmposition
noch über das Element, weder im skalierten noch im unskalierten Fenster löst
etwas aus: kein Dialog, keine Meldung, und unter *To-dos & Ergebnisse* steht
danach weiter „Für die gewählte Klasse gibt es aktuell keine To-dos."
Der Knopf ist ein `type=submit` und verlangt offenbar einen echten Mausklick.

**Vorgehen deshalb:** alles vorbereiten — Häkchen, Klasse, Empfänger, Frist —
und den Nutzer den Knopf *Austeilen* selbst drücken lassen. Vorher im Chat
zeigen, was drinsteht; das ist ohnehin Pflicht.

**Vor einem zweiten Versuch immer erst nachsehen,** ob nicht doch etwas
rausgegangen ist: `/one/tasks/maths/current` in einem zweiten Tab. Sonst
entstehen doppelte To-dos.

### Frist auf ein eigenes Datum setzen

Das Kalender-Symbol unter den drei Voreinstellungen öffnet **kein** Popup.
Der Weg: das Symbol mit `focus()` anwählen und **Return** drücken — dann
klappen zehn Eingabefelder auf (`Startdatum Tag/Monat/Jahr`,
`Startzeit Stunden/Minuten`, dieselben für `Abgabedatum`/`Abgabezeit`).
Tippen ändert sie nicht; sie werden mit `form_input` gesetzt. Die Kontrolle
läuft über das `aria-label` der Gruppe, das im Klartext
„Abgabedatum: 29. September 2026" anzeigt.

### Tücke: Häkchen lassen sich nicht per Skript setzen

Ein `click()` über das DOM setzt das Häkchen zwar, aber `cb.checked` gibt
danach weiter `false` zurück — der sichtbare Zustand steckt woanders. **Nicht
über `checked` prüfen**, sondern über die Leiste oben („7 · ca. 49 Min.") und
über das Panel *To-dos*, das die gewählten Inhalte im Klartext auflistet.
Die Checkboxen heißen alle gleich („Zur Auswahl hinzufügen") und sind über die
Baumstruktur nicht sicher einer Übung zuzuordnen — die Kontrolle läuft über
das Panel, nicht über die Refs.

Die Auswahl **überlebt einen Seitenwechsel** und steht beim nächsten Öffnen
noch da. Vor dem Aufbau einer neuen Auswahl also prüfen, ob noch eine alte
liegt, sonst teilt man versehentlich fremde Inhalte mit aus.

Bewährt als Diagnose: `3M2C` und `XQTE` trennen sauber zwischen *rechnen
können* und *erkennen können*. `V66A` und `3CXC` laufen selbst bei schwachen
Kindern hoch — sie messen nur das Rechenschema.

## Gesehene Übungscodes — Prozentrechnung (gelistet 19.10.2026, nicht ausgeteilt)

`bm_MathDE_78_Percentage_Interest_de` — 12 Tafelbilder, 66 Übungen. Lernhefte:
Vorwissen aktivieren · Grundlagen der Prozentrechnung · Prozentwerte berechnen ·
Prozentsätze berechnen · Grundwerte berechnen · Prozentuale Veränderungen ·
Wachstums- und Abnahmefaktor · Zinsrechnung · Überprüfen.

| Code | Inhalt | Art |
|---|---|---|
| `F7RD` / `7GCE` | Begriffe der Prozentrechnung in Sachkontexten / am Prozentstreifen | Tafelbild |
| `T2QE` / `YP1B` | Prozentwertberechnung erkunden / am Prozentstreifen | Tafelbild |
| `M2PD` / `DRDA` | Prozentuale Anteile bestimmen und vergleichen / Prozentsätze am Prozentstreifen | Tafelbild |
| `3CJD` / `36GC` | Grundwert im Asteroidenbergbau / am Prozentstreifen | Tafelbild |
| `63WA` / `C2XC` | Prozentuale Veränderung am Prozentstreifen / im Alltag erkunden | Tafelbild |
| `WA2D` `JY7C` `68CB` `WY4D` `DTAB` | Grundbegriffe zuordnen, Flächenanteile, schätzen | Übung |
| `2RQD` `LJMD` `C37A` `M3XA` `PJGA` `BU2D` | Prozentwert: Dreisatz, Formel, gemischt, im Kopf, einfacher/Sach-Kontext | Übung |
| `198A` `73BC` `WB1C` `2DGD` `JVXB` `M5UB` | Prozentsatz: Dreisatz, Formel, gemischt, im Kopf, einfacher/Sach-Kontext | Übung |
| `811D` `DGJB` `YXTB` `YW5C` `A3EA` `57GB` | Grundwert: Dreisatz, Formel, gemischt, im Kopf, einfacher/Sach-Kontext | Übung |
| `D2YD` `J9AA` `UFPA` `E3QC` `PQPE` `X45A` | Veränderung: um/auf, Prozentwert, -satz, Grundwert, vermischt, Sachkontext | Übung |
| `BG2M3` `U6RCF` `MCEJQ` `645QC` `5QDX8` | Tests: Begriffe, Prozentwert, Prozentsatz, Grundwert, Veränderung | Test |
| `EYXQJ` | Dreisatz-Test (Vorwissen), in einer 7. Klasse schon von gut der Hälfte bearbeitet | Test |

`bm_MathDE_56_BRGL_de`, Lernheft *Prozentschreibweise*: `V39C` Prozente in Brüche/Dezimalzahlen ·
`9DLA` Prozente an Rechtecken und Kreisen · `DM5A` Hundertstel/Dezimal → % · `D3UD` Brüche
durch Erweitern/Kürzen in % · `RUXB` Flächenanteile als Bruch und % · `U16A` Flächenanteile
schätzen · `CFEB` Sachaufgaben prozentuale Anteile · **Test `JF9EM`** „Die Prozentschreibweise
verwenden" (6 Aufgaben, 5 min; Vorschau gesehen: Flächenanteil als Bruch und %, % → gekürzter
Bruch und Dezimalzahl, Bruch → %) — taugt als Eingangsdiagnose.

## Tücken

- **„To-do löschen" löscht sofort, ohne Rückfrage.** Kein Bestätigungsdialog,
  keine Rückgängig-Funktion.
- **Die Klassenauswahl gilt überall und bleibt stehen.** Vor jedem Austeilen
  und vor jeder Auswertung prüfen, welche Klasse oben links steht — nach
  Navigation oder Neuladen kann sie auf die zuletzt gewählte zurückspringen.
- **Solange die Frist läuft, liegen die Ergebnisse unter „In der Zukunft".**
  Die Filter *Letzte 7/14 Tage* der Top-5-Kachel bleiben leer, obwohl
  bearbeitet wurde. Bei laufenden To-dos also *In der Zukunft* wählen.
- **Die Ampelfarben stehen nicht im Text.** `get_page_text` liefert Titel,
  Bearbeitungsstand und die Prozentwerte je Kind — die Farbe je Aufgabe nur
  ein Screenshot. Für die Frage „welche Aufgabe ist gekippt" also ansehen.
- **Das Suchfeld reagiert nur auf echtes Tippen.** Ein programmatisch
  gesetzter Wert löst die Suche nicht aus: hineinklicken und `type` benutzen.
- **Unter etwa 1024 px Breite verschwindet die Seitenleiste** hinter das
  ☰-Menü. Für die Arbeit das Ansichtsfenster auf mindestens 1024 px setzen.
- **Zwei Klassenauswahlen.** Eine in der Seitenleiste, eine in der Kopfzeile
  der Auswertung. Sie zeigen dasselbe an, aber die Kopfzeile hat zusätzlich
  den Empfängerfilter.
- **Die Sitzung hält nicht über Nacht.** `apps.bettermarks.com` direkt
  anzuspringen endet bei „Sie sind nicht eingeloggt!". Der Weg ist immer:
  `start.schulportal.hessen.de` öffnen, dort ist der Login meist noch gültig,
  dann die **bettermarks-Kachel oben links** anklicken. Die Kachel ist ein
  `heading`-Element ohne `href` — der Klick geht über die Bildschirmposition,
  nicht über einen Link.
- **Die Wissenslücken-Kachel ist ein `<button>` ohne Beschriftung.** Der
  Dialog *Offene Wissenslücken* rendert außerhalb von `<main>`, also liefert
  `get_page_text` ihn nicht. Über `document.querySelector` auf den
  Dialog-Container gehen oder einen Screenshot nehmen. Der Reiter
  *Nach Schüler:innen* gibt in einem Zug die Lückenzahl je Kürzel.
- **Der Export zählt anders als der Bildschirm.** Die Zahl `N/22` in der
  To-do-Liste enthält Nullergebnisse, die Datei nicht. Die Differenz je
  Übungscode ausrechnen und als Nullen ergänzen — am 14.09.2026 waren es drei
  Stück, am 09.09.2026 noch sieben.

## Erfahrungen beim Austeilen (25.10.2026)

- **Schwierigkeitsgrad vor dem Häkchen setzen.** Wird *Einfach* erst nach dem
  Anhaken gewählt, bleibt in der Auswahl *Standard*. Abhilfe: Häkchen raus und
  wieder rein. Im Panel steht der Grad hinter dem Titel („Brüche kürzen Einfach“).
- **Zeitfelder:** Tippen in die Spinbuttons ist unzuverlässig (Minuten und Monat
  sprangen falsch). Zuverlässig: Feld fokussieren und mit Pfeil hoch/runter
  verstellen, danach die `aria-label` der Gruppen lesen („Startzeit: 9:30“).
- **Gezielte Empfänger:** In der Liste zuerst „Gesamte Klasse“ abwählen (setzt alle
  zurück), dann die Kürzel anklicken; die Schaltfläche zeigt danach „13 von 22“.
- **Auswahl bleibt über Themenbücher hinweg erhalten** – Übungen aus mehreren
  Büchern lassen sich in einem To-do bündeln.
- Kürzel können von den Listen der Lehrkraft abweichen (Schreibung, Rufname statt Vorname):
  vor dem Austeilen gegen die Liste in bettermarks abgleichen, nicht raten.
- Dezimalzahl mal/durch 10, 100, 1000: `4DJB` / `184A` in
  `bm_MathDE_56_BRDZMuDi_de` (nur Standard).

## Ungeprüft

Beim nächsten Lauf klären und hier eintragen:

- ~~Auswertung herunterladen im Browser-Panel~~ **geklärt 30.10.2026:** Die
  Kachel „Auswertung“ ist ein `<button>` und löst einen Blob-Download aus
  (Name `Klassenaktivität <Klasse> (01.08.26 - TT.MM.JJ).xlsx`); die Datei kommt im
  Downloads-Ordner an. Ein sichtbares Zeichen im Panel gibt es nicht.
- **Präsentieren** — was beim Start eines Tafelbilds passiert (Vollbild?
  eigener Beitrittscode? Ansicht für die Lernenden?) ist bewusst nicht
  ausprobiert worden, weil an einer laufenden Klasse. Die Kachel eines
  Tafelbilds zeigt bei Beteiligung „Teilnahme 1 von 21".
- ~~Geplant~~ **geklärt 19.10.2026:** Über das Kalender-Symbol im Panel *To-dos*
  lassen sich Startdatum/-zeit und Abgabedatum/-zeit als Spinbuttons setzen
  (Tag, Monat, Jahr, Stunden, Minuten — hineinklicken und tippen). Ein Start in
  der Zukunft funktioniert; das To-do erscheint dann im Reiter **Geplant**.
  Beim Tippen der Startzeit „0920" in das Stundenfeld wurde nur die Stunde
  übernommen, die Minuten blieben auf dem Vorgabewert — Minuten getrennt setzen
  und vor dem Austeilen per Zoom auf das Panel prüfen.
- Buch-IDs der übrigen Themen der Stufe 7-8.


## Fristen ändern (erlebt 27.10.2026)

- Weg: To-do → ⋮ (*Weitere Aktionen anzeigen*) → *Datum ändern* → Panel mit
  Start- und Abgabedatum/-zeit als Spinbuttons.
- **Verdeckter Tab** (`document.visibilityState == "hidden"`): Das Panel bleibt in
  der Einblend-Animation hängen und liegt außerhalb des Bildes. Abhilfe: CSS
  `*{transition:none!important;animation:none!important}` einfügen und am Dialog
  samt Eltern `transform='none'` setzen.
- **Pfeiltasten greifen erst, wenn das Panel gerendert ist** — vorher einen
  Screenshot machen, dann Feld anklicken, dann Pfeiltasten.
- Nach dem Speichern bleibt das Panel im verdeckten Tab stehen und blockiert das
  Menü des nächsten To-dos: die Seite neu laden.
- Teilgruppen sind eigene To-dos (gleicher Titel, andere `N/M`) — alle einzeln ändern.

## Erfahrungen beim Austeilen (01.11.2026)

- **Der Knopf *Austeilen* nimmt den Fernklick inzwischen an** (dreimal in Folge, per
  Koordinate und per `ref` auf den `type=submit`-Knopf im Panel): Meldung „Austeilen
  erfolgreich!“, To-dos danach unter *Geplant*. Die Tücke vom 24.09.2026 gilt also nicht
  mehr zwingend — trotzdem vor jedem zweiten Versuch erst *Geplant/Aktuell* prüfen.
- **Zeitfenster:** `form_input` auf *Startdatum Tag* / *Abgabedatum Tag* setzt den Tag
  zuverlässig; Stunden/Minuten per Klick ins Feld + Pfeiltasten (eine Pfeiltaste = eine
  Minute bzw. Stunde). Kontrolle über die `aria-label` („Startzeit: 9:30“).
- **Verdeckter Tab (`document.visibilityState == "hidden"`) auch im angezeigten Panel:**
  Screenshots hinken dann dem DOM hinterher (Lernheft im DOM aufgeklappt, im Bild zu;
  Klick trifft daneben, z. B. „Vorwissen aktivieren“). Abhilfe: nach jeder Aktion
  `tabs_select` auf den Tab, dann Screenshot — danach stimmt das Bild. Zustand lieber per
  JS lesen (`Austeilen`-Leiste, `input:checked`, Panel-Text „2 von 22 Schüler:innen“).
- `184A` gibt es nur in *Standard* (bestätigt).

## Erfahrungen beim Austeilen (08.11.2026)

- **Das Panel liegt im schmalen Fenster außerhalb des Bildes**, und das Dokument meldet
  `visibilityState == "hidden"`, obwohl das Browser-Panel angezeigt wird. Klicks über Koordinaten
  oder `ref` landen dann daneben (einmal auf einem Kopier-Knopf — die Seite schrieb in die
  Zwischenablage). Was zuverlässig ging:
  - **Häkchen:** das `<label>` um die Checkbox per JS anklicken (`label.click()`), danach die
    Leiste lesen („1 · ca. 2 Min.“). `input.click()` allein reicht nicht.
  - **Panel öffnen:** JS-Klick auf den Knopf „Auswahl bearbeiten …“ in der Leiste.
  - **Eigenes Zeitfenster:** JS-Klick auf den vierten Knopf der Gruppe „Heute / 4 Tage / 7 Tage“.
  - **Datum und Uhrzeit:** `form_input` auf alle Spinbuttons (Tag, Stunden, Minuten) — die
    Pfeiltasten griffen diesmal nicht. Kontrolle über die `aria-label`.
  - **Austeilen:** `form.requestSubmit(button)` auf den `type=submit`-Knopf im Panel — danach
    erscheint „Austeilen erfolgreich!“.
- **Die Auswahl bleibt nach dem Austeilen stehen.** Vor der nächsten Zuweisung die Seite neu
  laden und prüfen, dass keine Leiste mehr da ist; sonst gehen die alten Übungen ein zweites Mal raus.
- Gesehen: `WA2D` Begriffe der Prozentrechnung im Sachkontext zuordnen (6 Aufg., ca. 4 min) ·
  `M3XA` Prozentwerte zu zentralen Prozentsätzen im Kopf (2 Aufg., ca. 4 min) ·
  `D2YD` Veränderung um und Veränderung auf umrechnen (6 Aufg., ca. 2 min).

## Erfahrungen beim Austeilen (15.11.2026)

- Das Panel heißt jetzt **„Auftrag erstellen“** und hat oben ein Feld **Kommentar – optional**
  (keine personenbezogenen Daten). Der Kommentar steht in *Aktuell* als Überschrift über dem
  To-do – gut für „Zum Nachholen … – wird nicht bewertet“.
- **Empfänger:** Erst den Knopf „Gesamte Klasse“ anklicken (öffnet die Liste), dann die
  `label.chakra-checkbox` per JS klicken. Kürzel über `textContent` lesen – `innerText` ist im
  verdeckten Tab leer.
- **Keine `setTimeout`-Pausen in Skripten** bei verdecktem Tab: Timer werden stark gedrosselt,
  das Skript läuft in den 45-s-Abbruch. Jeden Schritt als eigenen Aufruf ohne Warten.
- Bewährte Reihenfolge je To-do: Seite laden → Häkchen (Label-Klick) → „Auswahl bearbeiten …“ →
  „Gesamte Klasse“ → Kalender-Knopf → Empfänger → `form_input` Abgabedatum Tag + Kommentar →
  Stand lesen (`aria-label` der Gruppen, angehakte Kürzel, Leiste „(n/22)“) → `requestSubmit`.
- Tests (z. B. 645QC, MCEJQ) lassen sich an einzelne Kinder erneut austeilen.

## Erfahrungen beim Austeilen (17.11.2026)

- Reihenfolge vom 15.11. hat ohne Abweichung getragen, Tab diesmal `visible` (Fenster 1249 px).
- **Empfänger „alle außer …“:** Nach dem Öffnen der Liste über „Gesamte Klasse“ sind alle angehakt;
  einzelne Kürzel per Label-Klick abwählen genügt (Knopf zeigt danach „17 von 22 Schüler:innen“).
- **Startminuten:** `form_input` mit `0` blieb auf dem Vorgabewert (8:15), mit `00` übernommen
  (`aria-label` „Startzeit: 8:00“). Immer `00` schreiben und die Gruppe rücklesen.
- Gesehen und ausgeteilt (Prozentrechnung, Standard): `73BC` Prozentsatz mit Formel (5 Aufg., 7 min) ·
  `DGJB` Grundwerte mit Formel (5, 6) · `JVXB` Prozentsatz im einfachen Sachkontext (3, 4) ·
  `A3EA` Grundwerte im einfachen Sachkontext (3, 4) · `J9AA` Prozentwert bei Veränderung (5, 8) ·
  `UFPA` Prozentsatz bei Veränderung (5, 7) · `X45A` Veränderungen im Sachkontext (5, 13; Vorschau:
  neuer Wert nach Erhöhung, Prozentsatz der Erhöhung) · `E3QC` Grundwert bei Veränderung (5, 9; rückwärts,
  im B-Kurs nicht Stoff der Arbeit).
- Weitere Codes im Heft Prozentsätze/Grundwerte: `UCVD` PS schätzen, `1VYA` PS mit Eigenschaften,
  `LT1B` PS schätzen (G und W überschlagen), `R7JE` GW schätzen, `3UVA` Zahlenbereiche über Grundwerte.
- Computerraum-Schulstunde: ca. 15 min für Einloggen und Organisatorisches abziehen; Zuweisung ≤ ca. 30 min.

## Erfahrungen beim Austeilen (19.11.2026)

- **Vor jedem Austeilen „Geplant“ und „Aktuell“ lesen.** Die Lehrkraft teilt auch selbst aus; am
  19.11. lagen schon zwei Aufträge „Üben für die Arbeit“ für dieselbe Stunde – meine Zuweisung
  hat sie gedoppelt und musste zurückgenommen werden.
- Zuweisungen heißen jetzt **„Auftrag“**. Das Drei-Punkte-Menü sitzt **je Auftrag** (nicht je
  To-do): *Ergebnisse anonymisieren · Auftrag bearbeiten · Erneut austeilen … · Auftrag löschen*.
- **„Auftrag löschen“ fragt nicht nach** – sofort weg. Nur gezielt das Menü des richtigen Auftrags
  öffnen (nicht alle Menüs gleichzeitig), vorher Startzeit/Titel im Menü prüfen.
- **„Auftrag bearbeiten“** öffnet das Panel mit „Löschen“ je To-do: einzelne Übungen lassen sich
  herausnehmen, dann *Speichern* (`requestSubmit`).
- Das Zeitfenster ist jetzt eine **Radiogruppe** (`[role=radiogroup]`, Labels Heute / 4 Tage / 7 Tage /
  ohne Text = „Eigenes Datum“); das vierte Label klicken, dann erscheinen die Spinbuttons.
- Die Auswahl bleibt beim Wechsel zwischen Themenbüchern (`d2703c` → `d2703d` → `d2703e`) erhalten;
  nach dem Laden ein paar Sekunden warten, bis Leiste und Häkchen da sind.
- Codes Prozentrechnung (`bm_MathDE_78_Percentage_Interest_de`): `73BC` Prozentsatz mit Formel ·
  `WB1C` Prozentsatz berechnen · `UCVD` schätzen · `2DGD` im Kopf · `JVXB` Sachkontext ·
  `DGJB` Grundwert mit Formel · `YXTB` · `YW5C` · `A3EA` · `D2YD` um/auf · `J9AA` Prozentwert bei
  Veränderung · `UFPA` Prozentsatz bei Veränderung · `E3QC` Grundwert bei Veränderung.
