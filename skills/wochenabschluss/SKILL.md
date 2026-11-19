---
name: wochenabschluss
description: >
  Dieser Skill wird verwendet, wenn eine Unterrichtswoche abgeschlossen und
  nachgearbeitet werden soll — etwa "Wochenabschluss", "mach den Freitag fertig",
  "werte die Woche aus", "bettermarks-Frist ist rum, was jetzt", "wer hat diese
  Woche keine Hausaufgaben gemacht", "Hausaufgaben der Woche ins Protokoll",
  "sind Briefe fällig" oder "Kursstand nachziehen". Holt die bettermarks-Auswertung,
  wertet die Hausaufgaben je Kind, hängt die Ereignisse an, prüft die 3×-Regel,
  erzeugt fällige Elternbriefe, trägt Ausgeteiltes und Themenstand beim Kurs nach
  und übergibt an die Wochenplanung.
metadata:
  version: "0.9.0"
---

# Wochenabschluss

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` (Datenschutz, Werkzeuge,
Ordner) und `${CLAUDE_PLUGIN_ROOT}/references/kurse.md` lesen.

Der Skill erfindet keine eigenen Verfahren. Er legt die Reihenfolge fest, in der
die anderen Skills am Ende einer Woche laufen, und sorgt dafür, dass nichts liegen
bleibt. Jeder Schritt folgt dem zuständigen Skill; der steht in der Tabelle.

## Wann

Nach Ablauf der bettermarks-Frist der Woche (Regel: Freitag 23:45, sonst die im
Plan genannte), spätestens vor der Wochenplanung der Folgewoche. Den Kurs nach
`grundlagen.md` (*Kurswahl*) bestimmen. Nennt der Auftrag keinen und sind mehrere Kurse aktiv,
wird gefragt: ein bestimmter Kurs oder **alle aktiven nacheinander**. Dann gibt es einen
vollständigen Durchlauf **je Kurs**, mit Freigaben und Zusammenfassung je Kurs. Die
bettermarks-Frist kann je Kurs verschieden sein (`kurs.md`, *Regeln*).

## Ablauf

| # | Schritt | Skill | Ergebnis |
|---|---|---|---|
| 1 | Woche lesen: Schulportal-Historie der Woche, Ausgeteiltes, bettermarks-Zuweisungen und Fristen | `kurs`, `bettermarks` | Liste der Hausaufgaben und To-dos der Woche |
| 2 | bettermarks-Auswertungsdatei holen (Kachel *Auswertung*, Datei nach `Kurse/<Kurs>/_intern/<Thema>/bettermarks/`) | `bettermarks` | aktuelle `Klassenaktivität …xlsx` |
| 3 | Diagnose: sitzt / wackelt / nicht angefangen, Klassenschnitt mit Bearbeitungsquote | `bettermarks` | kurze Auswertung für die Lehrkraft |
| 4 | Hausaufgabenwertung je Kind und Zuweisung: gemacht / teilweise / fehlt | `bettermarks` (*Als Hausaufgabe werten*) | Liste mit Kürzeln **zur Freigabe** |
| 5 | Portal-Hausaufgaben der Woche übertragen (Leistungen → Ausführlich) | `schuelerdaten` | Tabelle für `ereignis.py` |
| 6 | Ereignisse anhängen: erst `--probe`, nach Freigabe ohne | `schuelerdaten` | `ereignisse.jsonl` fortgeschrieben |
| 7 | 3×-Regel: `auswerten.py --briefe` | `schuelerdaten` | wer einen Brief bekommt, mit Daten |
| 8 | Fällige Briefe mit `elternbrief_hausaufgaben.py`, PDF ansehen, vorlegen | `elternbrief` | Briefe in `Personenbezogenes/Elternbriefe/` |
| 9 | Nur wenn die Lehrkraft es für das Thema festgelegt hat: bettermarks-Schnitt als mündliche Leistung | `schulportal-leistung` | Leistung im Portal, rückgelesen |
| 10 | Kursdaten: gehaltene Stunden der Woche nach `ausgeteilt.csv`, Themenstand in `themenfolge.csv` | `kurs` | Kursordner aktuell |
| 11 | Übergabe: offene Punkte und Diagnose als Ist für die Rückschau | `wochenplanung` (*Rückschau*) | Rückschau und Plan der Folgewoche |

Schritte, die in dieser Woche nichts zu tun haben, werden in einem Halbsatz
abgehakt („keine bettermarks-Zuweisung diese Woche“), nicht weggelassen.

## Freigaben

Drei Stellen brauchen ein ausdrückliches Ja der Lehrkraft, auch wenn der Auftrag
„mach den Wochenabschluss“ lautet:

1. **Die Hausaufgabenwertung** (Schritt 4) — Können oder Lust entscheidet er aus
   dem Unterricht. Grenzfälle mit Prozentwert vorlegen.
2. **Das Anhängen der Ereignisse** (Schritt 6) — das Protokoll kennt kein Löschen.
3. **Alles, was ins Schulportal geht** (Schritt 9) — Schüler und Eltern lesen mit.

Briefe werden erstellt und vorgelegt, nie als versandt behandelt. Das
`elternkontakt`-Ereignis kommt erst, wenn die Lehrkraft den Versand bestätigt und das
Datum nennt.

## Was am Ende im Chat steht

```markdown
## Wochenabschluss <Kurs> — KW <NN>

**bettermarks:** <n>/<m> Zuweisungen bearbeitet · Klassenschnitt <x> % · sitzt: … · wackelt: …
**Hausaufgaben:** fehlt: <Kürzel> · teilweise: <Kürzel> · alle anderen gemacht
**3×-Regel:** Briefe fällig für <Kürzel> (Dateien in Personenbezogenes/Elternbriefe/) — oder „keine“
**Kurs:** <n> Zeilen in ausgeteilt.csv nachgetragen · Thema <…> läuft seit <…>, Arbeit am <…>
**Für die Planung:** <offene Punkte, Material das fehlt, Kinder mit Förderbedarf als Kürzel>
**Von dir noch:** <Briefe verschicken und Datum nennen · Portal-Einträge der Woche auf Ist ändern · …>
```

## Datenschutz

Es gelten die Regeln aus `grundlagen.md`: Kürzel im Chat nur so weit nötig,
Klarnamen nur lokal über die Werkzeuge, keine Kürzel in Kursordnern, Portalfeldern
oder Projektdokumenten. Berechnete Tabellen mit Kürzeln und Prozentwerten liegen in
`Kurse/<Kurs>/_intern/<Thema>/`.

## Übergaben

| Bedarf | Skill |
|---|---|
| Auswertung, Wertung, Fristen | `bettermarks` |
| Ereignisse, 3×-Regel, Portal-Übertrag | `schuelerdaten` |
| Briefe | `elternbrief` |
| Mündliche Leistung ins Portal | `schulportal-leistung` |
| Ausgeteiltes, Themenstand | `kurs` |
| Nächste Woche | `wochenplanung` |
