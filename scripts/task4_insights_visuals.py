import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


DATA_PATH = "data/processed/analyzed_reviews.csv"
FIG_DIR = Path("reports/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)


# 1. Sentiment distribution by bank
sentiment_counts = (
    df.groupby(["bank", "sentiment_label"])
    .size()
    .unstack(fill_value=0)
)

sentiment_counts.plot(kind="bar", figsize=(9, 5))
plt.title("Sentiment Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(FIG_DIR / "task4_sentiment_distribution_by_bank.png")
plt.close()


# 2. Average rating by bank
avg_rating = df.groupby("bank")["rating"].mean().sort_values()

avg_rating.plot(kind="bar", figsize=(8, 5))
plt.title("Average Rating by Bank")
plt.xlabel("Bank")
plt.ylabel("Average Rating")
plt.ylim(0, 5)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(FIG_DIR / "task4_average_rating_by_bank.png")
plt.close()


# 3. Theme frequency by bank
theme_counts = (
    df.groupby(["bank", "identified_theme"])
    .size()
    .unstack(fill_value=0)
)

theme_counts.plot(kind="bar", figsize=(11, 6))
plt.title("Theme Frequency by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=15)
plt.legend(title="Theme", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(FIG_DIR / "task4_theme_frequency_by_bank.png")
plt.close()


# 4. Rating distribution by bank
rating_counts = (
    df.groupby(["bank", "rating"])
    .size()
    .unstack(fill_value=0)
)

rating_counts.plot(kind="bar", figsize=(9, 5))
plt.title("Rating Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(FIG_DIR / "task4_rating_distribution_by_bank.png")
plt.close()


# 5. Sentiment trend over time
df["date"] = pd.to_datetime(df["date"], errors="coerce")
trend = (
    df.dropna(subset=["date"])
    .groupby([pd.Grouper(key="date", freq="ME"), "sentiment_label"])
    .size()
    .unstack(fill_value=0)
)

trend.plot(figsize=(10, 5))
plt.title("Monthly Sentiment Trend")
plt.xlabel("Review Month")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig(FIG_DIR / "task4_monthly_sentiment_trend.png")
plt.close()


# Summary tables
print("\nAverage rating by bank")
print(df.groupby("bank")["rating"].mean().round(2))

print("\nSentiment counts by bank")
print(sentiment_counts)

print("\nTheme counts by bank")
print(theme_counts)

print("\nTop theme per bank")
print(df.groupby("bank")["identified_theme"].agg(lambda x: x.value_counts().index[0]))

print("\nVisualizations saved in reports/figures/")