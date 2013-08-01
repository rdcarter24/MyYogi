from flask import Flask, render_template, request, redirect, url_for
import MyYogi
import training_data

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")



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
    return render_template("display_routine.html", name_list=asana_name) 



@app.route("/add_asana")
def add_asana():
    return render_template("add_asana.html")



@app.route("/new_asana")
def new_asana():
    name = request.args.get("name")
    routine = request.args.get("routine")
    asana = MyYogi.add_asana(name, routine)

    return redirect (url_for("display_asana", name=asana.name))



if __name__=="__main__":
    app.run(debug=True)
