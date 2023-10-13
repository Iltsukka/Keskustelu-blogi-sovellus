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
    time_of TIMESTAMP,
    visible BOOLEAN
    
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content TEXT,
    username TEXT,
    date_of TIMESTAMP,
    blog_id INTEGER REFERENCES blogs
);

CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    questions TEXT,
    created_at TIMESTAMP,
    username TEXT
);

CREATE TABLE options (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls,
    option TEXT
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    options_id INTEGER REFERENCES options,
    made_at TIMESTAMP
)