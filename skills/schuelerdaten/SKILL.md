---
name: schuelerdaten
description: >
  Dieser Skill wird verwendet, wenn der Nutzer den Stand einzelner Kinder
  festhalten oder abfragen möchte — etwa "wer hat dreimal keine Hausaufgaben",
  "trag ein, dass X die Aufgabe nicht hatte", "für wen muss ein Elternbrief
  raus", "was haben wir mit dem Kind vereinbart", "notier das zu S08",
  "Hausaufgaben aus dem Schulportal übertragen", "welche Sonderaufgaben sind
  offen" oder "zeig mir den Verlauf von MaMu". Arbeitet auf dem
  pseudonymisierten Bestand im Ordner Schuelerdaten, rechnet die 3x-Regel aus
  dem Ereignisprotokoll und rührt die Schlüsseldatei mit den Klarnamen nie an.
metadata:
  version: "0.8.0"
---

# Schülerdaten

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` lesen
(Datenschutzregeln, Ordnerstruktur), dann `${CLAUDE_PLUGIN_ROOT}/references/schuelerdaten.md` — dort stehen Ordneraufbau, Ereignisarten und der genaue
Wortlaut der 3×-Regel.

## Die eine Regel, die alles andere bestimmt

**Die Datei `Personenbezogenes/schluessel-<KURS>.csv` wird nicht gelesen,
nicht übertragen, nicht geöffnet.** Sie enthält die Klarnamen. Sie existiert
nur für die Werkzeuge auf dem Gerät des Nutzers.

Gearbeitet wird mit **Pseudonymen** (`S08`) und, wo es der Lesbarkeit dient,
mit den **bettermarks-Kürzeln** aus `Schuelerdaten/<KURS>/kuerzel-map.csv`
(`MaMu`). Nennt der Nutzer einen Klarnamen, wird er **nicht** aufgelöst und
**nicht** wiederholt — stattdessen wird er gebeten, das Kürzel zu nennen, oder
das Werkzeug erledigt die Übersetzung auf seinem Rechner.

Weiter gilt, was in `grundlagen.md` steht: nichts davon ins Repository, nichts
ins Memory, nichts in Artefakte.

## Wo was liegt

```
Schuelerdaten/<KURS>/ereignisse.jsonl     das Protokoll, nur anhängen
Schuelerdaten/<KURS>/kuerzel-map.csv      Pseudonym <-> Kürzel
Schuelerdaten/<KURS>/profile/S08.md       Kopfdaten und Freitext je Kind
$SKILLS/scripts/schuelerdaten/*.py              die drei Werkzeuge
```

`<KURS>` ist der **Kursschlüssel** aus `Kurse/` (z. B. `2026-27_KURSID`, siehe
`references/kurse.md`); den Kurs bestimmt `grundlagen.md` (*Kurswahl*). Jeder Kurs hat einen
eigenen Unterordner; die Werkzeuge bleiben dieselben und verlangen `--kurs` (ein unbekannter
Kursschlüssel bricht ab, es entsteht nie still ein neuer Bestand). **Pseudonym und Kürzel gelten nur
im Kurs:** bei mehr als einem aktiven Kurs werden sie mit Kurs genannt (`<Kurzname>/S08`).
Zu- und Abgänge: Ereignis `kurswechsel` (`eintritt` / `austritt`), siehe `references/kurse.md`.

## Lesen

Für jede Frage nach dem Stand **das Werkzeug laufen lassen, nicht selbst
zählen**:

```
python3 $SKILLS/scripts/schuelerdaten/auswerten.py --kurs 2026-27_KURSID --klarnamen
python3 $SKILLS/scripts/schuelerdaten/auswerten.py --kurs 2026-27_KURSID --briefe
python3 $SKILLS/scripts/schuelerdaten/auswerten.py --kurs 2026-27_KURSID --wer MaMu
```

Steht kein Shell-Zugang auf dem Gerät zur Verfügung, wird `ereignisse.jsonl`
gelesen und die Auswertung **programmatisch** nachgebaut — nie im Kopf
gezählt. Die Zählregeln stehen in `references/schuelerdaten.md` und sind verbindlich.

**Es sind zwei Zählungen, und sie werden nie vermischt:**

| | wofür | zurückgesetzt durch |
|---|---|---|
| **offen** | die 3×-Regel, der Elternbrief | `elternkontakt` zum Thema Hausaufgaben **oder** `hausaufgabe=nachgearbeitet` |
| **gesamt** | die sonstige Mitarbeit, die Note | nichts |

`entschuldigt` und `nachgereicht` sind gar keine Versäumnisse.
`nachgearbeitet` dagegen **löscht nichts** — es nimmt nur den Brief vom Tisch.
Wer danach fragt, ob ein Brief fällig ist, meint die offene Zählung; wer nach
der Mitarbeit fragt, die gesamte. Im Zweifel beide nennen.

Die Profile werden gelesen, bevor über ein einzelnes Kind etwas gesagt wird —
dort steht, was sich nicht aus Zahlen ergibt.

## Schreiben

Ereignisse werden über `ereignis.py` angehängt, nicht von Hand in die Datei
geschrieben. Das Werkzeug prüft Datum und erlaubte Werte und setzt `erfasst`.

```
python3 $SKILLS/scripts/schuelerdaten/ereignis.py --kurs 2026-27_KURSID --datum 12.09.2026 ^
  --wer MaMu --art sonderaufgabe --wert vereinbart ^
  --thema "bettermarks P49B/53VC/AB5B" --notiz "mit Mutter besprochen"
```

Regeln dafür:

- **Nur eintragen, was der Nutzer gesagt hat oder was in einer Quelle steht.**
  Keine Schlüsse, keine Vermutungen. „Wirkt unkonzentriert" ist eine
  Beobachtung des Nutzers, nicht eine von Claude.
- **Mit `--probe` zeigen, was geschrieben würde**, und bei mehr als zwei bis
  drei Zeilen bestätigen lassen, bevor angehängt wird.
- **Nichts löschen und nichts ändern.** Eine Korrektur ist ein neues Ereignis
  mit heutigem `erfasst`-Datum und einer Notiz, was richtiggestellt wird.
- **Keine Gesundheits-, Familien- oder Herkunftsangaben** ins Protokoll und
  nicht in die Profile — auch nicht sinngemäß. Was in einen Förderplan gehört,
  gehört in den Förderplan.
- Freitext gehört in die Profildatei, nicht in `notiz`, sobald er länger als
  eine Zeile wird.

## Übertragen aus dem Schulportal

**Die Historie ist der falsche Ort.** Sie nennt je Stunde nur „N erledigte
Hausaufgaben" ohne Namen. Kindweise steht es unter

**Mein Unterricht → Kurs → Leistungen → Ausführlich**
`meinunterricht.php?a=notenTableFull&id=<schulportal_id aus kurs.md>&halb=1`

Ablauf:

1. Den Nutzer fragen, für welchen Zeitraum übertragen werden soll.
2. Die Tabelle im Browser lesen. Die Spaltenköpfe sind zweistufig: obere
   Zeile Kategorie mit `colspan`, untere Zeile Datum und Gewicht. **Die
   Kategorien über die colspans auf die Datumsspalten abbilden** — nur die
   Spalten der Kategorie *Hausaufgaben* sind Hausaufgaben; Mitarbeit,
   Kopfrechentest und Bonusaufgabe stehen dazwischen.
3. **Die Namen nicht in die Antwort und nicht ins Protokoll schreiben.**
   Am saubersten schon im Browser in Kürzel umrechnen (zwei Buchstaben
   Vorname + zwei Nachname, die Zelle steht als „Nachname, Vorname").
4. Eine Tabelle `datum;wer;art;wert;thema;quelle;notiz` schreiben und den Nutzer
   `ereignis.py --tabelle … --probe` laufen lassen, dann ohne `--probe`.
   Pro Tabelle genau ein Lauf — das Protokoll kennt keine Dubletten.

Werte: `gemacht` → `gemacht`, `tlw. gemacht` → `teilweise`,
`nicht gemacht` → `fehlt`, Strich → gar kein Ereignis (nicht erfasst ist
kein Versäumnis).

Steht die Hausaufgabenkontrolle im Portal nicht kindweise, wird das gesagt
statt geraten.

## bettermarks-Hausaufgaben

bettermarks-Zuweisungen zählen als Hausaufgabe. Die Wertung je Kind (gemacht /
teilweise / fehlt) entsteht im Skill `bettermarks`, Abschnitt *Als Hausaufgabe
werten*, und wird nach Freigabe durch die Lehrkraft mit `thema: bettermarks` und dem Datum
der Frist angehängt. Trägt die Lehrkraft dieselbe Wertung auch im Portal ein, beim
nächsten Portal-Übertrag nicht doppelt übernehmen — vorher mit `auswerten.py --wer`
prüfen, was zum Datum schon steht.

## Übergaben

| Bedarf | Skill |
|---|---|
| Der Brief nach dreimal fehlender Hausaufgabe | `elternbrief` |
| Punkte und Noten einer Arbeit | `notenauswertung` |
| Zuweisungen und Ergebnisse in bettermarks | `bettermarks` |
| Die Stunde und ihre Hausaufgabe im Schulportal | `wochenplanung` |

Nach jedem Elternbrief wird ein `elternkontakt`-Ereignis angehängt — sonst
läuft der Zähler weiter und der nächste Brief kommt zu früh.
