import os
import pandas as pd
import logging
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DB_PORT = os.getenv('POSTGRES_PORT', '5432')
DB_NAME = os.getenv('POSTGRES_DB', 'TelegramShipping')
DB_USER = os.getenv('POSTGRES_USER', 'Tinbite')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'tinbite52')

CSV_PATH = 'data/yolo_detections.csv'

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def create_table_if_not_exists(cur):
    cur.execute('''
        CREATE TABLE IF NOT EXISTS fct_image_detections (
            message_id BIGINT,
            image_path TEXT,
            detected_object_class TEXT,
            confidence_score FLOAT,
            PRIMARY KEY (message_id, image_path, detected_object_class, confidence_score)
        );
    ''')

def upsert_detections(cur, detections):
    sql = '''
        INSERT INTO fct_image_detections (message_id, image_path, detected_object_class, confidence_score)
        VALUES %s
        ON CONFLICT (message_id, image_path, detected_object_class, confidence_score) DO NOTHING
    '''
    values = [
        (
            int(row['message_id']),
            row['image_path'],
            row['detected_object_class'],
            float(row['confidence_score'])
        ) for _, row in detections.iterrows()
    ]
    execute_values(cur, sql, values)

def main():
    if not os.path.exists(CSV_PATH):
        logging.error(f'CSV file not found: {CSV_PATH}')
        return
    detections = pd.read_csv(CSV_PATH)
    logging.info(f'Loaded {len(detections)} detection records from {CSV_PATH}')
    if detections.empty:
        logging.warning('No detection records to load. Exiting.')
        return
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        create_table_if_not_exists(cur)
        upsert_detections(cur, detections)
        conn.commit()
        cur.close()
        conn.close()
        logging.info('All detection records loaded into fct_image_detections table.')
    except Exception as e:
        logging.error(f'Failed to load detections into PostgreSQL: {e}')

if __name__ == '__main__':
    main() 