---
name: schulportal-leistung
description: >
  Dieser Skill wird verwendet, wenn Punkte oder Noten einer Arbeit ins Schulportal
  sollen — etwa "trag die Arbeit ins Schulportal ein", "leg die Leistung
  Zuordnungen an", "Punkte ins Schulportal übertragen", "Auswertungstabelle im
  Schulportal anlegen", "Berechnungsfaktor für die Arbeit setzen" oder "die Noten
  sind fertig, jetzt ins Portal", "bettermarks-Schnitt als mündliche Note
  eintragen" oder "Kopfrechentest ins Portal". Legt die Leistung mit
  Punkteverteilung und Notenskala an, überträgt die Rohpunkte je Aufgabe und
  setzt die Berechnungsfaktoren — für Arbeiten (schriftlich) und für mündliche
  Leistungen. Wird von `korrektur`, `notenauswertung` und `bettermarks` übergeben.
metadata:
  version: "0.8.0"
---

# Leistung im Schulportal anlegen und befüllen

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md`, `${CLAUDE_PLUGIN_ROOT}/references/notenschluessel.md`
und `${CLAUDE_PLUGIN_ROOT}/references/schulportal.md` lesen (Notenschlüssel,
Datenschutz).

Dieser Skill ist der letzte Schritt nach `korrektur` und `notenauswertung`: Er
trägt ein, was dort gerechnet und freigegeben wurde. Er bewertet nichts selbst.

## Voraussetzung

Eine freigegebene Punktetabelle, in der Regel
`Kurse/<Kurs>/_intern/<Thema>/Korrektur_<Arbeit>_<JJJJ-MM-TT>[_vN]/punkte_<arbeit>.csv` mit
einer Zeile je Schülercode × Teilaufgabe. **Ohne ausdrückliche Freigabe wird nichts
eingetragen** — Schüler und Eltern lesen im Portal mit.

## 0. Kurs und Kursmappe prüfen — vor jedem Schreiben

Eine Leistung gehört in genau eine Kursmappe, und Schüler und Eltern lesen dort mit. Deshalb:

1. **Kurs** nach `grundlagen.md` (*Kurswahl*) bestimmen und nennen. Die Punktetabelle muss aus dem
   `_intern/` **dieses** Kurses stammen (Spalte `kurs` stimmt).
2. **Kursmappe öffnen** über `schulportal_id` aus `kurs.md` dieses Kurses — nie über „zuletzt
   geöffnet“ oder die Liste.
3. **Abgleichen und im Chat nennen:** Titel bzw. Kennung der geöffneten Kursmappe gegen `bezeichnung`
   in `kurs.md`, Zahl der Kinder im Portal gegen `schuelerzahl`. Stimmt der Titel nicht: **nichts
   eintragen**, melden. Weicht nur die Kinderzahl ab, ist das bei Zu- und Abgängen möglich; die
   Differenz wird benannt, und die Lehrkraft bestätigt, bevor es weitergeht.

## 1. Leistung anlegen

**Mein Unterricht → Leistungen → + Leistung**

| Feld | Wert |
|---|---|
| Name | Titel der Arbeit, z. B. `Arbeit Zuordnungen` |
| Datum | Tag der Arbeit, nicht der Korrektur (z. B. 16.09.2026) |
| Notenart | `schriftlich` |
| Erfassung | `Auswertungstabelle zur Eingabe von (Roh-)Punkten einzelner Aufgaben` |
| Fehlerindex | `Ohne` |
| Notenskala | `Noten mit Tendenzen` |
| Anzahl der Aufgaben | genau so viele wie in der Arbeit |

Die Zahl der Aufgaben aktualisiert die Eingabebereiche darunter — erst setzen,
dann weiterfüllen.

## 2. Punkteverteilung

Je Aufgabe eine Zeile: **Name der Aufgabe** und **maximal erreichbare Punkte**,
in der Reihenfolge der Arbeit. Die Namen so schreiben, wie sie auf dem Blatt und
in der Auswertung stehen (`1 Wertetabellen`, `2 Art der Zuordnung`, …), damit
Schüler die Rückmeldung zuordnen können.

Die Summe muss der Gesamtpunktzahl der Arbeit entsprechen — vor dem Speichern
programmatisch gegen die CSV prüfen, nicht im Kopf addieren.

**Bonus oder Zusatz** wird nur gefüllt, wenn es in der Arbeit optionale Punkte
gab. Sonst bleibt das Feld leer.

## 3. Notenskala

- **Tendenzbereich: 33** (das obere und untere Drittel eines Intervalls ergeben
  + und −)
- **Notenverteilung**: der Schlüssel der Schule aus `notenschluessel.md` — 1 ab 95 %,
  2 ab 80 %, 3 ab 65 %, 4 ab 50 %, 5 ab 25 %, darunter 6. Die Punktgrenzen
  liefert `python3 $SKILLS/scripts/noten.py schluessel <gesamt> --tendenz`.

Die vom Portal errechneten Notengrenzen mit denen aus `notenauswertung`
vergleichen und Abweichungen benennen, bevor etwas gespeichert wird.

## 4. Punkte eintragen

Je Kind die Rohpunkte der einzelnen Aufgaben — nicht die Summe, die rechnet das
Portal. Reihenfolge und Aufgabenzahl müssen zur Punkteverteilung passen.

**Hier ist die Namensauflösung nötig**, denn das Portal führt Klarnamen, die CSV
führt Codes. Dafür gilt:

- Die Zuordnung Code → Name passiert **im Browser**, nicht in der Antwort und in
  keiner Datei. Die Schlüsseldatei `Personenbezogenes/schluessel-<KURS>.csv`
  wird nicht geöffnet (siehe `schuelerdaten`).
- Im Chat wird über Codes gesprochen: „S11 hat 22 Punkte", nie der Name.
- Vor dem Speichern die eingetragene Spalte gegen die CSV zurücklesen: Summe und
  Note je Kind müssen übereinstimmen. Abweichungen zuerst melden.

Fehlende Kinder (Nachschreiber) bleiben leer und werden benannt — kein Eintrag
von 0 Punkten für eine nicht geschriebene Arbeit.

## 5. Berechnungsfaktoren

**Mein Unterricht → Leistungen → Berechnungsfaktoren**

- Faktor der Arbeit: **1**
- Schriftlich und mündlich zählen je 50 %, im Portal also **beide Bereiche auf
  100 %**

Diese Einstellung gilt für den ganzen Kurs — vor der Änderung zeigen, was
umgestellt wird, und bestätigen lassen.

## Mündliche Leistung (bettermarks-Schnitt, Kopfrechentest, Bonus)

Gleicher Weg, andere Werte:

| Feld | Wert |
|---|---|
| Name | z. B. `bettermarks Prozent`, `Kopfrechen-Test` |
| Datum | Tag der Auswertung bzw. des Tests |
| Notenart | `mündlich` |
| Erfassung | `Auswertungstabelle zur Eingabe der (Roh-)Punkte einzelner Aufgabe` |
| Notenskala | `Noten mit Tendenzen`, Tendenzbereich 33 |
| Aufgaben | **eine** Aufgabe; bei Prozentwerten mit **100 Punkten** (Prozent = Punkte) |
| Notengrenzen | Note 1–5 = 95 / 80 / 65 / 50 / 25 (bei 100 Punkten identisch mit Prozent) |

**Nicht** „Erfassung der erreichten Prozente“ wählen: Diese Erfassung erlaubt nur
„Noten (1-6)“ oder „Punkte (15-0)“, keine Tendenzen.

Voraussetzung wie bei Arbeiten: eine freigegebene Tabelle mit Kürzel und Wert
(bei bettermarks z. B. `Kurse/<Kurs>/_intern/<Thema>/bettermarks/schnitt_<JJJJ-MM-TT>.csv`,
Verfahren in `notenschluessel.md`, Abschnitt *bettermarks*). Fehlende Werte sind
bei bettermarks 0 (nicht bearbeitet), bei einem Test „nicht mitgeschrieben“ — dann leer.

Bedienung des Formulars und der Erfassungstabelle: `references/schulportal.md`,
Abschnitt *Leistungen*.

## 6. Nach dem Eintragen

- Was eingetragen wurde, in einem Satz zurückmelden: Leistung, Datum, Zahl der
  Kinder, Notenspiegel.
- Weicht der Notenspiegel im Portal von dem aus `notenauswertung` ab, ist etwas
  falsch zugeordnet — dann nicht korrigieren, sondern melden.
- Auf Wunsch die Rückgabestunde mit `wochenplanung` eintragen.

## Datenschutz

Klarnamen bleiben im Portal und im verbundenen Ordner: nicht in den Chat, nicht
ins Memory, nicht ins Repository, nicht in Artefakte. Screenshots aus dem Portal
werden nicht abgelegt.

## Übergaben

| Bedarf | Skill |
|---|---|
| Punkte und Freigabe der Korrektur | `korrektur` |
| Noten, Notenspiegel, Zeugnisnote | `notenauswertung` |
| Vermerke zu einzelnen Kindern | `schuelerdaten` |
| Rückgabestunde und Hausaufgabe | `wochenplanung` |
