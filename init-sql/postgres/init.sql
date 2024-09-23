CREATE SCHEMA bitcoin;

CREATE TABLE bitcoin.coin_market (
    id SERIAL PRIMARY KEY,
    price numeric(10, 2) NOT NULL,
    crawl_at TIMESTAMP NOT NULL
);