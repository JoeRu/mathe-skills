# Schulportal Hessen — Wege, Felder, Tücken

Gemeinsame Referenz für `wochenplanung`, `schulportal-leistung`, `schuelerdaten` und
`kurs`. Kurs-spezifische Werte (Kursmappen-ID, Rhythmus) stehen in
`Kurse/<Kurs>/kurs.md`, nicht hier. Neu erlebte Tücken in der **Quelle**
(`$SKILLS/references/schulportal.md`) ergänzen.

## Grundregeln

- Der Nutzer meldet sich selbst an; Zugangsdaten werden nie eingegeben oder gespeichert.
- Nichts wird ungefragt gespeichert — Schüler und Eltern lesen mit.
- Die Kursmappe zeigt Klarnamen (Hausaufgaben-Rückmeldung, Entschuldigungen).
  **Beim Auslesen nur die Spalten Datum, Thema, Inhalt/Hausaufgaben und die
  Dateinamen der Anhänge übernehmen** — nie die Spalte „Weiteres“ mit Namen.
  Screenshots aus dem Portal werden nicht abgelegt.

## Wo was steht

| Was | Weg |
|---|---|
| Kursmappe | Startseite → **mein Unterricht** → Kurs; direkt `meinunterricht.php?a=view&id=<id>` |
| Historie des Halbjahrs | Kursmappe → Reiter **Historie**; zeigt nur die letzten Einträge. Vollständig: Link „Alle Einträge laden“ = `meinunterricht.php?a=loadHistory&id=<id>` (liefert HTML-Tabellenzeilen, per `fetch` lesbar) |
| Frühere Kurse | **Mein Unterricht → Archiv** (`meinunterricht.php?a=archiv`) |
| Hausaufgaben je Kind | Kurs → **Leistungen → Ausführlich**: `meinunterricht.php?a=notenTableFull&id=<id>&halb=1` (siehe Skill `schuelerdaten`) |
| Leistung anlegen, Punkte, Berechnungsfaktoren | **Mein Unterricht → Leistungen** (siehe Skill `schulportal-leistung`) |
| Klassenarbeitstermine | Startseite → **Klausurenplaner** |
| Feste, Ausflüge | Startseite → **Kalender** |
| Ausfälle | **Vertretungsplan** |

## Historie auslesen

Spalten der Historie: `Datum Stunden | Thema | Inhalt Hausaufgaben | Weiteres`.
Anhänge stehen als Links in „Weiteres“; nur deren Dateinamen übernehmen. Einträge
mit Datum in der Zukunft sind **Vorab-Einträge** (Soll), keine gehaltenen Stunden.
Ergebnis wandert nach `Kurse/<Kurs>/ausgeteilt.csv` (Skill `kurs`).

## Stundeneintrag (Kursmappe)

Schulportal Hessen.
Der Nutzer meldet sich selbst an; Zugangsdaten werden nie eingegeben
oder gespeichert. Klickweg aufgezeichnet am 31.08.2026.

### Klickweg

1. `https://start.schulportal.hessen.de` → Kreis und Schule wählen → Anmeldung
   durch den Nutzer
2. Startseite → Kachel **mein Unterricht**
3. Kursmappe der Lerngruppe — direkt: `meinunterricht.php?a=view&id=<schulportal_id>`
   (die ID steht in `Kurse/<Kurs>/kurs.md`)
4. Reiter **Historie** → prüfen, ob für die Zieltage schon Einträge stehen
   (zeigt Thema, Datum, Stunde, Inhalt, Hausaufgaben, Leistungen, Anhänge)
5. Reiter **Neuer Eintrag** → Formular ausfüllen
6. **Speichern**

### Formularfelder

