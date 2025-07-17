from .database import get_db

def get_top_channels(limit=10):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT channel_name, COUNT(*) as count
        FROM fct_messages
        GROUP BY channel_name
        ORDER BY count DESC
        LIMIT %s
    ''', (limit,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def get_channel_activity(channel_name):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT channel_name, COUNT(*) as total_messages
        FROM fct_messages
        WHERE channel_name = %s
        GROUP BY channel_name
    ''', (channel_name,))
    summary = cur.fetchone()
    cur.execute('''
        SELECT date::text, COUNT(*) as messages
        FROM fct_messages
        WHERE channel_name = %s
        GROUP BY date
        ORDER BY date
    ''', (channel_name,))
    per_day = {row['date']: row['messages'] for row in cur.fetchall()}
    cur.close()
    conn.close()
    if summary:
        summary['messages_per_day'] = per_day
    return summary

def search_messages(query):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        SELECT message_id, channel_name, date::text, text
        FROM fct_messages
        WHERE text ILIKE %s
        LIMIT 50
    ''', (f'%{query}%',))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results 