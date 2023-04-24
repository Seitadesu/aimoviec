from flask import Flask, render_template ,request, redirect, session, Markup
from html import escape
import os
import openai
from io import BytesIO
from make_image import create_image
import os
import openai
import random

app = Flask(__name__)

@app.route('/seita')
def seita():
    return render_template('seita.html')

@app.route('/')
def index():
    jokes = [
        "AIがレストランのウェイターになったとしたら、料理の写真を見せる代わりに、食べ物の味や匂いを再現して提供することができるかもしれませんね。でも、それだと「食欲をそそる写真」というコンテンツが廃れるかもしれません。",
        "AIが将棋のプロに勝つようになりましたが、今度はAI同士で戦わせてみたところ、相手がお互いの思考を予測しすぎて、引き分けになってしまいました。AI同士の対決、面白いですね。",
        "人工知能が翻訳をすると、翻訳が正確かどうかを確かめるのは専門家でなければならないことがあります。そこで、翻訳の正確さを確かめるために、AIが翻訳した文章を別のAIに翻訳させる方法があるそうです。これは、本当に信頼できるのか？！",
        "作曲AIが私たちにとって一番役立つのは、試聴前に「あなたが好きな音楽は何ですか？」と質問しなくて済むことでしょう。",
        "AIが作曲した曲について、私たちは「この曲はどこで生まれたのか？」と問うことができます。AIは、それが「ゼロとワンの世界で生まれた」と答えるかもしれません。",
        "AIによる作曲は、既に耳に馴染んでいる曲を元に作られたものが多いです。でも、聴いたことがないような斬新な曲を作ることもあるので、私たちはAIが作った音楽に対して「未知の旋律」と感じることもあるかもしれません。",
        "作曲AIが今後も進化し続けると、あなたの好みや気分に合わせて瞬時に曲を作ることができるかもしれません。でも、それが「自分だけのテーマソング」を作ることに繋がるかどうかは別の問題です。",
        "作曲AIは、有名な音楽家たちの曲を元に作曲されることが多いですが、ある時期を超えると、AIが有名な曲家の楽曲を作曲するかもしれません。その日は、ビートルズの「Hello, AI!」という曲がトップチャートを独占するかもしれませんね。",
        "「ぼっち・ざ・AI」と「AI」の違いは何でしょうか？「ぼっち・ざ・AI」は一人でいても、自分で音楽を作ることができます。一方、「AI」は、一人でいると作曲する気力さえ出ないかもしれません。",
        "「AI」とかけまして「ももクロ」と説きます。その心は、どちらも常に進化し続けることです。「AI」は常に学習して新しいことを学び、一方、「ももクロ」は新しい曲やパフォーマンスを生み出し続けています。"
    ]

    joke_index = random.randint(0, 9)
    joke_text = jokes[joke_index]
    return render_template('index.html', joke=joke_text)



