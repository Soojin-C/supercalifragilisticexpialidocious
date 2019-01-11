import os

from flask import Flask, render_template, request,session,url_for,redirect

from util import db, user_info


app = Flask(__name__)

app.secret_key=os.urandom(32)

@app.route("/", methods=['POST',"GET"])
def home():
	if session.get("uname"):
		return render_template("welcome.html")
	return render_template("login.html",Title = 'Login')

#Authenticates user and adds session
#Returns to the page the user was on previously(?)
@app.route("/login", methods=['POST'])
def login():
	given_user = request.form["username"]
	given_pwd = request.form["password"]
	if db.auth_user(given_user, given_pwd):
        session["uname"] = given_user
        return redirect(url_for("home"))
    else:
        flash("username or password is incorrect")
        return redirect(url_for(""))

#Logs the user out and removes session
#returns to the page the user was on previously
@app.route("/logout")
def logout():
	if session.get("uname"):
		session.pop("uname")
		print(session)
	return redirect(url_for("home"))

#Sends the user to the register.html to register a new account
@app.route("/register")
def register():
	return render_template("register.html")

#Attempts to add the user to the database
@app.route("/adduser")
def add_user():
	new_user = request.args["user"]
	new_pswd = request.args["password"]
	confirm_pswd = request.args["confirm_password"]

    if(not new_user.strip() or not new_pswd or not confirm_pswd):
        flash("Please fill in all fields")
        return redirect(url_for("register"))

    if(db.check_user(new_user)):
        flash("User already exists")
        return redirect(url_for("register"))

    if(new_pswd != confirm_pswd):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    db.add_user(new_user, new_pswd)
    session["logged_in"] = new_user
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.debug = True
    app.run()
