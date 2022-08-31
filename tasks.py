from db import db
import users

def get_task(id):
    sql = "SELECT taskname FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_list():
    sql = "SELECT T.id, T.taskname, T.task_state, T.content, T.time, U.username FROM tasks T, users U WHERE T.user_id = U.id ORDER BY T.id DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def send(taskname, content):
    task_state = "TODO"
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO tasks (taskname, content, task_state, user_id, time) VALUES (:taskname, :content, :task_state, :user_id, NOW()) RETURNING id"
    result = db.session.execute(sql, {"taskname":taskname, "content":content, "task_state": task_state, "user_id":user_id})
    task_id = result.fetchone()[0]
    db.session.commit()
    return True

def take_task(id):
    worker_id = users.user_id()
    if worker_id == 0:
        return False
    if get_state(id) == "TODO":
        sql = "UPDATE tasks SET task_state='WORKING', worker_id=:worker_id WHERE id=:id"
    elif get_state(id) == "WORKING":
        sql = "UPDATE tasks SET task_state='DONE', worker_id=:worker_id WHERE id=:id"
    result = db.session.execute(sql, {"worker_id":worker_id, "id": id})
    db.session.commit()
    return True

def get_state(id):
    sql = "SELECT task_state FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id": id})
    return result.fetchone()[0]

def mytasks():
    worker_id = users.user_id()
    if worker_id == 0:
        return False
    sql = "SELECT T.id, T.taskname, T.task_state, T.content, U.username FROM tasks T, users U WHERE T.worker_id=:worker_id AND T.worker_id = U.id AND T.task_state = 'WORKING' ORDER BY T.id"
    result = db.session.execute(sql, {"worker_id": worker_id})
    return result.fetchall()

