CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin INTEGER);
CREATE TABLE areas(id SERIAL PRIMARY KEY, name TEXT, user_id INTEGER REFERENCES users);
CREATE TABLE topics(id SERIAL PRIMARY KEY, topic TEXT, starter_id INTEGER REFERENCES users, area_id INTEGER REFERENCES areas, created_at TIMESTAMP);
CREATE TABLE accessRights(area_id INTEGER REFERENCES areas, user_id INTEGER REFERENCES users);
CREATE TABLE messages(id SERIAL PRIMARY KEY, message TEXT NOT NULL, sender_id INTEGER REFERENCES users, topic_id INTEGER REFERENCES topics, visibility INTEGER, sent_at TIMESTAMP);
INSERT INTO areas (name) VALUES ('Main');
INSERT INTO areas (name) VALUES ('Work&Study');
INSERT INTO areas (name) VALUES ('Coffee');
INSERT INTO areas (name) VALUES ('Eurovision');
INSERT INTO areas (name) VALUES ('Games');