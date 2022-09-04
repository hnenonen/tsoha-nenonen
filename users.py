import secrets
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if  check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password, admin):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, admin) VALUES (:username,:password, :admin)"
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
    except:
        return False
    return login(username, password)

def get_username(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]


def user_id():
    return session.get("user_id",0)

def get_list(user_id):
    sql = "SELECT DISTINCT UI.name, TI.teamname, T.user_id FROM teams T, user_info UI, team_info TI WHERE TI.id = T.team_id AND UI.user_id = T.user_id AND T.team_id IN (SELECT T.team_id FROM teams T WHERE T.user_id=:user_id) ORDER BY TI.teamname"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def count_all():
    sql = "SELECT COUNT(*) FROM users"
    result = db.session.execute(sql)
    return result.fetchone()[0]