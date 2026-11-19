---
name: bettermarks
description: >
  Dieser Skill wird verwendet, wenn der Nutzer mit bettermarks arbeitet — etwa
  "wie ist die Übung gelaufen", "wer hat die Zuordnungen noch nicht gemacht",
  "werte die bettermarks-Aufgaben aus", "such mir bettermarks-Übungen zum
  Dreisatz", "welches Tafelbild passt zum Einstieg", "plan mir die Stunde mit
  bettermarks", "teil den Schwachen leichtere Aufgaben zu", "Wissenslücken der
  Klasse", "was soll ich als Hausaufgabe in bettermarks geben" oder "Auswertung
  der Klassenaktivität". Liest die Ergebnisse, findet passende Inhalte,
  bereitet Stunden mit Tafelbildern und Lernpfaden vor und teilt gezielt
  differenzierte Aufgaben aus.
metadata:
  version: "1.2.1"
---

# bettermarks

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` lesen
(Kurssystem A/B/C, Ordnerstruktur, Datenschutz), dann
`${CLAUDE_PLUGIN_ROOT}/references/bettermarks-plattform.md` — dort stehen
Klickwege, URL-Schema, Aufbau der Auswertungsdatei und die Tücken der
Oberfläche. **Nicht raten, was wo steht: die Referenz sagt es.**

## Zweck

bettermarks liefert etwas, was Papier nicht liefert: **welches Kind an welcher
Aufgabe hängt**, aufgabengenau und ohne Korrekturzeit. Der Nutzen entsteht
nicht beim Austeilen, sondern danach — wenn aus den Zahlen die nächste Stunde
und die nächste Zuweisung werden.

Der Skill kann vier Dinge. Sie hängen zusammen und werden in dieser
Reihenfolge gebraucht:

| # | Ablauf | Ergebnis |
|---|---|---|
| 1 | **Auswerten** | Wo steht die Klasse, wer hängt woran, was ist offen |
| 2 | **Aufgaben finden** | Konkrete Inhalte mit ID und Niveau |
| 3 | **Stunde vorbereiten** | Ablauf aus Tafelbildern, Beispielen und Übungen |
| 4 | **Zuweisen** | Differenzierte To-dos, gezielt nach Auswertung |

## Grundregeln

- **Der Nutzer meldet sich selbst an.** Zugangsdaten werden nie eingegeben
  und nie gespeichert.
- **Zugang immer über das Schulportal:** `start.schulportal.hessen.de` →
  Kachel **bettermarks** (oben links). `apps.bettermarks.com` direkt aufzurufen
  endet bei „Sie sind nicht eingeloggt!“ — dann nicht den Nutzer bitten, sich bei
  bettermarks anzumelden, sondern den Weg über die Kachel gehen.
- **Vor jeder Aktion prüfen, welche Klasse oben links steht.** Die Auswahl
  gilt global und springt nach Navigation zurück. Sie muss `bettermarks_klasse` (bzw.
  `bettermarks_testklasse`) des **bestimmten Kurses** aus `kurs.md` entsprechen; der Kurs wird nach
  `grundlagen.md` (*Kurswahl*) bestimmt und die Soll-Klasse vorher genannt.
- **Ausprobiert wird in der Testklasse, nie in der echten.** Beide Namen stehen
  in `Kurse/<Kurs>/kurs.md` (`bettermarks_testklasse`, `bettermarks_klasse`). Jeder Versuchslauf —
  Austeilen, Fristen, Einstellungen — läuft in der Testklasse.
- **Nichts wird ungefragt ausgeteilt.** Vor dem Klick auf *Austeilen* steht
  die fertige Auswahl mit Empfängern und Frist im Chat und wird bestätigt.
  Das gilt auch dann, wenn der Nutzer den Inhalt selbst genannt hat.
- **Vor jedem Austeilen den Bestand lesen:** `/one/tasks/maths/current`,
  Reiter **Aktuell** *und* **Geplant** — ein Auftrag mit Start in der Zukunft
  steht nur unter *Geplant*. Die Lehrkraft teilt auch selbst aus. Je Kürzel
  festhalten, welche Übungs-IDs schon laufen oder geplant sind; eine Übung, die
  ein Kind bereits hat, wird ihm nicht noch einmal zugewiesen, und der Vorschlag
  im Chat nennt die Überschneidung. (Vorfall 19.11.2026: ohne Blick in *Geplant*
  waren vier Kinder kurzzeitig doppelt belegt.)
- **Nichts wird gelöscht.** Weder Aufträge/To-dos noch Wissenslücken. „Auftrag
  löschen" löscht sofort — ohne Rückfrage, ohne Rückgängig. Einzige Ausnahme:
  ein in dieser Sitzung **selbst** angelegter Auftrag, der noch nicht gestartet
  ist und doppelt vergibt, wird nach Rückmeldung an die Lehrkraft zurückgenommen
  (ganz, oder einzelne Übungen über *Auftrag bearbeiten*). Aufträge der
  Lehrkraft werden nie angefasst.
- **Zahlen werden gerechnet, nicht geschätzt** — aus der Auswertungsdatei,
  mit Python. Das ist dieselbe Regel wie in `dokumente.md`.
- **Keine Klarnamen.** In bettermarks stehen nur Kürzel; die bleiben auch im
  Chat auf das Nötige beschränkt und gehen nie ins Repository oder ins Memory.
  Der `Zugangsname` aus der Auswertungsdatei ist ein Zugangsmerkmal und wird
  nirgends wiedergegeben.
- **bettermarks-Prozente sind zuerst Diagnose.** In Noten umgerechnet wird nur,
  wenn die Lehrkraft es für ein Thema festlegt — dann als mündliche Leistung nach
  `references/notenschluessel.md`, Abschnitt *bettermarks*, nie „grob“ nebenbei.
- **bettermarks-Aufgaben sind Hausaufgaben**, sobald sie im Portal als solche
  stehen. Die Wertung je Kind steht unten im Abschnitt *Als Hausaufgabe werten*.

## 1 — Auswerten

### Datenquelle

**Erste Wahl: die Auswertungsdatei.** In `Kurse/<Kurs>/_intern/<Thema>/bettermarks/`
(Pfad: `kurs.py pfad --art bettermarks`) des laufenden Themas nach
`Klassenaktivität <Klasse> (<Zeitraum>).xlsx` mit der Klasse **dieses** Kurses sehen (ältere
liegen noch in `_Eingang/` oder in `<Thema>/_intern/`). Das Blatt „Schülerinnen und Schüler“
enthält Klarnamen — die Datei bleibt in `_intern/`. Liegt eine aktuelle da, wird mit ihr gerechnet —
Aufbau siehe Referenz.

Ist keine da oder ist sie zu alt: *To-dos & Ergebnisse → Kachel „Auswertung“*
anklicken (ein `<button>`). Der Download landet im Downloads-Ordner des Rechners;
Die Lehrkraft legt die Datei nach `Kurse/<Kurs>/_intern/<Thema>/bettermarks/`. Ist `Downloads` verbunden,
selbst dorthin verschieben. Über den Chat (Base64) wird die Datei nicht geholt.

**Zweite Wahl: der Bildschirm.** `/one/tasks/maths/current`, Reiter *Aktuell*
für laufende, *Zurückliegend* für abgelaufene Fristen. Prozentwerte je Kind
sind als Text lesbar; die Ampel je einzelner Aufgabe nur per Screenshot der
aufgeklappten Detailansicht (⋮ → *Details anzeigen*).

### Was ausgegeben wird

Nicht die Tabelle nacherzählen. Diese vier Punkte, in dieser Reihenfolge:

```markdown
## bettermarks-Auswertung <Klasse> — <Thema>, Stand <TT.MM.JJJJ>

