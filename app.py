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
	return render_template("login.html", title = "Login", heading = "Login", type = "home")

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
    db.add_profile(request.args["user"], 100000, 100000, 100000, 0.00)
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
		return render_template("login.html", title = "Login", heading = "Login", type = "stockResearch")

@app.route("/stockResults")
def stockResults():
	if "logged_in" in session:
		retval = {}
		#If the user hasn't inputted anything
		if (request.args["stock_info"] == ""):
			flash ("Please enter a company name")
			return (redirect(url_for("stockResearch")))

		#If the user comes form the watchlist.
		if (request.args["stock_info"].find("{*}") != -1):
			companyCode = request.args["stock_info"].replace("{*}watchlist", "")

			company_info = info.getStocks(companyCode)
			company_info["ytdChange"] = round(company_info["ytdChange"], 5)
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
				flash ("No company of that name found in our database...")
				return redirect(url_for("stockResearch"))

			#Each will hold a list with all the company info.
			for each in companyCode:
				#print(each)
				company_info = info.getStocks(each)
				company_info["ytdChange"] = round(company_info["ytdChange"], 5)
				#print(company_info)

				companyName = companyCode[each].replace(" ", "|~|~|")
				watchlistYet = db.check_watchlist(session["logged_in"], each.lower())
					            #[companyCode + search_that_led, TRUE/FALSE]
				watchlist_info = [each.lower() + "{!{!!}!}" + request.args["stock_info"].replace(" ", "|~|~|"), watchlistYet]

				retval[companyCode[each]] = [company_info, watchlist_info]

		return render_template("stockResults.html", title = "Stock Results", heading = "Stock Results", logged_in = True, companyInfo = retval)
	else:
		return render_template("login.html", title = "Login", heading = "Login", type = "stockResearch")

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
		watchlist_data = db.get_watchlist(session["logged_in"])
		for each in watchlist_data:
			each[0] = info.getStocks(each[1].lower())
		return render_template("watchlist.html", watchlist = watchlist_data, title = "Watchlist", heading = "Watchlist", logged_in = True)
	else:
		flash ("Please login to view Watchlist")
		return render_template("login.html", title = "Login", heading = "Login", type = "watchlist")#redirect(url_for("login"))

@app.route("/articles")
def articles():
	#print(request.form)
	query = request.args["article_search"]
	if query.strip() == "":
		query = "stock"
	dict= info.getArticles(query)
	if dict == None:
		flash("Invalid API KEY")
		return render_template("login.html", title = "Login", heading = "Login", type = "watchlist")#redirect(url_for("login"))
	if len(dict) < 1:
		flash("No articles found. Try again")
	if "logged_in" in session:
		return render_template("news.html", title = "Article Results", heading = "Article Results", articles = dict, logged_in= True)
	else:
		return render_template("news.html", title = "Article Results", heading = "Article Results", articles = dict, logged_in= False)

@app.route("/rankings")
def rankings():
	dict = db.rankings()
	ranks = {}
	if "logged_in" in session:
		for username in dict:
			stock_data = db.get_stocks(username)
			counter = 0
			for each in stock_data:
				data = db.get_portfolio(username)
				stock_info = info.getStocks(each[0])
				if (counter == 0):
					buying_power = data[2]
				else:
					buying_power = data[1]
				new_account_val = buying_power + round(stock_info["latestPrice"] * int(each[1]), 2)
				print(new_account_val)
				value = round((new_account_val / 100000.00) - 1.00, 2)
				counter = counter + 1
				db.add_profile(username,round(new_account_val, 2), data[2], data[3], value)
			data = db.get_portfolio(username)
		i = 1;
		for username in dict:
			ranks[i] = [username, dict[username]]
			i = i + 1
		return render_template("rankings.html", order = ranks, user = session["logged_in"] ,title = "Rankings", heading = "Rankings", logged_in = True)
	else:
		flash("Please login to view Rankings")
		return render_template("login.html", title = "Login", heading = "Login", type = "rankings")

