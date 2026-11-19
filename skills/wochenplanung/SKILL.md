---
name: wochenplanung
description: >
  Dieser Skill wird verwendet, wenn der Nutzer die kommende Unterrichtswoche
  eines Kurses plant und die Stunden im Schulportal vorab anlegt — etwa
  "Wochenplanung für nächste Woche", "plan mir die Woche in der 7", "was mache
  ich nächste Woche in Mathe", "Plan für KW 38", "trag die Stunden im
  Schulportal ein" oder "wir sind bei Prozentrechnung, wie geht es weiter".
  Beginnt mit einer Rückschau auf die Vorwoche (Plan gegen das, was die Lehrkraft
  erfasst hat, mit Rückfragen zu Abweichungen), plant dann nach dem Rhythmus des
  Kurses, rückwärts vom Arbeitstermin, entscheidet je Stunde zwischen vorhandenem
  und neuem Material, legt die Stunden im Schulportal an und benennt, welches
  Material noch erstellt werden muss.
metadata:
  version: "0.9.0"
---

# Wochenplanung Mathematik

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` lesen
(Kurse, Ordnerstruktur, Fachcurriculum, Datenschutz), dann
`${CLAUDE_PLUGIN_ROOT}/references/kurse.md` und für den Portal-Teil
`${CLAUDE_PLUGIN_ROOT}/references/schulportal.md`.

**Geplant wird immer für einen Kurs**, bestimmt nach `grundlagen.md` (*Kurswahl*). Mehrere Kurse in
einer Woche: ein Plan je Kurs. Material, das beide brauchen, wird einmal erstellt (`kurs.py parallel`
zeigt Parallelkurse); Ausgeteiltes, Termine und Hausaufgaben bleiben je Kurs.

## Zweck

Jede Woche dieselbe Denkarbeit: Wo steht die Klasse, was passt in die
verbleibenden Stunden, was ist letzte Woche liegen geblieben, welches
Material fehlt — und danach dasselbe Abtippen im Schulportal.
Dieser Skill hält Reihenfolge, Format und Eintragsweg fest, sodass nur noch
die inhaltlichen Entscheidungen zu treffen sind.

Der Schulportal-Eintrag ist zugleich **Nachweis**: vorab angelegt ist er das
*Soll* der Stunde, nach der Stunde ändert die Lehrkraft ihn auf das *Ist*. Beides
zusammen zeigt später, welche Ziele tatsächlich erreicht wurden. Deshalb wird
der Vorab-Eintrag so konkret formuliert, dass die spätere Korrektur klein ist —
und deshalb wird ein bestehender Eintrag **nie** überschrieben: er ist Nachweis,
nicht Entwurf.

Aus demselben Grund beginnt jede Planung mit einer **Rückschau**: Der Plan der
Vorwoche (Soll) wird gegen das gelegt, was die Lehrkraft inzwischen erfasst hat
(Ist). Geplant wird vom Ist aus, nie vom eigenen Plan.

Dieser Skill **plant und trägt ein** — er erstellt kein Material.
Dafür übergibt er an die anderen Skills des Plugins (siehe *Übergaben*).

## Zeitrahmen einer Stunde

Gerechnet wird mit dem **Stundenraster der Schule** (`$SCHULPAKET/schule.md`, *Stundenraster*;
fehlt es, einmal erfragen und dort eintragen lassen). Standard:

- **Eine Schulstunde = 45 Minuten.** Mehr Zeit gibt es nicht; ein Ablauf summiert sich auf 45.
- **Doppelstunde = 2 × 45 Minuten mit 5 Minuten Pause dazwischen.** Die Pause ist keine
  Unterrichtszeit und liegt an der **Gelenkstelle** nach den ersten 45 Minuten — der Ablauf
  wird in zwei Hälften zu je 45 Minuten geplant, nicht als 90 Minuten am Stück.
- Feste Vorlaufzeiten der Lehrkraft (z. B. Anwesenheit, Hausaufgabenkontrolle) stehen in
  `einstellungen.md` unter *Stundenrahmen* und werden von diesen Minuten abgezogen.

## Der Wochenrhythmus des Kurses

Der Rhythmus steht in `Kurse/<Kurs>/kurs.md` (`rhythmus:`). Beispiel 2026-27_KURSID:

| Block | Zeit | Länge | Rolle im Wochenverlauf |
|---|---|---|---|
| **Dienstag** | 2. Stunde | 45 min | Einstieg ins Wochenthema, Aufgreifen vom Freitag |
| **Mittwoch** | 1.+2. Stunde | 90 min | Doppelstunde — hier liegt die Erarbeitung neuer Inhalte |
| **Freitag** | 2. Stunde | 45 min | Sicherung, Üben, Kopfrechen-Test |

Im Schulportal steht die Stundenangabe genau so, wie sie dort geführt wird:
`1. - 2. Stunde` für die Doppelstunde, `2. Stunde` für eine Einzelstunde.

Hat der Kurs eine Doppelstunde, werden neue Inhalte dort erarbeitet; Einzelstunden sichern, üben
und greifen auf. Hat er keine, liegt die Erarbeitung in der längsten Stunde der Woche. Diese
Aufteilung ist der Standard und wird nur auf ausdrücklichen Wunsch verlassen. Fehlt `rhythmus` in `kurs.md`, einmal erfragen
und dort eintragen.

**Abstände zur Folgestunde** (bestimmen den Hausaufgabenumfang) aus dem
Rhythmus ausrechnen. Beim Beispiel oben: Di → Mi = 1 Tag (kleine Aufgabe) ·
Mi → Fr = 2 Tage (mittel) · Fr → Di = 4 Tage inkl. Wochenende.

## Vor einer Klassenarbeit

Steht im Klausurenplaner eine Arbeit in den nächsten zwei bis drei Wochen, wird
**rückwärts vom Termin** geplant, nicht vorwärts vom aktuellen Stand. Bewährte
Reihenfolge:

1. **Üben und differenzieren** — Bettermarks im Computerraum oder Übungsarbeit.
   Hier entsteht die Datenbasis: wer hängt woran? Für Auswahl, Zuweisung und
   Auswertung den Skill `bettermarks` aufrufen.
2. **Auswerten** — die zwei bis drei Fehlerschwerpunkte aufgreifen, Selbsttest
   oder Checkliste abgleichen.
3. **Letzte Stunde** — die zeitteuersten Aufgabentypen, die Begründungsaufgaben,
   dann Organisatorisches.

Dazu gehört:

- **Das Wochenende vor der Arbeit ist das Lernfenster.** Selbsttest und
  Checkliste müssen davor in den Händen der Klasse sein, nicht am Tag vorher.
- **Begründungsaufgaben brauchen eigene Unterrichtszeit.** Im B- und C-Kurs
  scheitert es am Formulieren, nicht am Rechnen — Satzanfänge an die Tafel.
- **In der letzten Stunde ansagen:** Gesamtpunktzahl, Taschenrechner ja oder
  nein, Schreibzeit, Notenschlüssel und mitzubringendes Material (Geodreieck
  und Bleistift, sobald ein Graph gezeichnet wird).
- **Die Doppelstunde der Arbeit als Zeitplan auslegen:** Vorlauf für Fragen und
  Austeilen, Schreibzeit, Einsammeln und Puffer.
- **Schreibzeit gegen Bearbeitungsbedarf gegenrechnen** (siehe Skill
  `klassenarbeit`). Steht deutlich mehr Zeit zur Verfügung als nötig, das
  ausdrücklich sagen — aus Zeitgründen gestrichene Aufgaben können dann zurück.

**Computerraumstunden:** Zuweisungen vorher anlegen, den Raum im Plan nennen und
ein Papier-Backup einplanen. Klemmt Netz oder Anmeldung, ist eine Doppelstunde
sonst verloren. Für Raumwechsel, Einloggen und Organisatorisches gehen in einer
Schulstunde etwa **15 Minuten** weg — die Zuweisung darf also höchstens die übrige Zeit
füllen (bei 45 min: ca. 30 min Bearbeitungszeit laut bettermarks).

## Schritte

0. **Kursordner lesen:** `kurs.py stand --kurs <Kurs>` — Niveau, Themenfolge
   (Soll/Ist, Arbeitstermine), zuletzt Ausgeteiltes. Liegt der Kurs gegenüber
   der Soll-Spalte zurück oder vorn, das im Plan benennen.
1. **Ausgangslage aus dem Schulportal lesen — nicht erfragen.**
   Das Portal weiß fast alles selbst; gefragt wird nur, was dort nicht steht.
   - **Reiter *Historie*** der Kursmappe: die letzten 3–4 Einträge zeigen,
     wo die Klasse steht, was zuletzt Hausaufgabe war und welche
     Leistungen erfasst wurden.
   - **Klausurenplaner** (Startseite): nächster Klassenarbeitstermin **dieses Kurses** — das Portal
     zeigt alle Kurse, nach der Kursbezeichnung aus `kurs.md` filtern.
   - **Kalender** (Startseite): Feiern, Feste, Ausflüge in der Zielwoche, für die Klassen des Kurses
     (`klassen:` in `kurs.md`).
   - **Vertretungsplan**: Ausfälle **dieses Kurses**.
   Nur was danach offen bleibt — etwa ob an einem Festtag Unterricht
   stattfindet — wird gefragt.
2. **Rückschau auf die Vorwoche** nach dem Abschnitt *Rückschau* unten: Soll
   gegen Ist, Rückfragen zu Abweichungen, Antworten abwarten. Was offen geblieben
   ist (nicht geschaffte Inhalte, verschobene Hausaufgaben, angekündigte, aber
   nicht geschriebene Tests), kommt zuerst in den neuen Plan, nicht als Anhang.
   Stehen in der Historie gehaltene Stunden mit Anhängen, die noch nicht in
   `ausgeteilt.csv` sind, zuerst nachtragen (Skill `kurs`).
3. **Blöcke zählen.** Ausgefallene Stunden streichen — *vor* der
   Themenverteilung. Fällt der Mittwoch aus, wird die Woche zur reinen
   Übungswoche; neuer Stoff wartet.
4. **Themen auf die Blöcke verteilen** nach dem Rhythmus oben.
   Pro Block ein Schwerpunkt, nicht zwei. Die Themenfolge steht in `themenfolge.csv`,
   die Kursdifferenzierung im Fachcurriculum der Stufe (siehe `grundlagen.md`).
5. **Ablauf skizzieren** je Block, Einstieg → Erarbeitung → Sicherung,
   mit grober Minutenangabe (Doppelstunde: zwei Hälften zu je 45 min, dazwischen 5 min Pause).
6. **Hausaufgabe je Block festlegen** (oder bewusst „keine"), Umfang nach
   der Abstandstabelle oben.
7. **Material je Block entscheiden:** `kurs.py material --kurs <Kurs> --thema <Thema>`
   zeigt, was es gibt und was dieser Kurs schon hatte. Reihenfolge nach
   `kurse.md`: noch nicht ausgeteiltes Passendes wiederverwenden → sonst anpassen
   als `_v2` → sonst neu erstellen. Die Entscheidung steht im Plan
   (*vorhanden, noch nicht im Kurs* / *wiederholt* / *anpassen* / *fehlt*).
8. **Plan im Format unten zeigen und bestätigen lassen.**
   Ohne ausdrückliches „passt" wird nichts ins Schulportal geschrieben.
   Der bestätigte Plan wird als `Kurse/<Kurs>/Wochenplan-<Kurzname>-KW<NN>-<JJJJ>.md`
   gespeichert: Er ist das **Soll** für die Rückschau der Folgewoche und wird danach
   nicht mehr geändert (das Ist steht im Portal und in der nächsten Rückschau).
9. **Schulportal befüllen** (siehe `references/schulportal.md`, Abschnitt
   Stundeneintrag) — erst nach der Bestätigung. Ausgeteiltes kommt **nicht** beim
   Vorab-Eintrag nach `ausgeteilt.csv`, sondern nach der Stunde (Schritt 2 im
   nächsten Wochenlauf, oder Skill `kurs`).
10. **Materiallücken als Angebot** ans Ende der Antwort stellen.

## Rückschau

Die Rückschau ist der erste inhaltliche Teil jeder Wochenplanung. Sie entfällt nur
in der ersten Woche eines Kurses; nach Ferien oder einer Lücke bezieht sie sich auf
die letzte Unterrichtswoche.

**Soll — was geplant war.** `Kurse/<Kurs>/Wochenplan-<Kurzname>-KW<NN-1>-<JJJJ>.md`.
Fehlt die Datei (Plan lag nur im Chat oder im Projektwissen), dort nachsehen. Gibt es
gar keinen Plan, läuft die Rückschau nur über das Ist, und das wird gesagt.

**Ist — was die Lehrkraft erfasst hat.** Jedes Mal neu lesen, nicht aus dem
Gedächtnis oder aus dem eigenen Plan:

| Quelle | Was sie zeigt |
|---|---|
| Schulportal, Historie der Vorwoche (je Stunde) | Thema, Inhalt, Hausaufgaben, Anhänge — nach der Stunde von der Lehrkraft auf das Ist geändert |
| Schulportal, erfasste Leistungen und Hausaufgabenkontrolle der Woche | was erhoben wurde (Test geschrieben? Hausaufgaben kontrolliert?) — nur als Anzahl, keine Namen |
| Vertretungsplan und Kalender der Vorwoche | ausgefallene oder vertretene Stunden |
| `ausgeteilt.csv`, Zeilen der Vorwoche | was wirklich ausgeteilt wurde |
| Ergebnis des Skills `wochenabschluss`, falls gelaufen | bettermarks-Diagnose (sitzt / wackelt), Hausaufgabenquote, offene Punkte |
| Notizen der Lehrkraft in `kurs.md` oder im Chat | alles, was das Portal nicht weiß |

**Abgleich je Block.** Jede geplante Stunde bekommt genau einen Befund:

| Befund | Bedeutung |
|---|---|
| *wie geplant* | Eintrag wurde geändert oder bestätigt und deckt sich mit dem Plan |
| *geändert* | Thema, Inhalt oder Hausaufgabe weichen ab — benennen, was |
| *nicht geschafft* | ein Teil des Plans fehlt im Ist |
| *ausgefallen / vertreten* | Stunde fand nicht oder nicht bei der Lehrkraft statt |
| *zusätzlich* | im Ist steht etwas, das nicht geplant war |
| *Eintrag unverändert* | der Vorab-Eintrag steht noch wortgleich da — offen, ob so gehalten oder nur nicht nachgetragen |

**Rückfragen — „Was ist anders gelaufen als geplant?"** Gefragt wird nur, was die
Aufzeichnungen nicht beantworten, in einem Durchgang und so konkret wie möglich:

- zu jeder Abweichung der **Grund**, soweit er die Planung ändert: Zeit zu knapp,
  Verständnis, Störung, Ausfall, bewusst umgestellt. Beispiel: „Mittwoch war das
  AB Prozentwert geplant, eingetragen ist nur die Buchseite — nicht geschafft oder
  bewusst weggelassen?"
- zu *Eintrag unverändert*: „So gehalten, oder noch nicht nachgetragen?" Bis zur
  Antwort gilt die Stunde **nicht** als wie geplant gelaufen.
- zu angekündigten Tests, Hausaufgaben und Abgaben, die im Ist nicht auftauchen.
- immer zum Schluss eine offene Frage: „Gibt es sonst etwas aus der Woche, das ich
  für die Planung wissen sollte?" (Tempo, Stimmung, was besser lief als gedacht).

Gibt es keine Abweichung, reicht ein Satz mit dieser einen offenen Frage. Höchstens
fünf Fragen; mehr Abweichungen werden zusammengefasst. **Die Antworten abwarten,
bevor geplant wird.** Ist die Lehrkraft nicht da (geplanter Lauf), wird mit der
vorsichtigsten Annahme geplant (*unverändert* = nicht gesichert, *nicht geschafft* =
nachholen), und jede Annahme steht sichtbar in der Rückschau.

**Folgen für den neuen Plan.**

- Nicht Geschafftes und Verschobenes steht im neuen Plan **vorn**; der neue Stoff
  rückt entsprechend, notfalls in die Folgewoche (*Für die Folgewoche vormerken*).
- Verschiebt sich dadurch der Abstand zur Klassenarbeit oder zur Soll-Spalte der
  `themenfolge.csv`, wird das benannt.
- Wiederholt sich ein Muster über zwei, drei Wochen (z. B. die Einzelstunde am
  Dienstag schafft regelmäßig nur zwei von drei Punkten), wird eine Regel
  vorgeschlagen — für `kurs.md` (*Regeln*) oder `einstellungen.md` (*Stundenrahmen*)
  — und erst nach einem Ja eingetragen.
- Die Rückschau steht mit den Antworten der Lehrkraft im neuen Plan. Der alte Plan
  wird nicht nachträglich geändert.

In die Rückschau gehören keine Namen und keine Kürzel; Beobachtungen zu einzelnen
Kindern gehören in die Schülerdaten (Skill `schuelerdaten`).

## Format

```markdown
# Wochenplanung <Kurs> — KW <NN> (<TT.MM.> – <TT.MM.JJJJ>)

