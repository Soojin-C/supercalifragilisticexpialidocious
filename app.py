import os

from flask import Flask, render_template, request,flash, session,url_for,redirect

from util import db , info

app = Flask(__name__)

app.secret_key=os.urandom(32)

@app.route("/")
def home():
	if "logged_in" in session:
		return render_template("home.html", title = "Home", heading = "Home", user = session["logged_in"], logged_in = True)
	return render_template("home.html", title = "Home", heading = "Home", user = "User", logged_in = False)

#Authenticates user and adds session
#Returns to the page the user was on previously(?)

@app.route("/auth", methods = ["GET", "POST"])
def auth():
	#print(request.args)
	#print(request.form)
	return_page = "home"

	for each in request.form:
		if request.form[each] == "Login":
			return_page = each

	given_user = request.form["username"]
	given_pwd = request.form["password"]
	if db.auth_user(given_user, given_pwd):
		session["logged_in"] = given_user
		return redirect(url_for(return_page))
	else:
		flash("Username or password is incorrect")
		return redirect(url_for("login"))

@app.route("/login")
def login():
	return render_template("login.html", title = "Login", heading = "Login")

#Sends the user to the register.html to register a new account
@app.route("/register")
def register():
	return render_template("register.html", title = "Register", heading = "Register")

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
		return render_template("stockResearch.html", title = "Stock Search", heading = "Stock Search", logged_in = True)
	else:
		flash("Please login to view Stock Research")
		return render_template("login.html", title = "Login", heading = "Login")

@app.route("/stockResults")
def stockResults():
	if "logged_in" in session:
		retval = {}
		#If the user hasn't inputted anything
		if (request.args["stock_info"] == ""):
			flash ("Please enter a company name")
			return (redirect(url_for("stockResearch")))

		#If the user comes form the watchlist.
		if (request.args["stock_info"].find("{*}") != - 1):
			companyCode = request.args["stock_info"].replace("{*}watchlist", "")

			company_info = info.getStocks(companyCode)
			watchlistYet = db.check_watchlist(session["logged_in"], companyCode)
					        #[companyNAme + search_that_led, TRUE/FALSE]
			watchlist_info = [companyCode + "{!{!!}!}" + request.args["stock_info"], watchlistYet]
			#{Actual company name: [companyInfo, [companyName + search, T/F]]}
			retval[company_info["companyName"]] = [company_info, watchlist_info]

		else:
			#print(request.args["stock_info"])
			search = " " + request.args["stock_info"].lower().replace("|~|~|", " ").replace("&", "and").replace(".", " ") + " "
			companyCode = info.getSymbol(search)
			if (companyCode == "NONE"):
				print("bad search...")
<<<<<<< HEAD
				flash ("No company of that name found...")
				return redirect(url_for("stockResearch"), title = "Stock Results", heading = "Stock Results")
=======
				flash ("No company of that name found in our database...")
				return redirect(url_for("stockResearch"))
>>>>>>> dcae61b534f2b2f6044928fe744117d5271e6d17
				#Each will hold a list with all the company info.

			for each in companyCode:
				#print(each)
				company_info = info.getStocks(each)
				#print(company_info)

				companyName = companyCode[each].replace(" ", "|~|~|")
				watchlistYet = db.check_watchlist(session["logged_in"], each.lower())
					            #[companyCode + search_that_led, TRUE/FALSE]
				watchlist_info = [each.lower() + "{!{!!}!}" + request.args["stock_info"].replace(" ", "|~|~|"), watchlistYet]

				retval[companyCode[each]] = [company_info, watchlist_info]

		return render_template("stockResults.html", title = "Stock Results", heading = "Stock Results", logged_in = True, companyInfo = retval)
	else:
		return render_template("login.html", title = "Stock Results", heading = "Stock Results")

# Depending on the current status, either adds or removes from the watchlist
# Returns to the original search page.
@app.route("/changeWatchlist", methods = ["GET", "POST"])
def changeWatchlist():
	print ("request.args: " )
	print ( request.args )
	print ( "\n ------------")
	#print ("request.form: " )
	#print ( request.form )
	#print ( "\n -----------")

	for each in request.args:
		if request.args[each] == "Add to watchlist":
			data = each.split("{!{!!}!}")
			search = data[1]
			companyCode = data[0].lower()
			db.add_watchlist(session["logged_in"], companyCode)
		if request.args[each] == "Remove from watchlist":
			data = each.split("{!{!!}!}")
			search = data[1].replace("|~|~|", " ")
			companyCode = data[0].lower()
			db.remove_watchlist(session["logged_in"], companyCode)
	return redirect(url_for("stockResults", stock_info = search))

@app.route("/removeWatchlist", methods = ["GET", "POST"])
def removeWatchlist():
	print(request.args)
	for each in request.args:
		if request.args[each] == "Remove from watchlist":
			data = each.split("{!{!!}!}")
			companyCode = data[0]
			db.remove_watchlist(session["logged_in"], companyCode)
	return redirect(url_for("watchlist"))

@app.route("/watchlist")
def watchlist():
	if "logged_in" in session:
		watchlist_data = []
		data = db.get_watchlist(session["logged_in"])
		for each in data:
<<<<<<< HEAD
			#each [stock_name]
			remove_data = each[0]. replace(" ", "|~|~|").replace("&", "and")
			print("rmv: " + remove_data)
			watchlist_data.append([each[0], remove_data])
		return render_template("watchlist.html", watchlist = watchlist_data, title = "Watchlist", heading = "Watchlist", logged_in = True)
=======
			companyCode = each[0]
			companyInfo = info.getStocks(companyCode.lower())
			watchlist_data.append([companyInfo, companyCode])
		return render_template("watchlist.html", watchlist = watchlist_data, logged_in = True)
>>>>>>> dcae61b534f2b2f6044928fe744117d5271e6d17
	else:
		flash ("Please login to view the watchlist")
		return render_template("login.html", title = "Login", heading = "Login")#redirect(url_for("login"))


@app.route("/articles")
def articles():
	print(request.form)
	dict= info.getArticles(request.args["article_search"])
	if "logged_in" in session:
		return render_template("news.html", title = "Article Results", heading = "Article Results", articles = dict, logged_in= True)
	else:
		return render_template("news.html", title = "Article Results", heading = "Article Results", articles = dict, logged_in= False)

@app.route("/rankings")
def rankings():
	dict = db.rankings()
	ranks = {}
	accvals = {}
	if "logged_in" in session:
		i = 1;
		for username, accval in dict:
			ranks[i] = username
			accvals[username] = accval
			i = i + 1
		return render_template("rankings.html", order = ranks, values = accvals, title = "Rankings", heading = "Rankings", logged_in = True)
	else:
		flash("Please login to view Rankings")
		return render_template("login.html", title = "Login", heading = "Login")


if __name__ == "__main__":
    app.debug = True
    app.run()
