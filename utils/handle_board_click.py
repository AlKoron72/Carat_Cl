"""
Board-Click-Handler-Funktion für das Carat Spiel
"""
from constants import *
import utils.render


def handle_board_click(game_instance, pos):
    """
    Verarbeitet Mausklicks auf dem Spielfeld

    Args:
        game_instance: CaratGame-Instanz
        pos: (x, y) Mausposition
    """
    x, y = pos

    # Berechne Board-Position
    col = (x - BOARD_OFFSET_X) // CELL_SIZE
    row = (y - BOARD_OFFSET_Y) // CELL_SIZE

    # Prüfe, ob Klick auf dem Board war
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        # Versuche Plättchen zu platzieren
        success = game_instance.game.place_tile(row, col)

        # Wenn erfolgreich platziert, reset die Vorschau
        if success:
            utils.render._last_preview_position = None
            utils.render._affected_chips = []
