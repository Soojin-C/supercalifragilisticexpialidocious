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
		return redirect(url_for("login"))

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
	if "logged_in" in session:
		return render_template("stockResearch.html", logged_in = True)
	else:
		flash("Please login to view Stock Research")
		return redirect(url_for("login"))

@app.route("/stockResults")
def stockResults():
	if "logged_in" in session:
		retval = {}

		if (request.args["stock_info"].find(".") == len(request.args["stock_info"]) - 1):
			companyName = request.args["stock_info"].replace(" ", "|~|~|")
			actualCompanyName = companyName.replace("|~|~|", " ").replace("and", "&")

			companyCode = info.quickGetSymbol(actualCompanyName )
			company_info = info.getStocks(companyCode)
			#print(company_info)

			watchlistYet = db.check_watchlist(session["logged_in"], actualCompanyName)
					        #[companyNAme + search_that_led, TRUE/FALSE]
			watchlist_info = [companyName.replace("and", "&") + "{!{!!}!}" + companyName, watchlistYet]
			#{Actual company name: [companyInfo, [companyName + search, T/F]]}
			retval[actualCompanyName] = [company_info, watchlist_info]

		else:
			#print(request.args["stock_info"])
			search = " " + request.args["stock_info"].lower().replace("|~|~|", " ").replace("&", "and") + " "
			companyCode = info.getSymbol(search)
			if (companyCode == "NONE"):
				print("bad search...")
				flash ("No company of that name found...")
				return redirect(url_for("stockResearch"))
				#Each will hold a list with all the company info.

			for each in companyCode:
				#print(each)
				company_info = info.getStocks(each)
				#print(company_info)

				companyName = companyCode[each].replace(" ", "|~|~|")
				watchlistYet = db.check_watchlist(session["logged_in"], companyCode[each])
					        #[companyNAme + search_that_led, TRUE/FALSE]
				watchlist_info = [companyName + "{!{!!}!}" + request.args["stock_info"].replace(" ", "|~|~|"), watchlistYet]

				retval[companyCode[each]] = [company_info, watchlist_info]

		return render_template("stockResults.html", logged_in = True, companyInfo = retval)
	else:
		return redirect(url_for("login"))


@app.route("/changeWatchlist", methods = ["GET", "POST"])
def changeWatchlist():
	print ("request.args: " )
	print ( request.args )
	print ( "\n ------------")
	print ("request.form: " )
	print ( request.form )
	print ( "\n -----------")

	for each in request.args:
		if request.args[each] == "Add to watchlist":
			data = each.split("{!{!!}!}")
			search = data[1]
			companyName = data[0].replace("|~|~|"," ")
			db.add_watchlist(session["logged_in"], companyName)
		if request.args[each] == "Remove from watchlist":
			data = each.split("{!{!!}!}")
			search = data[1].replace("|~|~|", " ")
			companyName = data[0].replace("|~|~|"," ")
			db.remove_watchlist(session["logged_in"], companyName)
	return redirect(url_for("stockResults", stock_info = search))

@app.route("/removeWatchlist", methods = ["GET", "POST"])
def removeWatchlist():

	for each in request.args:
		if request.args[each] == "Remove from watchlist":
			data = each.split("{!{!!}!}")
			companyName = data[0].replace("|~|~|"," ")
			db.remove_watchlist(session["logged_in"], companyName)
	return redirect(url_for("watchlist"))

@app.route("/watchlist")
def watchlist():
	if "logged_in" in session:
		watchlist_data = []
		data = db.get_watchlist(session["logged_in"])
		for each in data:
			#each [stock_name]
			remove_data = each[0]. replace(" ", "|~|~|").replace("&", "and")
			print("rmv: " + remove_data)
			watchlist_data.append([each[0], remove_data])
		return render_template("watchlist.html", watchlist = watchlist_data, logged_in = True)
	else:
		flash ("Please login to view the watchlist")
		return redirect(url_for("login"))

if __name__ == "__main__":
    app.debug = True
    app.run()
