import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("data/processed/analyzed_reviews.csv")


# 1. Sentiment distribution by bank
sentiment_counts = (
    df.groupby(["bank", "sentiment_label"])
    .size()
    .unstack(fill_value=0)
)

plt.figure(figsize=(8, 5))
sentiment_counts.plot(kind="bar")
plt.title("Sentiment Distribution by Bank")
plt.xlabel("Bank")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("sentiment_distribution_by_bank.png")
plt.close()


# 2. Rating distribution by bank
plt.figure(figsize=(8, 5))

for bank in df["bank"].unique():
    bank_ratings = df[df["bank"] == bank]["rating"]
    plt.hist(bank_ratings, alpha=0.6, label=bank)

plt.title("Rating Distribution by Bank")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("rating_distribution_by_bank.png")
plt.close()


# 3. Theme frequency
theme_counts = (
    df.groupby(["bank", "identified_theme"])
    .size()
    .unstack(fill_value=0)
)

theme_counts.T.plot(kind="bar", figsize=(10, 6))
plt.title("Theme Frequency by Bank")
plt.xlabel("Theme")
plt.ylabel("Number of Reviews")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("theme_frequency_by_bank.png")
plt.close()

print("Task 2 visualizations saved successfully.")