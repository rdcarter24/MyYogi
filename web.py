from flask import Flask, render_template, request, session, redirect, url_for
import MyYogi
import training_data
import model
import os
import json

app = Flask(__name__)


############ user log in/sign up ###########
@app.route("/")
def home():
    return render_template("home.html")


############ finish user log in#################
@app.route("/login")
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    try:
        user = model.session.query(model.User).filter_by(email=email).filter_by(password=password).one()
        if user:
            session["user_id"]=user.id
            return redirect(url_for("user_home"))
    except model.NoResultFound, e:
        print e
        message = "This is embarassing... It appears we don't have that login on file."
        return render_template("home.html", message=message)


@app.route("/user_home")
def user_home():
    user = MyYogi.get_user(id=session["user_id"])
    message = "Welcome %s" % user.first_name
    return render_template("user_home.html", message=message)


@app.route("/add_user")
def add_user():
    return render_template("add_user.html")


@app.route("/new_user")
def new_user():
    email = request.args.get("email")
    password = request.args.get("password")
    first_name = request.args.get("first_name")
    user = MyYogi.add_user(email, password, first_name)
    return redirect(url_for("user_home"))


######### Yoga Info ##########
@app.route("/display_asana")
def display_asana():
    name = request.args.get("name")
    if name:
        asana = MyYogi.get_asana(name=name)
    else:
        asana = MyYogi.get_random_asana()
    return render_template("display_asana.html", name=asana.name, id=asana.id, routine=asana.routine)


@app.route("/display_routine")
def display_routine():
    asana_name = []
    routine = MyYogi.generate_routine(training_data.good_warm_up)
    for i in routine:
        asana = MyYogi.get_asana(id=i)
        asana_name.append(asana.name)

    asana_json = json.dumps(asana_name)

    return render_template("display_routine.html", name_list=asana_json)


@app.route("/add_routine")
def add_routine():
    return render_template("add_routine.html")


@app.route("/new_routine")
def new_routine():
    name = request.args.get("name")
    user_id = session["user_id"]
    routine = MyYogi.save_routine(name, user_id)
    return redirect(url_for("user_home"))


app.secret_key = "jdfkafjdksah"

if __name__ == "__main__":

    app.run(debug=True)
