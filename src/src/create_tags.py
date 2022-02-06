import json
import time
import os
import steam_api
import asyncio
import urllib
from calc_time import calc_time

EXCEPT_TAGS = os.environ.get('EXCEPT_TAGS', '').split(',')
print(f'{EXCEPT_TAGS=}')

@calc_time
def run(steamid: str, language: str) -> str:
    appids = steam_api.download_owned_games(steamid)
    if not appids:
        return None

    downloader = steam_api.GamePageDownloader(appids, language)
    downloader.run()
    ret = [x.get_wordcloud_str() for x in downloader.results]
    return ' '.join(ret)