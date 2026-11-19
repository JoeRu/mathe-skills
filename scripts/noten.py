#!/usr/bin/env python3
"""Notenschlüssel — die einzige Stelle, an der gerechnet wird.

    python noten.py schluessel 40              Notengrenzen für 40 Punkte
    python noten.py schluessel 40 --tendenz    mit +/−-Grenzen (Tendenzbereich 33)
    python noten.py note 40 27,5 [--tendenz]   Note für 27,5 von 40 Punkten
    python noten.py gesamt 2,3 3,0             Gesamtnote 50 % mündlich / 50 % schriftlich
    python noten.py --test                     Selbsttest (mit dem Beispielschlüssel unten)
    --schluessel 95,80,65,50,25                Grenzen ausdrücklich angeben statt aus dem Schulpaket

Die Prozentgrenzen kommen aus `<Schulpaket>/notenschluessel.md` (Feld `grenzen:`),
gefunden über `einstellungen.md` im Schulordner (siehe schulordner.py).

Regeln (references/notenschluessel.md):
- Grenzen je Note 1–5 in Prozent, darunter 6 (Beispiel: 95/80/65/50/25)
- Grenzen = Prozent × Gesamtpunktzahl, auf halbe Punkte ABgerundet
- Tendenz: Intervall einer Note exakt dritteln (nicht runden); oberes Drittel +,
  unteres Drittel −. Die 1 hat kein +, die 6 keine Tendenz.
- Gesamtnote: Mittel aus mündlich und schriftlich, kaufmännisch gerundet (x,5 → auf).
"""
from __future__ import annotations
import math, sys
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

BEISPIEL = {1: 0.95, 2: 0.80, 3: 0.65, 4: 0.50, 5: 0.25}   # nur für den Selbsttest
PROZENT = dict(BEISPIEL)


def lade_schluessel(arg: str | None) -> None:
    """Setzt PROZENT aus --schluessel oder aus dem Schulpaket."""
    global PROZENT
    if arg:
        werte = [float(x.replace(",", ".")) for x in arg.split("/") if x] if "/" in arg else \
                [float(x) for x in arg.split(",")]
        if len(werte) != 5:
            sys.exit("--schluessel braucht fünf Werte für die Noten 1–5")
        PROZENT = {n: w / 100 for n, w in zip(range(1, 6), werte)}
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from schulordner import notenschluessel
    PROZENT = notenschluessel()["grenzen"]


def zahl(s) -> float:
    return float(str(s).replace(",", "."))


def fmt(x: float) -> str:
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def grenzen(gesamt: float) -> dict[int, float]:
    """Mindestpunktzahl je Note 1–5, auf halbe Punkte abgerundet."""
    return {n: math.floor(p * gesamt * 2 + 1e-9) / 2 for n, p in PROZENT.items()}


def note(punkte: float, gesamt: float) -> int:
    if not 0 <= punkte <= gesamt:
        raise ValueError(f"Punkte {punkte} außerhalb 0–{gesamt}")
    for n, g in grenzen(gesamt).items():
        if punkte >= g:
            return n
    return 6


def intervall(n: int, gesamt: float) -> tuple[float, float]:
    g = grenzen(gesamt)
    unten = g[n] if n <= 5 else 0.0
    oben = gesamt if n == 1 else g[n - 1]
    return unten, oben


def tendenz(punkte: float, gesamt: float) -> str:
    n = note(punkte, gesamt)
    if n == 6:
        return ""
    u, o = intervall(n, gesamt)
    d = (o - u) / 3
    if punkte < u + d:
        return "−"
    if punkte >= u + 2 * d and n != 1:
        return "+"
    return ""


def gesamtnote(muendlich: float, schriftlich: float) -> int:
    m = (Decimal(str(muendlich)) + Decimal(str(schriftlich))) / 2
    return int(m.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def tabelle(gesamt: float, mit_tendenz: bool) -> str:
    z = [f"Notenschlüssel für {fmt(gesamt)} Punkte"]
    for n in range(1, 7):
        u, o = intervall(n, gesamt)
        if n == 6:
            z.append(f"  6: unter {fmt(grenzen(gesamt)[5])} P")
            continue
        z.append(f"  {n}: ab {fmt(u)} P ({int(PROZENT[n]*100)} %)")
        if mit_tendenz:
            d = (o - u) / 3
            teile = [f"{n}− {fmt(u)}–{fmt(u + d)}", f"{n} {fmt(u + d)}–{fmt(u + 2*d if n != 1 else o)}"]
            if n != 1:
                teile.append(f"{n}+ {fmt(u + 2*d)}–{fmt(o)}")
            z.append("       " + " · ".join(teile))
    return "\n".join(z)


def _test() -> None:
    global PROZENT
    PROZENT = dict(BEISPIEL)
    # Beispiel aus der Korrektur (38 P) und der Notenauswertung (40 P)
    assert grenzen(38) == {1: 36.0, 2: 30.0, 3: 24.5, 4: 19.0, 5: 9.5}
    assert grenzen(40) == {1: 38.0, 2: 32.0, 3: 26.0, 4: 20.0, 5: 10.0}
    assert grenzen(24) == {1: 22.5, 2: 19.0, 3: 15.5, 4: 12.0, 5: 6.0}
    assert note(26, 40) == 3 and note(25.5, 40) == 4 and note(9.5, 40) == 6
    assert tendenz(30, 40) == "+" and tendenz(29.5, 40) == ""
    assert tendenz(27.5, 40) == "−" and tendenz(28, 40) == ""
    assert tendenz(34, 38) == "+" and tendenz(31.5, 38) == "−"
    assert tendenz(38, 38) == "" and tendenz(36, 38) == "−"   # die 1 hat kein +
    assert tendenz(3, 40) == ""                                # die 6 hat keine Tendenz
    assert gesamtnote(2, 3) == 3 and gesamtnote(2.3, 3.0) == 3 and gesamtnote(2, 2.9) == 2
    # unabhängige Gegenprobe: jede Grenze ist ein Vielfaches von 0,5 und <= exakter Wert
    for g in range(10, 61):
        for n, p in PROZENT.items():
            gr = grenzen(g)[n]
            assert gr * 2 == int(gr * 2) and gr <= p * g < gr + 0.5
    print("Selbsttest ok")


def main(a: list[str]) -> None:
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    if a[0] == "--test":
        _test(); return
    sk = None
    if "--schluessel" in a:
        i = a.index("--schluessel"); sk = a[i + 1]; a = a[:i] + a[i + 2:]
    lade_schluessel(sk)
    t = "--tendenz" in a
    a = [x for x in a if x != "--tendenz"]
    if a[0] == "schluessel":
        print(tabelle(zahl(a[1]), t))
    elif a[0] == "note":
        g, p = zahl(a[1]), zahl(a[2])
        n = note(p, g)
        print(f"{fmt(p)} von {fmt(g)} P = {fmt(round(p / g * 100, 1))} % → Note {n}{tendenz(p, g) if t else ''}")
        if n > 1:
            print(f"bis zur {n - 1}: {fmt(grenzen(g)[n - 1] - p)} P")
    elif a[0] == "gesamt":
        print(gesamtnote(zahl(a[1]), zahl(a[2])))
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
