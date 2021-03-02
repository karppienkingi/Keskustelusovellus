from db import db
from flask import session

def create_area(name, user_id):
    sql = "INSERT INTO areas(name, user_id) VALUES (:name, :user_id) RETURNING id"
    result = db.session.execute(sql, {"name":name, "user_id":user_id})
    area_id = result.fetchone()[0]
    db.session.commit()
    return area_id

def give_accessrights(area_id, user_id):
    sql = "INSERT INTO accessrights(area_id, user_id) VALUES (:area_id, :user_id)"
    db.session.execute(sql, {"area_id":area_id, "user_id":user_id}) 
    db.session.commit()