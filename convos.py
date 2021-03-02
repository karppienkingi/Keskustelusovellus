from db import db
from flask import session

def create_convo(topic, area_id, starter_id):
    sql = "INSERT INTO topics(topic, starter_id, area_id, created_at) \
        VALUES (:topic, :starter_id, :area_id, NOW()) RETURNING id"
    result = db.session.execute(sql, {"topic":topic, "starter_id":starter_id, "area_id":area_id})
    topic_id = result.fetchone()[0]
    db.session.commit()
    return topic_id

def send_message(message, starter_id, topic_id, visibility):
    sql = "INSERT INTO messages(message, sender_id, topic_id, visibility, sent_at) \
            VALUES (:message, :sender_id, :topic_id, :visibility, NOW())"
    db.session.execute(sql, {"message":message, "sender_id":starter_id, "topic_id":topic_id, "visibility":1})
    db.session.commit()

def delete_message(message_id):
    sql = "UPDATE messages SET visibility=0 WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    db.session.commit()

def update_message(message, id):
    sql = "UPDATE messages SET message=:message WHERE id=:id"
    db.session.execute(sql, {"message":message, "id":id})
    db.session.commit()

def search(visibility, word):
    sql = "SELECT messages.message, users.username, topics.id FROM messages, users, topics \
        WHERE visibility=:visibility AND messages.sender_id=users.id AND topics.id=messages.topic_id \
            AND messages.message LIKE :word"
    result = db.session.execute(sql, {"visibility":visibility, "word":"%"+word+"%"})
    messages = result.fetchall()
    return messages
