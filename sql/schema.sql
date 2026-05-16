DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS banks;

CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(150) NOT NULL
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    bank_id INTEGER NOT NULL,
    review_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score NUMERIC(6, 4),
    identified_theme VARCHAR(100),
    source VARCHAR(50) NOT NULL,
    FOREIGN KEY (bank_id) REFERENCES banks(bank_id)
);