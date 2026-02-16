"""
Game-Klasse mit Hauptspiellogik
"""
from board import Board
from player import PlayerManager
from tile import Tile
from scoring import ScoringSystem
from constants import *


class Game:
    """
    Hauptspiellogik für Carat
    """
    
    def __init__(self, player_count:int=2):
        """
        Initialisiert ein neues Spiel
        
        Args:
            player_count: Anzahl der Spieler (2-4)
        """
        self.state = None
        self.player_count = player_count
        self.board = Board(BOARD_SIZE)
        self.player_manager = PlayerManager(player_count)
        self.scoring_system = ScoringSystem(self.board, self.player_manager)
        
        self.state = GAME_STATE_MENU
        self.selected_tile = None
        self.selected_position = None
        self.valid_positions = []
        
        self.game_over = False
        self.winner = None
        
    def start_game(self):
        """Startet ein neues Spiel"""
        # Erstelle und verteile Plättchen
        tiles = Tile.create_tile_set()
        self.player_manager.distribute_tiles(tiles)
        
        # Setze Spielzustand
        self.state = GAME_STATE_PLAYING
        
        # Wähle das erste Plättchen des ersten Spielers
        self._select_current_player_tile()
        
        # Berechne gültige Positionen
        self.valid_positions = self.board.get_valid_placements()
    
    def _select_current_player_tile(self):
        """Wählt das aktuelle Plättchen des aktuellen Spielers"""
        current_player = self.player_manager.get_current_player()
        self.selected_tile = current_player.get_current_tile()
    
    def rotate_current_tile_clockwise(self):
        """Rotiert das ausgewählte Plättchen im Uhrzeigersinn"""
        if self.selected_tile:
            self.selected_tile.rotate_clockwise()
    
    def rotate_current_tile_counter_clockwise(self):
        """Rotiert das ausgewählte Plättchen gegen den Uhrzeigersinn"""
        if self.selected_tile:
            self.selected_tile.rotate_counter_clockwise()
    
    def place_tile(self, row:int, col:int) -> bool:
        """
        Platziert das ausgewählte Plättchen auf dem Spielfeld
        
        Args:
            row: Zeile
            col: Spalte
        
        Returns:
            bool: True wenn erfolgreich platziert
        """
        if not self.selected_tile:
            return False
        
        if not self.board.can_place_tile(row, col):
            return False
        
        # Platziere das Plättchen
        success = self.board.place_tile(self.selected_tile, row, col)
        
        if success:
            # Entferne Plättchen vom Spieler
            current_player = self.player_manager.get_current_player()
            current_player.remove_tile(self.selected_tile)
            
            # Prüfe auf vollständige Zeilen/Spalten und vergebe Punkte
            # --- old --- scoring_result = self.scoring_system.check_and_score_lines()

            # umgebende Chips für x, y
            print(f"Umgebende Chips für ({row} / {col}):")
            chip_1 = self.board.get_chip(row, col)
            chip_2 = self.board.get_chip(row, col+1)
            chip_3 = self.board.get_chip(row+1, col)
            chip_4 = self.board.get_chip(row+1, col+1)
            self.scoring_system.check_for_scores([chip_1, chip_2, chip_3, chip_4])

            # Prüfe ob Spiel zu Ende ist
            if self._is_game_over():
                self._end_game()
            else:
                # Nächster Spieler
                self.player_manager.next_player()
                self._select_current_player_tile()
                
                # Aktualisiere gültige Positionen
                self.valid_positions = self.board.get_valid_placements()
            
            return True
        
        return False
    
    def _is_game_over(self):
        """
        Prüft, ob das Spiel zu Ende ist
        Spiel endet wenn:
        - Alle Spieler keine Plättchen mehr haben
        - Kein Spieler mehr ein Plättchen platzieren kann
        
        Returns:
            bool: True wenn Spiel vorbei
        """
        # Prüfe ob alle Spieler keine Plättchen mehr haben
        all_tiles_used = all(not player.has_tiles() for player in self.player_manager.players)
        
        if all_tiles_used:
            return True
        
        # Prüfe ob noch gültige Positionen existieren
        if not self.board.get_valid_placements():
            return True
        
        return False
    
    def _end_game(self):
        """Beendet das Spiel und ermittelt den Gewinner"""
        self.game_over = True
        self.state = GAME_STATE_GAME_OVER
        self.winner = self.player_manager.get_winner()
    
    def get_current_player(self):
        """Gibt den aktuellen Spieler zurück"""
        return self.player_manager.get_current_player()
    
    def get_leaderboard(self):
        """Gibt die aktuelle Rangliste zurück"""
        return self.player_manager.get_leaderboard()
    
    def is_valid_placement(self, row:int, col:int) -> bool:
        """Prüft, ob eine Position für die Platzierung gültig ist"""
        return (row, col) in self.valid_positions
    
    def reset(self):
        """Setzt das Spiel zurück"""
        self.__init__(self.player_count)
    
    def __repr__(self):
        return f"Game(state={self.state}, current_player={self.get_current_player().name})"