**Bearbeitet:** <n> von <m> To-dos abgeschlossen · Klassenschnitt <x> %

### Sitzt
- <Übung> (<ID>) — <x> %, <n>/<m> bearbeitet

### Wackelt
- <Übung> (<ID>) — <x> %, <n>/<m> bearbeitet — <woran es liegt, wenn erkennbar>

### Nicht angefangen
- <Übung> (<ID>) — <n>/<m>

### Einzelne
- <n> Kinder unter 40 % im ganzen Thema: <Kürzel>
- <n> Kinder mit offenen Wissenslücken: <Kürzel>
- deutlich verbessert / eingebrochen gegenüber dem eigenen Schnitt: <Kürzel>

**Vorschlag:** <ein Satz, was daraus für die nächste Stunde folgt>
```

Regeln dafür:

- **Eine leere Zelle in der Datei kann „nicht bearbeitet" oder „0 %" heißen.**
  Für eine Leistung oder die Hausaufgabenwertung ist das gleichgültig (beides
  zählt 0). Für die **Diagnose** aber die Zahl der Bearbeitenden
  (`N/22`) vom Bildschirm holen; die Differenz zu den Werten in der Datei sind
  Nullergebnisse und zählen mit 0 in den Schnitt. Ohne diese Korrektur fällt
  der Schnitt zu gut aus — im Beispiel vom 09.09.2026 um sieben Prozentpunkte.
  Geht es nicht, den Schnitt ausdrücklich als **Obergrenze** ausweisen.
- **Bearbeitungsquote immer mitnennen.** Eine Übung mit 90 % bei 3 von 21
  Bearbeitenden ist kein guter Wert, sondern ein offener Posten.
- **Erst die Aufgabe, dann das Kind.** Was die halbe Klasse falsch macht, ist
  ein Unterrichtsthema; was ein Kind falsch macht, ist eine Zuweisung.
- Die **Top 5 fehlerhaften Aufgaben** (Kachel) benennen die konkrete
  Einzelaufgabe und zeigen sie als Bild — für die Rückgabestunde besser als
  jede Prozentzahl. Bei laufender Frist steht sie unter *In der Zukunft*.
- **Wissenslücken nur berichten.** Sie sind bettermarks' eigene Diagnose und
  bleiben stehen, bis das Kind sie schließt.
- **Wiederholungen mitlesen** (`↻ 2` hinter dem Kürzel): 60 % im zweiten
  Anlauf ist etwas anderes als 60 % im ersten.

## 2 — Aufgaben finden

Ziel ist immer eine **Liste mit ID**, nicht eine Beschreibung.

1. Thema im passenden Buch öffnen (Buch-IDs in der Referenz), Reiter
   *Übungen*. Alternativ das Suchfeld *Material durchsuchen* — es reagiert nur
   auf echtes Tippen.
2. Passendes Lernheft aufklappen, Übungen ansehen: Titel, ID, Anzahl der
   Aufgaben, Minuten.
3. Vor jeder Empfehlung **die Vorschau ansehen** (Übung aufklappen →
   *Aufgabenpaket ansehen* oder die Miniaturbilder). Keine Übung empfehlen,
   die nur dem Titel nach passt.
4. Niveau über den Schalter **Einfach / Standard / Schwierig** wählen —
   *Einfach* ≈ C-Kurs, *Standard* ≈ B-Kurs, *Schwierig* ≈ A-Kurs. Diese
   Zuordnung ist eine Einschätzung; bei Abweichung vom Standard vorher die
   Vorschau prüfen und im Vorschlag dazusagen, dass es eine Einschätzung ist.

Format der Antwort:

```markdown
## <Thema> — bettermarks, <Buchname>

