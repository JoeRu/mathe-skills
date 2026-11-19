# Kurse — Aufbau und Regeln

Ein **Thema** hat Material, ein **Kurs** hat Unterricht. Derselbe Stoff läuft in
verschiedenen Kursen zu verschiedenen Zeiten und in verschiedenem Tempo; was ein
Kurs schon bekommen hat, steht deshalb beim Kurs, nicht beim Material.

## Ablage

```
Kurse/<Schuljahr>_<Kurs-ID>/        z. B. Kurse/2026-27_KURSID/
  kurs.md          Steckbrief (YAML-Kopf + Notizen)
  themenfolge.csv  Soll und Ist je Thema
  ausgeteilt.csv   was der Kurs bekommen hat, eine Zeile je Datei und Einsatz
  Wochenplan-<Kurzname>-KW<NN>-<JJJJ>.md  bestätigter Wochenplan (Soll) mit Rückschau; ohne Namen
  Elterninfo-…docx                        ohne Namen
  _intern/<Thema>/…                       Scans, Korrekturen, Punkte, bettermarks-Exporte (git-ignoriert)
```

Der Ordnername ist der **Kursschlüssel**. Er wird überall gleich verwendet:
`Schuelerdaten/<Kursschlüssel>/`, `Personenbezogenes/schluessel-<Kursschlüssel>.csv`,
`--kurs <Kursschlüssel>` in den Werkzeugen. Das Schuljahr gehört dazu, weil sich
Kurs-IDs in späteren Jahren wiederholen.

Kursordner sind versioniert, **außer `_intern/`**. Außerhalb von `_intern/` stehen keine Namen,
Schülercodes oder Punkte. Alles, was bei Korrektur und Auswertung entsteht, liegt in
`_intern/<Thema>/` (Aufbau: `grundlagen.md`, *Der Kursordner*); den Pfad liefert
`kurs.py pfad`. So gehört jede Datei mit Personenbezug zu genau einem Kurs, und ein
abgeschlossener Kurs lässt sich als Ganzes archivieren oder löschen.

Der Kursschlüssel bleibt **das ganze Schuljahr gleich** — auch beim Wechsel ins zweite
Halbjahr (`halbjahr:` in `kurs.md` fortschreiben) und wenn Kinder dazukommen, gehen oder
wechseln (siehe *Zu- und Abgänge*).

## kurs.md

```markdown
---
kurs: 2026-27_KURSID
fach: Mathematik         # eines der Fächer aus einstellungen.md; bestimmt den Fachordner der Themen
kurzname: 7B-1           # kurz für Chat, Dateinamen und Codes (<Kurzname>/S08); eindeutig unter den Kursen
bezeichnung: Mathematik 7 (KURSID-IGS)
klassen: [7a, 7b, 7f]    # Stammklassen der Kinder dieses Kurses; Kurs ≠ Klasse; weglassen, wenn gleich
stufe: 7
niveau: B
schuljahr: 2026/27
halbjahr: 1
status: aktiv            # aktiv | abgeschlossen
schulportal_id: 5500     # meinunterricht.php?a=view&id=…
bettermarks_klasse: KURSID - IGS - ABC
bettermarks_testklasse: test-ABC
schuelerzahl: 21
rhythmus:
  - {tag: Dienstag, stunden: "2", minuten: 45}
  - {tag: Mittwoch, stunden: "1-2", minuten: 90}
  - {tag: Freitag, stunden: "2", minuten: 45}
---
Freitext: Besonderheiten, Absprachen mit der Parallelkollegin, Raum, Taschenrechner …

## Regeln

Regeln, die nur für diesen Kurs oder dieses Niveau gelten (z. B. Punkte je Schulstunde,
Taschenrechner je Thema, bettermarks-Frist). Vorrang: **`kurs.md` vor `einstellungen.md` vor
dem Standard der Skills.**
```

## themenfolge.csv

`;`-getrennt, UTF-8, eine Zeile je Thema in Unterrichtsreihenfolge:

| Spalte | Inhalt |
|---|---|
| `nr` | laufende Nummer |
| `thema` | Name des Themenordners (ohne Fach — der Ordner ist `<Fach des Kurses>/<Thema>/`) |
| `soll_wochen` | Umfang laut Fachcurriculum (`$SCHULPAKET/curricula/<Fach>/themenplan-<Stufe>.csv`) |
| `soll_von`, `soll_bis` | geplanter Zeitraum (`JJJJ-MM-TT`), wenn die Lehrkraft ihn festlegt — sonst leer |
| `ist_von`, `ist_bis` | tatsächlich begonnen / abgeschlossen (aus der Schulportal-Historie) |
| `arbeit_am` | Termin der Klassenarbeit (`JJJJ-MM-TT`) |
| `checkliste` | Pfad der Checkliste, die für diesen Kurs gilt (relativ zum Schulordner, beginnt mit dem Fach) |
| `status` | `offen`, `läuft`, `abgeschlossen`, `entfällt` |
| `notiz` | Kurzvermerk (z. B. „Wiederholungsarbeit angesetzt“) |

Optional ist die Spalte `arbeit_nr` (laufende Nummer der Arbeit im Schuljahr **in diesem Kurs**).
Fehlt sie, wird die Nummer aus den bisherigen Arbeiten des Kurses abgeleitet und der Lehrkraft genannt.

