"""
Renderer-Klasse für die grafische Darstellung
"""
import pygame
from board import Board
from constants import *
from game import Game
from point_chip import PointChip
from tile import Tile


class Renderer:
    """
    Verwaltet die grafische Darstellung des Spiels
    """
    
    def __init__(self, screen):
        """
        Initialisiert den Renderer
        
        Args:
            screen: PyGame-Screen-Objekt
        """
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
    
    def draw_board(self, board):
        """
        Zeichnet das Spielfeld mit Gitternetz
        
        Args:
            board: Board-Objekt
        """
        for row in range(board.size):
            for col in range(board.size):
                x = BOARD_OFFSET_X + col * CELL_SIZE
                y = BOARD_OFFSET_Y + row * CELL_SIZE
                
                # Zeichne Zelle
                pygame.draw.rect(self.screen, LIGHT_GRAY, (x, y, CELL_SIZE, CELL_SIZE), 3)
                
                # Zeichne Punktechip (wenn vorhanden)
                chip = board.get_chip(row, col)
                if chip and not chip.is_collected():
                    self._draw_chip(chip, x + CELL_SIZE // 2, y + CELL_SIZE // 2)
    
    def draw_tiles(self, board:Board) -> None:
        """
        Zeichnet alle platzierten Plättchen auf dem Spielfeld
        
        Args:
            board: Board-Objekt
        """
        for row in range(board.size):
            for col in range(board.size):
                tile = board.get_tile(row, col)
                if tile:
                    x = BOARD_OFFSET_X + col * CELL_SIZE + 2
                    y = BOARD_OFFSET_Y + row * CELL_SIZE + 2
                    self._draw_tile(tile, x, y)
    
    def _draw_tile(self, tile:Tile, x:int, y:int) -> None:
        """
        Zeichnet ein einzelnes Plättchen
        
        Args:
            tile: Tile-Objekt
            x: X-Position (Pixel)
            y: Y-Position (Pixel)
        """
        # Hintergrund des Plättchens (Spielerfarbe)
        if tile.owner:
            bg_color = PLAYER_COLORS[tile.owner]
            # Leicht transparent machen
            s = pygame.Surface((TILE_SIZE, TILE_SIZE))
            s.set_alpha(100)
            s.fill(bg_color)
            self.screen.blit(s, (x, y))
        
        # Rahmen
        pygame.draw.rect(self.screen, BLACK, (x, y, TILE_SIZE, TILE_SIZE), 2)
        
        # Zeichne die 4 Diamanten an den Positionen
        # oben links
        self._draw_diamond(
            x + TILE_BORDER_OFFSET,
            y + TILE_BORDER_OFFSET,
            tile.get_color('top'),
            'oben_links'
        )

        # Oben Rechts
        self._draw_diamond(
            x + TILE_SIZE - DIAMOND_RADIUS - TILE_BORDER_OFFSET*2,
            y + TILE_BORDER_OFFSET,
            tile.get_color('right'),
            'oben_rechts'
        )

        # Unten Rechts
        self._draw_diamond(
            x + TILE_SIZE - DIAMOND_RADIUS - TILE_BORDER_OFFSET*2,
            y + TILE_SIZE // 2,
            tile.get_color('bottom'),
            'unten_rechts'
        )

        # Unten Links
        self._draw_diamond(
            x + TILE_BORDER_OFFSET,
            y + TILE_SIZE // 2,
            tile.get_color('left'),
            'unten_links'
        )
    
    def _draw_diamond(self, x:int, y:int, color, direction:str='oben_links'):
        """
        Zeichnet einen Diamanten (Raute)
        
        Args:
            x: X-Position (Pixel)
            y: Y-Position (Pixel)
            color: RGB-Farbe
        points = [
            (x, y - DIAMOND_RADIUS),      # Oben
            (x + DIAMOND_RADIUS, y),      # Rechts
            (x, y + DIAMOND_RADIUS),      # Unten
            (x - DIAMOND_RADIUS, y)       # Links
        ]
        """

        d = DIAMOND_RADIUS / 5
        if direction == 'oben_links':
            points = [
                (x, y-d+DIAMOND_RADIUS),
                (x, y+DIAMOND_RADIUS),
                (x+DIAMOND_RADIUS, y+DIAMOND_RADIUS),
                (x+DIAMOND_RADIUS, y),
                (x+DIAMOND_RADIUS-d, y)
            ]
        elif direction == 'oben_rechts':
            points = [
                (x, y),
                (x+d, y),
                (x+DIAMOND_RADIUS, y+DIAMOND_RADIUS-d),
                (x+DIAMOND_RADIUS, y+DIAMOND_RADIUS),
                (x, y+DIAMOND_RADIUS)
            ]
        elif direction == 'unten_rechts':
            points = [
                (x, y),
                (x+DIAMOND_RADIUS, y),
                (x+DIAMOND_RADIUS, y+d),
                (x+d, y+DIAMOND_RADIUS),
                (x, y+DIAMOND_RADIUS)
            ]
        elif direction == 'unten_links':
            points = [
                (x, y),
                (x+DIAMOND_RADIUS, y),
                (x+DIAMOND_RADIUS, y+DIAMOND_RADIUS),
                (x+DIAMOND_RADIUS-d, y+DIAMOND_RADIUS),
                (x, y+d)
            ]
        else:
            raise ValueError(f"Invalid direction: {direction}")
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, BLACK, points, 2)
    
    def _draw_chip(self, chip:PointChip, x:int, y:int) -> None:
        """
        Zeichnet einen Punktechip
        
        Args:
            chip: PointChip-Objekt
            x: X-Position (Pixel)
            y: Y-Position (Pixel)
        """
        # Kreis
        pygame.draw.circle(self.screen, BLACK, (x+OFFSET, y+OFFSET), CHIP_RADIUS)
        pygame.draw.circle(self.screen, DARK_GRAY, (x, y), CHIP_RADIUS)
        pygame.draw.circle(self.screen, LIGHT_GRAY, (x, y), CHIP_RADIUS, 4)
        
        # Wert
        text = self.font.render(str(chip.value), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)
    
    def draw_valid_positions(self, valid_positions):
        """
        Zeichnet markierte gültige Positionen
        
        Args:
            valid_positions: Liste von (row, col) Tupeln
        """
        for row, col in valid_positions:
            x = BOARD_OFFSET_X + col * CELL_SIZE
            y = BOARD_OFFSET_Y + row * CELL_SIZE
            
            # Grüner Rahmen
            pygame.draw.rect(self.screen, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE), 3)
    
    def draw_preview_tile(self, tile:Tile, mouse_pos:tuple[int, int]):
        """
        Zeichnet eine Vorschau des Plättchens an der Mausposition
        
        Args:
            tile: Tile-Objekt
            mouse_pos: (x, y) Mausposition
        """
        x, y = mouse_pos
        x -= TILE_SIZE // 2
        y -= TILE_SIZE // 2
        
        # Semi-transparent
        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        s.set_alpha(150)
        
        # Zeichne Plättchen auf Surface
        if tile.owner:
            s.fill(PLAYER_COLORS[tile.owner])
        else:
            s.fill(WHITE)
        
        self.screen.blit(s, (x, y))
        self._draw_tile(tile, x, y)
    
    def draw_player_info(self, game):
        """
        Zeichnet Spielerinformationen (Punktestand, aktueller Spieler)
        
        Args:
            game: Game-Objekt
        """
        info_x = BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + 50
        info_y = BOARD_OFFSET_Y
        
        # Überschrift
        title = self.title_font.render("Spieler", True, BLACK)
        self.screen.blit(title, (info_x, info_y))
        info_y += 50
        
        # Spielerinformationen
        for player in game.player_manager.players:
            is_current = player == game.get_current_player()
            
            # Spielerfarbe
            pygame.draw.circle(self.screen, PLAYER_COLORS[player.color], 
                             (info_x + 20, info_y + 15), 15)
            
            # Name und Punktzahl
            text = f"{player.name}: {player.score} Punkte"
            if is_current:
                text += " ◄"
                color = (0, 150, 0)
            else:
                color = BLACK
            
            player_text = self.font.render(text, True, color)
            self.screen.blit(player_text, (info_x + 45, info_y))
            
            # Verbleibende Plättchen
            tiles_text = self.font.render(f"Plättchen: {player.get_tile_count()}", True, BLACK)
            self.screen.blit(tiles_text, (info_x + 45, info_y + 25))
            
            info_y += 70
    
    def draw_current_tile(self, tile:Tile) -> None:
        """
        Zeichnet das aktuelle Plättchen in einer separaten Vorschau
        
        Args:
            tile: Tile-Objekt
        """
        preview_x = BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE + 50
        preview_y = 500
        
        # Überschrift
        title = self.font.render("Aktuelles Plättchen:", True, BLACK)
        self.screen.blit(title, (preview_x, preview_y))
        
        # Plättchen
        tile_x = preview_x + 50
        tile_y = preview_y + 40
        self._draw_tile(tile, tile_x, tile_y)
        
        # Hinweis
        hint = self.font.render("R: Drehen →", True, DARK_GRAY)
        self.screen.blit(hint, (preview_x, tile_y + TILE_SIZE + 20))
        hint2 = self.font.render("E: Drehen ←", True, DARK_GRAY)
        self.screen.blit(hint2, (preview_x, tile_y + TILE_SIZE + 45))
    
    def draw_game_over(self, game:Game) -> None:
        """
        Zeichnet den Game-Over Bildschirm
        
        Args:
            game: Game-Objekt
        """
        # Semi-transparenter Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Titel
        title = self.title_font.render("Spiel beendet!", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Rangliste
        y = 250
        leaderboard = game.get_leaderboard()
        
        for i, player in enumerate(leaderboard):
            rank_text = f"{i+1}. {player.name}: {player.score} Punkte"
            color = PLAYER_COLORS[player.color]
            
            text = self.font.render(rank_text, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            
            y += 40
        
        # Neustart-Hinweis
        hint = self.font.render("Drücke SPACE für ein neues Spiel", True, WHITE)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        self.screen.blit(hint, hint_rect)