**Einstieg:** <Tafelbild> (<ID>) — <halber Satz zum Zugang>
**Üben:** <Übung> (<ID>) — <n> Aufgaben, ca. <m> min — <Niveau>
**Vertiefen:** <Übung> (<ID>) — …
**Überprüfen:** <Test> (<ID>) — …
```

Zu jeder Fundstelle einen halben Satz zum Inhalt, damit der Nutzer sie ohne
Aufschlagen wiedererkennt.

## 3 — Stunde vorbereiten

**Der Lernpfad ist die Vorlage, nicht die eigene Erfindung.** Zu jedem
Lernheft gibt es einen (Reiter *Lernpfade*) mit einer fertigen Phasenfolge:
Vorwissen aktivieren → Tafelbilder zum Einsteigen und Erarbeiten → Tafelbilder
zum Sichern (Wissenskästen, Beispiele) → Üben (Basisaufgaben, dann weitere) →
Überprüfen. Er nennt auch den Umfang („17 Materialien für 3
Unterrichtsstunden") und die neuen Begriffe.

Vorgehen:

1. Lernpfad zum Thema öffnen, Phasen und Begriffe lesen.
2. Reiter **Auswerten** des Lernpfads: der *Kompetenzfortschritt* zeigt, wo
   die Klasse je Lernziel steht (Marken bei 60 % und 90 % — bettermarks-
   Schwellen, kein Notenschlüssel).
3. Daraus einen Ablauf für den konkreten Block bauen, nicht den ganzen
   Lernpfad abbilden. Eine Doppelstunde trägt in der Regel: ein Tafelbild zum
   Einstieg, eine Erarbeitung, ein Wissenskasten zur Sicherung, eine Übung.
4. **Was an der Tafel läuft, macht der Nutzer selbst.** Der Skill nennt die
   Tafelbilder mit ID und Reihenfolge und sagt, was sie zeigen — er startet
   keine Präsentation in einer laufenden Klasse.

Ausgabe:

```markdown
## <Block> — <Thema>

