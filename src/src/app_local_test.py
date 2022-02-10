import awsgi
import create_tags
import create_wordcloud
from CacheTable import CacheTable

import re

def get_tags(steamid, language):
    print(f'{steamid=}')
    tags = create_tags.run(steamid, language, CacheTable())
    if not tags:
        return 'not found'
    return create_wordcloud.run(tags)

if __name__ == '__main__':
    ret =  get_tags('76561198001490836', 'en')
    print(ret)