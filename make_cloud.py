from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from googletrans import Translator
import os

def create_cloud(text, random_number):
    # Translate text to Japanese
    translator = Translator()
    text_ja = translator.translate(text, dest='ja').text

    # Tokenize Japanese text using Janome
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text_ja)

    # Generate word frequency dictionary
    freq_dict = {}
    stop_words = ['ため', '彼女', 'それ', 'これ', 'どれ', 'いずれ', '代わり', 'さまざま', 'その他']
    for token in tokens:
        if token.part_of_speech.startswith('名詞') and len(token.surface) > 2 and token.surface not in stop_words:
            if token.surface not in freq_dict:
                freq_dict[token.surface] = 0
            freq_dict[token.surface] += 1

    font_path = './static/fonts/YuGothM.ttc'

    wordcloud = WordCloud(background_color='white',
                          font_path=font_path,
                          max_words=100,
                          width=600, height=400)
    wordcloud.generate_from_frequencies(freq_dict)

    # Save word cloud image
    os.makedirs('./static/image', exist_ok=True)
    image_path = f'./static/image/wordcloud{random_number}.png'
    wordcloud.to_file(image_path)