| Phase | Inhalt | ID | Art | ca. |
|---|---|---|---|---|
| Einstieg | <Titel> | <ID> | Tafelbild | 10 min |
| Erarbeitung | <Titel> | <ID> | Tafelbild | 20 min |
| Sicherung | <Titel> | <ID> | Wissenskasten | 10 min |
| Üben | <Titel> | <ID> | Übung | 15 min |

**Tafelanschrieb:** <die zwei bis drei Sätze bzw. das Schema, das stehen bleibt>
**Womit es hakt:** <die Stelle, an der erfahrungsgemäß Rückfragen kommen>
**Papier-Backup:** <was ausgedruckt danebenliegt, falls Netz oder Anmeldung klemmt>
```

Das **Papier-Backup gehört immer dazu**, sobald der Block im Computerraum
liegt (siehe `wochenplanung`, Abschnitt Computerraumstunden). Fehlt es,
`arbeitsblatt` oder `buchaufgaben` aufrufen.

Braucht der Nutzer ein Tafelbild zum Ausdrucken oder Anschreiben statt zum
Klicken, wird der Inhalt **nicht aus bettermarks kopiert**, sondern mit
`arbeitsblatt` selbst erzeugt — bettermarks-Material ist lizenziert für die
Nutzung in der Plattform, nicht für den Nachbau in eigenen Dokumenten
(gleiche Linie wie `buchaufgaben`, Abschnitt Urheberrecht).

## 4 — Zuweisen

Der eigentliche Zweck des Skills: **aus der Auswertung folgt, wer was
bekommt.**

### Die drei Gruppen

Nach einer Auswertung ergeben sich fast immer drei Gruppen. Für jede eine
eigene Zuweisung, nicht eine für alle:

| Gruppe | Erkennungsmerkmal | Was sie bekommt |
|---|---|---|
| **Trägt** | Thema über ~75 %, nichts offen | dieselbe Übung auf *Schwierig*, oder die nächste Stufe des Lernpfads |
| **Wackelt** | 40–75 %, oder einzelne Aufgaben rot | dieselbe Übung erneut auf *Standard*, plus die Basisaufgabe davor |
| **Hängt** | unter 40 %, oder Wissenslücke offen | die Vorstufe auf *Einfach* — nicht dasselbe noch einmal |

Die Grenzen sind Startwerte, keine Wahrheit. Wer im zweiten Anlauf 60 %
schafft, gehört nicht in dieselbe Gruppe wie jemand mit 60 % im ersten.

### Weg

1. Klasse oben links prüfen, dann Bestand unter *Aktuell* und *Geplant* lesen
   (Grundregel): Welche Kürzel haben welche IDs schon? Bestehende Aufträge der
   Lehrkraft bleiben unverändert.
2. Inhalte im Reiter *Übungen* per Häkchen wählen, Niveau je Übung setzen.
3. **⚙** in der Leiste oben → Panel *To-dos*:
   - **Austeilen an**: Klasse, dann *Gesamte Klasse* **oder** die Kürzel der
     Gruppe
   - **Bearbeitungszeit**: eigenes Fenster über das Kalender-Symbol.
     **Standard (in `einstellungen.md` unter *Eigene Regeln* änderbar): Frist ist der Freitag
     der laufenden Woche, 23:45** (Abweichungen nur auf Ansage und im Plan
     genannt, z. B. KW 44: Donnerstag 20:00) — aufgegeben am Di oder Mi → Fr derselben
     Woche; aufgegeben am Fr → Fr der Folgewoche. Grund: Bei der Frist am
     Vorabend der nächsten Stunde (z. B. JF9EM, Di 09:45–23:45) haben nur 8 von
     22 bearbeitet; mit Frist Freitag bleibt Zeit zum Nachholen. Der Start darf
     nach der Stunde liegen (Startdatum/-zeit setzen, das To-do steht dann unter
     *Geplant*). Eine Diagnose, die vor der nächsten Stunde vorliegen muss,
     wird deshalb **in der Stunde** geschrieben, nicht als Hausaufgabe.
   - **Werte für alle gleich**: setzen, wenn die Aufgabe im Unterricht
     gemeinsam besprochen oder in Partnerarbeit verglichen wird. Ohne den
     Haken bekommt jedes Kind eigene Zahlen.
   - Für einen **Test** zusätzlich entscheiden: *Ergebnisanzeige
     deaktivieren*, *Wiederholen verbieten*, *Mit Startcode schützen*.
4. **Vor dem Klick auf Austeilen** im Chat zeigen und bestätigen lassen:

   ```
   Klasse:      <Klasse>
   Empfänger:   <Gesamte Klasse | Kürzel>
   Inhalte:     <Titel> (<ID>, <Niveau>, <n> Aufgaben, ca. <m> min)
   Frist:       <TT.MM.JJ, HH:MM>
   Optionen:    <Werte für alle gleich | Testoptionen | keine>
   Bestand:     <keine Überschneidung | <Kürzel> hat <ID> bereits (aktuell/geplant) — ausgenommen>
   ```

5. Austeilen, Bestätigung abwarten, Ergebnis in einem Satz melden.
6. Bei mehreren Gruppen: Schritt 2–5 je Gruppe wiederholen. Der erste
   Durchgang wird immer bestätigt, die weiteren nur, wenn der Nutzer nicht
   „mach die anderen genauso" sagt.

### Pflichtpaket für eine Kürzelliste

Nennt die Lehrkraft selbst eine Liste von Kürzeln (z. B. Grundlagen-Paket für alle,
denen im Kopfrechentest etwas fehlt), ist das keine Gruppenbildung aus der
Auswertung: die Liste wörtlich übernehmen, **gegen die Kürzel in bettermarks
abgleichen** (Schreibweisen weichen ab) und Abweichungen vor dem Austeilen nennen.
Wer in mehreren Zuweisungen landet — auch in einer, die bereits unter *Aktuell*
oder *Geplant* steht — bekommt die Übung nur einmal: das Kürzel aus dem **neuen**
Paket herausnehmen, den bestehenden Auftrag nicht anfassen.

### Fristen nachträglich ändern

To-do → ⋮ → *Datum ändern*. Die Zeitfelder sind Spinbuttons: hineinklicken und
mit **Pfeiltasten** stellen (Tippen greift unzuverlässig), danach die
`aria-label` der Gruppen lesen (`Abgabezeit: 20:00`) und erst dann speichern.
Bei verdecktem Tab hängt das Panel in der Animation — Tücken und Abhilfe in der
Referenz. Jede Zeile (Teilgruppe) hat ein eigenes To-do; alle ändern, dann die
Liste neu laden und die Uhrzeiten zählen.

### Nach dem Austeilen

Nennen, was der Nutzer noch tun muss:

- Die Zuweisung gehört als Hausaufgabe in den **Schulportal-Eintrag** der
  Stunde — mit Frist, aber **ohne Kürzel** (Schüler und Eltern lesen mit).
  Formulierung: `Bis Dienstag: bettermarks-Aufgaben bearbeiten`. Für
  differenzierte Zuweisungen reicht ein neutraler Satz; wer was bekommen hat,
  sieht jedes Kind in seinem eigenen Konto. Dafür `wochenplanung` aufrufen.
- Steht ein Computerraum-Block an, die Zuweisungen **vorher** anlegen.

## Als Hausaufgabe werten

Nach Ablauf der Frist aus der Auswertungsdatei je Kind und Zuweisung:

| Wert | Wann |
|---|---|
| `gemacht` | bearbeitet, auch mit schwachem Ergebnis, wenn es am **Können** liegt |
| `teilweise` | nur ein Teil bearbeitet, oder offensichtlich durchgeklickt ohne Versuch (**Lust**, nicht Können) |
| `fehlt` | nichts bearbeitet |

Ob ein schwaches Ergebnis Können oder Lust ist, entscheidet die Lehrkraft aus dem
Unterricht — Grenzfälle mit Prozentwert vorlegen, nicht selbst festlegen.
Ergebnis als Liste mit Kürzeln an die Lehrkraft; nach Freigabe als Ereignisse mit
`thema: bettermarks` anhängen (Skill `schuelerdaten`) und die 3×-Regel prüfen.

## Übergaben

| Bedarf | Skill |
|---|---|
| Die Zuweisung in die Woche und ins Schulportal eintragen | `wochenplanung` |
| Eigenes Arbeitsblatt statt bettermarks-Aufgaben, Papier-Backup | `arbeitsblatt` |
| Buchaufgaben und BiBox-Material zum selben Thema | `buchaufgaben` |
| Klassenarbeit, Übungsarbeit, Checkliste zum Thema | `klassenarbeit` |
| Punkte einer geschriebenen Arbeit in Noten | `notenauswertung` |
| Elternschreiben, wenn ein Kind wiederholt nichts bearbeitet | `elternbrief` |
| Hausaufgabenwertung als Ereignisse, 3×-Regel | `schuelerdaten` |
| bettermarks-Schnitt als mündliche Leistung ins Portal | `schulportal-leistung` |
| Die ganze Freitagsroutine in einem Lauf | `wochenabschluss` |

`wochenplanung` ruft diesen Skill auf, wenn im Plan eine Computerraumstunde
oder eine bettermarks-Hausaufgabe steht.

## Referenz fortschreiben

Nach jedem Lauf `bettermarks-plattform.md` in der **Quelle** `$SKILLS/references/`
ergänzen (nicht die installierte Kopie unter `${CLAUDE_PLUGIN_ROOT}`):

- neu abgelesene **Buch-IDs**
- Inhalte, die sich bewährt haben, mit ID und Einschätzung
- neu erlebte Tücken der Oberfläche
- was aus dem Abschnitt *Ungeprüft* geklärt wurde

**Nur eintragen, was gesehen wurde.** Ein `*offen*` ist besser als eine
geratene ID.