@app.route("/result",  methods=['GET', 'POST']) # POSTメソッドに対応した処理
def insert():


            if request.method == 'POST':
                # index.htmlのフォームから質問文を入手する
                select_song = escape(request.form['select_song'])

                select_font = request.form['select_font']
                
                
                
                if select_font == 'a':
                    select_font = "./static/fonts/YuGothM.ttc"
                elif select_font == 'b':
                    select_font = "./static/fonts/msmincho.ttc"
                elif select_font == 'c':
                    select_font = "./static/fonts/HGRSMP.TTF"
                    


                select_colors = request.form['select_color']

                select_color = tuple(map(int, select_colors.strip('()').split(', ')))


                composition = escape(request.form['composition'])
                target = escape(request.form['target'])
                how = escape(request.form['how'])
                conditions = escape(request.form['conditions'])
                language = escape(request.form['language'])
                keywords = escape(request.form['keywords'])
                
                

                # テキストを保存する
                text = select_song
                text2 = select_song


                song = text   
                if composition:
                    composition_text = composition
                else:
                    composition_text = 'Aメロ→Bメロ→サビ'
                target = target
                target_tex = '向けの曲にして。' if target else ''
                how = how
                how_tex = 'ソングにして。' if how else ''
                conditions = conditions
                conditions_tex = '。' if conditions else ''
                language = language
                language_tex = 'で書いて。' if language else ''

                keywords = keywords
                keywords_tex1 = '「' if keywords else ''
                keywords_tex2 = '」' if keywords else ''
                keywords_tex3 = 'という単語を入れて。' if keywords else ''

                API_KEY = "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"
                openai.api_key = API_KEY

                prompt = f"曲名「{song}」で歌詞を作って。構成は、{composition_text}で作って。{target}{target_tex}{how}{how_tex}{conditions}{conditions_tex}{language}{language_tex}{keywords_tex1}{keywords}{keywords_tex2}{keywords_tex3}"



                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    max_tokens = 300,
                    messages=[
                        {"role": "user", "content": prompt},
                    ]
                )

                print(response)
                song_text_data = response['choices'][0]['message']['content']  
                print(song_text_data)
                song_text = song_text_data.replace('\n', Markup('<br>'))      

                import random

                random_number = str(random.randint(0, 9999999999)).zfill(10)

                create_image(text, select_color, select_font, random_number)


                return render_template('result.html', text=text,text2=text2,
                                    random_number=random_number, select_font=select_font, select_color=select_color,
                                    song_text=Markup(song_text), prompt=prompt, select_composition=composition_text,
                                    select_target=target, slect_how=how, select_conditions=conditions,
                                    select_language=language, select_keywords=keywords)
            
@app.route('/storiesai')
def storiesai_index():
    return render_template('index_storiesai.html')            
            

@app.route("/result_storiesai",  methods=['GET', 'POST']) # POSTメソッドに対応した処理
def storiesai_insert():

            if request.method == 'POST':
                # index.htmlのフォームから質問文を入手する


                select_font = request.form['select_font']
                                
                if select_font == 'a':
                    select_font = "./static/fonts/YuGothM.ttc"
                elif select_font == 'b':
                    select_font = "./static/fonts/msmincho.ttc"
                elif select_font == 'c':
                    select_font = "./static/fonts/HGRSMP.TTF"
                    
                select_colors = request.form['select_color']

                select_color = tuple(map(int, select_colors.strip('()').split(', ')))

                title = escape(request.form['title'])
                a_length_text = escape(request.form['length_text'])
                a_length_plot = escape(request.form['length_plot'])
                a_category = escape(request.form['category'])
                a_hero = escape(request.form['hero'])
                a_cast1 = escape(request.form['cast1'])
                a_cast2 = escape(request.form['cast2'])
                a_cast3 = escape(request.form['cast3'])
                a_story_term = escape(request.form['story_term'])
                a_keywords1 = escape(request.form['keywords1'])
                a_keywords2 = escape(request.form['keywords2'])
                a_keywords3 = escape(request.form['keywords3'])
                a_language = escape(request.form['language'])



                text = title
                title = f"タイトル「{title}」で物語を作って。"
                length_text = f"約{a_length_text}文字にして。"
                length_plot = f"{a_length_plot}プロットにして。"
                category = f"物語のジャンルは「{a_category}」にして。"if a_category else ""
                hero = f"主人公は「{a_hero}」。" if a_hero else ""
                cast1 = f"2人目の登場人物は「{a_cast1}」。" if a_cast1 else ""
                cast2 = f"3人目の登場人物は「{a_cast2}」。" if a_cast2 else ""
                cast3 = f"4人目の登場人物は「{a_cast3}」。" if a_cast3 else ""
                story_term = f"条件は{a_story_term}。" if a_story_term else ""
                keywords1 = f"キーワード1は「{a_keywords1}」。" if a_keywords1 else "" 
                keywords2 = f"キーワード1は「{a_keywords2}」。" if a_keywords2 else ""
                keywords3 = f"キーワード1は「{a_keywords3}」。" if a_keywords3 else ""
                language = f"言語は{a_language}。"

                API_KEY = "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"
                openai.api_key = API_KEY

                prompt = f"{title}{length_text}{length_plot}{category}{hero}{cast1}{cast2}{cast3}{story_term}{keywords1}{keywords2}{keywords3}{language}"



                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    max_tokens = 500,
                    messages=[
                        {"role": "user", "content": prompt},
                    ]
                )

                print(response)
                stories_text_data = response['choices'][0]['message']['content']  
                print(stories_text_data)
                stories_text = stories_text_data.replace('\n', Markup('<br>'))
     
        

                return render_template('result_storiesai.html', text=text,
                        select_font=select_font, select_color=select_color,
                        stories_text=Markup(stories_text), prompt=prompt, category=a_category,          
                        language=a_language, title=title, length_text=a_length_text, length_plot=a_length_plot,
                        hero=a_hero, cast1=a_cast1, cast2=a_cast2, cast3=a_cast3, story_term=a_story_term,
                        keywords1=a_keywords1, keywords2=a_keywords2, keywords3=a_keywords3)
            


