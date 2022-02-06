from wordcloud import WordCloud

def run(text: str):
    options = {
        'max_font_size': 120,
        'min_font_size': 10,
        'font_step': 1,
        'prefer_horizontal': 0.9,
        'width': 1200,
        'height': 600,
        'regexp': None,
        'collocations': False,
        'include_numbers': True,
        'normalize_plurals': False
    }

    return WordCloud(**options).generate(text).to_svg()