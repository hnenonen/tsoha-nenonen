from db import db
import users

def get_task(id):
    sql = "SELECT taskname FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_status(id):
    sql = "SELECT task_state FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_worker(id):
    sql = "SELECT worker_id FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_worktime(id):
    sql = "SELECT work_time FROM tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()[0]

def get_list():
    sql = "SELECT T.id, T.taskname, T.task_state, T.content, T.time, T.worker_id, T.work_time, U.username FROM tasks T, users U WHERE T.user_id = U.id AND T.task_state!='DONE' ORDER BY T.id DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_archive():
    sql = "SELECT T.id, T.taskname, T.task_state, T.content, T.time, T.worker_id, T.work_time, U.username FROM tasks T, users U WHERE T.user_id = U.id AND T.task_state='DONE' ORDER BY T.id DESC"
    result = db.session.execute(sql)
    return result.fetchall()

def get_task_count(task_state):
    sql = "SELECT COUNT(*) FROM tasks T WHERE T.task_state=:task_state"
    result = db.session.execute(sql, {"task_state":task_state})
    return result.fetchone()[0]

def send(taskname, content, work_time):
    task_state = "TODO"
    user_id = users.user_id()
    worker_id = user_id
    if user_id == 0:
        return False
    sql = "INSERT INTO tasks (taskname, content, task_state, user_id, time, worker_id, work_time) VALUES (:taskname, :content, :task_state, :user_id, NOW(), :worker_id, :work_time) RETURNING id"
    result = db.session.execute(sql, {"taskname":taskname, "content":content, "task_state": task_state, "user_id":user_id, "worker_id":worker_id, "work_time":work_time})
    task_id = result.fetchone()[0]
    db.session.commit()
    return True

def update_task(id, taskname, content, task_state, work_time):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "UPDATE tasks SET taskname=:taskname, content=:content, task_state=:task_state, user_id=:user_id, time=NOW(), work_time=:work_time WHERE id=:id"
    result = db.session.execute(sql, {"taskname":taskname, "content":content, "task_state": task_state, "user_id":user_id, "id":id, "work_time":work_time})
    db.session.commit()
    return True

def take_task(id):
    user_id = users.user_id()
    worker_id = get_worker(id)
    if user_id == 0:
        return False
    if (get_status(id) == "TODO") | (user_id == worker_id):
        if get_status(id) == "TODO":
            sql = "UPDATE tasks SET task_state='WORKING', worker_id=:worker_id WHERE id=:id"
        elif get_status(id) == "WORKING":
            sql = "UPDATE tasks SET task_state='DONE', worker_id=:worker_id WHERE id=:id"
        result = db.session.execute(sql, {"worker_id":worker_id, "id": id})
        db.session.commit()
        return True
    else:
        return False

def mytasks():
    worker_id = users.user_id()
    if worker_id == 0:
        return False
    sql = "SELECT T.id, T.taskname, T.task_state, T.content, U.username FROM tasks T, users U WHERE T.worker_id=:worker_id AND T.worker_id = U.id AND T.task_state = 'WORKING' ORDER BY T.id"
    result = db.session.execute(sql, {"worker_id": worker_id})
    return result.fetchall()

