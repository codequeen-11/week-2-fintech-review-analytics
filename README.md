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


## Task 4: Insights and Recommendations

### Objective
The goal of Task 4 was to transform sentiment and thematic analysis into business-actionable insights for Ethiopian fintech banks. The analysis focused on customer satisfaction drivers, pain points, sentiment patterns, and practical recommendations.

### Cross-Bank Comparison

#### Average Ratings
| Bank | Average Rating |
|---|---:|
| Commercial Bank of Ethiopia | 4.14 |
| Dashen Bank | 3.97 |
| Bank of Abyssinia | 3.61 |

Commercial Bank of Ethiopia achieved the highest average customer rating, while Bank of Abyssinia recorded the lowest rating.

### Sentiment Analysis Summary

| Bank | Positive | Negative | Neutral |
|---|---:|---:|---:|
| Commercial Bank of Ethiopia | 307 | 139 | 4 |
| Bank of Abyssinia | 241 | 207 | 2 |
| Dashen Bank | 293 | 156 | 1 |

Commercial Bank of Ethiopia showed the strongest customer sentiment, while Bank of Abyssinia experienced the highest dissatisfaction level.

### Dominant Themes
The most common business themes identified include:

- User Interface & Experience
- Transaction Performance
- Account Access Issues
- App Reliability
- Customer Support
- Feature Requests

User Interface & Experience was the dominant theme across all three banking applications, indicating that usability and navigation strongly influence customer satisfaction.

### Bank-Specific Insights

#### Commercial Bank of Ethiopia (CBE)

**Satisfaction Drivers**
- Strong positive customer sentiment
- High satisfaction with app usability and interface design

**Pain Points**
- App reliability concerns such as crashes and failures
- Login and authentication issues

**Recommendations**
1. Improve app stability during peak transaction periods.
2. Strengthen OTP and login reliability.

---

#### Bank of Abyssinia (BOA)

**Satisfaction Drivers**
- Positive user perception of interface simplicity
- Functional mobile banking experience

**Pain Points**
- Highest negative sentiment among all banks
- App reliability and transaction performance issues

**Recommendations**
1. Prioritize performance optimization and bug fixing.
2. Improve transfer speed and transaction success rate.
3. Enhance customer support responsiveness.

---

#### Dashen Bank

**Satisfaction Drivers**
- Strong positive customer sentiment
- Positive feedback regarding usability and navigation

**Pain Points**
- High number of account access complaints
- Reliability-related concerns

**Recommendations**
1. Improve authentication and OTP systems.
2. Strengthen error handling and failure messaging.

### Visualizations
Task 4 generated the following visualizations:

```text
reports/figures/task4_sentiment_distribution_by_bank.png
reports/figures/task4_average_rating_by_bank.png
reports/figures/task4_theme_frequency_by_bank.png
reports/figures/task4_rating_distribution_by_bank.png
reports/figures/task4_monthly_sentiment_trend.png
```

### Key Takeaways
- Commercial Bank of Ethiopia currently leads in customer satisfaction.
- Bank of Abyssinia faces the greatest opportunity for product improvement.
- User experience and interface quality are the strongest satisfaction drivers across all banks.
- Authentication reliability and transaction performance remain major pain points in Ethiopian fintech apps.
## Task 3: PostgreSQL Database Storage

The processed review data was stored in a PostgreSQL database named `bank_reviews`.

### Database Schema
Two relational tables were created:

- `banks`: stores bank metadata including bank name and app name.
- `reviews`: stores review text, rating, review date, sentiment label, sentiment score, identified theme, and source.

The schema is defined in:

```text
sql/schema.sql
