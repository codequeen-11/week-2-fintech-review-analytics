import pandas as pd
from google_play_scraper import reviews, Sort


BANK_APPS = {
    "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
    "Bank of Abyssinia": "com.boa.boaMobileBanking",
    "Dashen Bank": "com.dashen.dashensuperapp",
}


def scrape_bank_reviews(bank_name, app_id, count=450):
    result, _ = reviews(
        app_id,
        lang="en",
        country="et",
        sort=Sort.NEWEST,
        count=count,
    )

    rows = []

    for item in result:
        rows.append({
            "review_id": item.get("reviewId"),
            "review": item.get("content"),
            "rating": item.get("score"),
            "date": item.get("at"),
            "bank": bank_name,
            "source": "Google Play",
        })

    return rows


def clean_reviews(df):
    print("Before cleaning:", df.shape)

    duplicate_count = df.duplicated(subset=["review_id"]).sum()
    missing_review_count = df["review"].isna().sum()
    missing_rating_count = df["rating"].isna().sum()

    print("Duplicate reviews:", duplicate_count)
    print("Missing review text:", missing_review_count)
    print("Missing rating:", missing_rating_count)

    df = df.drop_duplicates(subset=["review_id"])
    df = df.dropna(subset=["review", "rating"])

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    df = df[["review", "rating", "date", "bank", "source"]]

    print("After cleaning:", df.shape)
    print(df["bank"].value_counts())

    return df


def main():
    all_reviews = []

    for bank_name, app_id in BANK_APPS.items():
        print(f"Scraping reviews for {bank_name}...")
        bank_reviews = scrape_bank_reviews(bank_name, app_id)
        all_reviews.extend(bank_reviews)

    raw_df = pd.DataFrame(all_reviews)
    raw_df.to_csv("data/raw/raw_reviews.csv", index=False)

    clean_df = clean_reviews(raw_df)
    clean_df.to_csv("data/processed/clean_reviews.csv", index=False)

    print("Saved cleaned data to data/processed/clean_reviews.csv")


if __name__ == "__main__":
    main()