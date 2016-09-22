import threading

from cassiopeia import baseriotapi
from cassiopeia.type.core.currentgame import Game


def schedule_checks(on_new_game, minutes_per_check=2):
    __do_check(on_new_game, minutes_per_check)


def __do_check(on_new_game, minutes_per_check, previous_ids=set()):
    streamers = get_interested_streamers()

    current_games = set()
    for streamer in streamers:
        baseriotapi.set_region(streamer["region"])
        current_game = baseriotapi.get_current_game(streamer["summoner_id"])
        if current_game:
            current_games.add(Game(current_game))

    current_ids = set()
    for game in current_games:
        if game.id not in previous_ids:
            on_new_game(game)
        current_ids.add(game.id)

    timer = threading.Timer(60 * minutes_per_check, __do_check, [on_new_game, minutes_per_check, current_ids])
    timer.daemon = True
    timer.start()


def get_interested_streamers():
    """
    Example return:
    [
        {
            "region": "NA",
            "summoner_id": 12452352
        },
        {
            "region": "NA",
            "summoner_id": 65432
        }
    ]
    """
    return []
