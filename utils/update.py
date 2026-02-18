"""
Update-Funktion für das Carat Spiel
"""
import pygame
from constants import ZOOM_ANIMATION_DURATION


def update(game_instance):
    """
    Update-Logik (aktuell minimal)

    Args:
        game_instance: CaratGame-Instanz
    """
    # Update Animation des aktuellen Tiles
    if game_instance.game and game_instance.game.selected_tile:
        game_instance.game.selected_tile.update_animation()

    # Update KI-Züge
    if game_instance.game:
        game_instance.game.update_ai()

    # Update Zoom Animation
    if game_instance.zoom_animating:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - game_instance.zoom_animation_start

        if elapsed >= ZOOM_ANIMATION_DURATION:
            # Animation beendet
            game_instance.zoom_animation_progress = game_instance.zoom_target
            game_instance.zoom_animating = False
        else:
            # Easing: smooth interpolation
            t = elapsed / ZOOM_ANIMATION_DURATION
            # Easing-Funktion (ease-in-out)
            if t < 0.5:
                eased_t = 2 * t * t
            else:
                eased_t = 1 - pow(-2 * t + 2, 2) / 2

            # Interpoliere zwischen aktuellem und Zielwert
            start_value = 1.0 - game_instance.zoom_target  # Umkehrwert vom Ziel
            game_instance.zoom_animation_progress = start_value + (game_instance.zoom_target - start_value) * eased_t


def recalculate_chip_distribution(chip):
    """
    Berechnet die prozentuale Verteilung für einen PointChip neu.
    Wird aufgerufen nachdem Werte zur distribution hinzugefügt wurden.

    WICHTIG: distribution enthält akkumulierte Werte, distribution_preview enthält Prozente.

    Args:
        chip: PointChip-Objekt dessen distribution neu berechnet werden soll
    """
    if not chip.distribution:
        chip.distribution_preview = None
        return

    total = sum(chip.distribution.values())
    if total > 0:
        chip.distribution_preview = {}
        for color in chip.distribution:
            chip.distribution_preview[color] = chip.distribution[color] / total
    else:
        chip.distribution_preview = None


def preview_tile_placement(board, tile, row, col):
    """
    Berechnet temporär die Distribution-Vorschau für die 4 Ecken-Chips,
    wenn ein Tile über ein Feld bewegt wird (noch nicht platziert).

    Erstellt distribution_preview basierend auf distribution + Vorschau-Werte.

    Args:
        board: Board-Objekt
        tile: Tile-Objekt das vorschauend platziert werden soll
        row: Zeile
        col: Spalte

    Returns:
        list: Liste der betroffenen Chips mit ihren Positionen für späteres Reset
    """
    chip_data = [
        ((row, col), 0),         # oben links -> color_order[0]
        ((row, col + 1), 1),     # oben rechts -> color_order[1]
        ((row + 1, col + 1), 2), # unten rechts -> color_order[2]
        ((row + 1, col), 3)      # unten links -> color_order[3]
    ]

    affected_chips = []

    for (chip_row, chip_col), color_index in chip_data:
        chip = board.get_chip(chip_row, chip_col)
        if chip:
            # Erstelle temporäre Vorschau-Verteilung
            temp_distribution = chip.distribution.copy()

            # Füge Vorschau-Wert hinzu
            color = tile.color_order[color_index]
            if color in temp_distribution:
                temp_distribution[color] += tile.value
            else:
                temp_distribution[color] = tile.value

            # Berechne Prozente für Vorschau
            total = sum(temp_distribution.values())
            if total > 0:
                chip.distribution_preview = {}
                for c in temp_distribution:
                    chip.distribution_preview[c] = temp_distribution[c] / total

            affected_chips.append((chip_row, chip_col))

    return affected_chips


def reset_chip_preview(board, affected_chip_positions):
    """
    Setzt die distribution_preview auf die Anzeige der aktuellen distribution zurück.
    Wird aufgerufen wenn das Tile wieder von einem Feld wegbewegt wird.

    Args:
        board: Board-Objekt
        affected_chip_positions: Liste von (row, col) Tupeln der betroffenen Chips
    """
    for chip_row, chip_col in affected_chip_positions:
        chip = board.get_chip(chip_row, chip_col)
        if chip:
            # Setze distribution_preview auf Basis der aktuellen distribution zurück
            recalculate_chip_distribution(chip)
