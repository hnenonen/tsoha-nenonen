from db import db
import users

def create(user_id, name, age, motto, content):
    if user_id == 0:
        return False
    try:
        sql = "INSERT INTO user_info (user_id, name, age, motto, content, updated) VALUES (:user_id, :name, :age, :motto, :content, NOW())"
        db.session.execute(sql, {"user_id":user_id, "name":name, "age":age, "motto":motto, "content":content})
        db.session.commit()
    except:
        return False
    return True

def get_name(user_id):
    sql = "SELECT name FROM user_info WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def get_age(user_id):
    sql = "SELECT age FROM user_info WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def get_motto(user_id):
    sql = "SELECT motto FROM user_info WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def get_content(user_id):
    sql = "SELECT content FROM user_info WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def get_updated(user_id):
    sql = "SELECT updated FROM user_info WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def get_info(user_id):
    sql = "SELECT name, age, motto, content, updated FROM user_info WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]

def update_profile(user_id, name, age, motto, content):
    sql = "UPDATE user_info SET user_id=:user_id, name=:name, age=:age, motto=:motto, content=:content, updated=NOW() WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id, "name":name, "age":age, "motto":motto, "content":content})
    db.session.commit()
    return True


def check_validity():
    user_id = users.user_id()
    sql = "SELECT id FROM user_info WHERE user_id=:user_id"
    result = db.session.execute(sql, {"user_id":user_id})
    if result is None:
        return True


