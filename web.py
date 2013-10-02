from flask import Flask, render_template, request, session, redirect, url_for
import MyYogi
import training_data
import model
import os
import json
import re


app = Flask(__name__)
app.config['DEBUG'] = True

############ User log in/sign up info ###########
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login_info")
def login_info():
    return render_template("login_info.html")


@app.route("/login")
def login():
    email = request.args.get("email")
    password = request.args.get("password")
    user = MyYogi.get_user(email=email, password=password)
    if user:
        session["user_id"]=user.id
        return redirect(url_for("user_home"))
    else:
        message = "Login not on file. Please try again or sign up."
        return render_template("index.html", message=message)


@app.route("/user_home", methods=["GET"])
def user_home():
    user = MyYogi.get_user(id=session["user_id"])
    message = "Welcome %s" % user.username
    routines = user.routines
    if routines:
        return render_template("user_home.html", message=message, routines=routines)
    else:
        return render_template("user_home.html", message=message)


@app.route("/add_user")
def add_user():
    return render_template("add_user.html")


@app.route("/new_user")
def new_user():
    email = request.args.get("email")
    password = request.args.get("password")
    username = request.args.get("username")
    user = MyYogi.get_user(email=email, password=password)
    if user:
        message = "We already have that email on file. Please try again."
        return render_template("add_user.html", message=message)
    else:
        user = MyYogi.add_user(email, password, username)
        session["user_id"]=user.id
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
##### unit test for routine_id
@app.route("/display_routine")
def display_routine():
    routine_id = request.args.get("routine_id")
    asana_img = []
    asana_time = []
    sub_routine_list =[]

    ##### if user wants saved routine
    ##### get_routine returns a list of objects of the Routine_Asana class
    ##### BUG!!!!  redirect home after running saved routine
    if routine_id:
        routine = MyYogi.get_routine(routine_id)

        for obj in routine:
            asana_img.append(obj.asana.image)
            asana_json = json.dumps(asana_img)
            asana_time.append(obj.asana.breaths)
            sub_routine_list.append(obj.sub_routine)
            sub_routine_json=json.dumps(sub_routine_list)

        return render_template("display_routine.html", asana_list=asana_json, asana_time=asana_time, sub_routine_list=sub_routine_json, saved=True)
    ##### if user wants new routine
    ##### generate_routine returns a list of objects of the Asana class
    else:
        routine = MyYogi.get_yoga_routine(training_data, session["user_id"])

        for i in range(len(routine)):
            for obj in routine[i][0]:
                asana_img.append(obj[0].image)
                asana_json = json.dumps(asana_img)
                asana_time.append(obj[1])
                sub_routine_list.append(routine[i][1])
                sub_routine_json=json.dumps(sub_routine_list)

        return render_template("display_routine.html", asana_list=asana_json, asana_time=asana_time, sub_routine_list=sub_routine_json, saved=False)


@app.route("/add_routine")
def add_routine():
    save_routine = request.args.get("asana_list")
    sub_routine_list = request.args.get("sub_routine_list")
    return render_template("add_routine.html", asana_list=save_routine, sub_routine_list=sub_routine_list)


@app.route("/new_routine", methods=['POST'])
def new_routine():
    save_routine = None
    name = request.form.get("name")
    user_id = session["user_id"]
    save_routine = json.loads(request.form.get("asana_list"))
    sub_routine_list = json.loads(request.form.get("sub_routine_list"))
    routine = MyYogi.save_routine(name, user_id)

    for i in range(len(save_routine)):
        asana = MyYogi.get_asana(image=save_routine[i])
        routine_asana = MyYogi.save_routine_asana(asana.id,routine.id,i, sub_routine_list[i])
    return redirect(url_for("user_home"))

@app.route("/display_saved_routine")
def display_saved_routine():
    routine_id = request.args.get("routine")

    return redirect(url_for("display_routine", routine_id=routine_id ))


@app.route("/rate_routine")
def rate_routine():
    asana_list = json.loads(request.args.get("asana_list"))
    sub_routine_list = request.args.get("sub_routine_list")
    return render_template("rate_routine.html", asana_list=asana_list, sub_routine_list=sub_routine_list)


@app.route("/train_routine", methods=["POST"])
def train_routine():
    rated_routine = request.form.get("asana")
    asana_string = request.form.get("asana_list")
    sub_routine_list = json.loads(request.form.get("sub_routine_list"))
    asana_list = asana_string.split(',')
    routine = MyYogi.save_routine("train", "1")

    no_dupl =[]
    for i in range(len(asana_list)):
        if asana_list[i] in request.form and asana_list[i] not in no_dupl:
            asana = MyYogi.get_asana(image=asana_list[i])
            asana = MyYogi.train_routine_asana(asana.id, routine.id, sub_routine_list[i], "1")
            no_dupl.append(asana_list[i])
            print no_dupl
        ############# maybe don't need this part
        else:
            asana = MyYogi.get_asana(image=asana_list[i])
            asana = MyYogi.train_routine_asana(asana.id, routine.id, sub_routine_list[i], "0")

    return redirect(url_for("user_home"))


#app.secret_key = os.urandom(24)
app.secret_key = "jdfkafjdksah"


if __name__ == "__main__":
    if not os.environ.get('HEROKU_POSTGRESQL_VIOLET_URL'):
        app.run(debug=True)
