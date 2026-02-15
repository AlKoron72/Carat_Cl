"""
PointChip-Klasse für Punktechips auf dem Spielfeld
"""
import random

import constants
from constants import CHIP_VALUES


class PointChip:
    """
    Repräsentiert einen Punktechip mit einem Wert von 1-5
    """
    
    def __init__(self, value:int):
        """
        Initialisiert einen Punktechip
        
        Args:
            value: Punktwert (1-5)
        """
        if value not in [1, 2, 3, 4, 5, 6]:
            raise ValueError("Punktwert muss zwischen 1 und 6 liegen")
        
        self.value = value
        self.position = None  # (row, col) auf dem Spielfeld
        self.collected = False
        self.collected_by = None  # Spielerfarbe
    
    def set_position(self, row:int, col:int):
        """Setzt die Position des Chips auf dem Spielfeld"""
        self.position = (row, col)
    
    def collect(self, player_color):
        """
        Sammelt den Chip für einen Spieler ein
        
        Args:
            player_color: Farbe des Spielers
        """
        self.collected = True
        self.collected_by = player_color
    
    def is_collected(self):
        """Prüft, ob der Chip bereits eingesammelt wurde"""
        return self.collected
    
    def __repr__(self):
        status = f"collected by {self.collected_by}" if self.collected else "available"
        return f"PointChip(value={self.value}, pos={self.position}, {status})"
    
    @staticmethod
    def create_chip_set():
        """
        Erstellt einen kompletten Satz von 49 Punktechips
        Verteilung gemäß den Spielregeln
        """
        chips = [PointChip(value) for value in CHIP_VALUES]
        random.shuffle(chips)
        return chips
    
    @staticmethod
    def place_chips_on_board(board_size:int = constants.BOARD_SIZE):
        """
        Erstellt und platziert Chips auf einem Spielfeld an den Ecken der Tiles
        Die Chips werden in einem (board_size+1) x (board_size+1) Raster platziert

        Args:
            board_size: Größe des Spielfelds (Standard: 7x7 Tiles = 8x8 Ecken)

        Returns:
            dict: Dictionary mit (row, col) als Key und PointChip als Value
        """
        chips = PointChip.create_chip_set()
        chip_positions = {}

        chip_index = 0
        # Chips werden an den Ecken platziert: (board_size+1) x (board_size+1)
        for row in range(board_size + 1):
            for col in range(board_size + 1):
                if chip_index < len(chips):
                    chips[chip_index].set_position(row, col)
                    chip_positions[(row, col)] = chips[chip_index]
                    chip_index += 1

        return chip_positions
