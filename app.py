from flask import Flask, render_template, request, redirect, session, url_for
from markupsafe import Markup
from html import escape
import os
import openai

from moviepy.editor import *
from make_movie import create_movie
import psycopg2


app = Flask(__name__)
app.secret_key = os.urandom(24)  # セッションを暗号化するための秘密鍵

#openAIのAPIキーを記述してください
api_key = "・・・"

@app.route('/')
def index():
    return render_template('index_make.html')

@app.route('/pro' , methods=['POST'])
def product():
    if request.method == 'POST':
        # index.htmlのフォームから質問文を入手する
        import openai

        item_name = request.form['item_name']
        item_price = request.form['item_price']
        item_quantity = request.form['item_quantity']
        bottom_order = request.form['bottom_order']
        top_order = request.form['top_order']
        category = request.form['category']
        ship_origin = request.form['ship_origin']
        ship_days = request.form['ship_days']
        keywords = request.form['keywords']
        item_detail = request.form['item_detail']
        item_detail = item_detail.replace('\n', '<br>')
        target = request.form['target'] 


        prompt = f"""
        この商品を買いたくなる200文字ぐらいの商品紹介文を作って。
        """

        API_KEY = api_key
        openai.api_key = API_KEY

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
                max_tokens = 1000,
            messages=[
                {"role": "user", "content": "商品名は「" + item_name + "」"},
                {"role": "user", "content": "商品価格は「" + item_price + "円」"},
                {"role": "user", "content": "カテゴリーは「" + category + "」"},
                {"role": "user", "content": "キーワードは「" + keywords + "」"},
                {"role": "user", "content": "ターゲット層は「" + target + "」"},
                {"role": "user", "content": "商品の詳細は「" + item_detail + "」"},
                {"role": "assistant", "content": prompt},
            ],
        )
        print(response)
        intro_text_data = response['choices'][0]['message']['content']  
        print(intro_text_data)

        conn = psycopg2.connect(
            host="localhost",
            database="moviec",
            user="postgres",
            password="・・・"
        )

        cur = conn.cursor()
        # データの挿入
        cur.execute("""
        INSERT INTO moviec_table (
            item_name,
            item_price,
            item_quantity,
            bottom_order,
            top_order,
            category,
            ship_origin,
            ship_days,
            keywords,
            item_detail,
            target,
            prompt,
            intro_text_data
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        ) RETURNING id""", (
            item_name,
            item_price,
            item_quantity,
            bottom_order,
            top_order,
            category,
            ship_origin,
            ship_days,
            keywords,
            item_detail,
            target,
            prompt,
            intro_text_data
        ))

        # 挿入したデータの ID を取得
        inserted_id = cur.fetchone()[0]


        # 変更を確定し、接続を閉じる
        conn.commit()
        conn.close()

        # 最大のidを取得
        max_id = inserted_id
        max_id = str(max_id)
        from gtts import gTTS
        import os

        # Specify the language for text-to-speech conversion (in this case, Japanese)
        language = "ja"

        # Create a text-to-speech object and specify the text and language
        tts = gTTS(text=intro_text_data, lang=language)

        # Specify the path to the original audio file
        filename = f"static/contents/audio/sample_audio{max_id}.mp3"

        tts.save(filename)

        from pydub import AudioSegment

        # Load the audio file using pydub
        audio = AudioSegment.from_file(filename, format="mp3")

        # Speed up the audio by 1.5 times
        speed_factor = 1.25
        modified_audio = audio.speedup(playback_speed=speed_factor)

        # Specify the path to the modified audio file
        modified_filename = f"static/contents/audio/modified_audio{max_id}.mp3"

        # Export the modified audio file
        modified_audio.export(modified_filename, format="mp3")

        from PIL import Image
        import os 
        import random

        # Get files
        image_file = request.files.get('item_image')
        image_file2 = request.files.get('item_image2')
        image_file3 = request.files.get('item_image3')
        image_file4 = request.files.get('item_image4')
        image_file5 = request.files.get('item_image5')
        image_file6 = request.files.get('item_image6')

        # Check if each image_file is None
        print(image_file)
        print(image_file2)
        print(image_file3)
        print(image_file4)
        print(image_file5)
        print(image_file6)

        # Do something for each file
        for i, file in enumerate([image_file, image_file2, image_file3, image_file4, image_file5, image_file6]):
            if file and file.filename.split('.')[-1] in ['png', 'jpeg', 'jpg']:
                # Create file name
                filename = "item_photo" + max_id + "_" + str(i + 1) + ".png"

                # Open image
                image = Image.open(file)

                # Convert to PNG and save
                image.save(os.path.join(app.static_folder, "image/generate", filename), 'png')
        image_1 = f'<img width="60" height="60" class="rounded-2 " src="./static/image/generate/item_photo{max_id}_1.png" />'
        image_2 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_2.png")):
            image_2 = f'<img width="60" height="60" class="rounded-2" src="./static/image/generate/item_photo{max_id}_2.png" />'
        image_3 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_3.png")):
            image_3 = f'<img width="60" height="60" class="rounded-2" src="./static/image/generate/item_photo{max_id}_3.png" />'
        image_4 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_4.png")):
            image_4 = f'<img width="60" height="60" class="rounded-2" src="./static/image/generate/item_photo{max_id}_4.png" />'
        image_5 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_5.png")):
            image_5 = f'<img width="60" height="60" class="rounded-2" src="./static/image/generate/item_photo{max_id}_5.png" />'
        image_6 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_6.png")):
            image_6 = f'<img width="60" height="60" class="rounded-2" src="./static/image/generate/item_photo{max_id}_6.png" />'

        create_movie(max_id, intro_text_data)

        # your.htmlにリダイレクト
        return redirect(f'/shop_page/{max_id}')

