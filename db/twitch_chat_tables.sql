CREATE TABLE IF NOT EXISTS chat_logs (
    comment_id SERIAL PRIMARY KEY, 
    channel VARCHAR(100) NOT NULL, 
    username VARCHAR(100) NOT NULL, 
    date_time TIMESTAMP NOT NULL, 
    comment VARCHAR(500) NOT NULL, 
    sentiment VARCHAR(255) DEFAULT NULL, 
    labeler VARCHAR(100) DEFAULT NULL, 
    receiver VARCHAR(100) DEFAULT NULL);

CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY, 
    username VARCHAR(100) NOT NULL, 
    comment_count INTEGER DEFAULT 0, 
    label_count INTEGER DEFAULT 0);

CREATE TABLE IF NOT EXISTS inputs (
    comment_id SERIAL PRIMARY KEY, 
    username VARCHAR(255) NOT NULL);

CREATE TABLE IF NOT EXISTS features (
    comment_id SERIAL PRIMARY KEY, 
    username VARCHAR(255) NOT NULL);