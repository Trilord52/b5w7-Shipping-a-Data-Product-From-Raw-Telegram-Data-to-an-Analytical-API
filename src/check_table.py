import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="TelegramShipping",
    user="Tinbite",
    password="tinbite52"
)
cur = conn.cursor()
cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'raw_telegram_messages'
    );
""")
exists = cur.fetchone()[0]
print("Table exists:" if exists else "Table does NOT exist.")
cur.close()
conn.close()