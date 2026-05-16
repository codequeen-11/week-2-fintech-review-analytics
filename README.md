# Fintech Review Analytics

## Project Overview
This project analyzes Google Play Store reviews for three Ethiopian banking apps: Commercial Bank of Ethiopia, Bank of Abyssinia, and Dashen Bank. The goal is to collect, clean, and prepare customer review data for sentiment analysis, thematic analysis, and business recommendations.

## Task 1: Data Collection and Preprocessing

### Data Source
Reviews were collected from the Google Play Store using the `google-play-scraper` Python package.

### Banks Scraped
- Commercial Bank of Ethiopia
- Bank of Abyssinia
- Dashen Bank

### Methodology
For each bank, 450 recent reviews were scraped from Google Play. The scraper collected:
- Review text
- Rating
- Review date
- Bank name
- Source

The raw data was saved locally in `data/raw/raw_reviews.csv`, and the cleaned data was saved locally in `data/processed/clean_reviews.csv`.

### Data Cleaning
The preprocessing step included:
- Removing duplicate reviews using review ID
- Dropping rows with missing review text or rating
- Normalizing dates to `YYYY-MM-DD`
- Keeping only the required columns: `review`, `rating`, `date`, `bank`, and `source`

### Data Summary
The cleaned dataset contains 1,350 reviews:

| Bank | Number of Reviews |
|---|---:|
| Commercial Bank of Ethiopia | 450 |
| Bank of Abyssinia | 450 |
| Dashen Bank | 450 |

### Limitations
The dataset is based on recent Google Play Store reviews. Review availability may vary depending on Google Play access, app review volume, and scraper limitations.

## Repository Notes
The `data/` folder and CSV files are excluded from GitHub using `.gitignore` to avoid committing raw or processed datasets.

## How to Run

```bash
pip install -r requirements.txt
python scripts/scrape_reviews.py



## Task 2: Sentiment and Thematic Analysis

### Sentiment Analysis
Sentiment analysis was performed using `distilbert-base-uncased-finetuned-sst-2-english` from Hugging Face Transformers. Each review was classified as positive, negative, or neutral, with a confidence score.

### Thematic Analysis
Review themes were identified using cleaned review text, keyword matching, and TF-IDF keyword extraction. The main business themes include:

- Account Access Issues
- Transaction Performance
- App Reliability
- User Interface & Experience
- Customer Support
- Feature Requests

### Task 2 Outputs
The analyzed dataset is saved locally as:

```text
data/processed/analyzed_reviews.csv


## Task 3: PostgreSQL Database Storage

The processed review data was stored in a PostgreSQL database named `bank_reviews`.

### Database Schema
Two relational tables were created:

- `banks`: stores bank metadata including bank name and app name.
- `reviews`: stores review text, rating, review date, sentiment label, sentiment score, identified theme, and source.

The schema is defined in:

```text
sql/schema.sql