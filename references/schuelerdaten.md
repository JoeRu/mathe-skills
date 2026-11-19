# Schülerdaten — Aufbau und Regeln

Ablage für das, was sich über ein Schuljahr über einzelne Kinder ansammelt:
Hausaufgaben, Absprachen, Elternkontakte, Beobachtungen. Strukturiert genug,
um die 3×-Regel zu rechnen, offen genug für Sätze, die in keine Spalte passen.

## Die Trennlinie

| Was | Wo | Wer sieht es |
|---|---|---|
| **Klarnamen** | `Personenbezogenes/schluessel-<KURS>.csv` | nur die Lehrkraft |
| Pseudonym ↔ bettermarks-Kürzel | `Schuelerdaten/<KURS>/kuerzel-map.csv` | Lehrkraft und Assistent |
| Ereignisse, Profile | `Schuelerdaten/<KURS>/` | Lehrkraft und Assistent |

**Die Schlüsseldatei wird nie in die Cloud übertragen und nie von Claude
gelesen.** Sie wird ausschließlich von den Werkzeugen in `$SKILLS/scripts/schuelerdaten/` auf dem
eigenen Rechner benutzt, um Klarnamen in Pseudonyme zu übersetzen. In den
Ereignissen steht danach nur noch `S07`.

Die Kürzel-Map ist der Kompromiss: sie enthält die bettermarks-Kürzel (`MaMu`),
damit Auswertungen lesbar bleiben und sich mit bettermarks verbinden lassen.
Die Kürzel sind aus den Namen gebildet, also nur schwach pseudonym — sie
tauchen aber in bettermarks ohnehin auf.

**Beides ist git-ignoriert.** Pseudonyme Verhaltensdaten bleiben
personenbezogen, solange der Schlüssel existiert. `Schuelerdaten/` gehört
deshalb genauso wenig ins Repository wie `Personenbezogenes/`.

## Ordner

```
$SKILLS/scripts/schuelerdaten/          die Werkzeuge (gemeinsam für alle)
    schluessel_anlegen.py    Kursliste -> Schlüssel, Kürzel-Map, Profile
    ereignis.py              Ereignisse anhängen (einzeln oder als Stapel)
    auswerten.py             3x-Regel, Sonderaufgaben, Verlauf je Kind
    elternbrief_hausaufgaben.py  Brief nach der 3x-Regel aus der Vorlage des Schulpakets

Schuelerdaten/                          im Schulordner der Lehrkraft (ein Ordner je Kurs)
  README.md                  kurzer Hinweis auf diese Referenz
  2026-27_KURSID/
    ereignisse.jsonl         das Protokoll, nur anhängen
    kuerzel-map.csv          Pseudonym <-> bettermarks-Kürzel
    profile/S01.md ...       je Kind eine Datei, Kopfdaten plus Freitext
```

## Das Ereignisprotokoll

`ereignisse.jsonl` — eine JSON-Zeile pro Ereignis, **nur anhängen, nie
überschreiben, nie löschen**. Eine Korrektur ist ein neues Ereignis, kein
geänderter alter Eintrag. Nur so bleibt belegbar, worauf sich ein Elternbrief
stützt.

```json
{"datum": "2026-09-11", "pseudonym": "S08", "art": "hausaufgabe",
 "wert": "fehlt", "fach": "Mathematik", "erfasst": "2026-09-12",
 "quelle": "Schulportal", "thema": "", "notiz": ""}
```

`datum` ist der Tag, an dem es passiert ist, `erfasst` der Tag der Eintragung —
bei Nachträgen aus dem Schulportal fallen die auseinander.

### Arten und Werte

| art | erlaubte Werte | wofür |
|---|---|---|
| `hausaufgabe` | gemacht · fehlt · teilweise · entschuldigt · nachgereicht · nachgearbeitet | die Vollständigkeitskontrolle |
| `sonderaufgabe` | vereinbart · erledigt · nicht erledigt | individuelle Absprachen, `thema` nennt die Aufgabe |
| `elternkontakt` | brief · gespraech · telefonat · mail | `thema` nennt den Anlass |
| `material` | dabei · fehlt | Geodreieck, Taschenrechner, Heft |
| `beobachtung` | Freitext | alles, was sich nicht kategorisieren lässt |
| `test` | Freitext (Punkte, Prozent) | Kopfrechnen, kurze Tests |
| `kurswechsel` | eintritt · austritt | Zu- und Abgänge im Schuljahr (`kurse.md`, *Zu- und Abgänge*) |

`entschuldigt` und `nachgereicht` zählen **nicht** als Versäumnis — die
Aufgabe gilt als erbracht.

`nachgearbeitet` ist etwas anderes und die wichtigste Unterscheidung hier:
das Kind hat die versäumten Aufgaben aufgeholt. **Die Versäumnisse bleiben für
die Note stehen**, aber ein Elternbrief ist nicht mehr fällig.

### Zwei Zählungen, nicht eine

| Zählung | wofür | wird zurückgesetzt |
|---|---|---|
| **offen** | die 3×-Regel, also der Elternbrief | ja |
| **gesamt** | die sonstige Mitarbeit, also die Note | **nie** |

**Zurückgesetzt** wird die offene Zählung durch zwei Ereignisse:

1. einen `elternkontakt`, dessen `thema` oder `notiz` das Wort „Hausaufgab"
   enthält — der Brief ist raus, danach beginnt die Zählung von vorn;
2. ein `hausaufgabe` mit `wert=nachgearbeitet` — die Nacharbeit ist anerkannt.

