import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


CSV_FILE = "data/processed/analyzed_reviews.csv"


BANK_APPS = {
    "Commercial Bank of Ethiopia": "Commercial Bank of Ethiopia Mobile",
    "Bank of Abyssinia": "BOA Mobile Banking",
    "Dashen Bank": "Dashen Super App",
}


def connect_db():
    return psycopg2.connect(**DB_CONFIG)


def insert_banks(cursor):
    bank_mapping = {}

    for bank_name, app_name in BANK_APPS.items():
        cursor.execute(
            """
            INSERT INTO banks (bank_name, app_name)
            VALUES (%s, %s)
            ON CONFLICT (bank_name)
            DO NOTHING;
            """,
            (bank_name, app_name)
        )

    cursor.execute("SELECT bank_id, bank_name FROM banks;")
    rows = cursor.fetchall()

    for bank_id, bank_name in rows:
        bank_mapping[bank_name] = bank_id

    return bank_mapping


def insert_reviews(cursor, df, bank_mapping):
    inserted_count = 0

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO reviews (
                review_id,
                bank_id,
                review_text,
                rating,
                review_date,
                sentiment_label,
                sentiment_score,
                identified_theme,
                source
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (review_id)
            DO NOTHING;
            """,
            (
                int(row["review_id"]),
                bank_mapping[row["bank"]],
                row["review_text"],
                int(row["rating"]),
                row["date"],
                row["sentiment_label"],
                float(row["sentiment_score"]),
                row["identified_theme"],
                row["source"],
            )
        )

        inserted_count += 1

    return inserted_count


def main():
    df = pd.read_csv(CSV_FILE)

    conn = connect_db()
    cursor = conn.cursor()

    bank_mapping = insert_banks(cursor)

    inserted_count = insert_reviews(
        cursor,
        df,
        bank_mapping
    )

    conn.commit()

    print(f"Inserted {inserted_count} reviews.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()