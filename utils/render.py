"""
Render-Funktion für das Carat Spiel
"""
import pygame
from constants import *


def render(game_instance):
    """
    Zeichnet das Spiel

    Args:
        game_instance: CaratGame-Instanz
    """
    game_instance.screen.fill(BACKGROUND)

    if game_instance.game.state == GAME_STATE_PLAYING:
        # Zeichne Board und Spielelemente
        game_instance.renderer.draw_board(game_instance.game.board)
        game_instance.renderer.draw_tiles(game_instance.game.board)

        # Zeichne gültige Positionen
        game_instance.renderer.draw_valid_positions(game_instance.game.valid_positions)

        # Zeichne Spielerinfo
        game_instance.renderer.draw_player_info(game_instance.game)

        # Zeichne aktuelles Plättchen
        if game_instance.game.selected_tile:
            game_instance.renderer.draw_current_tile(game_instance.game.selected_tile)

            # Zeichne Vorschau an Mausposition wenn über Board
            x, y = game_instance.mouse_pos
            col = (x - BOARD_OFFSET_X) // CELL_SIZE
            row = (y - BOARD_OFFSET_Y) // CELL_SIZE

            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                if game_instance.game.is_valid_placement(row, col):
                    game_instance.renderer.draw_preview_tile(game_instance.game.selected_tile, game_instance.mouse_pos)

        # Zeichne Chips als letztes, damit sie im Vordergrund bleiben
        game_instance.renderer.draw_chips(game_instance.game.board)

    elif game_instance.game.state == GAME_STATE_GAME_OVER:
        # Zeichne finales Board
        game_instance.renderer.draw_board(game_instance.game.board)
        game_instance.renderer.draw_tiles(game_instance.game.board)

        # Zeichne Chips als letztes
        game_instance.renderer.draw_chips(game_instance.game.board)

        # Zeichne Game Over Screen
        game_instance.renderer.draw_game_over(game_instance.game)

    pygame.display.flip()