Die Reihenfolge und `soll_wochen` kommen aus `$SCHULPAKET/curricula/<Fach>/themenplan-<Stufe>.csv`,
das aus dem Fachcurriculum der Stufe (`$SCHULPAKET/curricula/<Fach>/<Stufe> Fachcurriculum Mathe 2024.pdf`)
abgeleitet ist. Themen, die für das Niveau des Kurses nicht vorgesehen sind,
fehlen in der Themenfolge.

## ausgeteilt.csv

| Spalte | Inhalt |
|---|---|
| `datum` | Einsatztag `JJJJ-MM-TT` |
| `thema` | Themenordner |
| `datei` | Pfad relativ zum Schulordner, beginnt mit dem Fach, genau die Fassung (`Mathematik/Zuordnungen/…_v2.docx`) |
| `art` | `ausgeteilt`, `hausaufgabe`, `arbeit`, `test`, `tafelbild`, `bettermarks`, `buch` |
| `quelle` | `schulportal`, `lehrkraft`, `claude` (ältere Zeilen: Vorname der Lehrkraft) |
| `notiz` | z. B. „nur Gruppe Basis“, bettermarks-ID, Buchseite |

Regeln:

- **Eine Zeile kommt erst hinzu, wenn es wirklich im Kurs war** — aus der
  Schulportal-Historie, auf Ansage der Lehrkraft oder nach Bestätigung eines
  Wochenplans. Ein bloß erstelltes Blatt ist nicht ausgeteilt.
- Nur anhängen. Korrekturen als neue Zeile mit Notiz.
- Nicht zuordenbare Einträge (Blatt der Stunde nicht im Ordner gefunden) mit
  `datei` leer und Beschreibung in `notiz` — nicht raten.

## Eingefroren

Eine Datei, die in **irgendeinem** `ausgeteilt.csv` steht, wird nicht mehr
verändert. Braucht ein anderer Kurs eine bessere Fassung, entsteht `…_v2` daneben;
dessen Eintrag verweist auf v2. So bleibt nachvollziehbar, wer welche Fassung hatte.

## Wiederverwenden oder neu erstellen

Für den nächsten Stoffschritt eines Kurses in dieser Reihenfolge:

1. Material im Themenordner, das **dieser Kurs noch nicht** hatte und zum Niveau passt
   → wiederverwenden.
2. Material, das dieser Kurs schon hatte → nur als bewusste Wiederholung.
3. Material eines anderen Niveaus → anpassen als `_v2`/neue Variante (`arbeitsblatt`).
4. Nichts Passendes → neu erstellen.

Die Entscheidung wird im Plan genannt, nicht stillschweigend getroffen.

## Zu- und Abgänge

Kinder kommen, gehen oder wechseln im Schuljahr; der Kurs bleibt derselbe (gleicher Kursschlüssel).

- **Zugang:** Kursliste neu exportieren und `schluessel_anlegen.py --kurs <K> --liste …` erneut
  laufen lassen. Bestehende Pseudonyme bleiben, neue kommen dazu. Dazu ein Ereignis
  `kurswechsel=eintritt` mit dem Datum (Hausaufgaben davor zählen nicht).
- **Abgang:** Das Werkzeug meldet Kinder, die nicht mehr in der Liste stehen. Sie bleiben im Bestand,
  Pseudonyme werden nie neu vergeben. Ereignis `kurswechsel=austritt` mit Datum; danach fallen sie aus
  den Briefen heraus, ihre bisherigen Ereignisse bleiben für die Note erhalten.
- `schuelerzahl` in `kurs.md` ist der Stand bei Anlage. Weicht die Zahl im Portal ab, ist das kein
  Fehler, aber die Differenz wird benannt (Skill `schulportal-leistung`).

## Parallelkurse

Parallelkurse sind aktive Kurse mit gleicher Stufe und gleichem Niveau, die dasselbe Thema haben
(`kurs.py parallel --kurs <K> --thema <T>`). Material wird einmal erstellt; Plan, Ausgeteiltes,
Termine, Korrektur und Ablage bleiben je Kurs. **Ob beide Kurse dieselbe Arbeit schreiben, wird
immer gefragt** — es kann so sein, muss aber nicht. Bei derselben Arbeit trägt jeder Kurs seinen
eigenen Termin ein, korrigiert wird getrennt, und die Kürzel-Kollisionsprüfung (Skill
`klassenarbeit`) läuft über beide Kurslisten.

## Neuer Kurs

1. `Kurse/<Schuljahr>_<Kurs-ID>/kurs.md` aus diesem Muster anlegen, Werte aus dem
   Schulportal (Kursmappe) und bettermarks. `fach` eintragen (aus `faecher:`), `kurzname` festlegen (eindeutig unter den Kursen),
   `klassen` eintragen, wenn die Kinder aus mehreren Stammklassen kommen.
2. `themenfolge.csv` aus `$SCHULPAKET/curricula/<Fach>/themenplan-<Stufe>.csv` vorbefüllen (nur Themen für das Niveau des Kurses).
3. `ausgeteilt.csv` mit Kopfzeile anlegen.
4. Schülerdaten: `$SKILLS/scripts/schuelerdaten/schluessel_anlegen.py --kurs <Kursschlüssel>`
   (siehe Skill `schuelerdaten`).
5. Einen abgeschlossenen Kurs auf `status: abgeschlossen` setzen, nicht löschen.
   Alte Kursmappen liegen im Schulportal unter **Mein Unterricht → Archiv**.
