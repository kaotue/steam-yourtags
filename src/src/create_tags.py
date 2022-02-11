import json
import time
import os
import steam_api
import copy
from SteamGame import SteamGame
from calc_time import calc_time

EXCEPT_TAGS = os.environ.get('EXCEPT_TAGS', '').split(',')
print(f'{EXCEPT_TAGS=}')

@calc_time
def run(steamid: str, language: str, cache_table: object) -> str:
    ids = steam_api.download_owned_games(steamid)
    if not ids:
        return None

    # get from cache
    games_from_cache = get_games_from_cache(ids, language, cache_table)
    print(f'{len(games_from_cache)=}')

    # get from steam
    ids_download_target = [id for id in ids if id not in [x.id for x in games_from_cache]]
    games_from_steam = get_games_from_steam(ids_download_target, language)
    print(f'{len(games_from_steam)=}')

    # cache games
    if games_from_steam:
        cache_games(games_from_steam, cache_table)

    # output
    results = []
    if games_from_cache:
        results.extend(games_from_cache)
    if games_from_steam:
        results.extend(games_from_steam)
    for game in results:
        if language == 'en':
            game.tags_ja = None
        else:
            game.tags_en = None
            
    print(f'{len(results)=}')
    ret = [x.get_wordcloud_str() for x in results]
    return ' '.join(ret)

@calc_time
def get_games_from_cache(ids: list[int], language: str, cache_table: object) -> list[SteamGame]:
    results = []
    for id in ids:
        if cache_table.get_data(id, 'tags_' + language):
            d = cache_table.get_item(id)
            game = SteamGame(**d)
            results.append(game)
    return results

@calc_time
def get_games_from_steam(ids: list[int], language: str) -> list[SteamGame]:
    downloader = steam_api.GamePageDownloader(ids, language)
    downloader.run()
    return downloader.results
    
@calc_time
def cache_games(games: list[SteamGame], cache_table: object):
    for game in games:
        cache_table.put_item(game.id, vars(game))