**Stand:** <wo der Kurs steht, Soll/Ist laut themenfolge.csv>  ·  **Blöcke diese Woche:** <n>

## Rückschau KW <NN-1>
| Block | Geplant (Soll) | Erfasst (Ist) | Befund | Grund / Antwort der Lehrkraft |
|---|---|---|---|---|
| Di <TT.MM.> | <Thema, Hausaufgabe> | <Thema, Hausaufgabe laut Portal> | <wie geplant / geändert / …> | <Stichwort> |

**Quellen:** Plan KW <NN-1> · Schulportal-Historie (gelesen am <TT.MM.JJJJ>) · <Wochenabschluss / ausgeteilt.csv>
**Mitgenommen in diese Woche:** <Stichpunkte oder „nichts">
**Annahmen (unbeantwortet):** <nur wenn Fragen offen geblieben sind>

## Dienstag <TT.MM.>, 2. Stunde (45 min)
| | |
|---|---|
| **Thema der Stunde(n)** | <eine Zeile — geht wörtlich ins Portalfeld> |
| **Inhalt** | <Stichpunkt> · <Stichpunkt> · <Stichpunkt> — je einer pro Zeile im Portal |
| **Hausaufgaben** | `Bis <Wochentag>:` + <Aufgabe> |
| **Bonusaufgabe** | `Bonusaufgabe (optional): <Aufgabe>` — oder weglassen |
| **Material** | <Blatt/Buchseite> — *vorhanden, noch nicht im Kurs* / *wiederholt* / *anpassen (_v2)* / *fehlt* |
| **Ablauf (nur für mich)** | Einstieg (<n> min): … · Erarbeitung (<n> min): … · Sicherung (<n> min): … |

