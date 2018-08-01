import pytest

from dfg import *
from dfg.errors import *

@pytest.fixture
def game(request):
    DEFAULT_PLAYER_COUNT = 4
    player_count = request.param if hasattr(request, 'param') else DEFAULT_PLAYER_COUNT
    return Game(player_count=player_count)

@pytest.fixture
def player(game, request):
    player = game.現在のプレイヤー()
    if hasattr(request, 'param'):
        player.手札に加える(request.param)
    return player

@pytest.fixture
def hands(game, request):
    ALL_CARDS = ['{}{}'.format(m, n) for m in 'SHDC' for n in 'A234567890JQK']
    if hasattr(request, 'param'):
        for i in range(len(game._players)):
            hands = request.param.get(i, ALL_CARDS)
            game._players[i].手札に加える(hands)
    else:
        for i in range(len(game._players)):
            game._players[i].手札に加える(ALL_CARDS)

@pytest.fixture
def ハートの3を出す(game):
    player = game.現在のプレイヤー()
    player.手札に加える(['H3'])
    player.play(['H3'])

def test_1人目がハートの3を出したのに対して2人目がスペードの6を出す(game, hands, ハートの3を出す):
    assert game.最後のカード().cards == ['H3']
    second_player = game.現在のプレイヤー()
    second_player.play(['S6'])
    assert game.最後のカード().cards == ['S6']

def test_1人目がハートの3を出したのに対して2人目がスペードの3は出せない(game, hands, ハートの3を出す):
    assert game.最後のカード().cards == ['H3']
    second_player = game.現在のプレイヤー()
    with pytest.raises(InvalidPlayError):
        second_player.play(['S3'])

def test_手札を出すとそれが最後のカードになる(game, hands, player):
    player.play(['S6'])
    assert game.最後のカード().cards == ['S6']

class Testプレイヤーの順序:
    def test_手番のプレイヤーしか手札を出せない(self, game, hands, player):
        player.do_pass()
        next_player = game.現在のプレイヤー()
        with pytest.raises(WrongPlayerError):
            player.play(['SA'])

    def test_手番のプレイヤーしかパスできない(self, game, player):
        player.do_pass()
        next_player = game.現在のプレイヤー()
        with pytest.raises(WrongPlayerError):
            player.do_pass()

    @pytest.mark.parametrize('game', [2], indirect=True)
    def test_最後のプレイヤーの次は最初のプレイヤーに戻る(self, game, hands):
        first_player = game.現在のプレイヤー()
        first_player.play(['DK'])
        second_player = game.現在のプレイヤー()
        second_player.play(['SA'])
        assert first_player is game.現在のプレイヤー()

@pytest.mark.parametrize('player', [['D0', 'C8']], indirect=True)
def test_手札しか出せない(game, player):
    with pytest.raises(ImpossiblePlayError):
        player.play(['DJ'])

@pytest.mark.parametrize('hands', [{0: ['D0', 'C8']}], indirect=True)
def test_手札を出すと手札が減る(hands, player):
    player.play(['D0'])
    assert 'D0' not in player.手札()
    assert 'C8' in player.手札()

@pytest.mark.parametrize('hands', [{0: ['D3', 'C8']}], indirect=True)
def test_手札を出せなかったら手札は減らない(hands, ハートの3を出す, player):
    with pytest.raises(InvalidPlayError):
        player.play(['D3'])
    assert 'D3' in player.手札()
    assert 'C8' in player.手札()

class Test出したカードの強弱:
    @pytest.mark.parametrize('c1, c2', [
        ('S4', 'S3'),
        ('S5', 'S4'),
        ('S6', 'S5'),
        ('S7', 'S6'),
        ('S8', 'S7'),
        ('S9', 'S8'),
        ('S0', 'S9'),
        ('SJ', 'S0'),
        ('SQ', 'SJ'),
        ('SK', 'SQ'),
        ('SA', 'SK'),
        ('S2', 'SA'),
    ])
    def test_1枚ずつ_1番違い(self, c1, c2):
        assert Trick([c1]).is_stronger(Trick([c2]))

    def test_ペア(self):
        assert Trick(["S7", "H7"]).is_stronger(Trick(["S5", "D5"]))

    def test_ペアは同じ数字に限る(self):
        with pytest.raises(InvalidPlayError):
            Trick(["S7", "DJ"])





