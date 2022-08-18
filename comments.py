from db import db
import tasks, users

def get_list(task_id):
    sql = "SELECT DISTINCT C.comment, U.username FROM comments C, tasks T, users U WHERE C.task_id=:task_id AND U.id = C.user_id"
    result = db.session.execute(sql, {"task_id": task_id})
    return result.fetchall()

def comment(task_id, comment):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO comments (task_id, comment, user_id) VALUES (:task_id, :comment, :user_id)"
    result = db.session.execute(sql, {"task_id": task_id, "comment":comment, "user_id":user_id})
    db.session.commit()
    return True