## Mittwoch <TT.MM.>, 1.+2. Stunde (90 min)
(gleiche Tabelle, Ablauf in zwei Hälften zu je 45 min mit 5 min Pause dazwischen)

## Freitag <TT.MM.>, 2. Stunde (45 min)
(gleiche Tabelle)

## Material, das noch entsteht
- [ ] <Was> — für <Block> — passender Skill: <arbeitsblatt / kopfrechnen / …>

## Für die Folgewoche vormerken
- <Punkte, die diese Woche nicht mehr reinpassen>
```

Der bestätigte Plan liegt als Markdown-Datei im Kursordner (Schritt 8), im Chat und
als Einträge im Schulportal. Auf Wunsch wird er zusätzlich als
`Wochenplan-<Kurzname>-KW<NN>-<JJJJ>.docx` daneben abgelegt, nach den Regeln in
`${CLAUDE_PLUGIN_ROOT}/references/dokumente.md`. Die Zeile „Ablauf (nur für mich)"
und die Rückschau gehen nie ins Portal.

## Schulportal-Eintrag

Klickweg, Formularfelder, Tücken des Datepickers, Schreibweisen und die Regeln fürs
Eintragen stehen in `${CLAUDE_PLUGIN_ROOT}/references/schulportal.md`, Abschnitt
*Stundeneintrag* — vor dem ersten Eintrag lesen. In Kürze:

- Erst Historie prüfen; bestehende Einträge sind Nachweis und bleiben unangetastet.
- Datum nur über das Kalender-Symbol, Schulstunden erst bei geschlossenem Datepicker.
- Vor dem Speichern zeigen und bestätigen lassen; Sichtbarkeits-Haken standardmäßig aus.
- Kein `<offen>`, keine Schülernamen, keine Kürzel in Portalfeldern.

## Regeln

- **Erst lesen, dann planen.** Die Historie der Kursmappe wird gelesen,
  bevor irgendetwas geplant wird — nicht der eigene Eindruck vom letzten Mal.
- **Keine Planung ohne Rückschau.** Geplant wird vom Ist der Vorwoche aus. Ein
  unverändert stehender Vorab-Eintrag ist kein Beleg, dass die Stunde so lief.
- **Klassenarbeitstermin immer prüfen.** Steht im Klausurenplaner eine Arbeit
  in den nächsten drei Wochen, ist die Woche Übungs- und Wiederholungswoche,
  kein neuer Stoff — dann gilt der Abschnitt *Vor einer Klassenarbeit*.
- **Ausgeteiltes ist eingefroren.** Ein Blatt, das irgendein Kurs in der Hand hat
  (`kurs.py eingefroren <datei>`), wird nicht mehr geändert. Verbesserungswünsche
  wandern in eine `_v2` oder in noch nicht ausgeteilte Dokumente. Bereits
  gehaltene Stunden werden nicht mitgeplant.
- **Wochentage und Daten ausrechnen, nie schätzen.** Ein um einen Tag
  verschobener Plan ist wertlos. Auch prüfen, ob die erste geplante Stunde
  heute schon stattgefunden hat.
- **Die Checkliste des Themas ist die verbindliche Grundlage.** Welche für diesen
  Kurs gilt und wann die Arbeit ist, steht in `themenfolge.csv` — vor der Planung lesen.
- **Erst bestätigen, dann eintragen.** Nichts geht ungefragt ins Schulportal.
- **Nur echte Blöcke.** Ausfälle werden abgezogen, bevor Themen verteilt werden.
- **Ein Schwerpunkt pro Block.** Lieber Puffer als zwei halbe Themen.
- **Höchstens n−1 der n Wochenstunden neuer Stoff** (n aus dem `rhythmus` des Kurses) — eine bleibt Puffer.
- **Nichts erfinden:** keine Buchseiten, Aufgabennummern oder
  Bettermarks-Zuweisungen, die nicht genannt wurden. Unbekanntes wird
  im Plan `<offen>` geschrieben. Bei fehlenden **Buchseiten und
  Aufgabennummern** wird nicht gefragt, sondern der Skill `buchaufgaben`
  aufgerufen — der schlägt in der BiBox nach und füllt die Lücke.
- **Vor jeder Klassenarbeit** steht eine Übungsstunde und eine Checkliste im
  Plan — die Checkliste zum Thema legt den prüfbaren Stoff fest und wird
  zuerst gelesen (siehe Skill `klassenarbeit`).
- **Datum immer TT.MM.JJJJ**, Wochen immer als `KW <NN>`.
- **Fachbegriffe korrekt schreiben,** auch wenn ein Alteintrag es anders
  tut: *antiproportional* (nicht „anto-"), *AB* groß.
- **Bonusaufgabe** wird angeboten, wenn sich eine anbietet — immer als
  letzter Punkt und immer mit dem Zusatz `(optional)`.

## Übergaben

Der Plan erstellt kein Material. Für jeden Eintrag unter
„Material, das noch entsteht" wird der passende Skill dieses Plugins genannt
und auf Wunsch aufgerufen:

| Bedarf | Skill |
|---|---|
| Buchseiten und Aufgabennummern, BiBox-Material | `buchaufgaben` |
| Übungs-/Arbeitsblatt | `arbeitsblatt` |
| Kopfrechenblatt, Rechentraining | `kopfrechnen` |
| Klassenarbeit, Übungsarbeit, Nachschreiber, Checkliste | `klassenarbeit` |
| Punkte → Noten, Notenspiegel | `notenauswertung` |
| bettermarks: Ergebnisse auswerten, Aufgaben zuweisen | `bettermarks` |
| Elternbrief (z. B. 3× Hausaufgaben gefehlt) | `elternbrief` |
| Stand des Kurses, Ausgeteiltes nachtragen, Arbeitstermin eintragen | `kurs` |

## Noch offen

Beim ersten echten Wochenlauf ergänzen:

- Ob die Regel „neuer Stoff gehört in die Mittwochs-Doppelstunde" auch in
  Übungs- und Wiederholungswochen trägt.
