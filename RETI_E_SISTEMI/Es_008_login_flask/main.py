"""

Author: Jacopo Van Cleeff
Date: 26-01-2021

"""

from flask import Flask,render_template, redirect, request
from flask.helpers import url_for

app = Flask(__name__)

@app.route("/")             # http://127.0.0.1:5000/
def index():                # decoratore. Per accedere alla pagina associata alla funzione index 
    return render_template("login.html")


@app.route("/", methods = ["GET","POST"])
def login():
    if request.method == "POST":
        usr = request.form["usr"]
        pwd = request.form["pwd"]

        completion = validate(usr,pwd)

        if completion:
            return redirect(url_for("secret"))
        else:
            error  = "Invalid Credentials. Please try again."
        
        return render_template("login.html", error = error)
    
def secret():
    return "This is a scerte page."

def validate(username,password):
    return False

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug = True)