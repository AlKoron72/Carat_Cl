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
                if len(chip.distribution) == 1:
                    # only one color left -> collect chip for color / player
                    print(f"only one color left: {chip.distribution.keys()}")
                    for key in chip.distribution.keys():
                        print(f"Key: {key}")
                        chip.collect(key)
                elif len(chip.distribution) == 2:
                    # two colors left -> find winner and collect chip for winner
                    print(f"two color left: {chip.distribution.keys()}")

                    list_of_players: list[str] = list(chip.distribution.keys())
                    print(f"list of players: {list_of_players}")
                    # wenn beide gleich hohe Wert haben
                    if chip.distribution[list_of_players[0]] == chip.distribution[list_of_players[1]]:
                        print(f"both players have the same value: {chip.distribution[list_of_players[0]]}")
                        print(f"list of players: {list_of_players}")
                        print(f"list of values: {chip.distribution.values()}")
                        chip.collect("noone")
                    else:
                        max_color = max(chip.distribution, key=chip.distribution.get)
                        print(f"max color: {max_color}")
                        chip.collect(max_color)
                elif len(chip.distribution) >= 3:
                    print(f"three colors left: {chip.distribution.keys()}")
                    if len(chip.distribution) > 3:
                        print(f"more than three colors left: {chip.distribution.keys()}")
                    max_value = max(chip.distribution.values())
                    players_with_max_value = [color for color, value in chip.distribution.items() if value == max_value]
                    print(f"max value: {max_value}")
                    print(f"players with max value: {players_with_max_value}")
                    if len(players_with_max_value) == 1:
                        chip.collect(players_with_max_value[0])
                    elif len(players_with_max_value) >= 2:
                        left_over = []
                        print(f"players with max value: {players_with_max_value}")
                        print(f"distribution: {chip.distribution}")
                        for player in chip.distribution.keys():
                            if player not in players_with_max_value:
                                left_over.append(player)
                        print(f"left_over players: {left_over}")
                        if len(left_over) == 0:
                            chip.collect("noone")
                            print(f"SPECIAL CASE if {len(chip.distribution)} == 3 and {len(left_over)} == 0: chip.collect('noone')")
                        elif len(left_over) == 1:
                            chip.collect(left_over[0])
                        elif len(left_over) == 2 and chip.distribution[left_over[0]] == chip.distribution[left_over[1]]:
                            chip.collect("noone")
                        else:
                            if chip.distribution[left_over[0]] > chip.distribution[left_over[1]]:
                                chip.collect(left_over[0])
                            else:
                                chip.collect(left_over[1])
                    else:
                        chip.collect("noone")

                # find player and add score of chip
                if chip.collected_by != "noone":
                    add_score_for_player = self._get_player_by_color(chip.collected_by)
                    add_score_for_player.score += chip.score

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

                # find player and add score of chip
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
