"""
Tile-Klasse für Diamantenplättchen
"""
import random
import pygame
from constants import *

class Tile:
    """
    Repräsentiert ein Diamantenplättchen mit 4 Diamanten
    Jeder Diamant hat einen Farbwert von 1-6
    """
    
    def __init__(self, diamonds=None):
        """
        Initialisiert ein Plättchen

        Args:
            diamonds: Liste von 4 Diamantenwerten (1-6) für [oben, rechts, unten, links]
                     Wenn None, werden Werte basierend auf color_order generiert
        """
        # Zuerst color_order festlegen
        self.color_order = []
        self.set_color_order()

        if diamonds is None:
            # Verwende color_order für die Diamantenwerte
            # Mappe Farben zu Werten: red=1, blue=2, green=3, yellow=4
            color_to_value = {'red': 1, 'blue': 2, 'green': 3, 'yellow': 4}
            self.diamonds = [color_to_value[self.color_order[k]] for k in range(4)]
        else:
            if len(diamonds) != 4:
                raise ValueError("Ein Plättchen muss genau 4 Diamanten haben")
            self.diamonds = diamonds

        self.position = None  # (row, col) auf dem Spielfeld
        self.owner = None  # Spielerfarbe
        self.value = self.set_tile_value()
        self._cached_surface = None  # Gecachte Surface für Performance
        self._surface_needs_update = True  # Flag ob Surface neu gerendert werden muss

        # Animations-Variablen
        self.is_animating = False
        self.animation_start_time = 0
        self.animation_start_angle = 0
        self.animation_target_angle = 0
        self.animation_direction = 1  # 1 für clockwise, -1 für counter-clockwise

    @staticmethod
    def set_tile_value() -> int:
        get_this = random.randint(0, len(CHIP_VALUES)-1)
        return CHIP_VALUES.pop(get_this)

    def get_diamond(self, direction):
        """
        Gibt den Diamantwert in einer bestimmten Richtung zurück
        
        Args:
            direction: 'top', 'right', 'bottom', 'left'
        
        Returns:
            int: Diamantwert (1-6)
        """
        direction_map = {
            'top': 0,
            'right': 1,
            'bottom': 2,
            'left': 3
        }
        return self.diamonds[direction_map[direction]]
    
    def rotate_clockwise(self, animate=True):
        """
        Rotiert das Plättchen um 90° im Uhrzeigersinn
        [oben, rechts, unten, links] -> [links, oben, rechts, unten]

        Args:
            animate: Wenn True, wird Animation gestartet
        """
        if animate and not self.is_animating:
            # Starte Animation - Rotation wird in update_animation() durchgeführt
            self.is_animating = True
            self.animation_start_time = pygame.time.get_ticks()
            self.animation_start_angle = 0
            self.animation_target_angle = -90  # Clockwise = negativ
            self.animation_direction = 1
        elif not self.is_animating:
            # Direkte Rotation ohne Animation
            self.diamonds = [self.diamonds[3], self.diamonds[0],
                            self.diamonds[1], self.diamonds[2]]
            # Rotiere auch color_order im Uhrzeigersinn
            self.color_order = [self.color_order[3], self.color_order[0],
                               self.color_order[1], self.color_order[2]]
            self._surface_needs_update = True

    def rotate_counter_clockwise(self, animate=True):
        """
        Rotiert das Plättchen um 90° gegen den Uhrzeigersinn

        Args:
            animate: Wenn True, wird Animation gestartet
        """
        if animate and not self.is_animating:
            # Starte Animation - Rotation wird in update_animation() durchgeführt
            self.is_animating = True
            self.animation_start_time = pygame.time.get_ticks()
            self.animation_start_angle = 0
            self.animation_target_angle = 90  # Counter-clockwise = positiv
            self.animation_direction = -1
        elif not self.is_animating:
            # Direkte Rotation ohne Animation
            self.diamonds = [self.diamonds[1], self.diamonds[2],
                            self.diamonds[3], self.diamonds[0]]
            # Rotiere auch color_order gegen den Uhrzeigersinn
            self.color_order = [self.color_order[1], self.color_order[2],
                               self.color_order[3], self.color_order[0]]
            self._surface_needs_update = True
    
    def get_color(self, position):
        """
        Gibt die Farbe eines Diamanten an einer bestimmten Position zurück
        
        Args:
            position: 'top', 'right', 'bottom', 'left'
        
        Returns:
            tuple: RGB-Farbwert
        """
        value = self.get_diamond(position)
        return DIAMOND_COLORS[value]
    
    def set_position(self, row:int, col:int) -> None:
        """Setzt die Position des Plättchens auf dem Spielfeld"""
        self.position = (row, col)
    
    def set_owner(self, player_color) -> None:
        """Setzt den Besitzer des Plättchens"""
        self.owner = player_color
        self._surface_needs_update = True  # Surface muss neu gerendert werden
    
    def __repr__(self):
        return f"Tile({self.diamonds}, owner={self.owner}, pos={self.position})"
    
    @staticmethod
    def create_random_tile():
        """Factory-Methode für ein zufälliges Plättchen"""
        return Tile()
    
    @staticmethod
    def create_tile_set():
        """
        Erstellt einen kompletten Satz von
        BOARD_SIZE * BOARD_SIZE
        Plättchen für jedes Spiel
        Jede Kombination sollte theoretisch möglich sein
        """
        tiles = []
        max_tiles = BOARD_SIZE * BOARD_SIZE
        for _ in range(max_tiles):
            tiles.append(Tile.create_random_tile())
        random.shuffle(tiles)
        return tiles

    def set_color_order(self):
        all_colors = list(PLAYER_COLORS.keys())
        random.shuffle(all_colors)
        self.color_order = all_colors

    def render(self) -> pygame.Surface:
        """
        Rendert das Tile als pygame.Surface
        Verwendet Caching für bessere Performance

        Returns:
            pygame.Surface: Gerenderte Surface des Tiles
        """
        # Wenn Surface bereits gecacht ist und aktuell, zurückgeben
        if self._cached_surface is not None and not self._surface_needs_update:
            return self._cached_surface

        # Neue Surface erstellen
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        # Hintergrund (Spielerfarbe wenn vorhanden)
        if self.owner:
            bg_color = PLAYER_COLORS[self.owner]
            bg_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            bg_surface.set_alpha(100)
            bg_surface.fill(bg_color)
            surface.blit(bg_surface, (0, 0))

        # Rahmen
        pygame.draw.rect(surface, BLACK, (0, 0, TILE_SIZE, TILE_SIZE), 2)

        # Zeichne die 4 Diamanten
        # Oben Links
        self._draw_diamond_on_surface(
            surface,
            TILE_BORDER_OFFSET,
            TILE_BORDER_OFFSET,
            self.get_color('top'),
            'oben_links'
        )

        # Oben Rechts
        self._draw_diamond_on_surface(
            surface,
            TILE_SIZE - DIAMOND_RADIUS - TILE_BORDER_OFFSET * 2,
            TILE_BORDER_OFFSET,
            self.get_color('right'),
            'oben_rechts'
        )

        # Unten Rechts
        self._draw_diamond_on_surface(
            surface,
            TILE_SIZE - DIAMOND_RADIUS - TILE_BORDER_OFFSET * 2,
            TILE_SIZE // 2,
            self.get_color('bottom'),
            'unten_rechts'
        )

        # Unten Links
        self._draw_diamond_on_surface(
            surface,
            TILE_BORDER_OFFSET,
            TILE_SIZE // 2,
            self.get_color('left'),
            'unten_links'
        )

        # Zeichne den Tile-Wert in der Mitte
        font = pygame.font.Font(None, 36)
        text = font.render(str(self.value), True, WHITE)
        text_rect = text.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2))
        surface.blit(text, text_rect)

        # Surface cachen
        self._cached_surface = surface
        self._surface_needs_update = False

        return surface

    def _draw_diamond_on_surface(self, surface: pygame.Surface, x: int, y: int,
                                  color, direction: str = 'oben_links'):
        """
        Zeichnet einen Diamanten auf eine Surface

        Args:
            surface: Surface auf die gezeichnet wird
            x: X-Position
            y: Y-Position
            color: RGB-Farbe
            direction: Richtung des Diamanten
        """
        d = DIAMOND_RADIUS / 5
        if direction == 'oben_links':
            points = [
                (x, y - d + DIAMOND_RADIUS),
                (x, y + DIAMOND_RADIUS),
                (x + DIAMOND_RADIUS, y + DIAMOND_RADIUS),
                (x + DIAMOND_RADIUS, y),
                (x + DIAMOND_RADIUS - d, y)
            ]
        elif direction == 'oben_rechts':
            points = [
                (x, y),
                (x + d, y),
                (x + DIAMOND_RADIUS, y + DIAMOND_RADIUS - d),
                (x + DIAMOND_RADIUS, y + DIAMOND_RADIUS),
                (x, y + DIAMOND_RADIUS)
            ]
        elif direction == 'unten_rechts':
            points = [
                (x, y),
                (x + DIAMOND_RADIUS, y),
                (x + DIAMOND_RADIUS, y + d),
                (x + d, y + DIAMOND_RADIUS),
                (x, y + DIAMOND_RADIUS)
            ]
        elif direction == 'unten_links':
            points = [
                (x, y),
                (x + DIAMOND_RADIUS, y),
                (x + DIAMOND_RADIUS, y + DIAMOND_RADIUS),
                (x + DIAMOND_RADIUS - d, y + DIAMOND_RADIUS),
                (x, y + d)
            ]
        else:
            raise ValueError(f"Invalid direction: {direction}")

        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, BLACK, points, 2)

    def update_animation(self):
        """
        Update die Animation des Tiles
        Muss im Game-Loop aufgerufen werden

        Returns:
            bool: True wenn Animation läuft, False wenn beendet
        """
        if not self.is_animating:
            return False

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.animation_start_time

        if elapsed >= ROTATION_ANIMATION_DURATION:
            # Animation beendet
            self.is_animating = False

            # Führe die tatsächliche Rotation durch
            if self.animation_direction == 1:
                self.diamonds = [self.diamonds[3], self.diamonds[0],
                                self.diamonds[1], self.diamonds[2]]
                self.color_order = [self.color_order[3], self.color_order[0],
                                   self.color_order[1], self.color_order[2]]
            else:
                self.diamonds = [self.diamonds[1], self.diamonds[2],
                                self.diamonds[3], self.diamonds[0]]
                self.color_order = [self.color_order[1], self.color_order[2],
                                   self.color_order[3], self.color_order[0]]

            self._surface_needs_update = True
            return False

        return True

    def get_animated_surface(self) -> pygame.Surface:
        """
        Gibt eine rotierte Surface für die Animation zurück

        Returns:
            pygame.Surface: Rotierte Surface
        """
        if not self.is_animating:
            return self.render()

        # Berechne aktuellen Rotationswinkel
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.animation_start_time
        progress = min(elapsed / ROTATION_ANIMATION_DURATION, 1.0)

        # Interpoliere den Winkel
        current_angle = self.animation_start_angle + (self.animation_target_angle * progress)

        # Hole die Original-Surface und rotiere sie
        original_surface = self.render()
        rotated_surface = pygame.transform.rotate(original_surface, current_angle)

        return rotated_surface


if __name__ == "__main__":
    print(f"länge der CHIP_VALUES: {len(CHIP_VALUES)} - vorher")
    tiles_to_create = len(CHIP_VALUES)  # Anzahl merken BEVOR iteriert wird
    for i in range(tiles_to_create):
        tile = Tile.create_random_tile()
        print(f"tile {i + 1}: {tile.value} -- ({tile.color_order})")
    print(f"länge der CHIP_VALUES: {len(CHIP_VALUES)} - nachher")
