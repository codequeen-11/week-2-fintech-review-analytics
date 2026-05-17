import re
import logging
import pandas as pd
import nltk

from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords


INPUT_FILE = "data/processed/clean_reviews.csv"
OUTPUT_FILE = "data/processed/analyzed_reviews.csv"

REQUIRED_COLUMNS = ["review", "rating", "date", "bank", "source"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    nltk.download("stopwords", quiet=True)
    STOP_WORDS = set(stopwords.words("english"))
except Exception as e:
    logging.error(f"Failed to load stopwords: {e}")
    STOP_WORDS = set()


THEME_KEYWORDS = {
    "Account Access Issues": [
        "login", "log in", "password", "otp", "pin",
        "authentication", "verify", "verification",
        "access", "sign in", "cannot login", "can't login",
        "locked", "account"
    ],
    "Transaction Performance": [
        "transfer", "transaction", "payment", "send",
        "receive", "slow", "loading", "delay",
        "withdraw", "deposit", "transfer failed",
        "takes time", "loading forever", "network"
    ],
    "App Reliability": [
        "crash", "crashes", "error", "bug",
        "failed", "problem", "issue",
        "not working", "freeze", "stuck",
        "broken", "open", "stopped"
    ],
    "User Interface & Experience": [
        "easy", "simple", "ui", "interface",
        "design", "user friendly", "good",
        "great", "nice", "smooth",
        "amazing", "excellent", "best",
        "friendly", "fast", "love"
    ],
    "Customer Support": [
        "support", "service", "help",
        "customer", "response",
        "complaint", "staff", "branch",
        "contact", "care"
    ],
    "Feature Requests": [
        "fingerprint", "budget", "statement",
        "update", "feature", "notification",
        "balance", "dark mode", "language",
        "history", "face id", "new feature"
    ],
}


def validate_dataframe(df, required_columns):
    if df.empty:
        raise ValueError("Input DataFrame is empty.")

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = [
        word for word in text.split()
        if word not in STOP_WORDS and len(word) > 2
    ]

    return " ".join(tokens)


def classify_sentiment(review, sentiment_pipeline):
    try:
        result = sentiment_pipeline(str(review)[:512])[0]

        label = result["label"].lower()
        score = result["score"]

        if score < 0.60:
            sentiment_label = "neutral"
        elif label == "positive":
            sentiment_label = "positive"
        else:
            sentiment_label = "negative"

        return sentiment_label, round(score, 4)

    except Exception as e:
        logging.error(f"Sentiment classification failed: {e}")
        return "neutral", 0.0


def assign_theme(cleaned_review):
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in cleaned_review:
                return theme

    return "Other"


def extract_tfidf_keywords(df, top_n=15):
    bank_keywords = {}

    try:
        vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words="english"
        )

        for bank in df["bank"].dropna().unique():
            bank_reviews = df[df["bank"] == bank]["cleaned_review"].dropna()

            if bank_reviews.empty:
                logging.warning(f"No reviews found for bank: {bank}")
                continue

            tfidf_matrix = vectorizer.fit_transform(bank_reviews)
            feature_names = vectorizer.get_feature_names_out()

            scores = tfidf_matrix.sum(axis=0).A1
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores = sorted(
                keyword_scores,
                key=lambda x: x[1],
                reverse=True
            )

            bank_keywords[bank] = keyword_scores[:top_n]

    except Exception as e:
        logging.error(f"TF-IDF keyword extraction failed: {e}")

    return bank_keywords


def load_sentiment_model():
    try:
        logging.info("Loading DistilBERT sentiment model...")

        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

        logging.info("Sentiment model loaded successfully.")
        return sentiment_pipeline

    except Exception as e:
        logging.error(f"Failed to load sentiment model: {e}")
        raise


def main():
    try:
        df = pd.read_csv(INPUT_FILE)
        logging.info(f"Loaded reviews dataset with shape: {df.shape}")

        validate_dataframe(df, REQUIRED_COLUMNS)

        df = df.reset_index().rename(columns={"index": "review_id"})

        df["cleaned_review"] = df["review"].apply(clean_text)

        sentiment_pipeline = load_sentiment_model()

        sentiment_results = df["review"].apply(
            lambda review: classify_sentiment(review, sentiment_pipeline)
        )

        df["sentiment_label"] = sentiment_results.apply(lambda x: x[0])
        df["sentiment_score"] = sentiment_results.apply(lambda x: x[1])

        df["identified_theme"] = df["cleaned_review"].apply(assign_theme)

        final_df = df[
            [
                "review_id",
                "review",
                "rating",
                "date",
                "bank",
                "source",
                "sentiment_label",
                "sentiment_score",
                "identified_theme",
            ]
        ]

        final_df = final_df.rename(columns={"review": "review_text"})

        final_df.to_csv(OUTPUT_FILE, index=False)
        logging.info(f"Saved analyzed reviews to: {OUTPUT_FILE}")

        logging.info("Sentiment by bank:")
        logging.info(final_df.groupby(["bank", "sentiment_label"]).size())

        logging.info("Average sentiment confidence by bank and rating:")
        logging.info(
            final_df.groupby(["bank", "rating"])["sentiment_score"].mean()
        )

        logging.info("Theme counts by bank:")
        logging.info(final_df.groupby(["bank", "identified_theme"]).size())

        keywords = extract_tfidf_keywords(df)

        logging.info("Top TF-IDF keywords by bank:")
        for bank, words in keywords.items():
            logging.info(f"{bank}: {words}")

    except FileNotFoundError:
        logging.error(f"Input file not found: {INPUT_FILE}")

    except ValueError as ve:
        logging.error(f"Validation error: {ve}")

    except Exception as e:
        logging.error(f"Unexpected error in analysis pipeline: {e}")


if __name__ == "__main__":
    main()