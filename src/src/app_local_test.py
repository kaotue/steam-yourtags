import awsgi
import create_tags
import create_wordcloud
from CacheTable import CacheTable

CACHE_TABLE = CacheTable(
    os.environ.get('CACHE_TABLE_NAME', 'steam_games'),
    os.environ.get('TTL_DAYS', 1))

def get_tags(steamid, language):
    print(f'{steamid=}')
    tags = create_tags.run(steamid, language, CACHE_TABLE)
    if not tags:
        return 'not found'
    return create_wordcloud.run(tags)

if __name__ == '__main__':
    ret =  get_tags('76561198001490836', 'en')
    print(ret)