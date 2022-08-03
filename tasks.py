from db import db
import users

def get_list():
    sql = "SELECT T.taskname, T.content, U.username FROM tasks T, users U WHERE T.user_id=U.id ORDER BY T.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(taskname, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO tasks (taskname, content, user_id) VALUES (:taskname, :content, :user_id)"
    db.session.execute(sql, {"taskname":taskname, "content":content, "user_id":user_id})
    db.session.commit()
    return True
