# Shipping a Data Product: From Raw Telegram Data to an Analytical API

## Overview
This project builds an end-to-end data pipeline for extracting, transforming, enriching, and serving insights from Telegram data about Ethiopian medical businesses. It leverages dbt for transformation, Dagster for orchestration, YOLOv8 for image enrichment, and FastAPI for analytics.

## Project Structure
```
├── data/                # Raw and processed data storage
├── src/ or app/         # (Optional) Source code for pipeline and API
├── requirements.txt     # Python dependencies
├── Dockerfile           # Containerization for reproducibility
├── docker-compose.yml   # Orchestrates app and PostgreSQL
├── .env                 # Environment variables (not committed)
├── .gitignore           # Excludes secrets, venv, and instructions
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

### 5. (Optional) Run with Docker
```sh
docker-compose up --build
```

## Running the Pipeline and API
- Data scraping, transformation, enrichment, and API serving are orchestrated via Dagster and FastAPI.
- See individual scripts and notebooks for details.

## Directory Structure
- `data/raw/telegram_messages/YYYY-MM-DD/channel_name.json`: Raw scraped data
- `data/processed/`: Processed/cleaned data (if needed)

## Diagrams
- [Pipeline diagram placeholder]
- [Star schema diagram placeholder]

## Examples
- [Add example API requests and responses here]

## Authors
- Tinbite Yonas

## License
- [Specify license here] 