@app.route("/buyStock")
def buyStock():
	print(request.args)
	for each in request.args:
		if request.args[each] == "Buy Stock":
			data = each.replace(" ", "").split("|~~|")
			break
	search = data[2].split("{!{!!}!}")[1]
	companyCode = data[0].lower()
	stockPrice = round(float(data[1]), 2)
	print(data)
	print(search)
	if (request.args["stock_buy"] == "" ):
		flash("Invalid number of stocks.")
		return redirect(url_for("stockResults" , stock_info = search))
	numStocks = int(request.args["stock_buy"])
	if ( numStocks <= 0):
		flash("Invalid number of stocks.")
		return redirect(url_for("stockResults" , stock_info = search))
	totalPrice = round(stockPrice * numStocks, 2)
	currPortfolio = db.get_portfolio(session["logged_in"])

	if ( totalPrice > currPortfolio[2] ):
		flash("You don't have enough money to buy this.")
		return redirect(url_for("stockResults" , stock_info = search))

	db.buy_stock(session["logged_in"], companyCode, numStocks, totalPrice)

	new_buying_power = currPortfolio[3] - totalPrice
	new_account_val = new_buying_power + info.getStocks(companyCode)["latestPrice"]
	new_cash = currPortfolio[3] - totalPrice
	new_annual_ret = round((new_account_val / 100000.0) - 1.00, 2)
	print (new_annual_ret)

	db.add_profile(session["logged_in"],round(new_account_val, 2), round(new_buying_power, 2), round(new_cash, 2), new_annual_ret)

	return redirect(url_for("portfolio"))

@app.route("/sellStock")
def sellStock():
	print(request.args)
	data = []
	for each in request.args:
		if request.args[each] == "Sell Stocks":
			data = each.replace(" ", "").split("|~~|")
			print(data)
			print("^data")
			break
	code = data[0]
	paid = data[1]
	sell = round(float(data[2]) , 2)
	numS = data[3]

	currPortfolio = db.get_portfolio(session["logged_in"])
	new_buying_power = currPortfolio[3] + sell
	new_cash = currPortfolio[3] + sell
	new_account_val = new_buying_power
	new_annual_ret = round((new_account_val / 100000.0) - 1.00, 2)
	db.add_profile(session["logged_in"],round(new_account_val), round(new_buying_power), round(new_cash), new_annual_ret)

	db.remove_stock(session["logged_in"], code, paid, numS)
	return redirect(url_for("portfolio"))

@app.route("/portfolio")
def portfolio():
	if "logged_in" in session:
		stock_data = db.get_stocks(session["logged_in"])
		print("stock data : " )
		print(stock_data)
		counter = 0;
		for each in stock_data:
			data = db.get_portfolio(session["logged_in"])
			stock_info = info.getStocks(each[0])
			stock_data[counter] = [each[0], each[1], each[2], stock_info["latestPrice"], round(stock_info["latestPrice"] * int(each[1]), 2), stock_info["companyName"]]
			print(stock_data)
			if (counter == 0):
				buying_power = data[2]
			else:
				buying_power = data[1]
			new_account_val = buying_power + stock_data[counter][4]
			print(new_account_val)
			value = round((new_account_val / 100000.0) - 1.00, 2)
			print(value)
			counter = counter + 1
			db.add_profile(session["logged_in"],round(new_account_val, 2), data[2], data[3], value)
		data = db.get_portfolio(session["logged_in"])
		return render_template("portfolio.html", title = "Portfolio", heading = "Portfolio", portfolio_data = data, bought_stocks = stock_data, logged_in = True)
	else:
		flash("Please login to view Portfolio")
		return render_template("login.html", title = "Login", heading = "Login", type = "portfolio")

if __name__ == "__main__":
    app.debug = True
    app.run()
