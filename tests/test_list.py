from pytest import fixture
from src.data_structures import BoundedList, DynamicList


GAMES = (
    'Assassin\'s Creed', 'Call of Duty', 'Counter-Strike', 'Dota 2', 'Fortnite',
    'Grand Theft Auto V', 'League of Legends', 'Minecraft', 'Overwatch', 'PlayerUnknown\'s Battlegrounds',
    'Red Dead Redemption 2', 'Rocket League', 'The Elder Scrolls V: Skyrim', 'The Legend of Zelda: Breath of the Wild',
    'The Sims', 'Uncharted', 'Valorant', 'World of Warcraft', 'XCOM 2'
)


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
    assert bounded_list.is_empty() is False
    assert bounded_list.is_full() is True
    assert bounded_list.get_first() == GAMES[-1]
    assert bounded_list.get_last() == GAMES[0]

    for i, item in enumerate(bounded_list):
        assert item == GAMES[bounded_list.size - i - 1]

    for i in range(bounded_list.size):
        assert bounded_list.get(i) == GAMES[bounded_list.size - i - 1]

    for i in range(bounded_list.size):
        idx = bounded_list.size - 1

        if i % 2 == 0:
            assert bounded_list.remove_first() == GAMES[idx]
        else:
            assert bounded_list.remove(0) == GAMES[idx]

    assert bounded_list.is_empty() is True


def test_dynamic_list(dynamic_list: DynamicList) -> None:
    assert dynamic_list.is_empty() is False
    assert dynamic_list.get_first() == GAMES[0]
    assert dynamic_list.get_last() == GAMES[-1]

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