@app.route('/shop_page/<int:max_id>')
def shop_page(max_id):

        conn = psycopg2.connect(
            host="localhost",
            database="moviec",
            user="postgres",
            password="・・・"
        )

        cur = conn.cursor()

        # idがmax_idの行を取得
        cur.execute("SELECT * FROM moviec_table WHERE id=%s", (max_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        # データの取得
        item_name = row[1]
        item_price = row[2]
        item_quantity = row[3]
        bottom_order = row[4]
        top_order = row[5]
        category = row[6]
        ship_origin = row[7]
        ship_days = row[8]
        keywords = row[9]
        item_detail = row[10]
        target = row[11]
        prompt = row[12]
        intro_text_data = row[13]

        image_1 = f'<img width="60" id="iamge_2" height="60" class="rounded-2 " src="/static/image/generate/item_photo{max_id}_1.png" />'
        image_2 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_2.png")):
            image_2 = f'<img width="60" id="iamge_2" height="60" class="rounded-2" src="/static/image/generate/item_photo{max_id}_2.png" />'
        image_3 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_3.png")):
            image_3 = f'<img width="60" id="iamge_2" height="60" class="rounded-2" src="/static/image/generate/item_photo{max_id}_3.png" />'
        image_4 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_4.png")):
            image_4 = f'<img width="60" id="iamge_2" height="60" class="rounded-2" src="/static/image/generate/item_photo{max_id}_4.png" />'
        image_5 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_5.png")):
            image_5 = f'<img width="60" id="iamge_2" height="60" class="rounded-2" src="/static/image/generate/item_photo{max_id}_5.png" />'
        image_6 = ""
        if os.path.exists(os.path.join(app.static_folder, f"image/generate/item_photo{max_id}_6.png")):
            image_6 = f'<img width="60" id="iamge_2" height="60" class="rounded-2" src="/static/image/generate/item_photo{max_id}_6.png" />'
        print(max_id)
        return render_template('pro.html',item_name=item_name, item_price=item_price, category=category, 
                            keywords=keywords, item_detail=Markup(item_detail), target=target,
                            intro_text_data=intro_text_data, max_id=str(max_id), ship_origin=ship_origin, ship_days=ship_days,
                            item_quantity=item_quantity, bottom_order=bottom_order, top_order=top_order, prompt=prompt,
                            image_1=image_1, image_2=image_2, image_3=image_3, image_4=image_4, image_5=image_5, image_6=image_6)


@app.route('/purchase', methods=['POST'])
def purchase():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    if request.method == 'POST':
        item_id = request.form['item_id']
        item_name = request.form['item_name']
        item_price = request.form['item_price']
        item_quantity = request.form['item_quantity']
        ship_days = request.form['ship_days']
        ship_origin = request.form['ship_origin']

        return render_template('purchase.html', 
                           username=session['username'], 
                           item_id=item_id, 
                           item_name=item_name, 
                           item_price=item_price, 
                           item_quantity=item_quantity, 
                           ship_days=ship_days, 
                           ship_origin=ship_origin)


@app.route('/comp', methods=['POST'])
def comp():
    if 'username' not in session:
        return redirect(url_for('login_page'))
    
    if request.method == 'POST':

        return render_template('comp.html', 
                           username=session['username'])
    

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')
