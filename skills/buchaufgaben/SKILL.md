---
name: buchaufgaben
description: >
  Dieser Skill wird verwendet, wenn der Nutzer Aufgaben oder Material aus dem
  Westermann-Schulbuch sucht — etwa "welche Buchaufgaben passen zum Dreisatz",
  "was steht auf S. 94", "such mir Hausaufgaben zur Prozentrechnung", "gibt es
  ein Arbeitsblatt zu Zuordnungen", "lade das BiBox-Material zu Kapitel 3",
  "womit kann ich die Stunde einsteigen" oder "welche Seiten brauche ich für die
  Wiederholung". Schlägt in der BiBox nach, nennt Seiten und Aufgabennummern mit
  Niveaueinschätzung, lädt auf Nachfrage die Arbeitsblätter herunter und legt sie
  benannt im Themenordner ab.
metadata:
  version: "0.8.0"
---

# Buchaufgaben und BiBox-Material finden

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` lesen
(Kurssystem A/B/C, Ordnerstruktur, Themenordner, Datenschutz), dann
`$SCHULPAKET/lehrwerk/Mathematik/westermann-mh7.md` — dort stehen die bereits
bestätigten Buch-, Kapitel- und Seitenangaben. **Immer zuerst dort nachsehen:**
Was da steht, muss nicht neu erblättert werden.

## Zweck

Die Frage „welche Aufgabe passt hier" kostet jedes Mal Blättern. Dieser Skill
schlägt in der BiBox nach, nennt konkrete Fundstellen und holt das passende
Material — und schreibt jede bestätigte Seitenangabe ins Seitenverzeichnis,
sodass die Suche beim nächsten Mal kürzer wird.

Er liefert vier Dinge, je nachdem was gefragt ist:

1. **Aufgabenvorschläge** — Seite und Nummer, getrennt nach Einstieg, Übung,
   Hausaufgabe und Bonus, mit Einschätzung für A-/B-/C-Kurs
2. **Material** — BiBox-Arbeitsblätter herunterladen und in `Arbeitsblätter/`
   des Themenordners ablegen
3. **Stundeneinstieg** — aus einer Buchseite einen konkreten Aufhänger ableiten
4. **Seitenverzeichnis** — `$SCHULPAKET/lehrwerk/Mathematik/westermann-mh7.md` in der Quelle fortschreiben

## Urheberrecht

Buch und Materialien sind von der Schule für den Unterrichtsgebrauch lizenziert.
Das heißt: Herunterladen, Ausdrucken und Einsetzen im Unterricht sind in Ordnung.

Trotzdem gilt:

- **Fundstellen nennen, nicht abschreiben.** „S. 86 Nr. 6" statt des
  Aufgabentexts. In der Antwort höchstens so viel zitieren, wie zum Wiedererkennen
  nötig ist — ein Stichwort zum Sachkontext, keine vollständigen Aufgaben.
- **Keine Buchaufgaben in eigene Arbeitsblätter kopieren.** Wer eigene Aufgaben
  braucht, nimmt `arbeitsblatt` — der Skill erzeugt sie selbst.
- Heruntergeladene Westermann-Dateien werden abgelegt und benutzt, aber nicht
  umgebaut und nicht weitergegeben.

## Zugang zur BiBox

`https://bibox2.westermann.de` — Anmeldung über `mein.westermann.de`.
**Die Anmeldung macht der Nutzer selbst.** Zugangsdaten werden nie eingegeben
oder gespeichert. Ist die Sitzung abgelaufen, wird er darum gebeten und gewartet.

### Klickweg (aufgezeichnet am 31.08.2026)

1. `https://bibox2.westermann.de` → **Meine Bibliothek**
2. Das Suchfeld **„Meine Bücher (Titel, ISBN)"** nutzen — die Bibliothek lädt
   nur einen Teil der Bände nach, ohne Filter fehlen Titel in der Liste
3. Buch öffnen, oder direkt `https://bibox2.westermann.de/v2/book/<Buch-ID>`
4. Zur Seite springen: `…/v2/book/<Buch-ID>/page/<Seite>`
5. Linke Leiste: **Inhalt** (Kapitel mit Seitenzahlen), **Material**
   (seitengebunden!), **Suche**