Für die Note ändert beides nichts. `auswerten.py` zeigt deshalb beide Listen
und schreibt bei der Gesamtzählung dazu, wie viele Versäumnisse schon
abgegolten sind.

Kein Zählerstand wird gespeichert; alles wird bei jeder Auswertung neu aus dem
Protokoll gerechnet. So kann er nicht veralten und der Brief nicht zweimal
ausgelöst werden.

### Codes sind nur im Kurs eindeutig

`S08` und `MaMu` gelten **innerhalb eines Kurses**. In einem zweiten Kurs gibt es wieder ein `S08`.
Deshalb wird jede Auswertung, jedes Werkzeug und jede Tabelle mit `--kurs` bzw. einer Spalte `kurs`
geführt, und im Gespräch werden Codes bei mehr als einem aktiven Kurs mit dem Kurznamen genannt
(`<Kurzname>/S08`). Die Werkzeuge brechen bei einem unbekannten Kursschlüssel ab und legen nie
still einen neuen Bestand an.

**Ausgetretene Kinder** (`kurswechsel=austritt` als letztes Ereignis) nimmt `auswerten.py` aus
`--briefe` und der Übersicht heraus und listet sie getrennt; ihre Versäumnisse bleiben für die Note.

## Die Profile

`profile/S08.md` — YAML-Kopf für das Strukturierte, darunter freier Text:

```markdown
---
pseudonym: S08
kurs: 2026-27_KURSID
kuerzel: MaMu
niveau: B
foerderbedarf: nein
nachteilsausgleich: nein
---

## Beobachtungen

### 12.09.2026
Rechnet antiproportional sicher, erkennt die Art der Zuordnung nicht.
Mutter hat um Zusatzaufgaben gebeten, P49B/53VC/AB5B zugeteilt.
```

Immer mit Datum als Überschrift, neueste Einträge unten. Keine Diagnosen,
keine Vermutungen über Gesundheit oder Familie — was beobachtet wurde, nicht
was es bedeuten könnte.

## Ablauf

**Einmal pro Kurs:**

```
python3 $SKILLS/scripts/schuelerdaten/schluessel_anlegen.py --kurs 2026-27_KURSID ^
   --liste "..\Personenbezogenes\Kursliste_Mathematik-7_20260909101618.xlsx"
```

**Nach einer Stunde oder beim Nacharbeiten aus dem Schulportal:**

```
python3 $SKILLS/scripts/schuelerdaten/ereignis.py --kurs 2026-27_KURSID --datum heute ^
   --art hausaufgabe --wert fehlt --datei fehlende.txt --quelle Schulportal
```

`fehlende.txt` ist eine schlichte Liste, ein Name pro Zeile — Klarname,
Kürzel oder Pseudonym, gemischt erlaubt. Die Klarnamen stehen nur in dieser
Hilfsdatei und werden nicht gespeichert; danach kann sie gelöscht werden.

**Einen ganzen Zeitraum auf einmal** — etwa alles, was im Schulportal schon
erfasst ist — über eine Tabelle mit Semikolon, Kopfzeile
`datum;wer;art;wert;thema;quelle;notiz` (alles ab `thema` darf fehlen;
`notiz` steht bewusst zuletzt, damit ein Semikolon im Freitext nichts
verschiebt):

```
python3 $SKILLS/scripts/schuelerdaten/ereignis.py --kurs 2026-27_KURSID --quelle Schulportal ^
   --tabelle 2026-27_KURSID\uebertrag-schulportal-2026-09-13.csv --probe
```

`--probe` zeigt nur, was geschrieben würde. Ohne `--probe` wird angehängt.
Zweimal laufen lassen heißt zweimal eintragen — das Protokoll kennt keine
Dubletten, deshalb pro Tabelle genau ein Lauf.

### Wo die Hausaufgaben im Schulportal stehen

Nicht in der Historie — die zeigt je Stunde nur „N erledigte Hausaufgaben"
ohne Namen. Kindweise steht es unter

**Mein Unterricht → Kurs → Leistungen → Ausführlich**
`meinunterricht.php?a=notenTableFull&id=<KURS-ID>&halb=1`

Dort steht je Kind und Termin `gemacht` / `tlw. gemacht` / `nicht gemacht`
oder ein Strich für „nicht erfasst". Die Spaltenköpfe sind zweistufig: die
obere Zeile nennt die Kategorie (Hausaufgaben, Mitarbeit, Kopfrechentest,
Bonusaufgabe) mit `colspan`, die untere Datum und Gewicht. **Die Kategorie
muss über die colspans auf die Datumsspalten abgebildet werden** — die
Reihenfolge der Kategorien allein trügt.

Übersetzung in die Werte hier: `gemacht` → `gemacht`, `tlw. gemacht` →
`teilweise`, `nicht gemacht` → `fehlt`, Strich → gar kein Ereignis.

**Vor dem Elternbrief oder wenn Claude den Stand braucht:**

```
python3 $SKILLS/scripts/schuelerdaten/auswerten.py --kurs 2026-27_KURSID --klarnamen
```

## Was noch zu klären ist

Die Pseudonymisierung schützt gegenüber der Cloud, nicht gegenüber dem
eigenen Rechner: Schlüssel und Daten liegen im selben OneDrive-Baum, wer
beides hat, hat Klarnamen. Ob Verhaltens- und Förderdaten so abgelegt werden
dürfen, richtet sich nach der Dienstanweisung des Landes und der Schule.
**Das einmal mit der Schulleitung oder der oder dem Datenschutzbeauftragten
der Schule klären** — es ist eine Frage an die Schule, keine technische.
