select
    message_id,
    image_path,
    detected_object_class,
    confidence_score
from {{ source('public', 'fct_image_detections') }} 