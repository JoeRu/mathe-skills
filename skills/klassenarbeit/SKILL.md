---
name: klassenarbeit
description: >
  Dieser Skill wird verwendet, wenn der Nutzer eine Mathematikarbeit,
  Klassenarbeit, Übungsarbeit, Wiederholungsarbeit, einen Test oder eine
  Nachschreibearbeit erstellen möchte — etwa "Arbeit Nr. 3 zu Dreiecken",
  "Mathearbeit Vierecke mit A- und B-Version", "Übungsarbeit vor der Arbeit",
  "Nachschreiber für Montag", "Arbeit mit Pseudonym statt Name",
  "Testfassung der Arbeit zum Ansehen", "Checkliste zur Arbeitsvorbereitung"
  oder "Erwartungshorizont für die Arbeit". Erzeugt Arbeit, Parallelversion,
  Lösung mit Punkteverteilung und Notenschlüssel sowie die
  Vorbereitungscheckliste, und trägt Termin und Checkliste beim Kurs ein.
metadata:
  version: "0.9.0"
---

# Klassenarbeit erstellen

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md`,
`${CLAUDE_PLUGIN_ROOT}/references/kurse.md`,
`${CLAUDE_PLUGIN_ROOT}/references/notenschluessel.md` und
`${CLAUDE_PLUGIN_ROOT}/references/dokumente.md` lesen.

## 1. Rahmen klären

- **Kurs** (nach `grundlagen.md`, *Kurswahl*, und genannt) → Stufe und Niveau aus `kurs.md`; Termin
  und gültige Checkliste aus `themenfolge.csv` (Spalten `arbeit_am`, `checkliste`). Fehlen sie,
  erfragen und nach der Freigabe dort eintragen (Skill `kurs`).
- **Parallelkurs?** `kurs.py parallel --kurs <Kurs> --thema <Thema>` aufrufen. Gibt es einen,
  **immer fragen**: dieselbe Arbeit für beide Kurse (dann ein Satz Blätter, jeder Kurs mit eigenem
  Termin) oder getrennte Fassungen? Es kann so sein, muss aber nicht; nichts annehmen.
- **Nummer** der Arbeit im Schuljahr **in diesem Kurs** (`Mathematikarbeit Nr. 4`; Spalte `arbeit_nr`
  in `themenfolge.csv`, fehlt sie, aus den bisherigen Arbeiten des Kurses ableiten und nennen)
- **Dauer** und daraus die Gesamtpunktzahl (Faustwert 40 Punkte je Schulstunde,
  `$SCHULPAKET/notenschluessel.md`)
- **Parallelversion** A/B gegen Abschreiben: Standard bei voller Klasse
- **Kennzeichnung** der Blätter: Namenszeile (Standard) oder **Pseudonym**
  (Kürzel) mit Nummernkästchen — Abschnitt 3
- **Testfassung** gewünscht? Dann zuerst eine Version als PDF zum Ansehen,
  erst nach der Freigabe der volle Satz — Abschnitt 7

Vorher die letzte Arbeit zum selben Thema in `<Fach>/<Thema>/Klassenarbeiten/` lesen —
Aufgabenzuschnitt, Punkteverteilung, Sprachniveau. Mit
`kurs.py material --kurs <Kurs> --thema <Thema>` prüfen, welche Übungs- und
Selbsttestblätter dieser Kurs schon hatte: Aufgaben daraus nicht 1:1 in die Arbeit.

## 2. Aufgaben zusammenstellen

Die **Checkliste** ist der verbindliche Rahmen: Was dort steht, darf drankommen;
was nicht dort steht, nicht. Existiert keine, aus dem Fachcurriculum der Stufe
(`$SCHULPAKET/curricula/<Fach>/<Stufe> Fachcurriculum Mathe 2024.pdf`, Spalte des Niveaus) ableiten
und die Checkliste gleich mit erzeugen (Schritt 6).

1. **Reproduktion** (ca. 30 % der Punkte) — Grundwissen, Definitionen, einfache Rechnung
2. **Anwendung** (ca. 50 %) — Standardverfahren auf neue Situationen
3. **Transfer** (ca. 20 %) — Begründen, Verallgemeinern, mehrschrittige Textaufgabe

Im C-Kurs den Transferanteil reduzieren und stärker vorstrukturieren.

**Punkte stehen genau einmal.** Die Klammerangabe `(n P)` gehört an die
**Teilaufgaben**, das Kästchen `_____ / n` am rechten Rand trägt die **Summe der
Aufgabe**. Die Kopfzeile einer Aufgabe bekommt keine Punktangabe — sonst steht
dieselbe Zahl zweimal auf derselben Zeilenhöhe. Hat eine Aufgabe keine
Teilaufgaben, bekommt sie welche. Die Summe aller Klammerangaben muss exakt der
Gesamtpunktzahl entsprechen — programmatisch prüfen. Geometrie mit GeoGebra vorbereiten, Abbildung
als PNG einbetten, `.ggb` daneben.

Schreibzeit gegen Bearbeitungsbedarf gegenrechnen und das Ergebnis nennen.

## 3. Kopf der Arbeit: Name oder Kürzel

**Standard** ist die Namenszeile `Dein Name: ____` im Seitenkopf. Sie läuft über
alle Seiten mit, damit jedes Blatt zugeordnet werden kann.

**Pseudonym-Fassung** (Parameter `pseudonym`), wenn die Lehrkraft die Arbeiten ohne
Namen korrigieren will:

- Statt der Namenszeile steht `Dein Kürzel: ____` im Seitenkopf.
- Das **Kürzel** sind die ersten zwei Buchstaben des Vornamens und die ersten
  zwei des Nachnamens, jeweils erster Buchstabe groß, zweiter klein:
  *Lisa Maier → LiMa*.
- Die Regel steht als **erster Hinweis in der Hinweisbox auf Seite 1** —
  vollständig, mit Beispiel. Im Seitenkopf steht sie nicht noch einmal.

**Nummernkästchen** (Parameter `nummer_box`): ein leeres Kästchen **oben rechts
auf jeder Seite**, beschriftet `Nr.`. Die Lehrkraft trägt die Schülernummer nach dem
Einsammeln ein; die Kinder lassen es frei (eigener Hinweis in der Box). Das
gedruckte `Nr.` ist zugleich der Ankerpunkt, an dem `korrektur` den
handschriftlichen Code oben rechts sucht.

Beide Parameter gehören zusammen: ein Kürzel ohne Nummernkästchen macht die
Zuordnung im Notenprogramm unnötig mühsam.

**Zusatzseite für Nebenrechnungen** (Parameter `zusatz_karo`): eine letzte Seite
mit ganzseitigem Karofeld, hinter dem Notenschlüssel. Darüber steht die
Aufforderung, zu jeder Nebenrechnung die Aufgabe dazuzuschreiben („zu 3 b") —
`korrektur` erkennt eine Nebenrechnung auf dem Zusatzblatt nur an, wenn die
Zuordnung erkennbar ist, und ein anerkannter Rechenweg entscheidet über die
halbe Punktzahl. Kopf und Nummernkästchen laufen auf der Zusatzseite mit,
damit auch ein loses Blatt zugeordnet werden kann. Die Seite zählt in den
Sollseiten mit.

Zwei Dinge vorher prüfen und der Lehrkraft nennen:

- **Kollisionen.** Zwei Kinder mit denselben vier Buchstaben bekommen dasselbe
  Kürzel. Die Kursliste des Kurses (bei gemeinsamer Arbeit die beider Kurse; Skill
  `schuelerdaten`) gegenprüfen und bei einer
  Kollision die Regel um einen dritten Buchstaben erweitern — die Lehrkraft
  entscheidet, die Regel im Hinweistext ändert sich dann mit.
- **Ein Kürzel ist ein Pseudonym, keine Anonymisierung.** Es ist innerhalb des
  Kurses eindeutig rückführbar. Blätter, Scans und Punktetabellen bleiben
  deshalb in `Kurse/<Kurs>/_intern/` und kommen nicht ins Repository.

Das Kästchen kostet Platz im Kopf: die Kopfzeile wird dafür in eine zweispaltige
Tabelle gesetzt. Danach mit `pdftotext -bbox` prüfen, dass der Titel samt
Versionsvermerk `(A)` **in einer Zeile** steht — bricht er um, wächst der Kopf
auf jeder Seite und die Arbeit wird länger. Gegenmittel: Tabulator der
Titelmitte verkleinern, nicht die Schrift.

## 4. Parallelversion A/B

Version B entsteht aus A durch **Zahlenaustausch, nicht durch andere Aufgaben**:
gleiche Struktur, gleiche Punkte, gleiche Schwierigkeit. Prüfen, dass die Zahlen in
B genauso glatt aufgehen wie in A. Nachschreibearbeit: dritte Zahlenvariante.

## 5. Lösung, Erwartungshorizont, Notenschlüssel

Je Version eine Lösungsfassung mit vollständigem Rechenweg, Teilpunkten (Ansatz,
Rechnung, Antwortsatz) und Bewertungshinweisen am Anfang (Folgefehler einmal
abziehen, Einheitenfehler 0,5 P, Ergebnis ohne Rechenweg höchstens die Hälfte).
Alle Ergebnisse programmatisch berechnen und unabhängig prüfen.

Am Ende der Arbeit Punktetabelle und Notenschlüssel mit den **Punktgrenzen**, erzeugt mit
`python3 $SKILLS/scripts/noten.py schluessel <Gesamtpunkte>` — nicht
von Hand.

## 6. Begleitmaterial

Auf Wunsch oder wenn es fehlt:

- **Checkliste** — „Das kann ich“ in Ich-Form, Ankreuzspalten, je Punkt eine
  Beispielaufgabe mit Lösung; dazu optional ein Selbsttest.
- **Übungsarbeit** — gleiche Struktur, andere Zahlen und Kontexte, mit Lösung.
- **Nachschreibearbeit** — dritte Zahlenvariante.

Checkliste und Selbsttest müssen **vor dem Wochenende vor der Arbeit** in der
Klasse sein (siehe `wochenplanung`).

## 7. Testfassung zum Überprüfen

Wird am Layout etwas geändert — Kopfzeile, Kästchen, neue Aufgabenform —, zuerst
eine **Testfassung**: nur Version A, nur PDF, ohne Lösung und ohne Word-Datei.
Sie wird vorgelegt, nicht abgelegt und nicht in `ausgeteilt.csv` eingetragen.
Erst nach „passt" entstehen A, B und die Lösungen vollständig.

Die Testfassung wird gegen die **Korrigierbarkeit durch `korrektur`** geprüft,
programmatisch mit `pdftotext -bbox`, nicht durch Ansehen allein:

1. **Seitenzahl** gegen die Sollseiten der Vorgängerfassung — wächst sie, ist
   meist der Kopf schuld.
2. **Auf jeder Seite**: Titel mit Versionsvermerk (`… (A)`), Kästchen oben
   rechts, Namens- bzw. Kürzelzeile. `korrektur` bestimmt die Version aus dem
   gedruckten Textlayer; steht der Titel auf jeder Seite, geht das auch bei
   vertauschten oder fehlenden Blättern.
3. **Ankerpunkte**: Aufgabennummern `1.` bis `n.` am linken Rand und
   Teilaufgabenbuchstaben `a)` bis `d)` müssen einzeln gefunden werden — daran
   hängt jede Randanmerkung.
4. **Keine Verwechslung**: Aufzählungen in Tabellen laufen mit Klammer (`1)`),
   Aufgaben mit Punkt (`1.`). Sonst setzt die Korrektur Anmerkungen in eine
   Ankreuztabelle.
5. **Punktekästchen** `_____ / n` je Aufgabe vorhanden, Summe gleich der
   Gesamtpunktzahl (`verify.py`).
6. **Rechter Rand frei** für die Randnotizen der Korrektur.

Das Ergebnis dieser Prüfung wird der Lehrkraft genannt, nicht nur die Datei.

## 8. Ablage und Kurs

Alles nach `<Fach>/<Thema>/Klassenarbeiten/`, Namen nach `grundlagen.md`
(`Arbeit-<Thema>-A-<Termin>.docx`, `…_Lösung.pdf`, `Checkliste-<Thema>-<JJJJ-MM-TT>.docx`).
Bestehende Dateien nie überschreiben; eine geänderte Fassung kommt als `_v2`,
`_v3` daneben, und der Generator baut beide Fassungen weiter (Parameter statt
Ersetzen), damit die alte reproduzierbar bleibt.

Nach Freigabe durch die Lehrkraft in der `themenfolge.csv` **dieses Kurses** `arbeit_am` und
`checkliste` setzen. Nach dem Schreiben der Arbeit die ausgeteilten Versionen als `art: arbeit`
in `ausgeteilt.csv` **dieses Kurses** (Skill `kurs`) — ab dann sind sie eingefroren. Schreibt ein
weiterer Kurs dieselbe Arbeit, trägt er seinen Termin und seine Zeile selbst ein; der Dateiname
(Termin des ersten Einsatzes) bleibt.

Danach in einem Satz die Dateien nennen und offen ansprechen, was die Lehrkraft prüfen
sollte: Punkteverteilung, Zeitbedarf, Passung zur Checkliste.

## Übergaben

| Bedarf | Skill |
|---|---|
| Scans korrigieren | `korrektur` |
| Punkte → Noten, Notenspiegel | `notenauswertung` |
| Übungsblätter zu Schwächen | `arbeitsblatt`, `bettermarks` |
| Termin, Übungsstunde, Rückgabestunde planen | `wochenplanung` |
| Kürzel → Name, Kursliste | `schuelerdaten` |
