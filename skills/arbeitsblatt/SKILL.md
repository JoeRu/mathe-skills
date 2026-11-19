---
name: arbeitsblatt
description: >
  Dieser Skill wird verwendet, wenn der Nutzer ein Arbeitsblatt, Übungsblatt,
  Aufgabenblatt, Lernblatt oder Tafelbild für den Mathematikunterricht erstellen
  oder überarbeiten möchte — etwa "Arbeitsblatt zu Termen", "Übungsblatt
  Prozentrechnung", "AB für den C-Kurs", "Aufgaben zum Dreisatz", "differenziere
  das Blatt in Basis und Plus", "Tafelbild zur antiproportionalen Zuordnung"
  oder "mach mir ein Lernblatt zu linearen Funktionen". Prüft zuerst, was der
  Kurs schon hatte, erzeugt Word, PDF und bei generierten Aufgaben LaTeX im
  Themenordner, mit geprüftem Lösungsblatt.
metadata:
  version: "0.8.0"
---

# Arbeitsblatt oder Tafelbild erstellen

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md`,
`${CLAUDE_PLUGIN_ROOT}/references/kurse.md` und
`${CLAUDE_PLUGIN_ROOT}/references/dokumente.md` lesen.

## 1. Auftrag klären

- **Kurs** — daraus Stufe und Niveau (A/B/C) aus `Kurse/<Kurs>/kurs.md`. Nicht
  nach A/B/C fragen, wenn der Kurs bekannt ist. Ohne Kursbezug (Vorrat, Vertretung)
  Niveau und Stufe erfragen.
- **Thema** und Unterkapitel (z. B. Prozentrechnung → Grundwert)
- **Zweck**: Einführung, Übung, Vertiefung, Hausaufgabe, Vorbereitung auf die
  Arbeit, Vertretungsstunde
- **Differenzierung im Kurs**: Basis/Plus wie bei `AB-Dreisatz-Zwischengroesse-*`
- **Umfang**: eine Seite ist der Normalfall

Nicht fragen, was im Ordner oder im Kursordner schon steht — erst nachsehen.

## 2. Vorhandenes Material und Kursstand sichten

```
python3 $SKILLS/scripts/kurs.py material --kurs <Kurs> --thema <Thema>
```

zeigt alles Material des Themas und markiert, was **dieser Kurs** schon hatte
(`[K]`) und was ein anderer Kurs hatte (`[e]`, eingefroren). Daraus folgt nach
`kurse.md`:

1. Passendes, das der Kurs noch nicht hatte → **vorschlagen statt neu bauen**.
2. Passendes eines anderen Niveaus oder mit Schwächen → als `_v2` anpassen, nie
   das Original ändern, wenn es eingefroren ist.
3. Nichts Passendes → neu erstellen.

Die Entscheidung dem Nutzer in einem Satz nennen. Außerdem ansehen:

- die Checkliste, die laut `themenfolge.csv` für den Kurs gilt — sie nennt die
  Kompetenzen, die das Blatt bedienen soll
- `Tafelbilder/` des Themas — eingeführte Notation und Merksätze übernehmen
- das Fachcurriculum der Stufe (`$SCHULPAKET/curricula/<Fach>/<Stufe> Fachcurriculum Mathe 2024.pdf`):
  Was dort für das Niveau nicht vorgesehen ist, kommt nicht aufs Blatt

## 3. Aufgaben entwerfen

Aufbau eines Blattes:

1. **Einstieg**: eine niedrigschwellige Aufgabe, die alle schaffen
2. **Kern**: 3–6 Aufgaben mit steigender Schwierigkeit zum Zielinhalt
3. **Abschluss**: eine Anwendungs- oder Knobelaufgabe (mit ★ markiert, freiwillig)

Regeln:

- Kontexte aus der Lebenswelt der Stufe (Handy, Sport, Einkauf, Schule), keine
  konstruierten Rechenmonster
- Zahlen im Kopf nachprüfbar halten — außer die Rechenfertigkeit ist das Lernziel
- C-Kurs: kürzere Sätze, mehr Struktur (Tabellen, Lückenrechnungen,
  vorstrukturierte Rechenwege), keine mehrschrittigen Textaufgaben ohne Hilfe
- A-Kurs: Begründungs- und Verallgemeinerungsaufgaben ergänzen
- Bei Differenzierung ein Blatt je Stufe (Basis/Plus bzw. je Kurs), gleiche
  Aufgabennummerierung, damit parallel gearbeitet werden kann
- Keine Buchaufgaben abschreiben und kein bettermarks-Material nachbauen
  (Urheberrecht, siehe `buchaufgaben`)

## 4. Lösungen erzeugen und prüfen

Jedes Blatt bekommt ein Lösungsblatt mit dem Zusatz `_Lösung`. Alle Ergebnisse mit
Python berechnen, unabhängig nachrechnen, erst dann setzen (`dokumente.md`). Bei
Textaufgaben den Rechenweg vollständig ausschreiben — das Lösungsblatt dient der
Selbstkontrolle.

## 5. Erzeugen und ablegen

Formate nach `dokumente.md`. Ablage `<Fach>/<Thema>/Arbeitsblätter/`, Name nach der
Konvention in `grundlagen.md` (`AB-<Thema>[-Basis|-Plus]-<JJJJ-MM-TT>`). Eine
Checkliste gehört nach `Klassenarbeiten/` (Skill `klassenarbeit`).

Das Blatt ist damit **erstellt, nicht ausgeteilt**. In `ausgeteilt.csv` kommt es
erst, wenn es im Kurs war (Skill `kurs` oder `wochenplanung`).

Danach in einem Satz sagen, welche Dateien wo liegen, und die Entscheidungen nennen,
die die Lehrkraft prüfen sollte (Niveau, Umfang, Kontexte, Wiederverwendung).

## Tafelbilder

Tafelbilder zum Ausdrucken oder Projizieren entstehen per Python-Skript (matplotlib
oder reportlab) in `<Fach>/<Thema>/Tafelbilder/`: Skript `tafelbilder-<thema>-<JJJJ>.py`
daneben, Ausgabe als PDF, PNG und SVG mit gleichem Basisnamen
(`Tafelbild-<Inhalt>-<JJJJ>`). Vorbild: `Mathematik/Zuordnungen/Tafelbilder/`. Große Schrift,
wenig Text, eingeführte Notation; Zahlen im Bild programmatisch aus derselben
Rechnung wie die Beschriftung.
