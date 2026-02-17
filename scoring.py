"""
Wertungssystem für Carat
"""
from board import Board
from player import PlayerManager, Player
from point_chip import PointChip


class ScoringSystem:
    """
    Verwaltet die Punkteberechnung bei vollständigen Reihen/Spalten
    """
    
    def __init__(self, board: Board, player_manager: PlayerManager) -> None:
        """
        Initialisiert das Wertungssystem
        
        Args:
            board: Board-Objekt
            player_manager: PlayerManager-Objekt
        """
        self.board = board
        self.player_manager = player_manager
    
    def check_for_scores(self, chips: list[PointChip]) -> None:
        """
        checks if any of the points chips need to be scored
        by player/s
        """
        print("------------- checking for scores -------------")
        for chip in chips:
            chip.placed_surrounding_pieces += 1
            print(f"Value (oben links): {chip.surrounding_pieces} -> {chip.distribution}")
            if chip.placed_surrounding_pieces == chip.surrounding_pieces:
                print(f"please score this chip {chip.position}")
                # implement score here
                # at this point player-color not in play produce errors
                # because the need for NPC-colors is not yet implemented
            if chip.surrounding_pieces == 1: # wenn es sich um eines der Eckfelder handelt
                print(f"Chip {chip} is complete")
                #spieler = _get_player_by_color(chip.distribution.key)
                for key in chip.distribution.keys():
                    print(f"Key: {key}")
                    chip.collect(key)
                print(f"Collected: {chip.collected}")
                print(f"Collected by: {chip.collected_by}")
                print(f"SCORE: {chip.score}")
                add_score_for_player = self._get_player_by_color(chip.collected_by)
                add_score_for_player.score += chip.score

    def _get_player_by_color(self, color: str) -> Player | None:
        """
        Gibt den Spieler mit der angegebenen Farbe zurück
        
        Args:
            color: Spielerfarbe
        
        Returns:
            Player oder None
        """
        for player in self.player_manager.players:
            if player.color == color:
                return player
        return None
