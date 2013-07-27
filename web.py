from flask import Flask, render_template, request, redirect, url_for
import MyYogi

app = Flask(__name__)

@app.route("/")
def get_asana():
    return render_template("get_asana.html")



@app.route("/display_asana")
def display_asana():
    name = request.args.get("name")
    if name:
        asana = MyYogi.get_asana(name)
    else: 
        asana = MyYogi.get_random_asana()
    return render_template("display_asana.html", name=asana.name, id=asana.id, routine=asana.routine)



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
