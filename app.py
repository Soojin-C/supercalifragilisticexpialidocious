import os

from flask import Flask, render_template, request,flash, session,url_for,redirect

from util import db #, user_info


app = Flask(__name__)

app.secret_key=os.urandom(32)

@app.route("/")
def home():
	if session.get("uname"):
		return render_template("home.html")
	return render_template("home.html",Title = 'Login')

#Authenticates user and adds session
#Returns to the page the user was on previously(?)

@app.route("/auth", methods = ["GET", "POST"])
def auth():
	given_user = request.form["username"]
	given_pwd = request.form["password"]
	if db.auth_user(given_user, given_pwd):
		session["uname"] = given_user
		return redirect(url_for("home"))
	else:
		flash("username or password is incorrect")
		return redirect(url_for("home"))

#Sends the user to the register.html to register a new account
@app.route("/register")
def register():
	return render_template("register.html")

#Attempts to add the user to the database
@app.route("/adduser")
def add_user():
    if(not request.args["user"].strip() or not request.args["password"] or not request.args["confirm_password"]):
        flash("Please fill in all fields")
        return redirect(url_for("register"))

    if(db.user_exist(request.args["user"])):
        flash("User already exists")
        return redirect(url_for("register"))

    if(request.args["password"] != request.args["confirm_password"]):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    db.add_user(request.args["user"], request.args["password"])
    session["logged_in"] = request.args["user"]
    return redirect(url_for("home"))
'''
#Logs the user out and removes session
#returns to the page the user was on previously
@app.route("/logout")
def logout():
	if session.get("uname"):
		session.pop("uname")
		print(session)
	return redirect(url_for("home"))
'''
if __name__ == "__main__":
    app.debug = True
    app.run()
