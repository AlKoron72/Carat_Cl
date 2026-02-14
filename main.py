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
