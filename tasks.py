from db import db
import users

def most_tasks_done(user_id):
    sql = "SELECT U.username, COUNT(U.username) FROM tasks T, users U WHERE T.task_state='DONE' AND U.id=T.worker_id GROUP BY U.username"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0] 

def most_tasks_done_user():
    sql = "SELECT U.username FROM tasks T, users U WHERE T.task_state='DONE' AND U.id=T.worker_id GROUP BY U.username"
    result = db.session.execute(sql)
    return result.fetchone()[0] 

def most_hours_done_user():
    sql = "SELECT U.username FROM tasks T, users U WHERE T.task_state='DONE' AND U.id=T.worker_id GROUP BY U.username"
    result = db.session.execute(sql)
    return result.fetchone()[0] 

def most_tasks_done_count():
    sql = "SELECT COUNT(U.username) AS count FROM tasks T, users U WHERE T.task_state='DONE' AND U.id=T.worker_id GROUP BY U.username"
    result = db.session.execute(sql)
    return result.fetchone()[0] 

def most_hours_done_count():
    sql = "SELECT SUM(T.work_time) AS hours FROM tasks T, users U WHERE T.task_state='DONE' AND U.id=T.worker_id GROUP BY U.username"
    result = db.session.execute(sql)
    return result.fetchone()[0] 

def get_total_worktime_done(user_id):
    sql = "SELECT SUM(work_time) FROM tasks WHERE user_id=:user_id AND task_state='DONE'"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]  

def get_total_tasks_done(user_id):
    sql = "SELECT COUNT(*) FROM tasks WHERE user_id=:user_id AND task_state='DONE'"
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchone()[0]  

def get_tasks_in_same_teams(user_id):
    sql = "SELECT DISTINCT TA.id, TA.taskname, TA.task_state, TA.content, TA.time, TA.worker_id, TA.work_time FROM tasks TA, users U WHERE TA.user_id IN (SELECT DISTINCT T.user_id FROM teams T WHERE T.team_id IN (SELECT T.team_id FROM teams T WHERE T.user_id=:user_id)) AND TA.task_state!='DONE' AND TA.user_id = U.id;" 
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

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

def get_list(user_id):
    sql = "SELECT T.id, T.taskname, T.task_state, T.content, T.time, T.worker_id, T.work_time, U.username FROM tasks T, users U WHERE T.user_id = U.id AND T.task_state!='DONE' ORDER BY T.id DESC"
    result = db.session.execute(sql, {"user_id":user_id})
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

