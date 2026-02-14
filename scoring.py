"""
Wertungssystem für Carat
"""


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
    
    def _score_row(self, row):
        """
        Berechnet Punkte für eine vollständige Zeile
        
        Args:
            row: Zeilen-Index
        
        Returns:
            dict: {player_color: points}
        """
        color_counts = {}
        
        # Zähle Diamanten jeder Farbe in der Zeile
        for col in range(self.board.size):
            tile = self.board.get_tile(row, col)
            if tile:
                # Zähle die Diamanten die zur Zeile beitragen (oben und unten)
                top_value = tile.get_diamond('top')
                bottom_value = tile.get_diamond('bottom')
                
                color_counts[top_value] = color_counts.get(top_value, 0) + 1
                color_counts[bottom_value] = color_counts.get(bottom_value, 0) + 1
        
        # Ermittle die dominante Farbe (höchste Anzahl)
        if not color_counts:
            return {}
        
        max_count = max(color_counts.values())
        dominant_colors = [color for color, count in color_counts.items() if count == max_count]
        
        # Bei Gleichstand: alle beteiligten Spieler bekommen Punkte
        points = {}
        for col in range(self.board.size):
            tile = self.board.get_tile(row, col)
            if tile and tile.owner:
                # Prüfe ob dieser Tile zur dominanten Farbe beiträgt
                top_value = tile.get_diamond('top')
                bottom_value = tile.get_diamond('bottom')
                
                if top_value in dominant_colors or bottom_value in dominant_colors:
                    # Sammle Chip ein wenn vorhanden und nicht bereits gesammelt
                    chip = self.board.get_chip(row, col)
                    if chip and not chip.is_collected():
                        if tile.owner not in points:
                            points[tile.owner] = 0
                        points[tile.owner] += chip.value
                        
                        # Markiere Chip als gesammelt
                        player = self._get_player_by_color(tile.owner)
                        if player:
                            player.collect_chip(chip)
        
        return points
    
    def _score_column(self, col):
        """
        Berechnet Punkte für eine vollständige Spalte
        
        Args:
            col: Spalten-Index
        
        Returns:
            dict: {player_color: points}
        """
        color_counts = {}
        
        # Zähle Diamanten jeder Farbe in der Spalte
        for row in range(self.board.size):
            tile = self.board.get_tile(row, col)
            if tile:
                # Zähle die Diamanten die zur Spalte beitragen (links und rechts)
                left_value = tile.get_diamond('left')
                right_value = tile.get_diamond('right')
                
                color_counts[left_value] = color_counts.get(left_value, 0) + 1
                color_counts[right_value] = color_counts.get(right_value, 0) + 1
        
        # Ermittle die dominante Farbe
        if not color_counts:
            return {}
        
        max_count = max(color_counts.values())
        dominant_colors = [color for color, count in color_counts.items() if count == max_count]
        
        # Vergebe Punkte
        points = {}
        for row in range(self.board.size):
            tile = self.board.get_tile(row, col)
            if tile and tile.owner:
                left_value = tile.get_diamond('left')
                right_value = tile.get_diamond('right')
                
                if left_value in dominant_colors or right_value in dominant_colors:
                    chip = self.board.get_chip(row, col)
                    if chip and not chip.is_collected():
                        if tile.owner not in points:
                            points[tile.owner] = 0
                        points[tile.owner] += chip.value
                        
                        player = self._get_player_by_color(tile.owner)
                        if player:
                            player.collect_chip(chip)
        
        return points
    
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
