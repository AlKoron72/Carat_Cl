"""
Board-Klasse für Spielfeldverwaltung
"""
from point_chip import PointChip
from tile import Tile


class Board:
    """
    Repräsentiert das Spielfeld
    BOARD_SIZE x BOARD_SIZE
    """
    
    def __init__(self, size:int = 7):
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
        Prüft, ob ein Plättchen an dieser Position platziert werden kann.
        Regeln:
        - Erstes Plättchen kann überall hin AUSSER auf Randfelder
        - weitere Plättchen müssen eine gemeinsame Außenkante mit einem vorhandenen haben
          (horizontal oder vertikal benachbart, NICHT diagonal)

        Args:
            row: Zeile
            col: Spalte

        Returns:
            bool: True wenn Platzierung erlaubt
        """
        # Position muss gültig und leer sein
        if not self.is_empty(row, col):
            return False

        # Erstes Plättchen darf überall hin, ABER NICHT auf Randfelder
        if self.placed_tiles_count == 0:
            # Prüfe ob es ein Randfeld ist
            is_edge = (row == 0 or row == self.size - 1 or
                      col == 0 or col == self.size - 1)
            return not is_edge

        # Prüfe ob es eine gemeinsame Kante mit einem vorhandenen Plättchen gibt
        # Kantennachbarn: horizontal oder vertikal benachbart (NICHT diagonal)
        edge_neighbors = [
            (row - 1, col),  # oben
            (row + 1, col),  # unten
            (row, col - 1),  # links
            (row, col + 1)   # rechts
        ]

        for neighbor_row, neighbor_col in edge_neighbors:
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

        # Markiere das Feld als besetzt
        self.placed_tiles[row][col] = 1

        # Aktualisiere die distribution der 4 Ecken-Chips
        # Jede Ecke entspricht einer Position im color_order
        chip_data = [
            ((row, col), 0),         # oben links -> color_order[0]
            ((row, col + 1), 1),     # oben rechts -> color_order[1]
            ((row + 1, col + 1), 2), # unten rechts -> color_order[2]
            ((row + 1, col), 3)      # unten links -> color_order[3]
        ]

        for (chip_row, chip_col), color_index in chip_data:
            chip = self.get_chip(chip_row, chip_col)
            if chip:
                color = tile.color_order[color_index]
                # Füge den tile.value zur entsprechenden Farbe hinzu
                if color in chip.distribution:
                    chip.distribution[color] += tile.value
                else:
                    chip.distribution[color] = tile.value

        # Berechne Distribution-Prozente für alle betroffenen Chips
        from utils.update import recalculate_chip_distribution
        for (chip_row, chip_col), _ in chip_data:
            chip = self.get_chip(chip_row, chip_col)
            if chip:
                recalculate_chip_distribution(chip)

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