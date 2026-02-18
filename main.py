"""
Hauptdatei für Carat Brettspiel - PyGame Umsetzung
"""
import pygame
import sys
from constants import *
from renderer import Renderer
from utils import start_menu, handle_events, update, render

class CaratGame:
    """
    Hauptklasse für das Spiel
    """
    
    def __init__(self):
        """Initialisiert PyGame und das Spiel"""
        pygame.init()

        # Fenster erstellen
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Carat - Brettspiel")

        # Clock für FPS
        self.clock = pygame.time.Clock()

        # Renderer
        self.renderer = Renderer(self.screen)

        # Spiel
        self.game = None
        self.running = True

        # Maus-State
        self.mouse_pos = (0, 0)

        # Zoom-State
        self.zoom_active = False
        self.zoom_surface = None
        self.zoom_animation_progress = 0.0  # 0.0 = normal, 1.0 = voll gezoomt
        self.zoom_animation_start = None
        self.zoom_animating = False
        self.zoom_target = 0.0  # Zielwert der Animation
        self.zoom_center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)  # Zoom-Zentrum
    
    
    def run(self):
        """Hauptspielschleife"""
        # Zeige Menü
        start_menu(self)

        # Spielschleife
        while self.running and self.game:
            handle_events(self)
            update(self)
            render(self)
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CaratGame()
    game.run()
