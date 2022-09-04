from asyncio import format_helpers
from db import db
from app import app
from flask import render_template, request, redirect, session, abort
import users, tasks, teams_info, comments, profiles

@app.route("/")
def index():
    user_id = users.user_id()
    task_list = tasks.get_tasks_in_same_teams(user_id)
    work_done = tasks.get_total_worktime_done(user_id)
    tasks_done = tasks.get_total_tasks_done(user_id)
    count_todo = tasks.get_task_count('TODO')
    count_working = tasks.get_task_count('WORKING')
    most_hours_user = tasks.most_hours_user()
    most_hours_hours = tasks.most_hours_hours()
    most_tasks_user = tasks.most_tasks_done_user()
    most_tasks_count = tasks.most_tasks_done_count()
    return render_template("index.html", most_hours_hours=most_hours_hours, count_todo=count_todo, count_working=count_working, tasks=task_list, user_id=user_id, work_done=work_done, tasks_done=tasks_done, most_tasks_user=most_tasks_user, most_hours_user=most_hours_user, most_tasks_count=most_tasks_count)

@app.route("/archive")
def archive():
    task_list = tasks.get_archive()
    user_id = users.user_id()
    return render_template("archive.html", count=len(task_list), tasks=task_list, user_id=user_id)

@app.route("/comment/<int:id>", methods=["POST"])
def comment(id):
    if session["csrf_token"] != request.form["csrf_token"]:abort(403)
    comment = request.form["comment"]
    if len(comment) == 0: return render_template("error.html", message="Syötteissä virhe")

    if comments.comment(id, comment):
        topic = tasks.get_task(id)
        comment_list = comments.get_list(id)
        return render_template("task.html", id=id, topic=topic, comments=comment_list)
    else:
        return render_template("error.html", message="Kommentin lähetys ei onnistunut")

@app.route("/mytasks")
def mytasks():
    #add check that user is logged in
    task_list = tasks.mytasks()
    return render_template("mytasks.html", tasks=task_list)

@app.route("/task/<int:id>", methods=["GET", "POST"])
def task(id):
    topic = tasks.get_task(id)
    status = tasks.get_status(id)
    comment_list = comments.get_list(id)
    work_time = tasks.get_worktime(id)
    message = "Take task"
    if status == "WORKING":
        message = "Mark_done"
    return render_template("task.html", id=id, topic=topic, status=status, message=message, comments=comment_list, work_time=work_time)

@app.route("/update_task/<int:id>", methods=["POST"])
def update_task(id):
    return render_template("update_task.html", id=id) 

@app.route("/send_update_task/<int:id>", methods=["POST"])
def send_update_task(id):
    if session["csrf_token"] != request.form["csrf_token"]:abort(403)
    taskname = request.form["taskname"]
    content = request.form["content"]
    task_state = request.form["task_state"]
    work_time = request.form["work_time"]

    if len(taskname) == 0: return render_template("error.html", message="Syötteissä virhe")
    if len(content) == 0: return render_template("error.html", message="Syötteissä virhe")
    if len(work_time) == 0: return render_template("error.html", message="Syötteissä virhe")

    if tasks.update_task(id, taskname, content, task_state, work_time):
        return redirect("/")
    else:
        return render_template("error.html", message="Tehtävän päivitys ei onnistunut")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if session["csrf_token"] != request.form["csrf_token"]:abort(403)
    if tasks.take_task(id):
        topic = tasks.get_task(id)
        status = tasks.get_status(id)
        comment_list = comments.get_list(id)
        work_time = tasks.get_worktime(id)
        message = ""
        if status == "TODO":
            message = "Take_task"
        if status == "WORKING":
            message = "Mark_done"
        return render_template("task.html", id=id, topic=topic, status=status, message=message, comments=comment_list, work_time=work_time)
    else:
        return render_template("error.html", message="Tehtävän ottaminen ei onnistunut")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    if session["csrf_token"] != request.form["csrf_token"]:abort(403)
    taskname = request.form["taskname"]
    content = request.form["content"]
    work_time = request.form["work_time"]

    if len(taskname) == 0: return render_template("error.html", message="Syötteissä virhe")
    if len(content) == 0: return render_template("error.html", message="Syötteissä virhe")
    if len(work_time) == 0: return render_template("error.html", message="Syötteissä virhe")

    if tasks.send(taskname, content, work_time):
        return redirect("/")
    else:
        return render_template("error.html", message="Tehtävän lähetys ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        admin = request.form["admin"]
        name = request.form["name"]
        age = request.form["age"]
        motto = request.form["motto"]
        content = request.form["content"]

        if len(username) == 0: return render_template("error.html", message="Syötteissä virhe")
        if len(password1) == 0: return render_template("error.html", message="Syötteissä virhe")
        if len(name) == 0: return render_template("error.html", message="Syötteissä virhe")
        if len(age) == 0: return render_template("error.html", message="Syötteissä virhe")
        if len(motto) == 0: return render_template("error.html", message="Syötteissä virhe")
        if len(content) == 0: return render_template("error.html", message="Syötteissä virhe")


        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1, admin):
            user_id = users.user_id()
            profiles.create(user_id, name, age, motto, content)
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/newteam", methods=["GET", "POST"])
def newteam():
    if request.method == "GET":
        return render_template("newteam.html")
    if request.method == "POST":
        teamname = request.form["teamname"]
        if teams_info.register(teamname):
            teams = teams_info.get_list()
            return render_template("teams.html", teams=teams)


@app.route("/teams")
def teams():
    teams = teams_info.get_list()
    return render_template("teams.html", teams=teams)

@app.route("/jointeam/<int:id>", methods=["GET", "POST"])
def jointeam(id):
    if teams_info.join_team(id):
        return redirect("/")
    else:
        return render_template("error.html", message="Tiimin liittyminen ei onnistunut")

@app.route("/profile/<int:id>", methods=["GET", "POST"])
def profile(id):
    name = profiles.get_name(id)
    age = profiles.get_age(id)
    motto = profiles.get_motto(id)
    content = profiles.get_content(id)
    updated = profiles.get_updated(id)
    return render_template("profile.html", id=id, name=name, age=age, motto=motto, content=content, updated=updated)

@app.route("/update_profile/<int:id>", methods=["POST"])
def update_profile(id):
    user_id = users.user_id()
    show = False
    if id == user_id:
        show = True
    return render_template("update_profile.html", id=id, show=show) 

@app.route("/send_update_profile/<int:id>", methods=["POST"])
def send_update_profile(id):
    name = request.form["name"]
    age = request.form["age"]
    motto = request.form["motto"]
    content = request.form["content"]

    if len(name) == 0: return render_template("error.html", message="Syötteissä virhe")
    if len(age) == 0: return render_template("error.html", message="Syötteissä virhe")
    if len(motto) == 0: return render_template("error.html", message="Syötteissä virhe")
    if len(content) == 0: return render_template("error.html", message="Syötteissä virhe")

    if profiles.update_profile(id, name, age, motto, content):
        updated = profiles.get_updated(id)
        return render_template("profile.html", id=id, name=name, age=age, motto=motto, content=content, updated=updated)
    else:
        return render_template("error.html", message="Profiilin päivitys ei onnistunut")

@app.route("/userlist")
def userlist():
    user_id = users.user_id()
    user_list = users.get_list(user_id)
    count_all = users.count_all()
    return render_template("users.html", count=len(user_list), users=user_list, count_all=count_all)
