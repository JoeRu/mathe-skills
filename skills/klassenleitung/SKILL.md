---
name: klassenleitung
description: >
  Dieser Skill wird verwendet, wenn Aufgaben der Klassenleitung anfallen, die
  nicht den Mathematikunterricht betreffen — etwa "Zeugnisbemerkungen für meine
  Klasse", "Elternabend der Klasse vorbereiten", "Klassenbuch prüfen",
  "Fehlzeiten der Klasse", "Elterngespräch Klassenleitung", "Klassenfahrt
  organisieren", "Klassenrat" oder "Beurlaubungen". Er ist ein Platzhalter: Er
  ordnet die Aufgabe der Klasse zu, fragt nach, was gebraucht wird, und
  erfindet kein Verfahren.
metadata:
  version: "0.1.0"
---

# Klassenleitung (Platzhalter)

Eine Klassenleitung hat Aufgaben, die über das Fach hinausgehen. Für sie gibt es in
diesem Plugin noch keine festen Verfahren. Dieser Skill sorgt dafür, dass sie **nicht
mit Mathe-Annahmen** bearbeitet werden, und sammelt, was eine Lehrkraft braucht, bis es
einen eigenen Skill dafür gibt.

Zuerst `${CLAUDE_PLUGIN_ROOT}/references/grundlagen.md` lesen (Abschnitt *Kurswahl*,
*Kurs ≠ Klasse*).

## Grundsatz: Klasse ist nicht Kurs

Die Klassenleitung gilt für eine **Stammklasse**, nicht für einen Kurs. Im
Fachunterricht (z. B. Mathe, Deutsch, Englisch in Stufe 7 und 8 an einer Gesamtschule)
sitzen Kinder einer Klasse in verschiedenen Kursen, und ein Kurs enthält Kinder mehrerer
Klassen. Deshalb:

- Kursdaten (`Kurse/<Kurs>/…`, `Schuelerdaten/<Kurs>/`) sind **keine** Klassenliste.
  Kinder der eigenen Klasse zu finden heißt, über mehrere Kurse zu suchen — das geht nur
  mit Zustimmung der Lehrkraft und nur mit den dafür vorgesehenen Werkzeugen.
- Kein Skill des Fachunterrichts wird für Klassenaufgaben zweckentfremdet (Elternbrief
  zu Hausaufgaben ≠ Elternbrief der Klassenleitung).

## Ablauf

1. **Klasse bestimmen.** `klassenleitung:` in `einstellungen.md` lesen. Steht dort `nein`
   oder nichts, nachfragen, ob und für welche Klasse die Aufgabe gemeint ist. Mehrere
   Klassen: eine nennen lassen.
2. **Aufgabe klären.** Eine kurze Rückfrage, was gebraucht wird (Text, Liste, Formular,
   Terminplanung, Gespräch vorbereiten) und woher die Angaben kommen. Nichts
   Personenbezogenes aus Kursordnern ohne Zustimmung heranziehen.
3. **Mit dem arbeiten, was da ist:** allgemeine Skills und Vorlagen des Schulpakets
   (`schule.md`, `vorlagen/`). Gibt es nichts Passendes, den Entwurf offen als Entwurf
   kennzeichnen und nicht so tun, als folge er einem Schulverfahren.
4. **Datenschutz wie überall:** Namen, Fehlzeiten, Zeugnisbemerkungen und
   Förderplanhinweise bleiben im Schulordner (`Personenbezogenes/`). Nicht ins
   Repository, nicht in Artefakte.
5. **Bedarf festhalten.** Kommt dieselbe Aufgabe wiederholt vor, der Lehrkraft vorschlagen,
   daraus einen eigenen Skill zu machen, und die bisherigen Eigenheiten (Fristen,
   Vorlagen, Schulabläufe) zusammentragen.

## Was dieser Skill nicht tut

- Er schreibt nichts ins Schulportal und verschickt nichts.
- Er legt keine Ordnerstruktur für die Klassenleitung an, solange die Lehrkraft nicht
  gesagt hat, wo sie liegen soll (Vorschlag: `Klassenleitung/<Klasse>/`, personenbezogen
  und nicht versioniert; `.gitignore` entsprechend ergänzen).
- Er erfindet keine Schulregeln (Entschuldigungsfristen, Zeugnisformeln, Ordnungsmaßnahmen).
  Diese stehen im Schulpaket oder müssen erfragt werden.
