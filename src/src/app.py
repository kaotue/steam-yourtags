import awsgi
import os
import create_tags
import create_wordcloud
from CacheTable import CacheTable
from Strage import Strage
from flask import Flask, request, render_template, send_file

CACHE_TABLE = CacheTable(
    os.environ.get('CACHE_TABLE_NAME', 'steam_games'),
    os.environ.get('TTL_DAYS', 1)
)
STRAGE = Strage(
    os.environ.get('STRAGE_BUCKET_NAME', 'steam-yourtags-bucket')
)
STOPWORDS = os.environ.get('STOPWORDS', 'Singleplayer,Multiplayer,シングルプレイヤー,マルチプレイヤー'.split(','))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yourtags', methods=['GET'])
def get_tags():

    # get params
    print(f'{request.args=}')
    steamid = request.args.get('steamid')
    if not steamid:
        return 'steamid is required'
    language = request.args.get('language', 'en')
    outputtype = request.args.get('outputtype', 'png')

    # create tags
    tags = create_tags.run(steamid, language, CACHE_TABLE)
    if not tags:
        return 'not found'

    # create wordcloud
    file_path = create_wordcloud.run(tags, outputtype, STOPWORDS)

    # upload to s3
    STRAGE.upload(file_path)

    if outputtype == 'svg':
        return send_file(file_path, mimetype='image/svg+xml')
    else:
        return send_file(file_path, mimetype=f'image/{outputtype}')

def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={'image/png', 'image/svg+xml'})

if __name__ == '__main__':
    app.run(debug=True)