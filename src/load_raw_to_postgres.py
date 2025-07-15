import os
import json
import glob
import logging
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'telegram')
DB_USER = os.getenv('POSTGRES_USER', 'postgres')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'postgres')

RAW_DATA_PATH = 'data/raw/telegram_messages'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def get_all_json_files(base_path):
    return glob.glob(os.path.join(base_path, '*', '*', '*.json'))

def flatten_message(msg, channel_name, scrape_date):
    return {
        'id': msg.get('id'),
        'date': msg.get('date'),
        'text': msg.get('text'),
        'has_media': msg.get('has_media'),
        'media_path': msg.get('media_path'),
        'channel_name': channel_name,
        'scrape_date': scrape_date
    }

def create_table_if_not_exists(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS raw_telegram_messages (
            id BIGINT,
            date TIMESTAMPTZ,
            text TEXT,
            has_media BOOLEAN,
            media_path TEXT,
            channel_name TEXT,
            scrape_date DATE,
            PRIMARY KEY (id, channel_name, scrape_date)
        );
    ''')

def upsert_messages(cur, messages):
    sql = '''
        INSERT INTO raw_telegram_messages (id, date, text, has_media, media_path, channel_name, scrape_date)
        VALUES %s
        ON CONFLICT (id, channel_name, scrape_date) DO UPDATE SET
            date = EXCLUDED.date,
            text = EXCLUDED.text,
            has_media = EXCLUDED.has_media,
            media_path = EXCLUDED.media_path
    '''
    values = [
        (
            m['id'],
            m['date'],
            m['text'],
            m['has_media'],
            m['media_path'],
            m['channel_name'],
            m['scrape_date']
        ) for m in messages
    ]
    execute_values(cur, sql, values)

def main():
    files = get_all_json_files(RAW_DATA_PATH)
    logging.info(f'Found {len(files)} JSON files to load.')
    all_messages = []
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Extract channel and date from path
            parts = file.split(os.sep)
            scrape_date = parts[-3]
            channel_name = parts[-2]
            for msg in data:
                all_messages.append(flatten_message(msg, channel_name, scrape_date))
        except Exception as e:
            logging.error(f'Failed to process {file}: {e}')
    logging.info(f'Loaded {len(all_messages)} messages from all files.')
    if not all_messages:
        logging.warning('No messages to load. Exiting.')
        return
    # Connect to PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cur = conn.cursor()
    create_table_if_not_exists(cur)
    upsert_messages(cur, all_messages)
    conn.commit()
    cur.close()
    conn.close()
    logging.info('All messages loaded into raw_telegram_messages table.')

if __name__ == '__main__':
    main() 