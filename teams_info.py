from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import users

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if  check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(teamname, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO team_info (teamname, password) VALUES (:teamname, :password)"
        db.session.execute(sql, {"teamname":teamname, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True

def user_id():
    return session.get("user_id",0)

def get_list():
    sql = "SELECT id, teamname FROM team_info"
    result = db.session.execute(sql)
    return result.fetchall()

def join_team(team_id):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO teams (user_id, team_id) VALUES (:user_id, :team_id)"
    result = db.session.execute(sql, {"user_id":user_id, "team_id":team_id})
    db.session.commit() 
    return True

#    user = result.fetchone()
#    if not user:
#        return False
#    else:
#        if  check_password_hash(user.password, password):
#            session["user_id"] = user.id
#            return True
#        else:
#            return False
#
