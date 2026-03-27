# Carat Brettspiel - PyGame Umsetzung

Eine digitale Umsetzung des Brettspiels "Carat" mit Python und PyGame.

## Installation

```bash
pip install pygame
```

## Spiel starten

```bash
python main.py
```

---

## Spielregeln

**Carat** ist ein taktisches Legespiel für 1–4 Spieler.

### Ziel des Spiels

Sammle die meisten Punkte, indem du Plättchen auf dem 7×7-Spielfeld platzierst und Punktechips für dich entscheidest.

### Spielvorbereitung

- Es gibt **49 Plättchen** (eines pro Feld) und **64 Punktechips** (an allen Ecken der Felder).
- Die Plättchen werden gleichmäßig auf die Spieler verteilt. Der zufällig bestimmte Startspieler erhält ein Plättchen mehr.
- **NPC-Farben**: Bei weniger als 4 Spielern bleiben übrige Farben als NPCs (non-playable colors) im Spiel – sie nehmen keine Züge, können aber Punktechips gewinnen.

### Spielablauf

1. Reihum platzieren Spieler jeweils eines ihrer Plättchen auf dem Spielfeld.
2. Das **erste Plättchen** darf auf jedem Feld platziert werden, ausgenommen die Randfelder.
3. Alle weiteren Plättchen müssen **kantenbenachbart** (horizontal oder vertikal) an ein bereits liegendes Plättchen angrenzen.
4. Vor dem Platzieren kann das Plättchen beliebig oft **gedreht** werden.

### Punktechips

- An jeder Feldecke liegt ein Punktechip mit einem Wert von **1–6 Punkten**.
- Jeder Chip grenzt an 1, 2 oder 4 Felder:
  - **Ecken** des Spielfelds: 1 Nachbarfeld
  - **Ränder** des Spielfelds: 2 Nachbarfelder
  - **Innenfelder**: 4 Nachbarfelder
- Wenn alle Nachbarfelder eines Chips belegt sind, wird der Chip **ausgewertet**.
- Jedes Plättchen hat 4 farbige Diamanten. Deren Farbwerte akkumulieren sich im jeweiligen Chip.
- Die Farbe mit dem **höchsten Gesamtwert** gewinnt den Chip.
- Bei **Gleichstand** unter den Spitzenfarben gewinnt niemand – der Chip bleibt unverteilt.
- **Punkteberechnung**: `Chipwert × Anzahl beteiligter Farben`

### Spielende

Das Spiel endet, wenn alle Plättchen gelegt wurden oder keine gültigen Züge mehr möglich sind.

Gewinner ist der Spieler mit dem **höchsten Punktestand**.

---

## Steuerung

| Taste / Aktion | Funktion |
|---|---|
| **Mausklick** | Plättchen auf markiertem Feld platzieren |
| **R** | Plättchen im Uhrzeigersinn drehen |
| **E** | Plättchen gegen Uhrzeigersinn drehen |
| **Z** | Zoom ein-/ausschalten (150 %, zentriert auf Mausposition) |
| **Leertaste** (Spielende) | Neues Spiel mit gleichen Einstellungen |
| **ESC** (Spielende) | Zurück zum Hauptmenü |

---

## Startmenü

- Auswahl der **Spieleranzahl**: 1–4
- Optionale **KI-Gegner** für Spieler 2, 3 und 4 (Schaltfläche „P2 AI" etc.)
- Bei 1 Spieler dienen die übrigen Farben als NPCs

---

## KI-Spieler

- KI-Spieler setzen ihren Zug automatisch nach einer kurzen Verzögerung (~1 Sekunde).
- Während des KI-Zugs zeigt eine Animation das Plättchen, das verschiedene Felder durchläuft, bevor es platziert wird.
- Schwierigkeitsgrade (Easy/Medium/Hard) sind vorbereitet; aktuell agiert die KI zufällig.

---

## Projekt-Struktur

```
Carat_Cl/
│
├── main.py              # Einstiegspunkt und Spielschleife
├── constants.py         # Konstanten und Konfiguration
│
├── game.py              # Spiellogik und Zustandsverwaltung
├── board.py             # Spielfeld (7×7) und Chip-Verwaltung
├── tile.py              # Plättchen mit 4 Diamanten und Rotation
├── point_chip.py        # Punktechips mit Akkumulation und Animation
├── player.py            # Spieler- und PlayerManager-Klassen
├── scoring.py           # Wertungslogik beim Chip-Abschluss
├── npc.py               # KI-Spieler (AIPlayer)
├── renderer.py          # Grafische Darstellung (PyGame)
│
└── utils/
    ├── __init__.py          # Exportiert alle Utils
    ├── start_menu.py        # Startmenü-Rendering und Eingabe
    ├── handle_events.py     # Tastatur- und Maus-Events
    ├── handle_board_click.py# Klick → Spielfeldposition → Zug
    ├── update.py            # Update-Logik, Animationen, KI-Ablauf
    └── render.py            # Render-Hilfsfunktionen
```

---

## Features

- 1–4 Spieler (lokal)
- Optionale KI-Gegner für Spieler 2, 3 und 4
- NPC-Farben als passive Mitspieler
- Plättchen-Rotation mit Animation (250 ms)
- Zoom-Funktion (Z-Taste)
- Hover-Vorschau: zeigt Chip-Farbverteilung vor dem Platzieren
- Chip-Sammel-Animation (500 ms Füllung + 300 ms Texteinblendung)
- Automatische Wertung und Spielende-Erkennung
- Rangliste am Spielende

---

## Lizenz

Dieses Projekt ist eine Fan-Umsetzung des Brettspiels "Carat" zu Lern- und Demonstrationszwecken.