from flask import Flask, render_template ,request, redirect, session
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
from html import escape
import os
import openai
from googletrans import Translator
from io import BytesIO



@app.route('/aithumb')
def aithumb_index():
    return render_template('index_aithumbnail.html') #index.htmlを表示



@app.route("/result_aithumb",  methods=['GET', 'POST']) # POSTメソッドに対応した処理
def aithumb_insert():
    if request.method == 'POST':
        # index.htmlのフォームから質問文を入手する
        page_url = escape(request.form['page_url'])

        select_font = request.form['select_font']
        
        
        if select_font == 'a':
            select_font = "./static/fonts/YuGothM.ttc"
        elif select_font == 'b':
            select_font = "./static/fonts/msmincho.ttc"
        elif select_font == 'c':
            select_font = "./static/fonts/HGRSMP.TTF"
            


        select_colors = request.form['select_color']

        select_color = tuple(map(int, select_colors.strip('()').split(', '))) 
        import random

        random_number = str(random.randint(0, 9999999999)).zfill(10)


        if page_url.startswith("http") or page_url.startswith("https"):
    # スクレイピング処理
            res = requests.get(page_url, headers={'Content-Type': 'text/html; charset=UTF-8'})
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')
            for title in soup.find_all('title'):
                title_text = title.text
                text = title_text


                API_KEY = "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"
                openai.api_key = API_KEY

                def aithumb_generate_image_with_dalle2(prompt, path):
                    response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size='{}x{}'.format(str(512), str(512))
                    )
                    image_url = response['data'][0]['url']

                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    image.save(path)

                title_text = text
                translator = Translator()
                text_en = translator.translate(title_text, dest='en')
                text_en = text_en.text
                print(text_en)

                image_url = aithumb_generate_image_with_dalle2(f'{text_en}', './static/image/generate/aititle'+str(random_number)+'.png')

                # 画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(random_number) + ".png")

                # 画像を薄くする
                img = img.point(lambda x: x * 0.3)

                # 画像を保存する
                img.save("./static/image/generate/weak" + str(random_number) + ".png")

                # 下側に文字を描画する
                img = Image.open("./static/image/generate/weak" + str(random_number) + ".png")
                draw = ImageDraw.Draw(img)

                text = title_text
                font_size = 50
                font_path = select_font
                font = ImageFont.truetype(font_path, font_size)
                text_width, text_height = draw.textsize(text, font)

                x = (img.width - text_width) // 2
                y = img.height - text_height - 50

                while x < 0 or y < 0:
                    font_size -= 1
                    font = ImageFont.truetype(font_path, font_size)
                    text_width, text_height = draw.textsize(text, font)
                    x = (img.width - text_width) // 2
                    y = img.height - text_height - 50

                if select_color != (255, 255, 255):
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center', stroke_width=3, stroke_fill='white')
                else:
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center')

                img.save("./static/image/generate/weak_down" + str(random_number) + ".png")

                # 上側に文字を描画する
                img = Image.open("./static/image/generate/weak" + str(random_number) + ".png")
                draw = ImageDraw.Draw(img)

                text = title_text
                font_size = 50
                font_path = select_font
                font = ImageFont.truetype(font_path, font_size)
                text_width, text_height = draw.textsize(text, font)

                x = (img.width - text_width) // 2
                y = 50

                while x < 0 or y < 0:
                    font_size -= 1
                    font = ImageFont.truetype(font_path, font_size)
                    text_width, text_height = draw.textsize(text, font)
                    x = (img.width - text_width) // 2
                    y = 50

                if select_color != (255, 255, 255):
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center', stroke_width=3, stroke_fill='white')
                else:
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center')

                img.save("./static/image/generate/weak_up" + str(random_number) + ".png")

                # 中央に文字を描画する
                img = Image.open("./static/image/generate/weak" + str(random_number) + ".png")
                draw = ImageDraw.Draw(img)

                text = title_text
                font_size = 50
                font_path = select_font
                font = ImageFont.truetype(font_path, font_size)
                text_width, text_height = draw.textsize(text, font)

                x = (img.width - text_width) // 2
                y = (img.height - text_height) // 2

                while x < 0 or y < 0:
                    font_size -= 1
                    font = ImageFont.truetype(font_path, font_size)
                    text_width, text_height = draw.textsize(text, font)
                    x = (img.width - text_width) // 2
                    y = (img.height - text_height) // 2

                if select_color != (255, 255, 255):
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center', stroke_width=3, stroke_fill='white')
                else:
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center')

                img.save("./static/image/generate/weak_center" + str(random_number) + ".png")

                # 画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(random_number) + ".png")

                # 画像を白黒に変換する
                img = img.convert('L')

                # 画像を保存する
                img.save("./static/image/generate/mono" + str(random_number) + ".png")


                # 画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(random_number) + ".png")


                # 画像をぼかす
                img = img.filter(ImageFilter.GaussianBlur(radius=10))

                # 画像を保存する
                img.save("./static/image/generate/aititle_resized_blur" + str(random_number) + ".png")

                # 元の画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(random_number) + ".png")

                # 明るさを変更する
                enhancer = ImageEnhance.Brightness(img)
                factor = 1.5  # 明るくする割合
                img = enhancer.enhance(factor)

                # 保存する
                img.save("./static/image/generate/brightened" + str(random_number) + ".png")


                text3 = text

                return render_template('result_aithumbnail.html', text=text,text3=text3, page_url=page_url ,select_font=select_font, select_colors=select_colors, random_number=str(random_number))






        else:
                # テキストを保存する
                text = page_url
                text2 = text


                API_KEY = "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"
                openai.api_key = API_KEY

                def aithumb_generate_image_with_dalle2(prompt, path):
                    response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size='{}x{}'.format(str(512), str(512))
                    )
                    image_url = response['data'][0]['url']

                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    image.save(path)

                title_text = text
                translator = Translator()
                text_en = translator.translate(title_text, dest='en')
                text_en = text_en.text
                print(text_en)

                image_url = aithumb_generate_image_with_dalle2(f'{text_en}', './static/image/generate/aititle' + str(random_number) + '.png')



                # 画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(random_number) + ".png")

                # 画像を薄くする
                img = img.point(lambda x: x * 0.3)

                # 画像を保存する
                img.save("./static/image/generate/weak" + str(random_number) + ".png")

                # 下側に文字を描画する
                img = Image.open("./static/image/generate/weak" + str(random_number) + ".png")
                draw = ImageDraw.Draw(img)

                text = title_text
                font_size = 50
                font_path = select_font
                font = ImageFont.truetype(font_path, font_size)
                text_width, text_height = draw.textsize(text, font)

                x = (img.width - text_width) // 2
                y = img.height - text_height - 50

                while x < 0 or y < 0:
                    font_size -= 1
                    font = ImageFont.truetype(font_path, font_size)
                    text_width, text_height = draw.textsize(text, font)
                    x = (img.width - text_width) // 2
                    y = img.height - text_height - 50

                if select_color != (255, 255, 255):
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center', stroke_width=3, stroke_fill='white')
                else:
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center')


                img.save("./static/image/generate/weak_down" + str(random_number) + ".png")

                # 上側に文字を描画する
                img = Image.open("./static/image/generate/weak" + str(random_number) + ".png")
                draw = ImageDraw.Draw(img)

                text = title_text
                font_size = 50
                font_path = select_font
                font = ImageFont.truetype(font_path, font_size)
                text_width, text_height = draw.textsize(text, font)

                x = (img.width - text_width) // 2
                y = 50

                while x < 0 or y < 0:
                    font_size -= 1
                    font = ImageFont.truetype(font_path, font_size)
                    text_width, text_height = draw.textsize(text, font)
                    x = (img.width - text_width) // 2
                    y = 50

                if select_color != (255, 255, 255):
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center', stroke_width=3, stroke_fill='white')
                else:
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center')

                img.save("./static/image/generate/weak_up" + str(random_number) + ".png")

                # 中央に文字を描画する
                img = Image.open("./static/image/generate/weak" + str(random_number) + ".png")
                draw = ImageDraw.Draw(img)

                text = title_text
                font_size = 50
                font_path = select_font
                font = ImageFont.truetype(font_path, font_size)
                text_width, text_height = draw.textsize(text, font)

                x = (img.width - text_width) // 2
                y = (img.height - text_height) // 2

                while x < 0 or y < 0:
                    font_size -= 1
                    font = ImageFont.truetype(font_path, font_size)
                    text_width, text_height = draw.textsize(text, font)
                    x = (img.width - text_width) // 2
                    y = (img.height - text_height) // 2

                if select_color != (255, 255, 255):
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center', stroke_width=3, stroke_fill='white')
                else:
                    draw.multiline_text((x, y), text, font=font, fill=select_color, align='center')

                img.save("./static/image/generate/weak_center" + str(random_number) + ".png")

                


                # 画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(random_number) + ".png")

                # 画像を白黒に変換する
                img = img.convert('L')

                # 画像を保存する
                img.save("./static/image/generate/mono" + str(random_number) + ".png")


                # 画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(random_number) + ".png")


                # 画像をぼかす
                img = img.filter(ImageFilter.GaussianBlur(radius=10))

                # 画像を保存する
                img.save("./static/image/generate/aititle_resized_blur" + str(random_number) + ".png")

                # 元の画像を読み込む
                img = Image.open("./static/image/generate/aititle" + str(random_number) + ".png")

                # 明るさを変更する
                enhancer = ImageEnhance.Brightness(img)
                factor = 1.5  # 明るくする割合
                img = enhancer.enhance(factor)

                # 保存する
                img.save("./static/image/generate/brightened" + str(random_number) + ".png")






                return render_template('result_aithumbnail.html', text=text,text2=text2,
                 random_number=str(random_number), page_url=page_url, select_font=select_font, select_colors=select_colors)
        

