select
    id as message_id,
    channel_name,
    date,
    text,
    has_media,
    media_path,
    scrape_date
from {{ source('public', 'raw_telegram_messages') }} 