from db import db
from app import app
from flask import render_template, request, redirect
import users, tasks, teams_info, comments, profiles

@app.route("/")
def index():
    task_list = tasks.get_list()
    return render_template("index.html", count=len(task_list), tasks=task_list)

@app.route("/comment/<int:id>", methods=["POST"])
def comment(id):
    comment = request.form["comment"]
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
    comment_list = comments.get_list(id)
    return render_template("task.html", id=id, topic=topic, comments=comment_list)

@app.route("/update_task/<int:id>", methods=["POST"])
def update_task(id):
    return render_template("update_task.html", id=id) 

@app.route("/send_update_task/<int:id>", methods=["POST"])
def send_update_task(id):
    taskname = request.form["taskname"]
    content = request.form["content"]
    task_state = request.form["task_state"]
    if tasks.update_task(id, taskname, content, task_state):
        return redirect("/")
    else:
        return render_template("error.html", message="Tehtävän päivitys ei onnistunut")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if tasks.take_task(id):
        topic = tasks.get_task(id)
        comment_list = comments.get_list(id)
        return render_template("task.html", id=id, topic=topic, comments=comment_list)
    else:
        return render_template("error.html", message="Tehtävän ottaminen ei onnistunut")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/send", methods=["POST"])
def send():
    taskname = request.form["taskname"]
    content = request.form["content"]
    if tasks.send(taskname, content):
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
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/newteam", methods=["GET", "POST"])
def newteam():
    if request.method == "GET":
        return render_template("newteam.html")
    if request.method == "POST":
        teamname = request.form["teamname"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if teams_info.register(teamname, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Uuden tiimin lisääminen ei onnistunut")


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

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        motto = request.form["motto"]
        content = request.form["content"]
        if profiles.modify(name, age, motto, content):
            return redirect("/")
        else:
            return render_template("error.html", message="Profiilin päivittäminen ei onnistunut")
