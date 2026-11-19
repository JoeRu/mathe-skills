---
name: elternbrief
description: >
  Dieser Skill wird verwendet, wenn der Nutzer ein Schreiben an Eltern oder ein
  Verwaltungsdokument der Schule erstellen möchte — etwa "Elternbrief wegen
  Fehlzeiten", "Mitteilung über Fehlstunden für X", "Brief wegen dreimal keine
  Hausaufgaben", "Elterninfo zur Wiederholungsarbeit", "Elterninfo zum
  Mathewettbewerb", "Antrag auf Dienstbefreiung", "Dyskalkulie-Empfehlung",
  "Protokoll der Versetzungskonferenz" oder "Brief aus der Vorlage füllen".
  Füllt die vorhandenen Vorlagen der Schule mit erhaltenem Briefkopf.
metadata:
  version: "0.8.0"
---

# Elternbrief und Verwaltungsschreiben

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` und
`${CLAUDE_PLUGIN_ROOT}/references/dokumente.md` lesen.

## Grundregel

**Nie ein neues Dokument von Grund auf bauen.** Immer eine vorhandene Vorlage
kopieren und darin den Text ersetzen. Briefkopf, Fußzeile, Rücklaufabschnitte und
Formatvorlagen stecken in der Datei.

## Vorlagen

| Anlass | Vorlage |
|---|---|
| Fehlzeiten mitteilen | `$SCHULPAKET/vorlagen/Elternbriefe/Mitteilung über  Fehlzeiten_Vorlage.docx` |
| 3× keine Hausaufgaben / Material | `$SCHULPAKET/vorlagen/Elternbriefe/3x Keine Hausaufgaben-template.docx` |
| Mathewettbewerb, Ergebnis | `$SCHULPAKET/vorlagen/Elternbriefe/Eltern-Info zum Ergebnis der Note.docx` |
| Info an alle Eltern (z. B. Wiederholungsarbeit) | zuletzt verschickte Elterninfo desselben Anlasses (`Kurse/<Kurs>/`, ältere im Themenordner), z. B. `Mathematik/Zuordnungen/Elternbrief-Wiederholungsarbeit-Zuordnungen 2026.docx` |
| Dyskalkulie-Empfehlung | `Personenbezogenes/Dyskalkulie-Empfehlung.docx` |
| Dienstbefreiung / Lehrausflug | `Personenbezogenes/Antrag Lehrausflug Dienstbefreiung online.docx` |
| Versetzungskonferenz | `Personenbezogenes/Protokoll der Konferenz zur Feststellung der Versetzung in den Mathematik A.docx` |

Die drei letzten liegen in `Personenbezogenes/`, weil sie ausgefüllt sein können —
vor dem Kopieren prüfen, ob noch Daten eines früheren Falls darin stehen, und
diese ersetzen. Vor dem Schreiben `$SCHULPAKET/vorlagen/Elternbriefe/` auflisten; es können
Vorlagen dazugekommen sein. Passt keine, die nächstliegende kopieren und umbauen.

## 3× keine Hausaufgaben: das Werkzeug

Für diesen Anlass nicht von Hand füllen, sondern auf dem Gerät:

```
python3 $SKILLS/scripts/schuelerdaten/elternbrief_hausaufgaben.py \
  --kurs <Kursschlüssel> --datum TT.MM.JJJJ <Kürzel> [<Kürzel> …]
```

Es liest die offenen Versäumnisse aus `ereignisse.jsonl` (nur wer ≥ 3 hat), setzt
Name (aus der Schlüsseldatei, nur lokal), Datum, Anzahl und die Stundendaten ein
(„(Buch und bettermarks)“ zusammengefasst), schreibt `.docx` und `.pdf` nach
`Personenbezogenes/Elternbriefe/<Kursschlüssel>/3x Keine Hausaufgaben_<JJJJ-MM-TT>_<Kürzel>` und
überschreibt nichts (`--version v2` für eine zweite Fassung am selben Tag). Es gibt
keine Namen aus. Danach das PDF einmal ansehen (Feld für Feld) und der Lehrkraft vorlegen.

## Zu ersetzende Felder

Platzhalter stehen als `XXX`, `_______` oder leere Felder nach `Name:` /
`Klasse:` / `Unterrichtsfach:`. Typisch:

- Name des Kindes, Klasse, Unterrichtsfach
- Ort und Datum (`<Ort aus schule.md>, TT.MM.JJJJ` — heute, wenn nichts anderes gesagt)
- Anrede `Sehr geehrte Familie <Nachname>,`
- Zahlen (Fehlstunden gesamt, davon unentschuldigt, Anwesenheitsstunden)
- Unterschriftzeile mit dem Namen des Nutzers
- Ankreuzfelder ☐ in der Hausaufgaben-Vorlage

`Klasse:` ist die **Stammklasse des Kindes**, nicht der Kurs (`grundlagen.md`, *Kurswahl*). Steht sie
nicht in den Unterlagen, wird gefragt.

Den Klarnamen nennt die Lehrkraft oder die Werkzeuge in `$SKILLS/scripts/schuelerdaten/`
setzen ihn auf seinem Rechner ein — Claude löst Kürzel nicht über die
Schlüsseldatei auf. Fehlzeiten aus `Personenbezogenes/Klassenbuch_*.xlsx` bzw.
`Anwesenheitsliste.xlsx` ziehen, wenn nicht genannt, und die Werte zur Bestätigung
zeigen, bevor der Brief entsteht.

## Ton

Sachlich, freundlich, konkret, ohne Vorwurf. Anliegen im ersten Absatz, Bitte an die
Eltern im zweiten, Gesprächsangebot am Schluss. Formulierungen aus bereits
verschickten Briefen desselben Anlasses übernehmen (liegen in
`Personenbezogenes/Elternbriefe/`). Keine Verschärfung erfinden.

## Ablage und Übergabe

- **Briefe an einzelne Familien:** `Personenbezogenes/Elternbriefe/<Kursschlüssel>/<Anlass>_<JJJJ-MM-TT>_<Kürzel>.docx`
  und `.pdf` (Muster: `3x Keine Hausaufgaben_2026-09-22_MaMu.docx`). Kürzel gibt es in mehreren
  Kursen; der Kursordner unterscheidet sie. Der Kurs wird nach *Kurswahl* bestimmt, nie aus dem
  Kürzel erraten. Nie im Wurzelordner oder im Themenordner.
- **Infos an alle Eltern (ohne Namen):** mit dem Termin eines Kurses nach
  `Kurse/<Kurs>/Elterninfo-<Thema>-<JJJJ-MM-TT>.docx`, kursübergreifend (Elternabend) nach
  `Elternarbeit/`. Nach dem Verteilen als `art: ausgeteilt` beim Kurs eintragen, an den es ging
  (Skill `kurs`).

Den fertigen Brief **vor dem Versand zur Durchsicht vorlegen** (Zahlen, Schreibweise
des Namens, Datum). Nie unterstellen, dass ein Brief schon abgeschickt ist.

**Nach dem Versand** eines Hausaufgaben- oder Mitarbeitsbriefs ein
`elternkontakt`-Ereignis anhängen (Skill `schuelerdaten`) — sonst läuft die
3×-Zählung weiter und der nächste Brief kommt zu früh.

## Datenschutz

Schülernamen und Fehlzeiten bleiben in `Personenbezogenes/`. Nicht in Memory,
nicht als Artefakt, im Chat nur so weit wie für die Rückfrage nötig.
