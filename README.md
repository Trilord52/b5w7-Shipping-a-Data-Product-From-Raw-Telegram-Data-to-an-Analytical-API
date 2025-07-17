# Shipping a Data Product: From Raw Telegram Data to an Analytical API

## Project Status
- **Task 0:** Project setup & environment management ✅
- **Task 1:** Data scraping and collection ✅
- **Task 2:** Data modeling and transformation (dbt) ✅
- **Task 3:** Data enrichment with YOLO ✅
- **Task 4:** Analytical API ⏳
- **Task 5:** Pipeline orchestration ⏳

## Overview
This project builds an end-to-end data pipeline for extracting, transforming, enriching, and serving insights from Telegram data about Ethiopian medical businesses. It leverages dbt for transformation, Dagster for orchestration, YOLOv8 for image enrichment, and FastAPI for analytics. The pipeline is designed for reproducibility, scalability, and secure handling of secrets.

## Project Structure
```
├── data/                # Raw and processed data (gitignored)
├── notebooks/           # Jupyter/Colab notebooks for scraping, EDA, etc.
├── src/                 # Source code for pipeline and loaders
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerization for reproducibility
├── docker-compose.yml   # Orchestrates app and PostgreSQL
├── .env                 # Environment variables (not committed)
├── .gitignore           # Excludes secrets, venv, data, and instructions
├── README.md            # Project documentation
```

## Setup Instructions
1. **Clone the repository**
2. **Create and activate a virtual environment**
3. **Install dependencies**
4. **Configure environment variables in `.env`**
5. **Start PostgreSQL with Docker Compose**
6. **Load raw data into PostgreSQL**
7. **Initialize and configure dbt**

## Data Scraping (Task 1)
- Scraping is performed using Telethon in a Jupyter/Colab notebook.
- Data is saved in `data/raw/telegram_messages/YYYY-MM-DD/channel_name/` as JSON and images.
- Logging and error handling are implemented for traceability.

## Data Modeling & Transformation (Task 2)
- Raw data is loaded into the `raw_telegram_messages` table in the `TelegramShipping` database using `src/load_raw_to_postgres.py`.
- dbt project is initialized and configured to connect to the database.
- **Staging model:** Cleans and restructures raw data.
- **Mart models:**
  - `dim_channels`: Channel info
  - `dim_dates`: Date dimension
  - `fct_messages`: Fact table with foreign keys and metrics
- **Testing:** dbt built-in and custom tests for data quality.
- **Documentation:** dbt docs generated for all models.

### Star Schema Diagram (placeholder)
```
FCT_MESSAGES
  |-- channel_id --> DIM_CHANNELS
  |-- date_id    --> DIM_DATES
```

## Data Enrichment with YOLO (Task 3)
- All images scraped in Task 1 are processed using a YOLOv8 model (ultralytics) to detect objects of interest.
- The enrichment script (`src/yolo_enrichment.py`) scans for new images and runs YOLOv8 inference, saving detection results to `data/yolo_detections.csv`.
- The loader script (`src/load_yolo_detections_to_postgres.py`) imports these detections into the `fct_image_detections` table in PostgreSQL, linking each detection to its source message.
- A dbt source and mart model (`fct_image_detections_mart`) are defined to expose these detections for analytics, with tests and documentation.
- This enables analysis of visual content (e.g., most common detected objects, confidence scores, image-level trends) alongside text data in the warehouse.

### How to Run YOLO Enrichment
1. Ensure all images are present in the data directory (from Task 1 scraping).
2. Run the enrichment script:
   ```sh
   python src/yolo_enrichment.py
   ```
3. Load the detection results into PostgreSQL:
   ```sh
   python src/load_yolo_detections_to_postgres.py
   ```
4. Build and test the dbt mart model:
   ```sh
   cd telegram_dbt
   dbt run
   dbt test
   ```

### Data Model
- **fct_image_detections_mart**: Contains one row per detected object, with columns:
  - `message_id` (foreign key to messages)
  - `image_path`
  - `detected_object_class`
  - `confidence_score`

---
- **Task 3:** Data enrichment with YOLO ✅

## Testing & Validation
- dbt built-in and custom tests for data quality
- Logging for all pipeline steps

## Documentation & Support
- Inline comments in code and notebooks
- This README for setup, usage, and troubleshooting
- For questions, open an issue or contact the author

## Contributing
Contributions are welcome! Please fork the repo and submit a pull request.

## Authors
- Tinbite Yonas

## License
- [Specify license here] 