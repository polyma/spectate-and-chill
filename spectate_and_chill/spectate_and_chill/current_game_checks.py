import threading

from cassiopeia import baseriotapi
from cassiopeia.type.core.currentgame import Game


def schedule_checks(region, summoner_ids, on_new_game, minutes_per_check=2):
    __do_check(region, summoner_ids, on_new_game, minutes_per_check)


def __do_check(region, summoner_ids, on_new_game, minutes_per_check):
    baseriotapi.set_region(region)

    for summoner_id in summoner_ids:
        try:
            current_game = baseriotapi.get_current_game(summoner_id)
        except:
            current_game = None

        if current_game:
            on_new_game(Game(current_game))

    timer = threading.Timer(60 * minutes_per_check, __do_check, [region, summoner_ids, on_new_game, minutes_per_check])
    timer.daemon = True
    timer.start()
