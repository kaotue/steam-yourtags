from wordcloud import WordCloud
import uuid

def run(file_name: str, text: str, outputtype: str, font_path: str, stopwords: list[str]) -> str:
    options = {
        'max_font_size': 120,
        'min_font_size': 10,
        'font_step': 1,
        'prefer_horizontal': 0.9,
        'width': 1200,
        'height': 600,
        'regexp': r"\w[\w'#+-]+",
        'collocations': False,
        'include_numbers': True,
        'normalize_plurals': False,
        'stopwords': stopwords,
        'font_path': font_path
    }

    if outputtype == 'png':
        file_path = f'/tmp/{file_name}'
        WordCloud(**options).generate(text).to_file(file_path)
        return file_path
    else:
        svg_text = WordCloud(**options).generate(text).to_svg()
        file_path = f'/tmp/{file_name}'
        with open(file_path, 'w') as f:
            f.write(svg_text)
        return file_path