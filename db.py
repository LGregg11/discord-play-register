DEFAULT_EXPIRY_S = 60 * 60 * 4
import time

class WouldPlay:
    def __init__(self, player, game, expires_at=None):
        self.player = player
        self.game = game
        self.recorded_at = time.time()
        self.expires_at = expires_at or (self.recorded_at + DEFAULT_EXPIRY_S)

    @property
    def user(self):
        return self.player.name

    @property
    def expired(self):
        return self.expires_at <= time.time()

    def __eq__(self, other):
        if type(other) is type(self):
            return (self.player.id == other.player.id and self.game.name == other.game.name)
        else:
            return False

    def __hash__(self):
        return hash((self.player.id, self.game.name))



class DB:
    def __init__(self):
        self._store = set()

    def record_would_play(self, player, game):
        if not game.name:
            raise RuntimeError('Cannot record for a game with no name')
        wp = WouldPlay(player=player, game=game)
        self._store.add(wp)
        self._prune_expired()
        return wp

    def get_players_for_game(self, game):
        return [wp.player for wp in self.get_would_plays_for_game(game)]

    def get_would_plays_for_game(self, game):
        self._prune_expired()
        return sorted([wp for wp in self._store if wp.game.name == game.name], key=lambda x: x.recorded_at)

    def _prune_expired(self):
        # why can't I do self.prune(wp -> wp.expired)
        self._store = set([wp for wp in self._store if not wp.expired])

    def clear_game(self, game):
        self._store = set([wp for wp in self._store if wp.game.name != game.name])


db = DB()