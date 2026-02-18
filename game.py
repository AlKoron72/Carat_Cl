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
    
    def __init__(self, player_count:int=2, ai_enabled_players:list=None):
        """
        Initialisiert ein neues Spiel

        Args:
            player_count: Anzahl der Spieler (2-4)
            ai_enabled_players: Liste von Player-Indizes die KI-gesteuert sind (z.B. [1, 3])
        """
        self.state = None
        self.player_count = player_count
        self.ai_enabled_players = ai_enabled_players or []
        self.board = Board(BOARD_SIZE)
        self.player_manager = PlayerManager(player_count, ai_enabled_players=self.ai_enabled_players)
        self.scoring_system = ScoringSystem(self.board, self.player_manager)
        
        self.state = GAME_STATE_MENU
        self.selected_tile = None
        self.selected_position = None
        self.valid_positions = []
        
        self.game_over = False
        self.winner = None

        # AI-State
        self.ai_move_timer = None
        self.ai_animating = False
        self.ai_animation_start = None
        self.ai_selected_position = None
        self.ai_selected_rotation = None
        self.ai_animation_positions = []  # Liste aller Positionen für Animation
        self.ai_current_animation_index = 0  # Aktueller Index in der Animation
        self.ai_last_position_change = None  # Zeitpunkt der letzten Positions-Änderung

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

        # Wenn erster Spieler KI ist, starte KI-Zug
        self._check_ai_turn()
    
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

                # Prüfe ob nächster Spieler KI ist
                self._check_ai_turn()

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

    def _check_ai_turn(self):
        """Prüft ob aktueller Spieler KI ist und startet KI-Zug"""
        import pygame
        import random
        current_player = self.player_manager.get_current_player()
        if current_player.is_ai and not current_player.is_npc:
            # Starte KI-Entscheidung
            self.ai_move_timer = pygame.time.get_ticks()
            self.ai_animating = True
            self.ai_animation_start = pygame.time.get_ticks()
            self.ai_last_position_change = pygame.time.get_ticks()

            # Lass KI entscheiden
            row, col, rotation = current_player.ai_controller.decide_placement(
                self.board, self.selected_tile, self.valid_positions
            )

            # Setze Rotation
            for _ in range(rotation):
                self.selected_tile.rotate_clockwise()

            # Speichere Position
            self.ai_selected_position = (row, col)
            self.ai_selected_rotation = rotation

            # Erstelle Animation: Mische gültige Positionen und füge finale Position ans Ende
            shuffled = list(self.valid_positions)
            random.shuffle(shuffled)
            # Entferne finale Position falls sie in der Liste ist
            if (row, col) in shuffled:
                shuffled.remove((row, col))
            # Füge finale Position ans Ende
            shuffled.append((row, col))
            self.ai_animation_positions = shuffled
            self.ai_current_animation_index = 0

    def update_ai(self):
        """
        Update-Funktion für KI-Züge. Muss in der Game-Loop aufgerufen werden.
        Wartet AI_MOVE_DELAY Millisekunden bevor der Zug ausgeführt wird.
        Animiert das Tile über verschiedene Positionen.
        """
        import pygame
        if self.ai_animating:
            current_time = pygame.time.get_ticks()
            elapsed_total = current_time - self.ai_animation_start
            elapsed_since_change = current_time - self.ai_last_position_change

            # Wechsle Position alle AI_POSITION_CYCLE_TIME Millisekunden
            if elapsed_since_change >= AI_POSITION_CYCLE_TIME:
                if self.ai_current_animation_index < len(self.ai_animation_positions) - 1:
                    self.ai_current_animation_index += 1
                    self.ai_last_position_change = current_time

            # Führe Zug aus wenn Gesamtzeit abgelaufen ist
            if elapsed_total >= AI_MOVE_DELAY:
                # Speichere Position und reset AI State VOR place_tile
                row, col = self.ai_selected_position
                self.ai_animating = False
                self.ai_selected_position = None
                self.ai_selected_rotation = None
                self.ai_animation_positions = []
                self.ai_current_animation_index = 0

                # Führe KI-Zug aus (ruft intern _check_ai_turn für nächsten Spieler auf)
                self.place_tile(row, col)

    def get_ai_preview_position(self):
        """
        Gibt die aktuelle Vorschau-Position für die AI-Animation zurück.

        Returns:
            tuple: (row, col) oder None
        """
        if self.ai_animating and self.ai_animation_positions:
            if 0 <= self.ai_current_animation_index < len(self.ai_animation_positions):
                return self.ai_animation_positions[self.ai_current_animation_index]
        return None

    def __repr__(self):
        return f"Game(state={self.state}, current_player={self.get_current_player().name})"
