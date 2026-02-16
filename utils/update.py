"""
Update-Funktion für das Carat Spiel
"""


def update(game_instance):
    """
    Update-Logik (aktuell minimal)

    Args:
        game_instance: CaratGame-Instanz
    """
    # Update Animation des aktuellen Tiles
    if game_instance.game and game_instance.game.selected_tile:
        game_instance.game.selected_tile.update_animation()


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