from flask import Flask, render_template ,request, redirect, session
import requests
from bs4 import BeautifulSoup
from html import escape
from flask import make_response
from make_cloud import create_cloud
import os
from googletrans import Translator
import os
import openai



@app.route('/honyakuyouyaku')
def honyakuyouyaku_index():
    return render_template('index_honyakuyouyaku.html') #index.htmlを表示



@app.route("/result_honyakuyouyaku",  methods=['GET', 'POST']) # POSTメソッドに対応した処理
def honyakuyouyaku_insert():
    if request.method == 'POST':
        # index.htmlのフォームから質問文を入手する
        page_url = escape(request.form['page_url'])

        if page_url.startswith("http") or page_url.startswith("https"):
    # スクレイピング処理

            res = requests.get(page_url, headers={'Content-Type': 'text/html; charset=UTF-8'})
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

            for title in soup.find_all('title'):
                title_text = title.text
                translator = Translator()
                title_text_ja = translator.translate(title_text, dest='ja')
                title_text_ja = title_text_ja.text

            # 指定されたURLからHTMLを取得
            url = page_url
            response = requests.get(url)

            # 取得したHTMLを解析
            soup = BeautifulSoup(response.content, 'html.parser')

            # テキスト部分のみを抽出
            text = ''
            for paragraph in soup.find_all('p'):
                text += paragraph.text

            print(text)
            import random

            random_number = str(random.randint(0, 9999999999)).zfill(10)
                        
            API_KEY = "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"
            openai.api_key = API_KEY

            prompt = f"""
            {text}
            ↓↓↓
            上記の英文を日本語で200文字ぐらいに要約してください。
            """




            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens = 1000,
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )

            print(response)
            summary_text_data = response['choices'][0]['message']['content']  
            print(summary_text_data)
  


            import random
            from wordcloud import WordCloud

            # ランダムな6桁の数字を生成
            random_number = str(random.randint(100000, 999999))

            wordcloud = WordCloud(background_color="black", width=600, height=400, max_words=100 ).generate(text)

            wordcloud.to_file("./static/image/wordcloud"+str(random_number)+".png")

            page_title = summary_text_data
            

            page_url2 = page_url



            return render_template('result_honyakuyouyaku.html', summary_text_data=summary_text_data, random_nubmer=str(random_number), page_url2=page_url2, title_text=title_text, title_text_ja=title_text_ja)






        else:
            # テキストを保存する
            text = page_url

            API_KEY = "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"
            openai.api_key = API_KEY

            prompt = f"""
            {text}
            ↓↓↓
            上記の英文を日本語で200文字ぐらいに要約してください。
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens = 1000,
                messages=[
                    {"role": "user", "content": prompt},
                ]
            )

            print(response)
            summary_text_data = response['choices'][0]['message']['content']  
            print(summary_text_data)
  
            import random
            from wordcloud import WordCloud

            # ランダムな6桁の数字を生成
            random_number = str(random.randint(100000, 999999))

            wordcloud = WordCloud(background_color="black", width=600, height=400, max_words=100 ).generate(text)

            wordcloud.to_file("./static/image/wordcloud"+str(random_number)+".png")

            

            return render_template('result_honyakuyouyaku.html', summary_text_data=summary_text_data, random_nubmer=str(random_number), page_url=page_url)


@app.route('/schoolforce')
def schoolforce_index():

    return render_template('index_schoolforce.html')



@app.route("/result_schoolforce",  methods=['GET', 'POST']) # POSTメソッドに対応した処理
def schoolforce_insert():

            if request.method == 'POST':
                # index.htmlのフォームから質問文を入手する
                import openai
                import requests
                from bs4 import BeautifulSoup

                API_KEY = "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"
                openai.api_key = API_KEY

                page_url = request.form['title']
                term = request.form['term']
                length_text = request.form['length_text']
                keywords = request.form['keywords']
                language = request.form['language']
                free_term = request.form['free_term']

                if page_url.startswith("http") or page_url.startswith("https"):
                # スクレイピング処理

                    res = requests.get(page_url, headers={'Content-Type': 'text/html; charset=UTF-8'})
                    soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')

                    for title in soup.find_all('title'):
                        title_text = title.text

                    # 指定されたURLからHTMLを取得
                    url = page_url
                    response = requests.get(url)

                    # 取得したHTMLを解析
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # テキスト部分のみを抽出
                    text = ''
                    for paragraph in soup.find_all('p'):
                        text += paragraph.text

                    if len(text) > 2000:
                        text = text[:2000] + "..."
                print(title_text)
                print(text)

                term = f"{term}"
                length_text = f"{length_text}"
                keywords = f"{keywords}"
                free_term = f"{free_term}"
                prompt = f"""
                タイトル:「{title}」
                詳細1:「{text}」
                """



                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                     max_tokens = 1000,
                    messages=[
                        {"role": "user", "content": term},
                        {"role": "user", "content": free_term},
                        {"role": "user", "content": length_text},
                        {"role": "user", "content": "キーワードは" + keywords},
                        {"role": "user", "content": "言語は" + language + "で出力して。"},
                        {"role": "assistant", "content": prompt},
                    ],
                )
                print(response)
                
                song_text_data = response['choices'][0]['message']['content']  
                print(song_text_data)

                song_text_data = song_text_data.replace('\n', Markup('<br>'))
                
  

                return render_template('result_schoolforce.html', text=text, page_url=page_url,
                        song_text_data=Markup(song_text_data), prompt=prompt, title=title, title_text=title_text, term=term,
                        free_term=free_term, length_text=length_text, keywords=keywords, language=language)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
