import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="moviec",
    user="postgres",
    password="・・・"
)

cur = conn.cursor()

# sakkyokutable テーブルの作成
cur.execute("""
CREATE TABLE moviec_table (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(255),
    item_price FLOAT,
    item_quantity INTEGER,
    bottom_order VARCHAR(255),
    top_order VARCHAR(255),
    category VARCHAR(255),
    ship_origin VARCHAR(255),
    ship_days VARCHAR(255),
    keywords VARCHAR(255),
    item_detail VARCHAR(2000),
    target VARCHAR(255),
    prompt VARCHAR(510),
    intro_text_data VARCHAR(2000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")


conn.commit()
conn.close()