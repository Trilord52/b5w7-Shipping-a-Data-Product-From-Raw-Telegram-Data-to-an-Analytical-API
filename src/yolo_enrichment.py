import os
import glob
import json
import logging
import pandas as pd
from ultralytics import YOLO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RAW_IMAGE_PATH = 'data/raw/telegram_messages'
OUTPUT_CSV = 'data/yolo_detections.csv'
MODEL_PATH = os.getenv('YOLO_MODEL_PATH', 'yolov8n.pt')  # Use a default YOLOv8 model

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def find_all_images(base_path):
    # Search for images in all subdirectories
    images = glob.glob(os.path.join(base_path, '*', '*', '*.jpg'))
    print(f"Found images: {images}")  # Debug print
    return images

def extract_message_id(image_path):
    # Assumes image filename is photo_<message_id>.jpg
    filename = os.path.basename(image_path)
    if filename.startswith('photo_') and filename.endswith('.jpg'):
        try:
            return int(filename.replace('photo_', '').replace('.jpg', ''))
        except Exception:
            return None
    return None

def main():
    images = find_all_images(RAW_IMAGE_PATH)
    logging.info(f'Found {len(images)} images to process.')
    if not images:
        logging.warning('No images found. Please check your data directory structure.')
        return
    model = YOLO(MODEL_PATH)
    results = []
    for image_path in images:
        message_id = extract_message_id(image_path)
        if message_id is None:
            logging.warning(f'Could not extract message_id from {image_path}')
            continue
        try:
            detections = model(image_path, verbose=False)[0]
            for box in detections.boxes:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                results.append({
                    'message_id': message_id,
                    'image_path': image_path,
                    'detected_object_class': class_name,
                    'confidence_score': confidence
                })
            logging.info(f'Processed {image_path}: {len(detections.boxes)} detections')
        except Exception as e:
            logging.error(f'Error processing {image_path}: {e}')
    if results:
        df = pd.DataFrame(results)
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        df.to_csv(OUTPUT_CSV, index=False)
        logging.info(f'Saved detection results to {OUTPUT_CSV}')
    else:
        logging.warning('No detections found in any images.')

if __name__ == '__main__':
    main() 