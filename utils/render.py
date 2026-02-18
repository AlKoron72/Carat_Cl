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
    global _last_preview_position, _affected_chips, _force_refresh

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

            # Prüfe ob KI gerade animiert
            ai_preview_pos = game_instance.game.get_ai_preview_position()

            if ai_preview_pos:
                # AI-Animation: Zeichne Vorschau an AI-Position
                row, col = ai_preview_pos

                current_position = (row, col)
                if current_position != _last_preview_position or _force_refresh:
                    # Reset vorherige Vorschau
                    if _last_preview_position is not None and _affected_chips:
                        reset_chip_preview(game_instance.game.board, _affected_chips)

                    # Neue Vorschau berechnen
                    _affected_chips = preview_tile_placement(
                        game_instance.game.board,
                        game_instance.game.selected_tile,
                        row, col
                    )
                    _last_preview_position = current_position
                    _force_refresh = False

                # Zeichne AI-Vorschau-Tile (berechne screen position aus row/col)
                screen_x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                screen_y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                game_instance.renderer.draw_preview_tile(game_instance.game.selected_tile, (screen_x, screen_y))
            else:
                # Normale Maus-Steuerung: Zeichne Vorschau an Mausposition wenn über Board
                x, y = game_instance.mouse_pos
                col = (x - BOARD_OFFSET_X) // CELL_SIZE
                row = (y - BOARD_OFFSET_Y) // CELL_SIZE

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

    # Zoom-Effekt anwenden (animiert, zentriert auf Mausposition)
    if game_instance.zoom_animation_progress > 0:
        # Berechne aktuellen Zoom-Faktor basierend auf Animation
        current_zoom = 1.0 + (ZOOM_LEVEL - 1.0) * game_instance.zoom_animation_progress

        # Erstelle gezoomte Surface
        zoomed_width = int(WINDOW_WIDTH * current_zoom)
        zoomed_height = int(WINDOW_HEIGHT * current_zoom)

        # Skaliere Screen-Inhalt
        zoomed_surface = pygame.transform.smoothscale(
            game_instance.screen,
            (zoomed_width, zoomed_height)
        )

        # Berechne Offset basierend auf Zoom-Zentrum (Mausposition)
        # Die Mausposition soll nach dem Zoom an der gleichen Stelle bleiben
        zoom_center_x, zoom_center_y = game_instance.zoom_center

        # Berechne wo das Zoom-Zentrum auf der gezoomten Surface liegt
        zoomed_center_x = zoom_center_x * current_zoom
        zoomed_center_y = zoom_center_y * current_zoom

        # Berechne Offset so dass Zoom-Zentrum an ursprünglicher Position bleibt
        offset_x = int(zoom_center_x - zoomed_center_x)
        offset_y = int(zoom_center_y - zoomed_center_y)

        game_instance.screen.fill(BLACK)  # Schwarzer Hintergrund
        game_instance.screen.blit(zoomed_surface, (offset_x, offset_y))

    pygame.display.flip()
