import sqlite3
DB_FILE = "data/stock.db"

def create_tables():
    """Creates tables for users' info, portfolios, users' stocks and watchlist"""
    db = sqlite3.connect("../" + DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE user_info (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE portfolio (username TEXT, account_val FLOAT, buying_power FLOAT, cash FLOAT, annual_ret FLOAT)"
    c.execute(command)

    command = "CREATE TABLE user_stocks (username TEXT, stock_name TEXT, num_stocks INTEGER, price_paid FLOAT, dup INTEGER)"
    c.execute(command)

    command = "CREATE TABLE watchlist (username TEXT, stock_name TEXT)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

#login / register routes
def add_user(username, password):
    """Insert the credentials for newly registered users into the database"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO user_info VALUES(?, ?)", (username, password))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    """Authenticate user attempting to log in"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    for each in c.execute("SELECT user_info.username, user_info.password FROM user_info"):
        if(each[0] == username and each[1] == password):
            db.close()
            return True
    db.close()
    return False

def user_exist(username):
    """Check if a username has already been taken when registering."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for each in c.execute("SELECT user_info.username FROM user_info"):
        if(each[0] == username):
            db.close()
            return True
    db.close()
    return False

#Adding to stock and profile functions
def buy_stock(user, new_stock_name, new_num_stock, new_price_paid):
    """Inserts a new stock into the list of users' bought stocks"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    dup = get_lowestNum(user, new_stock_name,  new_price_paid, new_num_stock,"add")
    c.execute("INSERT INTO user_stocks VALUES(?, ?, ?, ?, ?)", (user, new_stock_name, new_num_stock, new_price_paid, dup))

    db.commit()
    db.close()

def add_profile(user, new_account_val, new_buying_power, new_cash, new_annual_ret):
    """Inserts an updated version of the user's portfolio. Removes the old version"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (check_portfolio(user)):
        rmv_user(user)
    c.execute("INSERT INTO portfolio VALUES(?, ?, ?, ?, ?)", (user, new_account_val, new_buying_power, new_cash, new_annual_ret))

    db.commit()
    db.close()

def add_watchlist(user, new_watchlist):
    """Inserts a new watchlist stock into the db for a users watchlist"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (check_watchlist(user, new_watchlist)):
        db.close()
        return False
    c.execute("INSERT INTO watchlist VALUES(?, ?)", (user, new_watchlist))

    db.commit()
    db.close()
    return True

def check_portfolio(user):
    """Check to see if the user is already in the portfolio."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for each in c.execute("SELECT portfolio.username FROM portfolio WHERE username = '{}'".format(user)):
        if(each[0] == user):
            db.close()
            return True

    db.close()
    return False

def rmv_user(user):
    """Remove the portfolio info of user"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("DELETE FROM portfolio WHERE username = '{}'".format(user))

    db.commit()
    db.close()

def remove_watchlist(user, rmv_watchlist_name):
    """Remove the stock rmv_watchlist_name from the watchlist for user."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("DELETE FROM watchlist WHERE username = '{}' and stock_name = '{}'".format(user, rmv_watchlist_name))

    db.commit()
    db.close()


def check_watchlist(user, company_name):
    """Check to see if the user already has the stock in the watchlist."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for each in c.execute("SELECT watchlist.stock_name FROM watchlist WHERE username = '{}'".format(user)):
        if(each[0] == company_name):
            db.close()
            return True

    db.close()
    return False

def get_watchlist(user):
    """Gets all the watchlist stocks for the user."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    watchlist_data = []
    ret_val = c.execute("SELECT watchlist.stock_name FROM watchlist WHERE username = '{}'".format(user))
    for each in ret_val:
        companyCode = each[0]
        watchlist_data.append([0, companyCode])

    db.close()
    return watchlist_data

def get_portfolio(user):
    """Gets all the watchlist stocks for the user."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute("SELECT * FROM portfolio WHERE username = '{}'".format(user))
    for each in data:
        ret_val = each
    db.close()
    return ret_val

def get_stocks(user):
    """Remove the stock rmv_watchlist_name from the watchlist for user."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    stock_data = []
    ret_val = c.execute("SELECT user_stocks.stock_name, user_stocks.num_stocks, user_stocks.price_paid FROM user_stocks WHERE username = '{}'".format(user))
    for each in ret_val:
        stock_data.append([each[0], each[1], each[2]])
    db.close()
    print (stock_data)
    return stock_data

def remove_stock(user, rmv_stock_name, rmv_price_paid, rmv_num_stocks):
    """Remove the stock rmv_stock_name when the user sells stocks."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    dup = get_lowestNum(user, rmv_stock_name, rmv_price_paid, rmv_num_stocks, "rmv")
    c.execute("DELETE FROM user_stocks WHERE username = '{}' and stock_name = '{}' and price_paid = '{}' and num_stocks= '{}' and dup = '{}'".format(user, rmv_stock_name, rmv_price_paid, rmv_num_stocks, dup))

    db.commit()
    db.close()

def get_lowestNum(user, rmv_stock_name, rmv_price_paid, rmv_num_stocks, type):
    """Remove the stock rmv_watchlist_name from the watchlist for user."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (check_dup(user, rmv_stock_name, rmv_price_paid, rmv_num_stocks)):
        ret = c.execute("SELECT dup FROM user_stocks WHERE username = '{}' and stock_name = '{}' and price_paid = '{}' and num_stocks= '{}'".format(user, rmv_stock_name, rmv_price_paid, rmv_num_stocks))
        ret_val = 0;
        for each in ret:
            if (each[0] > ret_val):
                ret_val = each[0]
        if (type == "add"):
            return ret_val + 1
        else:
            return ret_val
    else:
        if (type == "add"):
            return 0;

    db.close()
    return -1

def check_dup(user, rmv_stock_name, rmv_price_paid, rmv_num_stocks):
    """Remove the stock rmv_watchlist_name from the watchlist for user."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    stock_data = []
    ret_val = c.execute("SELECT * FROM user_stocks")
    for each in ret_val:
        print(each)
        if (each[0] == user):
            print("9")
            if (each[1] == rmv_stock_name):
                print(round(float(rmv_price_paid), 2))
                if (each[3] == round(float(rmv_price_paid), 2)):
                    print("9")
                    if (each[2] == round(int(rmv_num_stocks))):
                        print("TRUE ===========================")
                        return True
    db.close()
    print("FALSE ===========================")
    return False


def rankings():
    """Retrieve rankings,"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    moolah = []
    bignames = []
    dict = {}
    accounts = c.execute("SELECT portfolio.username, portfolio.account_val FROM portfolio")


    for name, dollas in accounts:
        moolah.append(dollas)
        bignames.append(name)

    for num in range(len(moolah)- 1, 0, -1):
        for x in range(num):
            if moolah[x] < moolah[x+1]:
                temp = moolah[x]
                moolah[x] = moolah[x+1]
                moolah[x+1] = temp
                temp = bignames[x]
                bignames[x] = bignames[x+1]
                bignames[x+1] = temp
    for y in range(len(moolah)):
        dict[bignames[y]] = moolah[y]

    return dict
    db.commit()
    db.close()
# =====================================================================================



#create_tables()

#buy_stock('user', 'new_stock_name', 10, 100)
#buy_stock('user1', 'new_stock_name', 13, 14)
#buy_stock('user', 'new_stock_name', 19, 6)
#buy_stock('user1', 'new_stock_name', 14, 14)
#buy_stock('user1', 'new_stock_name', 10, 10)
