from app import app
from flask import render_template, request, redirect, session
import users, convos, areas
from db import db


@app.route("/")
def index():
    sql = "SELECT name, id, user_id FROM areas WHERE user_id IS NULL"
    result = db.session.execute(sql)
    areas = result.fetchall()
    result = db.session.execute("SELECT id, topic, area_id FROM topics ORDER BY id DESC")
    topics = result.fetchall()
    admin = users.admin()  
    user_id = users.user_id()
    sql = "SELECT areas.name, areas.id, areas.user_id FROM areas, accessrights \
        WHERE accessrights.user_id=:user_id AND accessrights.area_id=areas.id"
    result = db.session.execute(sql, {"user_id":user_id})
    private_areas = result.fetchall()
    if private_areas == None:
        private_areas = []
    return render_template("index.html", areas = areas, topics = topics, admin = admin, private_areas = private_areas)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message = "Wrong username or password")


@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = request.form.get("admin")
        if users.register(username, password, admin):
            return redirect("/")
        else:
            return render_template("error.html", message = "Registration was not successful")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/") 

@app.route("/new/<int:id>")
def new(id):
    sql = "SELECT name FROM areas WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    area = result.fetchone()[0] 
    return render_template("new.html", id = id, area = area)

@app.route("/create", methods=["POST"])
def create():
    topic = request.form["topic"]
    if topic == "":
        return render_template("error.html", message = "You have to have a topic on your conversation")
    area_id = request.form["id"]
    starter_id = users.user_id()
    topic_id = convos.create_convo(topic, area_id, starter_id)
    message = request.form["message"]
    if message != "":
        convos.send_message(message, starter_id, topic_id, 1)
    return redirect("/")

@app.route("/convo/<int:id>")
def convo(id):
    sql = "SELECT id, topic FROM topics WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic = result.fetchone()
    if topic == None:
        return render_template("error.html", message="There is no conversation here yet")
    visibility = 1
    sql = "SELECT messages.id, messages.message, users.username, users.id \
        FROM messages, users WHERE messages.topic_id=:id AND visibility=:visibility \
            AND messages.sender_id=users.id"
    result = db.session.execute(sql, {"id":id, "visibility":visibility})
    messages = result.fetchall()
    return render_template("convo.html", topic = topic, messages = messages)

@app.route("/send", methods=["POST"])
def send():
    topic_id = request.form["id"]
    user_id = users.user_id()
    message = request.form["message"]
    if message != "":
        convos.send_message(message, user_id, topic_id, 1)
    else:
        return render_template("error.html", message = "message couldn't be sent")

    return redirect("/convo/"+str(topic_id))

@app.route("/delete", methods=["POST"])
def delete():
    message_id = request.form["message_id"]
    convos.delete_message(message_id)
    id = request.form["id"]
    return redirect("/convo/"+str(id))

@app.route("/edit/<int:id>", methods=["POST"])
def update(id):
    sql = "SELECT message FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    message = result.fetchone()[0]
    return render_template("update.html", id = id, message = message)

@app.route("/update_message", methods=["POST"])
def update_message():
    message = request.form["message"]
    id = request.form["id"]
    convos.update_message(message, id)
    sql = "SELECT topic_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    topic_id = result.fetchone()[0]
    return redirect("/convo/"+str(topic_id))

@app.route("/search")
def search():
    word = request.args["word"]
    if word == "":
        return redirect("/")
    messages = convos.search(1, word)
    if len(messages) == 0:
        return render_template("error.html", message = "There were no search results")
    return render_template("search.html", messages = messages)

@app.route("/create_area")
def create_area():
    return render_template("create_area.html")

@app.route("/create_private_area", methods=["POST"])
def create_private():
    name = request.form["theme"]
    if name == "":
        return render_template("error.html", message = "Area has to have a name")
    user_id = users.user_id()
    area_id = areas.create_area(name, user_id)
    areas.give_accessrights(area_id, user_id)
    return redirect("add_users/"+str(area_id))

@app.route("/add_users/<int:id>")
def add_users(id):
    return render_template("add_users.html", id = id)


@app.route("/add", methods=["POST"])
def add():
    username = request.form["username"]
    if username == "" or username == None:
        return render_template("error.html", message = "You have to write a username")
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    name = result.fetchone()
    if name == None or name == "":
        return render_template("error.html", message = "There is no user with that username")
    area_id = request.form["id"]
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user_id = result.fetchone()[0]
    if users.check_rights(user_id, area_id):
        return render_template("add_users.html", id=area_id, message="That user already has accessrights")
    areas.give_accessrights(area_id, user_id)
    return render_template("add_users.html", id = area_id)