# Shipping a Data Product: From Raw Telegram Data to an Analytical API

## Project Summary
This project delivers an end-to-end data pipeline for extracting, transforming, enriching, and serving insights from Telegram data about Ethiopian medical businesses. It leverages dbt for transformation, Dagster for orchestration, YOLOv8 for image enrichment, and FastAPI for analytics. The pipeline is designed for reproducibility, scalability, and secure handling of secrets.

## Key Features
- **Data Scraping:** Extracts messages and images from public Telegram channels using Telethon.
- **Data Lake:** Stores raw data in a partitioned directory structure (`data/raw/telegram_messages/YYYY-MM-DD/channel_name/`).
- **Data Warehouse:** Loads and transforms data in PostgreSQL using dbt, following a star schema (fact and dimension tables).
- **Data Enrichment:** Uses YOLOv8 for object detection on images, linking results to messages.
- **Analytical API:** Exposes insights via FastAPI endpoints for business questions.
- **Orchestration:** Uses Dagster for robust, observable, and schedulable pipelines.
- **Testing & Validation:** Includes dbt tests and robust logging.
- **Documentation:** Comprehensive README, inline comments, and diagrams.

## Project Structure
```
├── data/                # Raw and processed data (not tracked by git)
├── notebooks/           # Jupyter/Colab notebooks for scraping, EDA, etc.
├── src/ or app/         # (Optional) Source code for pipeline and API
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerization for reproducibility
├── docker-compose.yml   # Orchestrates app and PostgreSQL
├── .env                 # Environment variables (not committed)
├── .gitignore           # Excludes secrets, venv, data, and instructions
├── README.md            # Project documentation
```

## Setup Instructions
### 1. Clone the repository
```sh
git clone <repo-url>
cd <repo-directory>
```

### 2. Create and activate a virtual environment
```sh
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure environment variables
- Copy `.env` template and fill in your secrets (Telegram API, DB credentials, etc).
- **Never commit your .env file or data/ directory.**

### 5. (Optional) Run with Docker
```sh
docker-compose up --build
```

## Usage
### Data Scraping (Task 1)
- Use the notebook at `notebooks/scraping.ipynb` (recommended: run on Google Colab).
- Scraped data will be saved in `data/raw/telegram_messages/YYYY-MM-DD/channel_name/`.

### Data Modeling & Transformation (Task 2)
- Load raw JSON into PostgreSQL.
- Use dbt to transform and model data (star schema: `dim_channels`, `dim_dates`, `fct_messages`).
- Run dbt tests for data quality.

### Data Enrichment (Task 3)
- Use YOLOv8 to detect objects in images and link results to messages.

### Analytical API (Task 4)
- Serve insights using FastAPI endpoints (see `src/app/` or `app/`).
- Example endpoints:
  - `/api/reports/top-products?limit=10`
  - `/api/channels/{channel_name}/activity`
  - `/api/search/messages?query=paracetamol`

### Orchestration (Task 5)
- Use Dagster to orchestrate the full pipeline (see `src/` or `dag/`).
- Schedule and monitor jobs with Dagster UI.

## Directory Structure
- `data/raw/telegram_messages/YYYY-MM-DD/channel_name/`: Raw scraped data (JSON, images)
- `notebooks/`: Jupyter/Colab notebooks for scraping and EDA
- `src/` or `app/`: Source code for pipeline, API, and orchestration

## Diagrams
- [Pipeline diagram placeholder]
- [Star schema diagram placeholder]

## Examples
- Example API request:
  ```sh
  curl -X GET "http://localhost:8000/api/reports/top-products?limit=10"
  ```
- Example dbt test run:
  ```sh
  dbt test
  ```

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