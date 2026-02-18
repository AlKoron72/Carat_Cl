"""
KI-Spieler-Klasse für Carat
"""
import random
from constants import AI_DIFFICULTY


class AIPlayer:
    """
    KI-Spieler mit Entscheidungslogik für automatisches Spielen
    """

    def __init__(self, difficulty='medium'):
        """
        Initialisiert einen KI-Spieler

        Args:
            difficulty: Schwierigkeitsgrad ('easy', 'medium', 'hard')
        """
        self.difficulty = difficulty

    def decide_placement(self, board, tile, valid_positions):
        """
        Entscheidet wo und wie das Tile platziert werden soll

        Args:
            board: Board-Objekt
            tile: Tile-Objekt das platziert werden soll
            valid_positions: Liste von gültigen (row, col) Positionen

        Returns:
            tuple: (row, col, rotation) - Position und Anzahl der Rotationen (0-3)
        """
        if not valid_positions:
            return None

        if self.difficulty == 'easy':
            return self._random_placement(valid_positions)
        elif self.difficulty == 'medium':
            # TODO: Implementiere medium Strategie später
            return self._random_placement(valid_positions)
        elif self.difficulty == 'hard':
            # TODO: Implementiere hard Strategie später
            return self._random_placement(valid_positions)
        else:
            return self._random_placement(valid_positions)

    def _random_placement(self, valid_positions):
        """
        Wählt zufällige Position und Rotation

        Args:
            valid_positions: Liste von gültigen (row, col) Positionen

        Returns:
            tuple: (row, col, rotation)
        """
        position = random.choice(valid_positions)
        rotation = random.randint(0, 3)  # 0-3 Rotationen (0°, 90°, 180°, 270°)
        return (*position, rotation)

    def _score_based_placement(self, board, tile, valid_positions, player_color):
        """
        Wählt Position basierend auf Score-Maximierung
        TODO: Implementiere später

        Args:
            board: Board-Objekt
            tile: Tile-Objekt
            valid_positions: Liste von gültigen Positionen
            player_color: Farbe des Spielers

        Returns:
            tuple: (row, col, rotation)
        """
        # Placeholder für spätere Implementierung
        best_score = -1
        best_placement = None

        for row, col in valid_positions:
            for rotation in range(4):
                # TODO: Berechne Score für diese Platzierung
                # score = self._calculate_score(board, tile, row, col, rotation, player_color)
                pass

        return best_placement or self._random_placement(valid_positions)

    def _calculate_score(self, board, tile, row, col, rotation, player_color):
        """
        Berechnet Score für eine potenzielle Platzierung
        TODO: Implementiere später

        Args:
            board: Board-Objekt
            tile: Tile-Objekt
            row, col: Position
            rotation: Anzahl der Rotationen
            player_color: Farbe des Spielers

        Returns:
            int: Score für diese Platzierung
        """
        # Placeholder für spätere Implementierung
        return 0
