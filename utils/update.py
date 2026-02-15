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
