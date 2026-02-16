"""
Renderer-Klasse für die grafische Darstellung
"""
import pygame
import pygame.gfxdraw
import math
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
        Zeichnet das Spielfeld-Gitternetz (ohne Chips)

        Args:
            board: Board-Objekt
        """
        # Zeichne das Tile-Raster
        for row in range(board.size):
            for col in range(board.size):
                x = BOARD_OFFSET_X + col * CELL_SIZE
                y = BOARD_OFFSET_Y + row * CELL_SIZE

                # Zeichne Zelle
                pygame.draw.rect(self.screen, LIGHT_GRAY, (x, y, CELL_SIZE, CELL_SIZE), 3)

    def draw_chips(self, board):
        """
        Zeichnet die Punktechips an den Ecken der Tiles
        Sollte als letztes aufgerufen werden, damit Chips im Vordergrund bleiben

        Args:
            board: Board-Objekt
        """
        # Zeichne Punktechips an den Ecken (board.size+1 x board.size+1 Raster)
        for row in range(board.size + 1):
            for col in range(board.size + 1):
                chip = board.get_chip(row, col)
                if chip:
                    # Chips sitzen an den Ecken der Tiles
                    x = BOARD_OFFSET_X + col * CELL_SIZE
                    y = BOARD_OFFSET_Y + row * CELL_SIZE
                    self._draw_chip(chip, x, y)
    
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
    
    def _draw_tile(self, tile:Tile, x:int, y:int, surface:pygame.Surface=None) -> None:
        """
        Zeichnet ein einzelnes Plättchen mit Caching

        Args:
            tile: Tile-Objekt
            x: X-Position (Pixel)
            y: Y-Position (Pixel)
            surface: Optionale Surface für Animation (wenn None, wird tile.render() verwendet)
        """
        if surface is None:
            # Verwende gecachte Surface vom Tile
            surface = tile.render()

        # Blitte die Surface auf den Screen
        self.screen.blit(surface, (x, y))
    
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
        Zeichnet einen Punktechip mit optionaler prozentualer Verteilung
        Ebenen (von unten nach oben): Schatten -> Tortendiagramm -> Dunkelgrauer Hintergrund -> Grauer Rand -> Zahl

        Args:
            chip: PointChip-Objekt
            x: X-Position (Pixel)
            y: Y-Position (Pixel)
        """
        x = int(x)
        y = int(y)
        radius = int(CHIP_RADIUS)

        # Ebene 1 (ganz unten): Schatten mit Anti-Aliasing
        pygame.gfxdraw.filled_circle(self.screen, x+OFFSET, y+OFFSET, radius, BLACK)
        pygame.gfxdraw.aacircle(self.screen, x+OFFSET, y+OFFSET, radius, BLACK)

        # Ebene 2: Tortendiagramm im Hintergrund (größer)
        # Verwende distribution_preview (enthält Prozente) statt distribution (enthält Rohwerte)
        display_distribution = chip.distribution_preview if chip.distribution_preview else None
        if display_distribution:
            distribution_radius = int(CHIP_RADIUS + POINTS_DISTRIBUTION_BORDER)
            start_angle = 0
            for color, percentage in display_distribution.items():
                if percentage > 0:
                    angle = percentage * 360  # Winkel in Grad
                    self._draw_pie_slice(x, y, distribution_radius, start_angle, angle, PLAYER_COLORS[color])
                    start_angle += angle

        # Ebene 3: Dunkelgrauer Hintergrund (Hauptkreis) mit Anti-Aliasing
        pygame.gfxdraw.filled_circle(self.screen, x, y, radius, DARK_GRAY)
        pygame.gfxdraw.aacircle(self.screen, x, y, radius, DARK_GRAY)

        # Ebene 4: Grauer Rand mit Anti-Aliasing (mehrere Kreise für Dicke)
        for i in range(4):
            pygame.gfxdraw.aacircle(self.screen, x, y, radius - i, LIGHT_GRAY)

        # Ebene 5 (ganz oben): Zahl
        text = self.font.render(str(chip.value), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)

    def _draw_pie_slice(self, x:int, y:int, radius:int, start_angle:float, angle_size:float, color:tuple) -> None:
        """
        Zeichnet ein Tortenstück mit Anti-Aliasing

        Args:
            x, y: Mittelpunkt
            radius: Radius
            start_angle: Startwinkel in Grad (0 = oben)
            angle_size: Größe des Winkels in Grad
            color: RGB-Farbe
        """
        import math

        # Konvertiere zu Radiant (pygame verwendet Radiant für Winkel)
        # -90 damit 0° oben ist statt rechts
        start_rad = math.radians(start_angle - 90)
        end_rad = math.radians(start_angle + angle_size - 90)

        # Erstelle Polygon-Punkte für das Tortenstück
        points = [(x, y)]  # Mittelpunkt

        # Generiere mehr Punkte für glattere Kanten
        steps = max(10, int(angle_size / 2))  # Deutlich mehr Steps für glattere Kurven
        for i in range(steps + 1):
            angle = start_rad + (end_rad - start_rad) * i / steps
            point_x = int(x + radius * math.cos(angle))
            point_y = int(y + radius * math.sin(angle))
            points.append((point_x, point_y))

        # Zeichne das gefüllte Tortenstück
        pygame.gfxdraw.filled_polygon(self.screen, points, color)

        # Zeichne geglätteten Rand um das Tortenstück
        pygame.gfxdraw.aapolygon(self.screen, points, color)

    def _draw_star(self, x:int, y:int, radius:int, color:tuple) -> None:
        """
        Zeichnet einen 5-zackigen Stern

        Args:
            x, y: Mittelpunkt
            radius: Radius (äußere Spitzen)
            color: RGB-Farbe
        """
        inner_radius = radius * 0.4  # Innere Punkte sind 40% des Radius
        points = []

        # Erstelle 10 Punkte (5 äußere, 5 innere abwechselnd)
        for i in range(10):
            angle = math.radians(i * 36 - 90)  # -90 damit Spitze nach oben zeigt
            if i % 2 == 0:  # Äußere Punkte
                r = radius
            else:  # Innere Punkte
                r = inner_radius

            point_x = x + r * math.cos(angle)
            point_y = y + r * math.sin(angle)
            points.append((point_x, point_y))

        # Zeichne gefüllten Stern
        pygame.gfxdraw.filled_polygon(self.screen, points, color)
        # Zeichne geglätteten Rand
        pygame.gfxdraw.aapolygon(self.screen, points, color)

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

        # Wenn Animation läuft, verwende animierte Surface
        if tile.is_animating:
            tile_surface = tile.get_animated_surface().copy()
            # Zentriere die rotierte Surface
            offset_x = (tile_surface.get_width() - TILE_SIZE) // 2
            offset_y = (tile_surface.get_height() - TILE_SIZE) // 2
            tile_surface.set_alpha(150)
            self.screen.blit(tile_surface, (x - offset_x, y - offset_y))
        else:
            # Hole gerenderte Surface
            tile_surface = tile.render().copy()
            tile_surface.set_alpha(150)
            self.screen.blit(tile_surface, (x, y))
    
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

        # Trenne echte Spieler und NPCs
        real_players = [p for p in game.player_manager.players if not p.is_npc]
        npcs = [p for p in game.player_manager.players if p.is_npc]

        # Zeichne echte Spieler
        for i, player in enumerate(real_players):
            player_index = game.player_manager.players.index(player)
            is_current = player == game.get_current_player()
            is_starting = game.player_manager.is_starting_player(player_index)

            # Spielerfarbe
            circle_x = info_x + 20
            circle_y = info_y + 15
            pygame.draw.circle(self.screen, PLAYER_COLORS[player.color],
                             (circle_x, circle_y), 15)

            # Zeichne Stern für Startspieler
            if is_starting:
                self._draw_star(circle_x, circle_y, 8, WHITE)

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

        # Trennlinie wenn NPCs vorhanden
        if npcs:
            line_width = 250
            pygame.draw.line(self.screen, DARK_GRAY, (info_x, info_y), (info_x + line_width, info_y), 2)
            info_y += 20

            # Zeichne NPCs
            for player in npcs:
                # Spielerfarbe
                circle_x = info_x + 20
                circle_y = info_y + 15
                pygame.draw.circle(self.screen, PLAYER_COLORS[player.color],
                                 (circle_x, circle_y), 15)

                # Name und Punktzahl (ohne aktuelle Spieler-Markierung)
                text = f"{player.name}: {player.score} Punkte"
                player_text = self.font.render(text, True, DARK_GRAY)
                self.screen.blit(player_text, (info_x + 45, info_y))

                # Keine Plättchen-Anzeige für NPCs

                info_y += 50
    
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

        # Plättchen mit Animation
        tile_x = preview_x + 50
        tile_y = preview_y + 40

        # Wenn Animation läuft, verwende animierte Surface
        if tile.is_animating:
            animated_surface = tile.get_animated_surface()
            # Zentriere die rotierte Surface (sie kann größer sein)
            offset_x = (animated_surface.get_width() - TILE_SIZE) // 2
            offset_y = (animated_surface.get_height() - TILE_SIZE) // 2
            self.screen.blit(animated_surface, (tile_x - offset_x, tile_y - offset_y))
        else:
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

        # Echte Spieler
        for i, player in enumerate(leaderboard['players']):
            rank_text = f"{i+1}. {player.name}: {player.score} Punkte"
            color = PLAYER_COLORS[player.color]

            text = self.font.render(rank_text, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(text, text_rect)

            y += 40

        # Trennlinie wenn NPCs vorhanden
        if leaderboard['npcs']:
            y += 20
            line_width = 300
            line_x = (WINDOW_WIDTH - line_width) // 2
            pygame.draw.line(self.screen, WHITE, (line_x, y), (line_x + line_width, y), 2)
            y += 40

            # NPCs
            for player in leaderboard['npcs']:
                rank_text = f"{player.name}: {player.score} Punkte"
                color = PLAYER_COLORS[player.color]

                text = self.font.render(rank_text, True, color)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
                self.screen.blit(text, text_rect)

                y += 40
        
        # Neustart-Hinweis
        hint = self.font.render("Drücke SPACE für ein neues Spiel", True, WHITE)
        hint_rect = hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        self.screen.blit(hint, hint_rect)
