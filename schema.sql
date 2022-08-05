CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    taskname TEXT,
    content TEXT,
    task_state TEXT,
    user_id INTEGER REFERENCES users
);
