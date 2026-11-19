---
struktur: 3                     # Version der Ordner-Schnittstelle (nicht von Hand ändern)
lehrkraft: <<VORNAME>>          # so spricht der Assistent dich an
anrede: du                      # du | Sie
lehrkraft_name: <<VORNAME NACHNAME>>   # Unterschrift in Briefen
kuerzel: <<ABC>>                # Lehrerkürzel, z. B. in Korrekturvermerken
faecher: [Mathematik]           # alle unterrichteten Fächer, z. B. [Mathematik, Physik]; je Fach ein Ordner mit den Themen
klassenleitung: nein            # nein | Stammklasse, z. B. 7a (Skill klassenleitung)
schulpaket: schule-xyz          # Ordner des Schulpakets, relativ zu diesem Ordner
skills: mathe-skills            # Ordner der Skills (lokale Kopie oder Verknüpfung)
---
# Einstellungen

Diese Datei macht den Ordner zum Schulordner. Die Skills lesen sie bei jedem Start.
Was hier steht, geht den Standards der Skills und des Schulpakets vor.

## Eigene Regeln

Abweichungen von den Standards der Skills, je eine Zeile. Beispiele:

- bettermarks-Hausaufgaben: Frist Freitag der laufenden Woche, 23:45
- Schülerblätter tragen „Kürzel“ statt „Name“
- Einheitenfehler kosten 0,5 Punkte

## Stundenrahmen

- In jeder Stunde etwa 5 Minuten Anwesenheit und 5–10 Minuten Hausaufgabenkontrolle einplanen
