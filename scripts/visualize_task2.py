import pandas as pd
import matplotlib.pyplot as plt
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_dataframe(df, required_columns):
    """Validate DataFrame before processing."""

    if df.empty:
        raise ValueError("DataFrame is empty.")

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


try:
    # Load data
    df = pd.read_csv(
        "data/processed/analyzed_reviews.csv"
    )

    logging.info(
        "Dataset loaded successfully."
    )

    # Validate dataset
    required_columns = [
        "bank",
        "sentiment_label",
        "rating",
        "identified_theme"
    ]

    validate_dataframe(
        df,
        required_columns
    )

    # Create output folder
    os.makedirs(
        "visualizations",
        exist_ok=True
    )

    # 1. Sentiment distribution by bank
    sentiment_counts = (
        df.groupby(
            ["bank", "sentiment_label"]
        )
        .size()
        .unstack(fill_value=0)
    )

    sentiment_counts.plot(
        kind="bar",
        figsize=(8, 5)
    )

    plt.title(
        "Sentiment Distribution by Bank"
    )
    plt.xlabel("Bank")
    plt.ylabel(
        "Number of Reviews"
    )
    plt.xticks(rotation=15)
    plt.tight_layout()

    plt.savefig(
        "visualizations/sentiment_distribution_by_bank.png"
    )
    plt.close()

    logging.info(
        "Sentiment visualization saved."
    )

    # 2. Rating distribution by bank
    plt.figure(figsize=(8, 5))

    for bank in df["bank"].unique():
        bank_ratings = df[
            df["bank"] == bank
        ]["rating"]

        plt.hist(
            bank_ratings,
            alpha=0.6,
            label=bank
        )

    plt.title(
        "Rating Distribution by Bank"
    )
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "visualizations/rating_distribution_by_bank.png"
    )
    plt.close()

    logging.info(
        "Rating distribution saved."
    )

    # 3. Theme frequency
    theme_counts = (
        df.groupby(
            ["bank", "identified_theme"]
        )
        .size()
        .unstack(fill_value=0)
    )

    theme_counts.T.plot(
        kind="bar",
        figsize=(10, 6)
    )

    plt.title(
        "Theme Frequency by Bank"
    )
    plt.xlabel("Theme")
    plt.ylabel(
        "Number of Reviews"
    )
    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig(
        "visualizations/theme_frequency_by_bank.png"
    )
    plt.close()

    logging.info(
        "Theme visualization saved."
    )

    logging.info(
        "Task 2 visualizations completed successfully."
    )

except FileNotFoundError:
    logging.error(
        "Input CSV file not found."
    )

except ValueError as ve:
    logging.error(
        f"Validation error: {ve}"
    )

except Exception as e:
    logging.error(
        f"Unexpected error: {e}"
    )