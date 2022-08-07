from db import db
import users, tasks

def get_list():
    sql = "SELECT C.comment, U.username FROM users U, C comments WHERE T.id_id=C.id ORDER BY T.id"
    result = db.session.execute(sql)
    return result.fetchall()

def send(comment):
    user_id = users.user_id()
    task_id = tasks.task_id()
    if user_id or task_id == 0:
        return False
    sql = "INSERT INTO comments (task_id, comment, user_id) VALUES (:task_id, :comment, :user_id)"
    db.session.execute(sql, {"task_id":task_id, "comment":comment, "user_id":user_id})
    db.session.commit()
    return True