| Feld | Pflicht | Was hinein kommt |
|---|---|---|
| **Datum** | ja | vorbelegt mit heute — **nur über das Kalender-Symbol** ändern, nie tippen |
| Checkbox *„Zeige den Eintrag den Lernenden und deren Eltern vor diesem Tag an!"* | nein | siehe Sichtbarkeitsregel unten |
| **Schulstunden von / bis** | ja | laut `rhythmus` in `kurs.md`, z. B. Di `2`–`2` · Mi `1`–`2` · Fr `2`–`2` |
| **Thema der Stunde(n)** | nein | eine Zeile, für Lernende und Eltern sichtbar |
| **Inhalt** | nein | Stichpunkte, einer pro Zeile, sichtbar |
| **Hausaufgaben** | nein | Stichpunkte, einer pro Zeile, sichtbar |
| Checkbox *„Erlaube das Abgeben von Dateien zu dieser Stunde"* | nein | nur setzen, wenn der Nutzer es sagt |

### Tücken des Formulars (am 31.08.2026 erlebt)

- **Das Datum niemals tippen.** Ein getippter Wert wird beim Verlassen des
  Feldes vom Datepicker auf „heute" zurückgesetzt — lautlos. Immer über das
  **Kalender-Symbol** rechts im Feld auswählen.
- **Schulstunden erst setzen, wenn der Datepicker zu ist.** Solange er offen
  ist, überdeckt er die beiden Dropdowns und die Auswahl greift nicht.
- **Reihenfolge, die funktioniert:** Thema → Inhalt → Hausaufgaben →
  Schulstunden von/bis → Datum über den Kalender → prüfen → speichern.
- **Vor dem Speichern immer per Screenshot prüfen**, dass alle sechs Felder
  wirklich gefüllt sind. Zwei davon setzen sich stillschweigend zurück.
- **Datum auch nicht per Skript setzen** (01.11.2026 erlebt): `$('#datum').datepicker('setDate', …)`
  schreibt `11/03/2026` (US-Format); der anschließende Klick auf das Kalender-Symbol warf die
  Seite auf die Startseite, nichts gespeichert. Funktioniert: Kalender-Symbol klicken, Tag
  anklicken (Kalender zeigt KW-Nummern links), dann auf die Überschrift klicken, damit er zu ist.
  Textfelder und Stunden-Dropdowns dürfen per jQuery `.val(…).change()` gefüllt werden.
- **Prüfen ohne Screenshot:** `$('#datum').val()`, `#stundenVon/#stundenBis`, `#subject`,
  `#inhalt`, `#homework`, `input[name=zeigeauchvorheran]` und `input[name=abgabe]` per JS lesen;
  nach dem Speichern die Historie über `loadHistory` rücklesen.

Zusätzlich hängen an einem Eintrag **Anhänge** (das Arbeitsblatt der Stunde)
und **Leistungen** (Kopfrechentest, Mitarbeit, Hausaufgaben, Bonusaufgabe).
Beides trägt der Nutzer selbst nach — der Skill fasst es nicht an, weist aber
darauf hin, wenn ein erstelltes Arbeitsblatt an die Stunde gehört.

### Schreibweisen, wie der Nutzer sie führt

Werden übernommen, nicht ersetzt:

- Buchbezug: `S. 86 Nr. 6`, `S. 85 Infokasten gelesen`, `S.80/S.81`
  (Lehrwerk Westermann, siehe `grundlagen.md`)
- Arbeitsblatt: `AB`, z. B. `AB Aufgabe 2, 3` oder `AB fertig bearbeiten`
- Frist steht als erste Zeile im Hausaufgabenfeld: `Bis Dienstag:`
- Freiwilliges: `Bonusaufgabe (optional): S. 89 Nr. 6` — zählt zur
  sonstigen Mitarbeit und steht als eigener, letzter Punkt
- Ein Stichpunkt pro Zeile, keine Nummerierung, keine ganzen Sätze
- Ein **Kopfrechentest wird in der Vorstunde angekündigt** — als Zeile im
  Hausaufgabenfeld, mit dem, was zu lernen ist
  (`Ankündigung Kopfrechnen-Test am Freitag - Quadratzahlen bis 25 auswendig lernen`)
- Organisatorisches der Stunde gehört ins Inhaltsfeld
  (`Probealarm`, `Hinweis auf die Taschenrechner-Sammelbestellung.`)

