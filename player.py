"""
Player-Klasse für Spielerverwaltung
"""
import random
from point_chip import PointChip
from tile import Tile


class Player:
    """
    Repräsentiert einen Spieler im Spiel
    """

    def __init__(self, name:str, color:str, is_human=True, is_npc=False):
        """
        Initialisiert einen Spieler

        Args:
            name: Name des Spielers
            color: Farbe des Spielers (z.B. 'red', 'blue')
            is_human: Ob der Spieler ein Mensch oder KI ist
            is_npc: Ob der Spieler ein NPC ist (bekommt keine Tiles, nur Punkte)
        """
        self.name = name
        self.color = color
        self.is_human = is_human
        self.is_npc = is_npc
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
        self.starting_player_index = 0  # Index des Startspielers
        self._setup_players()
        self._select_starting_player()
    
    def _setup_players(self):
        """
        Erstellt die Spieler basierend auf der Spielerzahl
        Bei 2-3 Spielern werden zusätzlich NPCs für die fehlenden Farben angelegt
        """
        colors = ['red', 'blue', 'green', 'yellow']
        names = ['Spieler 1', 'Spieler 2', 'Spieler 3', 'Spieler 4']
        npc_names = ['NPC Grün', 'NPC Gelb']

        # Erstelle echte Spieler
        for i in range(self.player_count):
            player = Player(names[i], colors[i], is_human=True, is_npc=False)
            self.players.append(player)

        # Erstelle NPCs für fehlende Farben (bei 2-3 Spielern)
        npc_count = 4 - self.player_count
        for i in range(npc_count):
            npc_color_index = self.player_count + i
            npc = Player(npc_names[i], colors[npc_color_index], is_human=False, is_npc=True)
            self.players.append(npc)

    def _select_starting_player(self):
        """Wählt zufällig einen Startspieler aus"""
        self.starting_player_index = random.randint(0, self.player_count - 1)
        self.current_player_index = self.starting_player_index
        print(f"Startspieler: {self.players[self.starting_player_index].name}")
    
    def get_current_player(self):
        """Gibt den aktuellen Spieler zurück"""
        return self.players[self.current_player_index]

    def is_starting_player(self, player_index):
        """
        Prüft ob ein Spieler der Startspieler ist

        Args:
            player_index: Index des Spielers

        Returns:
            bool: True wenn Startspieler
        """
        return player_index == self.starting_player_index
    
    def next_player(self):
        """
        Wechselt zum nächsten echten Spieler (überspringt NPCs)
        """
        # Suche nächsten nicht-NPC Spieler
        for _ in range(len(self.players)):
            self.current_player_index = (self.current_player_index + 1) % self.player_count
            if not self.players[self.current_player_index].is_npc:
                return self.get_current_player()

        # Fallback: sollte nicht passieren, aber sicher ist sicher
        return self.get_current_player()
    
    def distribute_tiles(self, tiles) -> None:
        """
        Verteilt Plättchen gleichmäßig an alle echten Spieler (keine NPCs).
        Der Startspieler erhält das übrig bleibende Tile.

        Args:
            tiles: Liste von Tile-Objekten
        """
        # Nur echte Spieler (keine NPCs) erhalten Tiles
        real_players = [p for p in self.players if not p.is_npc]

        tiles_per_player = len(tiles) // len(real_players)
        remaining_tiles = len(tiles) % len(real_players)

        for i, player in enumerate(real_players):
            start_idx = i * tiles_per_player
            end_idx = start_idx + tiles_per_player
            player_tiles = tiles[start_idx:end_idx]

            for tile in player_tiles:
                player.add_tile(tile)

        # Gebe übrig bleibendes Tile dem Startspieler
        if remaining_tiles > 0:
            extra_tile_idx = tiles_per_player * len(real_players)
            extra_tile = tiles[extra_tile_idx]
            self.players[self.starting_player_index].add_tile(extra_tile)
            print(f"{self.players[self.starting_player_index].name} erhält das Extra-Tile")

        print(f"Number of tiles distributed: {len(tiles)}")
        print(f"Tiles per player: {tiles_per_player} (Startspieler +{remaining_tiles})")
    
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
        Echte Spieler und NPCs werden getrennt sortiert

        Returns:
            dict: {'players': [echte Spieler], 'npcs': [NPC Spieler]}
        """
        real_players = [p for p in self.players if not p.is_npc]
        npcs = [p for p in self.players if p.is_npc]

        return {
            'players': sorted(real_players, key=lambda p: p.get_score(), reverse=True),
            'npcs': sorted(npcs, key=lambda p: p.get_score(), reverse=True)
        }
    
    def __repr__(self):
        return f"PlayerManager(players={len(self.players)}, current={self.get_current_player().name})"