### Eine Buchseite lesen

Das Buch enthält **keinen auslesbaren Text** — BiBox weist selbst darauf hin.
Die Seiten sind Bilder.

- `get_page_text` liefert **nur die Oberfläche**, nie den Buchinhalt.
- Eine Seite wird **angesehen**: `computer{action:"screenshot"}`, bei kleinen
  Zahlen und Tabellen zusätzlich `zoom` auf den Bereich.
- Das geht **Seite für Seite**. Nicht versuchen, ein halbes Kapitel auf einmal
  zu erfassen — lieber gezielt die zwei bis drei Seiten ansehen, die zum
  Thema gehören, und deren Aufgabennummern nennen.
- Bei einer Doppelseitenansicht prüfen, welche Seitenzahl links und welche
  rechts steht, bevor Nummern zugeordnet werden.

### Material zu einer Seite

Das Material-Panel ist **an die aufgeschlagene Seite gebunden** — erst zur
richtigen Seite navigieren, dann Material öffnen. Kategorien: Arbeitsblätter,
Lösungen, Lernerfolgskontrollen, Medienpool, Mathe-Trainer, Erweiterungsmodule.

Jeder Eintrag hat **Vorschau** (im Browser ansehen, kein Download) und
**Öffnen** (lädt herunter). Vor jedem Download die **Vorschau** öffnen und
prüfen, dass Titel und Kategorie stimmen — die Material-IDs in den Links laufen
fortlaufend, aber sie werden **gelesen, nie hochgerechnet**.

## Download und Ablage

**Jeder Download wird einzeln angefragt** — mit Titel, Kategorie und Größe.
Ohne ausdrückliches Ja wird nichts geladen.

Ablauf pro Datei:

1. In der Vorschau bestätigen, dass es das richtige Material ist
2. **Öffnen** klicken — die Datei landet im **Downloads-Ordner** des Rechners,
   unter dem Rohnamen `314_<Produktcode>_<Nr>.doc`
3. Ein paar Sekunden warten, dann in `~/mnt/Downloads` nachsehen, wie die Datei
   tatsächlich heißt — **nicht** den Namen annehmen
4. Nach dem Namensschema unten in den Zielordner kopieren (siehe unten)
5. Die Datei in Downloads mit dem Präfix `.bibox-erledigt-` markieren, damit
   sie beim nächsten Lauf nicht erneut auftaucht
6. Ergebnis melden: neuer Dateiname und Ordner

### Namensschema

Der Rohname bleibt erhalten, ein sprechender Zusatz kommt dahinter:

```
314_150425_033.doc   →   314_150425_033_handytarife.doc
```

- **Die Materialnummer nie ändern** — über sie findet der Nutzer das Material
  in der BiBox wieder
- Der Zusatz ist der **BiBox-Titel**, kleingeschrieben, Leerzeichen zu
  Unterstrichen (`Rechne dich fit` → `_rechne_dich_fit`)
- Material mit klarer Gattung bekommt stattdessen ein Präfix, wie im Ordner
  vorhanden: `Checkliste_Westermann_…`, `Probe-Arbeit-…`
- Zielordner ist `<Themenordner des Kapitels>/Arbeitsblätter/` (siehe
  `grundlagen.md`), nicht das Wurzelverzeichnis. Den Unterordner anlegen, wenn
  er dort noch fehlt. **Ausnahme:** Material mit klarer Gattung folgt seiner
  Gattung — `Probe-Arbeit-…` und `Checkliste_Westermann_…` nach
  `Klassenarbeiten/`, Tafelbild-Vorlagen nach `Tafelbilder/`
- **Nie überschreiben.** Existiert der Zielname schon, wird das gemeldet und
  nichts getan.

### Was schon da ist

