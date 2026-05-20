-- init.sql — runs once when the DB container is first created
CREATE TABLE IF NOT EXISTS items (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Seed data for demo
INSERT INTO items (name) VALUES ('Sample Item 1'), ('Sample Item 2');
