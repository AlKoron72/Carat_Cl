"""
Render-Funktion für das Carat Spiel
"""
import pygame
from constants import *
from utils.update import preview_tile_placement, reset_chip_preview


# Tracking-Variable für die Vorschau
_last_preview_position = None
_affected_chips = []
_force_refresh = False


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

            global _last_preview_position, _affected_chips, _force_refresh

            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                if game_instance.game.is_valid_placement(row, col):
                    # Prüfe ob sich die Position geändert hat oder Force-Refresh aktiv
                    current_position = (row, col)
                    #print(f">>> RENDER CHECK: current={current_position}, last={_last_preview_position}, affected_chips={len(_affected_chips) if _affected_chips else 0}, force_refresh={_force_refresh}")
                    if current_position != _last_preview_position or _force_refresh:
                       # print(f"\n>>> RENDER: Position changed from {_last_preview_position} to {current_position}")
                        # Reset vorherige Vorschau
                        if _last_preview_position is not None and _affected_chips:
                            #print(f">>> RENDER: Resetting preview for {len(_affected_chips)} chips")
                            reset_chip_preview(game_instance.game.board, _affected_chips)
                        elif _last_preview_position is None and _affected_chips:
                            #print(f">>> RENDER: _last_preview_position is None but _affected_chips has {len(_affected_chips)} entries - resetting")
                            reset_chip_preview(game_instance.game.board, _affected_chips)

                        # Neue Vorschau berechnen
                        #print(f">>> RENDER: Calculating new preview with color_order: {game_instance.game.selected_tile.color_order}")
                        _affected_chips = preview_tile_placement(
                            game_instance.game.board,
                            game_instance.game.selected_tile,
                            row, col
                        )
                        _last_preview_position = current_position
                        _force_refresh = False  # Reset force refresh flag

                        # Debug: Zeige neue preview
                        for chip_row, chip_col in _affected_chips:
                            chip = game_instance.game.board.get_chip(chip_row, chip_col)
                            if chip:
                                pass
                                #print(f">>> RENDER: Chip ({chip_row},{chip_col}) - preview nach Berechnung: {chip.distribution_preview}")

                    game_instance.renderer.draw_preview_tile(game_instance.game.selected_tile, game_instance.mouse_pos)
                else:
                    # Ungültige Position - Reset Vorschau
                    if _last_preview_position is not None and _affected_chips:
                        reset_chip_preview(game_instance.game.board, _affected_chips)
                        _last_preview_position = None
                        _affected_chips = []
            else:
                # Nicht über dem Board - Reset Vorschau
                if _last_preview_position is not None and _affected_chips:
                    reset_chip_preview(game_instance.game.board, _affected_chips)
                    _last_preview_position = None
                    _affected_chips = []
        else:
            # Kein Tile ausgewählt - Reset Vorschau
            if _last_preview_position is not None and _affected_chips:
                reset_chip_preview(game_instance.game.board, _affected_chips)
                _last_preview_position = None
                _affected_chips = []

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
