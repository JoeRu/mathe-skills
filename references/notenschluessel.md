# Notenschlüssel — Rechenregeln

**Die Grenzen stehen im Schulpaket** (`$SCHULPAKET/notenschluessel.md`, Feld
`grenzen:`), ebenso Gesamtnote und schulische Sonderregeln. Gerechnet wird
ausschließlich mit `python3 $SKILLS/scripts/noten.py` (Selbsttest:
`noten.py --test`); das Werkzeug liest die Grenzen selbst.

```
noten.py schluessel 45 --tendenz      Grenzen für 45 Punkte
noten.py note 45 31,5 --tendenz       Note und Abstand zur nächsten
noten.py gesamt 2,4 3,0               Gesamtnote mündlich/schriftlich
```

## Grenzen in Punkten

Punktgrenze = Prozent × Gesamtpunktzahl, **auf halbe Punkte abgerundet**.
Beispiel (Grenzen 95/65 %) bei 38 Punkten: 95 % = 36,1 → ab 36; 65 % = 24,7 → ab 24,5.

## Tendenzen (+/−)

Nur wenn vereinbart; ohne Ansage gelten ganze Noten, und das wird gesagt.

- Das Punktintervall einer Note reicht von ihrer Grenze bis zur Grenze der
  nächstbesseren Note (bei der 1 bis zur Gesamtpunktzahl).
- Es wird **exakt gedrittelt, nicht gerundet** (Schulportal: „Noten mit Tendenzen“,
  Tendenzbereich 33): unteres Drittel `−`, mittleres glatt, oberes `+`.
- Die 1 bekommt kein `+`, die 6 weder `+` noch `−`.
- Die Tendenz wird zusätzlich zur Note geführt (eigene Spalte), nie statt ihrer.

## Endgültig entscheidet die Lehrkraft

Kein Skill stellt eine Note als endgültig dar. Gerechnet und vorgelegt wird hier,
entschieden von der Lehrkraft.

## bettermarks

bettermarks-Prozente sind zunächst Diagnose. **Als Leistung zählen sie nur, wenn die
Lehrkraft es für ein Thema festlegt** — dann als **mündliche** Leistung:

- Grundlage sind die **zugewiesenen** Übungen und Tests des Themas (keine selbst
  gewählten Übungen, keine Pakete, die nur ein Teil der Klasse hatte, keine laufenden).
- Je Kind der Durchschnitt über diese Aufgaben; **nicht Bearbeitetes zählt 0 %**.
  Leere Zellen der Auswertungsdatei sind damit ohne Bildschirmabgleich korrekt.
- Auf halbe Prozentpunkte runden; prüfen, dass dabei niemand über eine Notengrenze rutscht.
- Eintrag im Portal als 1 Aufgabe mit 100 Punkten, Schlüssel der Schule, Tendenzen
  (Skill `schulportal-leistung`, Abschnitt *Mündliche Leistung*).
- Die Lehrkraft vorher auf Sechsen hinweisen, die nur aus „nicht bearbeitet“
  entstehen und dasselbe Versäumnis schon als Hausaufgabe zählen.
