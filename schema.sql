CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin INTEGER
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    taskname TEXT,
    content TEXT,
    work_time INTEGER,
    task_state TEXT,
    user_id INTEGER REFERENCES users,
    worker_id INTEGER REFERENCES users,
    time TIMESTAMP
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks,
    comment TEXT,
    time TIMESTAMP,
    user_id INTEGER REFERENCES users
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    team_id INTEGER REFERENCES team_info
);

CREATE TABLE team_info (
    id SERIAL PRIMARY KEY,
    teamname TEXT UNIQUE,
    password TEXT
);

CREATE TABLE direct_message (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users,
    receiver_id INTEGER REFERENCES users,
    message TEXT,
    time TIMESTAMP
);

CREATE TABLE user_info (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    name TEXT,
    age INTEGER,
    motto TEXT,
    content TEXT,
    updated TIMESTAMP
); 

