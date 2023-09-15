CREATE TABLE testi (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE blogs (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    username TEXT,
    time_of TIMESTAMP
    
);