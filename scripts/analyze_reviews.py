import re
import pandas as pd
import nltk

from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer


nltk.download("stopwords")
from nltk.corpus import stopwords


INPUT_FILE = "data/processed/clean_reviews.csv"
OUTPUT_FILE = "data/processed/analyzed_reviews.csv"


STOP_WORDS = set(stopwords.words("english"))


# THEME_KEYWORDS = {
#     "Account Access Issues": [
#         "login", "password", "otp", "pin", "authentication", "verify", "verification", "access"
#     ],
#     "Transaction Performance": [
#         "transfer", "transaction", "payment", "send", "receive", "slow", "loading", "delay"
#     ],
#     "App Reliability": [
#         "crash", "error", "bug", "failed", "problem", "issue", "not working", "freeze"
#     ],
#     "User Interface & Experience": [
#         "easy", "simple", "ui", "interface", "design", "user friendly", "fast", "good"
#     ],
#     "Customer Support": [
#         "support", "service", "help", "customer", "response", "complaint"
#     ],
#     "Feature Requests": [
#         "fingerprint", "budget", "statement", "update", "feature", "notification", "balance"
#     ],
# }

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


def clean_text(text):
    """Clean review text for keyword and theme analysis."""
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    tokens = [
        word for word in text.split()
        if word not in STOP_WORDS and len(word) > 2
    ]

    return " ".join(tokens)


def classify_sentiment(review, sentiment_pipeline):
    """
    Classify sentiment using DistilBERT.
    Adds neutral logic when confidence is low.
    """
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


def assign_theme(cleaned_review):
    """Assign business theme based on keyword matching."""
    for theme, keywords in THEME_KEYWORDS.items():
        for keyword in keywords:
            if keyword in cleaned_review:
                return theme

    return "Other"


def extract_tfidf_keywords(df, top_n=15):
    """Extract top TF-IDF keywords and bigrams per bank."""
    bank_keywords = {}

    vectorizer = TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 2),
        stop_words="english"
    )

    for bank in df["bank"].unique():
        bank_reviews = df[df["bank"] == bank]["cleaned_review"]

        tfidf_matrix = vectorizer.fit_transform(bank_reviews)
        feature_names = vectorizer.get_feature_names_out()

        scores = tfidf_matrix.sum(axis=0).A1
        keyword_scores = list(zip(feature_names, scores))
        keyword_scores = sorted(keyword_scores, key=lambda x: x[1], reverse=True)

        bank_keywords[bank] = keyword_scores[:top_n]

    return bank_keywords


def main():
    df = pd.read_csv(INPUT_FILE)

    df = df.reset_index().rename(columns={"index": "review_id"})

    print("Loaded reviews:", df.shape)

    df["cleaned_review"] = df["review"].apply(clean_text)

    print("Loading DistilBERT sentiment model...")
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )

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

    print("Saved analyzed reviews to:", OUTPUT_FILE)
    print("\nSentiment by bank:")
    print(final_df.groupby(["bank", "sentiment_label"]).size())

    print("\nAverage sentiment confidence by bank and rating:")
    print(final_df.groupby(["bank", "rating"])["sentiment_score"].mean())

    print("\nTheme counts by bank:")
    print(final_df.groupby(["bank", "identified_theme"]).size())

    print("\nTop TF-IDF keywords by bank:")
    keywords = extract_tfidf_keywords(df)

    for bank, words in keywords.items():
        print(f"\n{bank}")
        for word, score in words:
            print(f"{word}: {score:.2f}")


if __name__ == "__main__":
    main()