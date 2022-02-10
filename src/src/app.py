import awsgi
import create_tags
import create_wordcloud
from CacheTable import CacheTable
from flask import Flask, request, render_template

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
    tags = create_tags.run(steamid, language, CacheTable())
    if not tags:
        return 'not found'

    return create_wordcloud.run(tags)

def lambda_handler(event, context):
    return awsgi.response(app, event, context)

if __name__ == '__main__':
    app.run(debug=True)