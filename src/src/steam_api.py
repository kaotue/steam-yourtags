import os
import base64
import json
import asyncio
import aiohttp
import urllib
import re
from bs4 import BeautifulSoup
from SteamGame import SteamGame

STEAM_API_KEY = os.environ['STEAM_API_KEY']
STEAM_ID = os.environ['STEAM_ID']

def download_owned_games(steamid: str) -> list[int]:
    params = {
        'key': STEAM_API_KEY,
        'steamid': steamid
    }
    url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?{urllib.parse.urlencode(params)}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        res_json = json.load(res)
        return [x['appid'] for x in res_json['response']['games']]

class GamePageDownloader:
    def __init__(self, appids: list[str], language: str='en'):
        urls = []
        self.appids: list[int] = appids
        self.language: str = language
        self.htmls: list[str] = []
        self.results: list[SteamGame] = []
        self.cookies = {'birthtime': '568022401'}

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(self.fetch())
        loop.run_until_complete(future)
        self.html_to_results()

    def html_to_results(self):
        for html in self.htmls:
            soup = BeautifulSoup(html, 'html.parser')
            id = soup.find('div', {'class': 'glance_tags popular_tags'})
            if id:
                id = id.attrs.get('data-appid')
            else:
                continue
            developers = soup.select('#appHeaderGridContainer > div:nth-child(2) > a')
            tags = soup.find_all('a', {'class': 'app_tag'})
            date_temp = soup.find('div', {'class': 'grid_content grid_date'})
            date_temp = date_temp.get_text(strip=True) if date_temp else None
            release_year = None
            if date_temp and (ret := re.search('[0-9]{4}', date_temp)):
                release_year = ret.group()
            d = {
                'id': int(id),
                'developers': [x.get_text(strip=True) for x in developers],
                'tags_' + self.language: [x.get_text(strip=True) for x in tags],
                'release_year': release_year
            }
            game = SteamGame(**d)
            self.results.append(game)

    async def fetch(self):
        tasks = []
        async with aiohttp.ClientSession() as session:
            for appid in self.appids:
                task = asyncio.ensure_future(self.download(appid, session))
                tasks.append(task)
            self.htmls = await asyncio.gather(*tasks)

    async def download(self, appid, session):
        headers = {
            'Accept-Language': self.language
        }
        url = f'https://store.steampowered.com/app/{appid}/'
        async with session.get(url, headers=headers, cookies=self.cookies) as response:
            return await response.text()
