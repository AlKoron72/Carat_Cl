"""
Tile-Klasse für Diamantenplättchen
"""
import random
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
                     Wenn None, werden zufällige Werte generiert
        """
        if diamonds is None:
            self.diamonds = [random.randint(1, 4) for _ in range(4)]
        else:
            if len(diamonds) != 4:
                raise ValueError("Ein Plättchen muss genau 4 Diamanten haben")
            self.diamonds = diamonds
        
        self.position = None  # (row, col) auf dem Spielfeld
        self.owner = None  # Spielerfarbe
        self.value = self.set_tile_value()
        self.color_order = []
        self.set_color_order()

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
    
    def rotate_clockwise(self):
        """
        Rotiert das Plättchen um 90° im Uhrzeigersinn
        [oben, rechts, unten, links] -> [links, oben, rechts, unten]
        """
        self.diamonds = [self.diamonds[3], self.diamonds[0], 
                        self.diamonds[1], self.diamonds[2]]
    
    def rotate_counter_clockwise(self):
        """
        Rotiert das Plättchen um 90° gegen den Uhrzeigersinn
        """
        self.diamonds = [self.diamonds[1], self.diamonds[2], 
                        self.diamonds[3], self.diamonds[0]]
    
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
    
    def __repr__(self):
        return f"Tile({self.diamonds}, owner={self.owner}, pos={self.position})"
    
    @staticmethod
    def create_random_tile():
        """Factory-Methode für ein zufälliges Plättchen"""
        return Tile()
    
    @staticmethod
    def create_tile_set():
        """
        Erstellt einen kompletten Satz von 36 Plättchen für das Spiel
        Jede Kombination sollte theoretisch möglich sein
        """
        tiles = []
        for _ in range(36):
            tiles.append(Tile.create_random_tile())
        random.shuffle(tiles)
        return tiles

    def set_color_order(self):
        all_colors = list(PLAYER_COLORS.keys())
        random.shuffle(all_colors)
        self.color_order = all_colors


if __name__ == "__main__":
    print(f"länge der CHIP_VALUES: {len(CHIP_VALUES)} - vorher")
    tiles_to_create = len(CHIP_VALUES)  # Anzahl merken BEVOR iteriert wird
    for i in range(tiles_to_create):
        tile = Tile.create_random_tile()
        print(f"tile {i + 1}: {tile.value} -- ({tile.color_order})")
    print(f"länge der CHIP_VALUES: {len(CHIP_VALUES)} - nachher")
