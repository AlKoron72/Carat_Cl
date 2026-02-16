"""
Wertungssystem für Carat
"""
from point_chip import PointChip


class ScoringSystem:
    """
    Verwaltet die Punkteberechnung bei vollständigen Reihen/Spalten
    """
    
    def __init__(self, board, player_manager):
        """
        Initialisiert das Wertungssystem
        
        Args:
            board: Board-Objekt
            player_manager: PlayerManager-Objekt
        """
        self.board = board
        self.player_manager = player_manager
    
    def check_and_score_lines(self):
        """
        Prüft auf vollständige Zeilen/Spalten und vergibt Punkte
        
        Returns:
            dict: Informationen über die Wertung
                  {'scored': bool, 'rows': [], 'cols': [], 'points': {player_color: points}}
        """
        completed = self.board.get_completed_lines()
        
        if not completed['rows'] and not completed['cols']:
            return {'scored': False, 'rows': [], 'cols': [], 'points': {}}
        
        points_awarded = {}
        
        # Werte Zeilen aus
        for row in completed['rows']:
            row_points = self._score_row(row)
            for player_color, points in row_points.items():
                points_awarded[player_color] = points_awarded.get(player_color, 0) + points
        
        # Werte Spalten aus
        for col in completed['cols']:
            col_points = self._score_column(col)
            for player_color, points in col_points.items():
                points_awarded[player_color] = points_awarded.get(player_color, 0) + points
        
        # Vergebe Punkte an Spieler
        for player in self.player_manager.players:
            if player.color in points_awarded:
                player.score += points_awarded[player.color]
        
        return {
            'scored': True,
            'rows': completed['rows'],
            'cols': completed['cols'],
            'points': points_awarded
        }

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

    def _score_row(self, row):
        """
        old --- needs deletion
        """
        return row
    
    def _score_column(self, col):
        """
        old --- needs deletion
        """
        return col
    
    def _get_player_by_color(self, color):
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
