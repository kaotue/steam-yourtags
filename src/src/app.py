import awsgi
import os
import base64
import uuid
import create_tags
import create_wordcloud
from CacheTable import CacheTable
from Strage import Strage
from flask import Flask, request, render_template, jsonify, redirect

CACHE_TABLE = CacheTable(
    os.environ.get('CACHE_TABLE_NAME', 'steam_games'),
    os.environ.get('TTL_DAYS', 7)
)
STRAGE = Strage(
    os.environ.get('STRAGE_BUCKET_NAME', 'steam-yourtags-bucket')
)
WC_FONT_PATH = os.environ.get('WC_FONT_PATH', './fonts/NotoSansJP-Regular.otf')
WC_STOPWORDS = os.environ.get('WC_STOPWORDS', 'Singleplayer,Multiplayer,シングルプレイヤー,マルチプレイヤー'.split(','))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/yourtags/<tagsname>', methods=['GET'])
def get_tags(tagsname):
    share_url = request.url
    print(f'{share_url=}')
    if '.svg' in tagsname:
        b = STRAGE.download_bytesio(tagsname)
        b64 = base64.b64encode(b.getvalue()).decode("utf-8")
        tags_b64 = f'data:image/svg+xml;base64,{b64}'
        tags_html = f'<img src={tags_b64}>'
        return render_template('tags.html', tags_html=tags_html, share_url=share_url)
    else:
        b = STRAGE.download_bytesio(tagsname)
        b64 = base64.b64encode(b.getvalue()).decode("utf-8")
        tags_b64 = f'data:image/png;base64,{b64}'
        tags_html = f'<img src={tags_b64}>'
        return render_template('tags.html', tags_html=tags_html, share_url=share_url)

@app.route('/yourtags', methods=['GET'])
def post_tags():
    # get params
    print(f'{request.args=}')
    if not (steamid := request.args.get('steamid')):
        return jsonify({'message': 'steamid is required'}), 400
    if (language := request.args.get('language')) not in ['en', 'ja']:
        return jsonify({'message': 'invalid language'}), 400
    if (outputtype := request.args.get('outputtype')) not in ['png','svg']:
        return jsonify({'message': 'invalid outputtype'}), 400

    # create tags
    tags = create_tags.run(steamid, language, CACHE_TABLE)
    if not tags:
        return jsonify({'message': 'tags not found'}), 400

    # create wordcloud
    file_name = f'{uuid.uuid4()}.{outputtype}'
    file_path = create_wordcloud.run(file_name, tags, outputtype, WC_FONT_PATH, WC_STOPWORDS)

    # upload to s3
    STRAGE.upload(file_path)

    return redirect(f'./yourtags/{file_name}')

def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={'image/png', 'image/svg+xml'})

if __name__ == '__main__':
    app.run(debug=True)