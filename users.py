from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0], password):
            session["user_id"] = user[1]
            return True
        else:
            return False

def register(username, password, admin):
    if username == None or password == "":
        return False

    hash_value = generate_password_hash(password)
    if admin == None:
        admin = 0

    try: 
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, :admin)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()            
    except:
        return False
    return login(username, password)



def user_id():
    return session.get("user_id", 0)


def logout():
    del session["user_id"]

def admin():
    if user_id()==0:
        return False
    id = user_id()
    sql = "SELECT admin FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    admin = result.fetchone()[0]
    return admin == 1

def check_rights(user_id, area_id):
    sql = "SELECT user_id FROM accessrights WHERE user_id=:user_id AND area_id=:area_id"
    result = db.session.execute(sql, {"user_id":user_id, "area_id":area_id})
    rights = result.fetchone()
    print(rights)
    if rights == None:
        return False
    else:
        return True
