"""
Board-Klasse für Spielfeldverwaltung
"""
from constants import *
from point_chip import PointChip
from tile import Tile


class Board:
    """
    Repräsentiert das 7x7 Spielfeld
    """
    
    def __init__(self, size:int = BOARD_SIZE):
        """
        Initialisiert das Spielfeld
        
        Args:
            size: Größe des Spielfelds (Standard: 8x8)
        """
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]  # Plättchen
        self.chips = PointChip.place_chips_on_board(size)  # Punktechips
        self.placed_tiles_count = 0 # for first placed tile
        self.placed_tiles = [[0 for _ in range(size)] for _ in range(size)]
    
    def is_valid_position(self, row, col):
        """
        Prüft, ob eine Position auf dem Spielfeld gültig ist
        
        Args:
            row: Zeile
            col: Spalte
        
        Returns:
            bool: True wenn Position gültig
        """
        return 0 <= row < self.size and 0 <= col < self.size
    
    def is_empty(self, row, col):
        """
        Prüft, ob eine Position leer ist
        
        Args:
            row: Zeile
            col: Spalte
        
        Returns:
            bool: True wenn Position leer
        """
        return self.is_valid_position(row, col) and self.grid[row][col] is None
    
    def can_place_tile(self, row, col):
        """
        Prüft, ob ein Plättchen an dieser Position platziert werden kann
        Regeln:
        - Erstes Plättchen kann überall hin
        - Weitere Plättchen müssen eine gemeinsame Ecke mit einem vorhandenen haben
        
        Args:
            row: Zeile
            col: Spalte
        
        Returns:
            bool: True wenn Platzierung erlaubt
        """
        # Position muss gültig und leer sein
        if not self.is_empty(row, col):
            return False
        
        # Erstes Plättchen darf überall hin
        if self.placed_tiles_count == 0:
            return True
        
        # Prüfe ob es eine gemeinsame Ecke mit einem vorhandenen Plättchen gibt
        # Ecknachbarn: diagonal benachbart
        corner_neighbors = [
            (row - 1, col - 1),  # oben links
            (row - 1, col + 1),  # oben rechts
            (row + 1, col - 1),  # unten links
            (row + 1, col + 1)   # unten rechts
        ]
        
        for neighbor_row, neighbor_col in corner_neighbors:
            if self.is_valid_position(neighbor_row, neighbor_col):
                if self.grid[neighbor_row][neighbor_col] is not None:
                    return True
        
        return False
    
    def place_tile(self, tile, row, col):
        """
        Platziert ein Plättchen auf dem Spielfeld
        
        Args:
            tile: Tile-Objekt
            row: Zeile
            col: Spalte
        
        Returns:
            bool: True wenn erfolgreich platziert
        """
        if not self.can_place_tile(row, col):
            return False
        
        self.grid[row][col] = tile
        tile.set_position(row, col)
        self.placed_tiles_count += 1
        return True
    
    def get_tile(self, row:int, col:int) -> Tile | None:
        """
        Gibt das Plättchen an einer Position zurück
        
        Args:
            row: Zeile
            col: Spalte
        
        Returns:
            Tile oder None
        """
        if self.is_valid_position(row, col):
            return self.grid[row][col]
        return None
    
    def get_chip(self, row:int, col:int) -> PointChip | None:
        """
        Gibt den Punktechip an einer Position zurück
        
        Args:
            row: Zeile
            col: Spalte
        
        Returns:
            PointChip oder None
        """
        return self.chips.get((row, col))
    
    def is_row_complete(self, row:int) -> bool:
        """
        Prüft, ob eine Zeile vollständig mit Plättchen gefüllt ist
        
        Args:
            row: Zeile
        
        Returns:
            bool: True wenn Zeile vollständig
        """
        for col in range(self.size):
            if self.grid[row][col] is None:
                return False
        return True
    
    def is_column_complete(self, col:int) -> bool:
        """
        Prüft, ob eine Spalte vollständig mit Plättchen gefüllt ist
        
        Args:
            col: Spalte
        
        Returns:
            bool: True wenn Spalte vollständig
        """
        for row in range(self.size):
            if self.grid[row][col] is None:
                return False
        return True
    
    def get_completed_lines(self):
        """
        Gibt alle vollständigen Zeilen und Spalten zurück
        
        Returns:
            dict: {'rows': [row_indices], 'cols': [col_indices]}
        """
        completed = {'rows': [], 'cols': []}
        
        for row in range(self.size):
            if self.is_row_complete(row):
                completed['rows'].append(row)
        
        for col in range(self.size):
            if self.is_column_complete(col):
                completed['cols'].append(col)
        
        return completed
    
    def get_valid_placements(self):
        """
        Gibt alle gültigen Positionen zurück, an denen ein Plättchen platziert werden kann
        
        Returns:
            list: Liste von (row, col) Tupeln
        """
        valid_positions = []
        for row in range(self.size):
            for col in range(self.size):
                if self.can_place_tile(row, col):
                    valid_positions.append((row, col))
        return valid_positions
    
    def __repr__(self):
        return f"Board(size={self.size}, placed_tiles={self.placed_tiles_count})"

if __name__ == "__main__":
    board = Board()
    print(board.placed_tiles)