Vor jedem Download `<Fach>/<Thema>/Arbeitsblätter/` (samt `BiBox/`-Unterordner, wo es
ihn gibt) auflisten und gegen die BiBox-Liste abgleichen. Was bereits vorliegt, wird nicht erneut geladen — nur benannt, was
fehlt. Der Abgleich läuft über die **Materialnummer**, nicht über den Dateinamen,
weil ältere Dateien abweichend heißen können (`Aus_Graphen.docx` = Nr. 032).

## Aufgabenvorschläge

Format der Antwort:

```markdown
## <Thema> — Mathematik heute <Band>, Kapitel <N> (S. <von>–<bis>)

**Einstieg:** S. <n> Nr. <x> — <ein Halbsatz zum Sachkontext>
**Übung:** S. <n> Nr. <x>, <y> — <Niveau: A / B / C>
**Hausaufgabe:** S. <n> Nr. <x> — <warum diese>
**Bonus:** S. <n> Nr. <x> (optional)

**Material dazu:** <BiBox-Titel> — *vorhanden* / *fehlt, kann ich laden*
```

Regeln dafür:

- **Nur Nummern nennen, die tatsächlich auf der angesehenen Seite stehen.**
  Keine Aufgabennummer aus dem Gedächtnis, keine plausible Schätzung.
- Zu jeder Fundstelle **einen Halbsatz zum Sachkontext**, damit der Nutzer sie
  ohne Aufschlagen wiedererkennt („Busfahrt mit Festpreis", „Mosterei").
- **Niveau einschätzen**, nicht behaupten: Grundlage ist die Aufgabenstellung,
  nicht das Fachcurriculum. Mehrschrittige Sachaufgaben und Aufgaben mit
  Begründungsanteil sind A-/B-Niveau, reine Rechenwege C.
- **Wiederholungsstunden** bedienen sich zuerst bei `Punkte sammeln`,
  `Vermischte und komplexe Übungen`, `Was du gelernt hast` und `Bist du fit?` —
  die Seiten stehen im Seitenverzeichnis.
- Vor einer Klassenarbeit die **Checkliste zum Thema** lesen — sie liegt in
  `<Themenordner>/Klassenarbeiten/` — ; sie legt den prüfbaren Stoff fest
  (siehe Skill `klassenarbeit`).

## Stundeneinstieg

Auf Wunsch aus einer angesehenen Seite ableiten:

- **Aufhänger** — welche Sachsituation der Seite trägt die Stunde
- **Beispielaufgabe** — welche Nummer sich gemeinsam an der Tafel rechnen lässt
- **Reihenfolge** — welche Nummern danach in Einzel- oder Partnerarbeit passen
- **Womit es hakt** — welche Stelle erfahrungsgemäß Rückfragen erzeugt, sofern
  aus der Aufgabenstellung erkennbar

Kein fertiger Stundenverlauf — dafür ist `wochenplanung` da, an die hier
übergeben wird.

## Seitenverzeichnis pflegen

Nach jedem Lauf `westermann-mh7.md` in der **Quelle** `$SKILLS/references/` ergänzen
(nicht die installierte Kopie unter `${CLAUDE_PLUGIN_ROOT}`):

- neu bestätigte Kapitel- und Abschnittsseiten
- gesichtete Seiten mit einem Zweizeiler, was dort steht
- Materiallisten mit Nummer, BiBox-Titel und Dateiname im Ordner
- neue Buch-IDs anderer Bände

**Nur eintragen, was gesehen wurde.** Ein `*offen*` im Verzeichnis ist besser
als eine geratene Seitenzahl — genau dafür ist die Spalte da.

## Übergaben

| Bedarf | Skill |
|---|---|
| Eigene Aufgaben statt Buchaufgaben | `arbeitsblatt` |
| Kopfrechenblatt | `kopfrechnen` |
| Klassenarbeit, Übungsarbeit, Checkliste | `klassenarbeit` |
| Die gefundenen Aufgaben in die Woche einplanen | `wochenplanung` |

Der Skill `wochenplanung` ruft diesen hier auf, wenn im Plan eine Hausaufgabe
als `<offen>` steht — dann werden die fehlenden Buchseiten hier nachgeschlagen
und der Plan gefüllt.
