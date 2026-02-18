"""
Hauptdatei für Carat Brettspiel - Pygbag (Browser) Version
"""
import asyncio
import pygame
import sys
from constants import *
from renderer import Renderer
from game import Game
from utils import handle_events, update, render


class CaratGame:
    """
    Hauptklasse für das Spiel (Pygbag Version)
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
        self.in_menu = True

        # Maus-State
        self.mouse_pos = (0, 0)

        # Menu-Elemente
        self.menu_font = pygame.font.Font(None, TITLE_FONT_SIZE)
        self.button_font = pygame.font.Font(None, FONT_SIZE)
        self.menu_buttons = [
            {"text": "1 Spieler (Testing)", "rect": pygame.Rect(400, 240, 400, 60), "players": 1},
            {"text": "2 Spieler", "rect": pygame.Rect(400, 320, 400, 60), "players": 2},
            {"text": "3 Spieler", "rect": pygame.Rect(400, 400, 400, 60), "players": 3},
            {"text": "4 Spieler", "rect": pygame.Rect(400, 480, 400, 60), "players": 4},
            {"text": "Beenden", "rect": pygame.Rect(400, 560, 400, 60), "players": 0},
        ]

    def handle_menu_events(self):
        """Event-Handling für Menü"""
        self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.menu_buttons:
                    if button["rect"].collidepoint(self.mouse_pos):
                        if button["players"] == 0:
                            self.running = False
                            return
                        else:
                            # Starte Spiel
                            self.game = Game(button["players"])
                            self.game.start_game()
                            self.in_menu = False
                            return

    def render_menu(self):
        """Zeichnet das Menü"""
        self.screen.fill(BACKGROUND)

        # Titel
        title = self.menu_font.render("Carat", True, BLACK)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Buttons
        for button in self.menu_buttons:
            # Hover-Effekt
            if button["rect"].collidepoint(self.mouse_pos):
                color = BUTTON_HOVER
            else:
                color = BUTTON_COLOR

            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2)

            # Text
            text = self.button_font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    async def run(self):
        """Hauptspielschleife (async für Browser)"""
        while self.running:
            if self.in_menu:
                # Menü-Loop
                self.handle_menu_events()
                self.render_menu()
                self.clock.tick(FPS)
            elif self.game:
                # Spiel-Loop
                handle_events(self)
                update(self)
                render(self)
                self.clock.tick(FPS)

            # WICHTIG: Yield control an Browser zurück
            await asyncio.sleep(0)

        pygame.quit()
        sys.exit()

async def main():
    """Entry point für Pygbag"""
    game = CaratGame()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
