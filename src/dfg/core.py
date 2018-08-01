from collections import namedtuple

from dfg.errors import *

class Player:
    def __init__(self, field):
        self._field = field
        self._hands = set()

    def play(self, cards):
        if not cards:
            raise ImpossiblePlayError()
        if not any([c in self._hands for c in cards]):
            raise ImpossiblePlayError()

        self._field.手札を出す(self, cards)
        for c in cards:
            self._hands.remove(c)

    def do_pass(self):
        self._field.パスする(self)

    def 手札に加える(self, cards):
        for c in cards:
            self._hands.add(c)

    def 手札(self):
        return self._hands


class Trick:
    ORDER = '34567890JQKA2'
    def __init__(self, cards):
        self._cards = cards
        self._eval_cards()

    def _eval_cards(self):
        self._is_pair = False
        if len(self._cards) == 1:
            return
        elif all(c[1] == self._cards[0][1] for c in self._cards):
            self._is_pair = True
        else:
            raise InvalidPlayError

    @property
    def cards(self):
        return self._cards

    def is_stronger(self, other):
        return Trick.order(self.cards[0][1]) > Trick.order(other.cards[0][1])

    @staticmethod
    def order(n):
        return Trick.ORDER.index(n)


Play = namedtuple('Play', ('player', 'trick'))

class Field:
    def __init__(self, game):
        self._game = game
        self._deals = []

    def 手札を出す(self, player, cards):
        trick = Trick(cards)
        if self._game.現在のプレイヤー() is not player:
            raise WrongPlayerError()
        if self.最後のカード() and not trick.is_stronger(self.最後のカード()):
            raise InvalidPlayError()
        self._deals.append(Play(player, trick))
        self._game.次のプレイヤーに進む()

    def パスする(self, player):
        if self._game.現在のプレイヤー() is not player:
            raise WrongPlayerError()
        self._game.次のプレイヤーに進む()

    def 最後のカード(self):
        if not self._deals:
            return None
        return self._deals[-1].trick


class Game:
    def __init__(self, player_count):
        self._field = Field(self)
        self._players = [Player(self._field) for i in range(player_count)]
        self._current_player_idx = 0

    def 最後のカード(self):
        return self._field.最後のカード()

    def 現在のプレイヤー(self):
        return self._players[self._current_player_idx]

    def 次のプレイヤーに進む(self):
        self._current_player_idx = (self._current_player_idx + 1) % len(self._players)



