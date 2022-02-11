import awsgi
import os
import create_tags
import create_wordcloud
from CacheTable import CacheTable
from flask import Flask, request, render_template

CACHE_TABLE = CacheTable(
    os.environ.get('CACHE_TABLE_NAME', 'steam_games'),
    os.environ.get('TTL_DAYS', 1))
STOPWORDS = os.environ.get('STOPWORDS', 'Singleplayer,Multiplayer,シングルプレイヤー,マルチプレイヤー'.split(','))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yourtags', methods=['GET'])
def get_tags():
    print(f'{request.args=}')
    if not (steamid := request.args.get('steamid')):
        return 'steamid is required'
    language = request.args.get('language', 'en')
    tags = create_tags.run(steamid, language, CACHE_TABLE)
    if not tags:
        return 'not found'

    return create_wordcloud.run(tags, STOPWORDS)

def lambda_handler(event, context):
    return awsgi.response(app, event, context)

if __name__ == '__main__':
    app.run(debug=True)