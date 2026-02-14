"""
Event-Handler-Funktion für das Carat Spiel
"""
import pygame
from constants import *
from game import Game
from utils.handle_board_click import handle_board_click
from utils.start_menu import start_menu


def handle_events(game_instance):
    """
    Verarbeitet Eingaben

    Args:
        game_instance: CaratGame-Instanz
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_instance.running = False

        elif event.type == pygame.MOUSEMOTION:
            game_instance.mouse_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_instance.game.state == GAME_STATE_PLAYING:
                handle_board_click(game_instance, event.pos)

        elif event.type == pygame.KEYDOWN:
            if game_instance.game.state == GAME_STATE_PLAYING:
                if event.key == pygame.K_r:
                    # Rotiere Plättchen im Uhrzeigersinn
                    game_instance.game.rotate_current_tile_clockwise()
                elif event.key == pygame.K_e:
                    # Rotiere Plättchen gegen Uhrzeigersinn
                    game_instance.game.rotate_current_tile_counter_clockwise()

            elif game_instance.game.state == GAME_STATE_GAME_OVER:
                if event.key == pygame.K_SPACE:
                    # Neues Spiel starten
                    player_count = game_instance.game.player_count
                    game_instance.game = Game(player_count)
                    game_instance.game.start_game()
                elif event.key == pygame.K_ESCAPE:
                    # Zurück zum Menü
                    game_instance.game = None
                    start_menu(game_instance)
