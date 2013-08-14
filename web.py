from flask import Flask, render_template, request, session, redirect, url_for
import MyYogi
import training_data
import model
import os
import json
import re

app = Flask(__name__)


############ User log in/sign up info ###########
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
    routines = user.routines
    return render_template("user_home.html", message=message, routines=routines)


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


####### find a way to test this!!!!
@app.route("/display_routine")
def display_routine():
    routine_id = request.args.get("routine_id")
    asana_name = []
    asana_time = []

    ##### if user wants saved routine
    ##### get_routine returns a list of objects of the Routine_Asana class
    if routine_id:
        routine = MyYogi.get_routine(routine_id)
        for obj in routine:
            asana_name.append(obj.asana.name)
            asana_json = json.dumps(asana_name)
            asana_time.append(obj.asana.breaths)
        return render_template("display_routine.html", asana_list=asana_json, asana_time=asana_time, saved=True)
    ##### if user wants new routine 
    ##### generate_routine returns a list of objects of the Asana class
    else:
        routine = MyYogi.generate_routine(training_data.good_warm_up,2)

        for obj in routine:
            asana_name.append(obj[0].name)
            asana_json = json.dumps(asana_name)
            asana_time.append(obj[1])
        return render_template("display_routine.html", asana_list=asana_json, asana_time=asana_time, saved=False)


@app.route("/add_routine")
def add_routine():
    save_routine = request.args.get("asana_list")
    return render_template("add_routine.html", asana_list=save_routine)


########## use POST!!!
@app.route("/new_routine", methods=["POST"])
def new_routine():
    name = request.args.get("name")
    user_id = session["user_id"]
    save_routine = json.loads(request.args.get("asana_list"))
    routine = MyYogi.save_routine(name, user_id)

    for i in range(len(save_routine)):
        asana = MyYogi.get_asana(name=save_routine[i])
        routine_asana = MyYogi.save_routine_asana(asana.id,routine.id,i)
    return redirect(url_for("user_home"))

@app.route("/display_saved_routine")
def display_saved_routine():
    routine_id = request.args.get("routine")

    return redirect(url_for("display_routine", routine_id=routine_id ))


@app.route("/rate_routine")
def rate_routine():
    asana_list = json.loads(request.args.get("asana_list"))
    return render_template("rate_routine.html", asana_list=asana_list)


@app.route("/train_routine", methods=["POST"])
def train_routine():
    rated_routine = request.form.get("asana")
    asana_string = request.form.get("asana_list")
    asana_list = asana_string.split(',')
    routine = MyYogi.save_routine("train", "0")

############ BUG!!! prints 1 for asana everytime it shows up if in request.form
    for item in asana_list:
        if item in request.form:
            asana = MyYogi.get_asana(name=item)
            asana = MyYogi.train_routine_asana(asana.id, routine.id, "1")
        else:
            asana = MyYogi.get_asana(name=item)
            asana = MyYogi.train_routine_asana(asana.id, routine.id, "0")

    return redirect(url_for("user_home"))



app.secret_key = "jdfkafjdksah"

if __name__ == "__main__":

    app.run(debug=True)