**Vorab-Einträge stehen in Planform.** Die bestehenden Einträge sind im
Rückblick geschrieben („AB bearbeitet", „Aufgabe 1 zusammen gerechnet").
Beim Vorab-Anlegen wird der Inhalt als Vorhaben formuliert; nach der Stunde
passt der Nutzer an, was tatsächlich lief.

### Regeln fürs Eintragen

- **Erst Historie prüfen, dann anlegen.** Existiert für einen Zieltag schon
  ein Eintrag, wird er gemeldet und **unangetastet gelassen** — er ist
  Nachweis, nicht Entwurf. Nur nach ausdrücklicher Ansage wird ergänzt.
- **Vor dem Speichern** wird der fertig ausgefüllte Eintrag gezeigt und
  bestätigt — der erste Eintrag der Woche immer, die weiteren nur, wenn
  der Nutzer nicht „mach die anderen genauso" sagt.
- **Sichtbarkeit:** Vorab-Einträge werden standardmäßig **ohne** den Haken
  „Zeige den Eintrag den Lernenden und deren Eltern vor diesem Tag an"
  gespeichert — sonst lesen Schüler die Stunde vorab. Nur setzen, wenn
  der Nutzer es für eine Stunde ausdrücklich will.
- **Dateiabgabe-Haken** bleibt aus, sofern nicht verlangt.
- **Kein `<offen>` ins Portal.** Platzhalter sind ein Werkzeug für den Plan
  im Chat. Was in ein Portalfeld geht, ist entweder ausgefüllt oder die
  Zeile entfällt — Schüler und Eltern lesen dieses Feld.
- **Keine Schülernamen** in Thema, Inhalt oder Hausaufgaben (Datenschutzregeln
  in `grundlagen.md`).
- Das Thema ist die Kurzform aus dem Plan, nicht der ganze Ablauf.
- Als Hausaufgabe wird nur die Aufgabe eingetragen, ohne Erwartungshorizont —
  geprüft wird ohnehin nur die Vollständigkeit.
- Klappt der Portalzugang nicht, wird der Plan trotzdem fertig ausgegeben,
  zum Selbst-Eintragen kopierbar.

## Leistungen (erlebt 30.10.2026)

| Was | Weg |
|---|---|
| Neue Leistung | Kursmappe → *Leistungen* → *Neue Leistung* = `meinunterricht.php?a=notenDaten&id=<id>&datum=TT.MM.JJJJ` |
| Erfassungstabelle | `meinunterricht.php?a=notenErfassung&id=<id>&noten=<nr>` |
| Einstellungen einer Leistung | `meinunterricht.php?a=notenDaten&id=<id>&noten=<nr>` |

- **Formular per jQuery füllen.** Die Seite reagiert auf jQuery-Events: `$('#erfassung').val('rohpunkte').change()`,
  dann `#fehlerindex`, `#anznoten` (19 = Noten mit Tendenzen), `#anzahl`, `#name1`, `#points_1`,
  `#note_1` … `#note_5` (Prozentgrenzen), `#notentendenzbereichProzent`. Native `dispatchEvent`
  reicht nicht immer; ein Wert, den die Seite nicht übernommen hat, fehlt nach dem Speichern lautlos.
- **Welche Notenskala zu welcher Erfassung passt,** steht an den Optionen (`data-erfassung`).
  „Noten mit Tendenzen“ gibt es nur bei Rohpunkten und direkter Noteneingabe — nicht bei
  „Erfassung der erreichten Prozente“. Eine nicht erlaubte Option wird lautlos verworfen.
- **Erfassung und Notenskala sind nach dem Speichern fest** (im Bearbeiten-Formular nur Text).
  Falsch angelegt heißt: neu anlegen, die alte leeren und von der Lehrkraft löschen lassen.
- **Löschen verlangt das Portal-Passwort** (Dialog mit Passwortabfrage) — das macht immer die Lehrkraft.
- **Werte eintragen:** Je Zeile ein Feld `punkte_<schueler-id>_<aufgabe>`. Wert per
  `$(feld).val('84,5').trigger('change')` setzen — das Portal speichert die Zeile sofort per POST
  und rechnet die Note. Komma als Dezimaltrennzeichen geht.
