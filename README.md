# Carat Brettspiel - PyGame Umsetzung

Eine digitale Umsetzung des Brettspiels "Carat" mit Python und PyGame.

## Installation

```bash
pip install pygame --break-system-packages
```

## Spiel starten

```bash
python main.py
```

## Spielregeln

**Carat** ist ein taktisches Legespiel für 2-4 Spieler.

### Ziel des Spiels
Sammle die meisten Punkte, indem du Plättchen geschickt platzierst und vollständige Reihen/Spalten bildest.

### Spielablauf
1. Jeder Spieler erhält gleichmäßig Diamantenplättchen
2. Reihum platzieren Spieler ihre Plättchen auf dem 7x7-Spielfeld
3. Plättchen müssen mit mindestens einer Ecke an ein vorhandenes Plättchen angrenzen
4. Sobald eine Zeile oder Spalte vollständig ist, wird gewertet

### Wertung
- In vollständigen Zeilen/Spalten wird die dominante Diamantenfarbe ermittelt
- Spieler, deren Plättchen zu dieser Farbe beitragen, erhalten die Punktechips
- Bei Gleichstand erhalten alle beteiligten Spieler Punkte

### Steuerung
- **Mausklick**: Plättchen platzieren (auf grün markierte Felder)
- **R**: Plättchen im Uhrzeigersinn drehen
- **E**: Plättchen gegen Uhrzeigersinn drehen
- **SPACE** (Game Over): Neues Spiel starten
- **ESC** (Game Over): Zurück zum Menü

## Projekt-Struktur

```
carat-game/
│
├── main.py              # Hauptdatei mit Spielschleife
├── constants.py         # Konstanten und Konfiguration
│
├── game.py              # Hauptspiellogik
├── board.py             # Spielfeld-Verwaltung
├── tile.py              # Diamantenplättchen
├── point_chip.py        # Punktechips
├── player.py            # Spielerverwaltung
├── scoring.py           # Wertungssystem
├── renderer.py          # Grafische Darstellung
│
└── README.md            # Diese Datei
```

## Klassen-Übersicht

### Core-Klassen

#### `Game`
- Hauptspiellogik und Spielablauf
- Verwaltet Spielzustände (Menü, Spielen, Game Over)
- Koordiniert alle anderen Komponenten

#### `Board`
- 7x7 Spielfeld
- Platzierungsregeln ("gemeinsame Ecke")
- Prüfung auf vollständige Zeilen/Spalten

#### `Tile`
- Diamantenplättchen mit 4 Diamanten
- Rotation im/gegen Uhrzeigersinn
- Zufallsgenerierung

#### `PointChip`
- Punktechips mit Werten 1-5
- 49 Chips insgesamt
- Sammel-Status

#### `Player` & `PlayerManager`
- Spielerverwaltung (2-4 Spieler)
- Punktestand
- Plättchen-Hand

#### `ScoringSystem`
- Berechnet Punkte bei vollständigen Linien
- Ermittelt dominante Farben
- Vergibt Chips an Spieler

#### `Renderer`
- Zeichnet alle grafischen Elemente
- Board, Plättchen, Chips
- Spielerinformationen
- Vorschau-Funktion

## Features

✅ Vollständige Spielmechanik implementiert
✅ 2-4 Spieler Unterstützung
✅ Grafische Benutzeroberfläche
✅ Plättchen-Rotation
✅ Vorschau-Funktion
✅ Automatische Wertung
✅ Spielende-Erkennung
✅ Rangliste

## Mögliche Erweiterungen

- 🤖 KI-Gegner (verschiedene Schwierigkeitsgrade)
- 🎵 Sound-Effekte und Musik
- ✨ Animationen (Plättchen-Platzierung, Wertung)
- 💾 Speichern/Laden von Spielständen
- 📊 Statistiken und Spielhistorie
- 🌐 Netzwerk-Multiplayer
- 🎨 Verschiedene Themes/Skins
- ⚙️ Einstellungsmenü

## Code-Statistik

- **Gesamt**: ~1.500 Zeilen Code
- **9 Module**
- **8 Hauptklassen**
- **Geschätzte Entwicklungszeit**: 25-35 Stunden

## Lizenz

Dieses Projekt ist eine Fan-Umsetzung des Brettspiels "Carat" zu Lern- und Demonstrationszwecken.

## Entwickler-Hinweise

### Testing
```python
# Teste einzelne Komponenten
python -c "from tile import Tile; t = Tile(); print(t)"
python -c "from board import Board; b = Board(); print(b)"
```

### Debug-Modus
Füge in `constants.py` hinzu:
```python
DEBUG = True
SHOW_GRID_COORDS = True
```

### Performance
- Aktuell keine Optimierung notwendig (kleine Spielfeldgröße)
- Bei Bedarf: Sprite-Caching für Plättchen
- Event-basierte Neuzeichnung statt jeden Frame
