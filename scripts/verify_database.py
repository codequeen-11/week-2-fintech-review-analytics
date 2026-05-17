import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)

cursor = conn.cursor()

queries = {
    "Total reviews": "SELECT COUNT(*) FROM reviews;",
    "Reviews per bank": """
        SELECT b.bank_name, COUNT(r.review_id)
        FROM banks b
        JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
        ORDER BY b.bank_name;
    """,
    "Average rating per bank": """
        SELECT b.bank_name, ROUND(AVG(r.rating), 2)
        FROM banks b
        JOIN reviews r ON b.bank_id = r.bank_id
        GROUP BY b.bank_name
        ORDER BY b.bank_name;
    """,
    "Null check": """
        SELECT
            COUNT(*) FILTER (WHERE review_text IS NULL) AS missing_review_text,
            COUNT(*) FILTER (WHERE rating IS NULL) AS missing_rating,
            COUNT(*) FILTER (WHERE sentiment_label IS NULL) AS missing_sentiment,
            COUNT(*) FILTER (WHERE identified_theme IS NULL) AS missing_theme
        FROM reviews;
    """
}

for title, query in queries.items():
    print(f"\n{title}")
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

cursor.close()
conn.close()