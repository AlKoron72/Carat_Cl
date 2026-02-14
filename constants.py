"""
Konstanten und Konfiguration für Carat Brettspiel
"""

# Fenster-Einstellungen
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
FPS = 60

# Farben (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
BACKGROUND = (37, 150, 190)  # Grey

# Spielerfarben
PLAYER_COLORS = {
    'red': (220, 33, 33),
    'blue': (33, 33, 220),
    'green': (33, 180, 33),
    'yellow': (220, 200, 33)
}

# Diamantenfarben (für die Plättchen)
DIAMOND_COLORS = {
    1: PLAYER_COLORS['red'],
    2: PLAYER_COLORS['blue'],
    3: PLAYER_COLORS['green'],
    4: PLAYER_COLORS['yellow']
}

# Spielfeld-Einstellungen
BOARD_SIZE = 8
CELL_SIZE = 100
BOARD_OFFSET_X = 50
BOARD_OFFSET_Y = 50

# Plättchen-Einstellungen
TILE_SIZE = CELL_SIZE - 4
TILE_BORDER_OFFSET = 4
DIAMOND_RADIUS = TILE_SIZE / 2 - TILE_BORDER_OFFSET*2

# Punktechip-Einstellungen
CHIP_RADIUS = 30
CHIP_VALUES = [1]*11 + [2]*11 + [3]*11 + [4]*11 + [5]*11 + [6]*10
OFFSET: int = 3

# UI-Einstellungen
BUTTON_COLOR = (100, 150, 200)
BUTTON_HOVER = (120, 170, 220)
TEXT_COLOR = BLACK
FONT_SIZE = 24
TITLE_FONT_SIZE = 36

# Spielzustände
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_GAME_OVER = "game_over"

if __name__ == "__main__":
    print("Chip-Values: ", CHIP_VALUES, len(CHIP_VALUES), "\n")
    print("DIAMOND_COLORS: ", DIAMOND_COLORS, len(DIAMOND_COLORS), "\n")