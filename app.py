import os

from flask import Flask, render_template, request,flash, session,url_for,redirect

from util import db , info


app = Flask(__name__)

app.secret_key=os.urandom(32)

@app.route("/")
def home():
	if "logged_in" in session:
		return render_template("home.html", user = session["logged_in"], logged_in = True)
	return render_template("home.html",Title = 'Login', logged_in = False)

#Authenticates user and adds session
#Returns to the page the user was on previously(?)

@app.route("/auth", methods = ["GET", "POST"])
def auth():
	given_user = request.form["username"]
	given_pwd = request.form["password"]
	if db.auth_user(given_user, given_pwd):
		session["logged_in"] = given_user
		return redirect(url_for("home"))
	else:
		flash("username or password is incorrect")
		return redirect(url_for("home"))

@app.route("/login")
def login():
	return render_template("login.html")

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

#Logs the user out and removes session
#returns to the page the user was on previously
@app.route("/logout")
def logout():
	if session.get("logged_in"):
		session.pop("logged_in")
		print(session)
	return redirect(url_for("home"))

@app.route("/stockResearch")
def stockResearch():
	return render_template("stockResearch.html", logged_in = True)

@app.route("/stockResults")
def stockResults():
	search = " " + request.args["stock_info"].lower() + " "
	companyCode = info.getSymbol(search)
	if (companyCode == "NONE"):
		print("bad search...")
		flash ("No company of that name found...")
		return redirect(url_for("stockResearch"))
	#Each will hold a list with all the company info.
	retval = {};
	for each in companyCode:
		print(each)
		company_info = info.getStocks(each)
		print(company_info)
		retval[companyCode[each]] = company_info
	return render_template("stockResults.html", logged_in = True, companyInfo = retval)

if __name__ == "__main__":
    app.debug = True
    app.run()
