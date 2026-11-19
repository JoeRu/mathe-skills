---
paket: schule-xyz
struktur: 1
schule: <<Name der Schule>>
schulform: <<z. B. Integrierte Gesamtschule>>
ort: <<Ort>>                    # erscheint im Briefdatum
anschrift: <<Straße, PLZ Ort>>
telefon: <<…>>
homepage: <<…>>
bundesland: <<z. B. Hessen>>
portal: <<z. B. Schulportal Hessen>>
kurssystem: <<z. B. A/B/C oder Klassenverband>>
lehrwerk: <<Verlag, Titel, Stufe>>
---
# Schulpaket <<Name der Schule>> — Mathematik

Gemeinsame Grundlage aller Mathe-Lehrkräfte der Schule. Was nur eine Lehrkraft
betrifft, gehört in deren `einstellungen.md`.

## Schule

<<Name, Schulform, Anschrift, Telefon, Homepage>>

## Stundenraster

<<Länge einer Schulstunde (z. B. 45 min); Doppelstunde: Pause dazwischen (z. B. 5 min nach 45 min)?>>

## Kurssystem

<<Wie wird differenziert? Welche Niveaus? Faustwert Punkte je Schulstunde?>>

## Notenschlüssel

`notenschluessel.md` in diesem Ordner.

## Fachcurriculum

Je Fach ein Unterordner: Fachcurricula je Stufe in `curricula/<Fach>/` (PDF), Themenfolge je
Stufe als `curricula/<Fach>/themenplan-<Stufe>.csv` (`nr;thema;wochen;niveau;hinweis`).

| Stufe | Themenfolge |
|---|---|
| <<5>> | <<…>> |

## Lehrwerk

<<Titel, ISBN, digitale Plattform>>. Seitenverzeichnis je Fach in `lehrwerk/<Fach>/`.

## Plattformen

<<Schulportal, Lernplattformen>>

## Vorlagen

| Ordner | Inhalt |
|---|---|
| `vorlagen/Elternbriefe/` | Briefvorlagen mit Briefkopf der Schule |
| `vorlagen/Verwaltung/` | Formulare |
| `vorlagen/LaTeX/` | Präambeln |