- **Zuordnung Name → Kürzel im Browser:** Zeile steht als „Nachname, Vorname“; Kürzel =
  zwei Buchstaben Vorname + zwei Nachname. Vor dem Eintragen prüfen: alle Zeilen eindeutig
  zugeordnet, keine doppelt, keine übrig. Namen nie in die Antwort.
- **Rücklesen:** Seite neu laden und je Zeile Wert und Note gegen die Tabelle prüfen; den
  Notenspiegel aus `#auswertung` mit dem eigenen vergleichen.

## Erlebt 08.11.2026

- **Das Feld „Inhalt“ ist nur für Lehrkräfte sichtbar** (Symbol 👤 im Formular, Legende unter den
  Knöpfen). Für Lernende und Eltern sichtbar sind nur *Thema* und *Hausaufgaben* (Symbol ♟).
  Alles, was die Klasse lesen muss (z. B. Arbeitsanweisungen und Links an einem
  Home-Schooling-Tag), gehört deshalb ins Hausaufgabenfeld. Die Sichtbarkeit lässt sich über
  „Sichtbarkeit ändern“ umstellen — nicht ungefragt.
- **Nach dem Datumswechsel lädt das Formular die Schulstunden neu und leert „von/bis“** —
  asynchron, etwa 1–2 s nach dem Klick auf den Tag. Werden die Stunden sofort gesetzt, sind sie
  beim Speichern wieder leer; „Speichern“ zeigt dann nur einen Hinweis (`hasRequiredFieldsFilled`)
  und speichert nichts. Reihenfolge: Tag anklicken → 2 s warten → Stunden setzen → prüfen → speichern.
- Den Kalendertag kann man per jQuery anklicken
  (`$('.datepicker:visible td.day').filter(...).click()`); das Datum steht danach korrekt als
  TT.MM.JJJJ. Nur `datepicker('setDate', …)` ist verboten (US-Format, siehe oben).
- Nach jedem Speichern über `loadHistory` rücklesen — ein stiller Fehlschlag ist sonst nicht zu sehen.

## Sitzung abgelaufen (15.11.2026)

- „Datenbankauswahl nicht möglich“ oder „Es wurde kein gültiges Tool gewählt“ auf
  `meinunterricht.php` bzw. der bettermarks-Kachel heißt meist nur: die Sitzung ist
  abgelaufen. Die Sitzung ist kurz, und es sieht dann so aus, als sei eine neue Anmeldung nötig.
  Zuerst **einmal „zurück“** klicken (bzw. `index.php` aufrufen): Das frischt die Sitzung oft auf,
  und Kursmappe und Kacheln gehen wieder. Erst wenn das nicht hilft, die Lehrkraft bitten, sich
  neu anzumelden (Hinweis der Lehrkraft, 15./16.11.2026).
- Kalender der Schule: `kalender.php` (Monatsansicht, Arbeiten stehen dort, z. B. „7:45 Mathematik 7 Arbeit“).
- Neuer Eintrag ohne Screenshot: Reiter per `$('a[href="#new"]').click()`, Felder per jQuery,
  Kalender-Symbol `$('#datum').parent().find('span').first().click()`, Tag per
  `$('.datepicker:visible td.day')…click()`, 3 s warten, Datepicker ausblenden, dann Stunden setzen,
  Speichern-Knopf klicken, Historie per `fetch('meinunterricht.php?a=loadHistory&id=…')` rücklesen.
- **Eintrag bearbeiten** (`editBookEntry&entry=<n>`): Die Textfelder heißen dort `textarea[name=content]`
  und `textarea[name=homework]` und haben **keine id** – `$('#inhalt')`/`$('#content')` greift ins Leere,
  gespeichert wird dann nur das Thema. Nach dem Speichern immer die Historie rücklesen (15.11.2026 erlebt).
