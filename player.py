"""
Player-Klasse für Spielerverwaltung
"""
from point_chip import PointChip
from tile import Tile


class Player:
    """
    Repräsentiert einen Spieler im Spiel
    """
    
    def __init__(self, name:str, color:str, is_human=True):
        """
        Initialisiert einen Spieler
        
        Args:
            name: Name des Spielers
            color: Farbe des Spielers (z.B. 'red', 'blue')
            is_human: Ob der Spieler ein Mensch oder KI ist
        """
        self.name = name
        self.color = color
        self.is_human = is_human
        self.score = 0
        self.tiles = []  # Plättchen des Spielers
        self.collected_chips = []  # Eingesammelte Punktechips
    
    def add_tile(self, tile:Tile) -> None:
        """
        Fügt dem Spieler ein Plättchen hinzu
        
        Args:
            tile: Tile-Objekt
        """
        tile.set_owner(self.color)
        self.tiles.append(tile)
    
    def remove_tile(self, tile):
        """
        Entfernt ein Plättchen vom Spieler
        
        Args:
            tile: Tile-Objekt
        """
        if tile in self.tiles:
            self.tiles.remove(tile)
    
    def get_tile_count(self):
        """Gibt die Anzahl der Plättchen des Spielers zurück"""
        return len(self.tiles)
    
    def collect_chip(self, chip:PointChip) -> None:
        """
        Sammelt einen Punktechip ein
        
        Args:
            chip: PointChip-Objekt
        """
        chip.collect(self.color)
        self.collected_chips.append(chip)
        self.score += chip.value
    
    def get_score(self):
        """Gibt die aktuelle Punktzahl zurück"""
        return self.score
    
    def has_tiles(self):
        """Prüft, ob der Spieler noch Plättchen hat"""
        return len(self.tiles) > 0
    
    def get_current_tile(self):
        """
        Gibt das aktuelle Plättchen zurück (das erste in der Hand)
        
        Returns:
            Tile oder None
        """
        if self.tiles:
            return self.tiles[0]
        return None
    
    def __repr__(self):
        return f"Player(name={self.name}, color={self.color}, score={self.score}, tiles={len(self.tiles)})"


class PlayerManager:
    """
    Verwaltet mehrere Spieler und deren Reihenfolge
    """
    
    def __init__(self, player_count:int =2):
        """
        Initialisiert den PlayerManager
        
        Args:
            player_count: Anzahl der Spieler (2-4)
        """
        if player_count < 2 or player_count > 4:
            raise ValueError("Spielerzahl muss zwischen 2 und 4 liegen")
        
        self.player_count = player_count
        self.players = []
        self.current_player_index = 0
        self._setup_players()
    
    def _setup_players(self):
        """Erstellt die Spieler basierend auf der Spielerzahl"""
        colors = ['red', 'blue', 'green', 'yellow']
        names = ['Spieler 1', 'Spieler 2', 'Spieler 3', 'Spieler 4']
        
        for i in range(self.player_count):
            player = Player(names[i], colors[i], is_human=True)
            self.players.append(player)
    
    def get_current_player(self):
        """Gibt den aktuellen Spieler zurück"""
        return self.players[self.current_player_index]
    
    def next_player(self):
        """Wechselt zum nächsten Spieler"""
        self.current_player_index = (self.current_player_index + 1) % self.player_count
        return self.get_current_player()
    
    def distribute_tiles(self, tiles) -> None:
        """
        Verteilt Plättchen gleichmäßig an alle Spieler
        
        Args:
            tiles: Liste von Tile-Objekten
        """
        tiles_per_player = len(tiles) // self.player_count
        
        for i, player in enumerate(self.players):
            start_idx = i * tiles_per_player
            end_idx = start_idx + tiles_per_player
            player_tiles = tiles[start_idx:end_idx]
            
            for tile in player_tiles:
                player.add_tile(tile)
    
    def get_winner(self):
        """
        Ermittelt den Gewinner basierend auf der höchsten Punktzahl
        
        Returns:
            Player: Gewinner oder None bei Gleichstand
        """
        max_score = max(player.get_score() for player in self.players)
        winners = [p for p in self.players if p.get_score() == max_score]
        
        if len(winners) == 1:
            return winners[0]
        return None  # Gleichstand
    
    def get_leaderboard(self):
        """
        Gibt eine sortierte Liste aller Spieler nach Punktzahl zurück
        
        Returns:
            list: Sortierte Liste von Spielern (höchste Punktzahl zuerst)
        """
        return sorted(self.players, key=lambda p: p.get_score(), reverse=True)
    
    def __repr__(self):
        return f"PlayerManager(players={len(self.players)}, current={self.get_current_player().name})"
