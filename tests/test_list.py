from os import path, mkdir
from pytest import fixture
import json

from src.linkeds import BoundedList, DynamicList


GAMES = (
    'Assassin\'s Creed', 'Call of Duty', 'Counter-Strike', 'Dota 2', 'Fortnite',
    'Grand Theft Auto V', 'League of Legends', 'Minecraft', 'Overwatch', 'PlayerUnknown\'s Battlegrounds',
    'Red Dead Redemption 2', 'Rocket League', 'The Elder Scrolls V: Skyrim', 'The Legend of Zelda: Breath of the Wild',
    'The Sims', 'Uncharted', 'Valorant', 'World of Warcraft', 'XCOM 2'
)
OUTPUT_FOLDER = path.abspath(path.join(path.dirname(__file__), 'output'))
DYNAMIC_LIST_JSON = path.join(OUTPUT_FOLDER, 'dynamic_list.json')


@fixture
def bounded_list() -> BoundedList:
    lst = BoundedList(len(GAMES))

    for i, game in enumerate(GAMES):
        if i % 2 == 0:
            lst.add_first(game)
        else:
            lst.insert(0, game)

    return lst


@fixture
def dynamic_list() -> DynamicList:
    lst = DynamicList()

    for i, game in enumerate(GAMES):
        if i % 2 == 0:
            lst.add_last(game)
        else:
            lst.insert(i, game)

    return lst


def test_bounded_list(bounded_list: BoundedList) -> None:
    reversed_games = GAMES[::-1]

    assert bounded_list.is_empty() is False
    assert bounded_list.is_full() is True
    assert bounded_list.get_first() == reversed_games[0]
    assert bounded_list.get_last() == reversed_games[-1]

    assert bounded_list.to_list() == list(reversed_games)
    assert bounded_list.to_tuple() == reversed_games
    assert bounded_list.reverse().to_tuple() == GAMES
    assert bounded_list.to_set() == set(reversed_games)

    for i, item in enumerate(bounded_list):
        assert item == reversed_games[i]

    for i in range(bounded_list.size):
        assert bounded_list.get(i) == reversed_games[i]

    for i in range(bounded_list.size):
        if i % 2 == 0:
            assert bounded_list.remove_first() == reversed_games[i]
        else:
            assert bounded_list.remove(0) == reversed_games[i]

    assert bounded_list.is_empty() is True


def test_dynamic_list(dynamic_list: DynamicList) -> None:
    if not path.exists(OUTPUT_FOLDER):
        mkdir(OUTPUT_FOLDER)

    assert dynamic_list.is_empty() is False
    assert dynamic_list.get_first() == GAMES[0]
    assert dynamic_list.get_last() == GAMES[-1]

    dynamic_list.dump_json(DYNAMIC_LIST_JSON)
    assert path.exists(DYNAMIC_LIST_JSON) is True
    
    dynamic_list.load_json(DYNAMIC_LIST_JSON)
    assert dynamic_list.to_tuple() == GAMES

    assert dynamic_list.dumps_json(indent=0) == json.dumps(GAMES, indent=0)

    dynamic_list.loads_json(json.dumps(GAMES))
    assert dynamic_list.to_tuple() == GAMES

    for i, item in enumerate(dynamic_list):
        assert item == GAMES[i]

    for i in range(dynamic_list.size):
        assert dynamic_list.get(i) == GAMES[i]

    for i in range(dynamic_list.size):
        idx = dynamic_list.size - 1

        if i % 2 == 0:
            assert dynamic_list.remove_last() == GAMES[idx]
        else:
            assert dynamic_list.remove(idx) == GAMES[idx]

    assert dynamic_list.is_empty() is True
