import app

if __name__ == '__main__':

    test_params = {
        'steamid': '76561198001490836',
        'language': 'en',
        'outputtype': 'svg'
    }

    with app.app.test_client() as c:
        r = c.get('/yourtags', query_string=test_params)
        print(r)