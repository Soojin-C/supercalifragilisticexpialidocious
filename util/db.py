import sqlite3
DB_FILE = "data/stock.db"
'''
def create_tables():
    """Creates tables for users' info, portfolios, users' stocks and watchlist"""
    db = sqlite3.connect("../" + DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE user_info (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE portfolio (username TEXT, account_val FLOAT, buying_power FLOAT, cash FLOAT, annual_ret FLOAT)"
    c.execute(command)

    command = "CREATE TABLE user_stocks (username TEXT, stock_name TEXT, num_stocks INTEGER, price_paid FLOAT)"
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

    c.execute("INSERT INTO user_stocks VALUES(?, ?, ?, ?)", (user, new_stock_name, new_num_stock, new_price_paid))

    db.commit()
    db.close()

def add_profile(user, new_account_val, new_buying_power, new_cash, new_annual_ret):
    """Inserts an updated version of the user's portfolio. Removes the old version"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    rmv_user(user)
    c.execute("INSERT INTO portfolio VALUES(?, ?, ?, ?, ?)", (user, new_account_val, new_buying_power, new_cash, new_annual_ret))

    db.commit()
    db.close()

# =====================================================================================
def add_watchlist(user, new_watchlist):
    """Inserts a new stock into the list of users' bought stocks"""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("INSERT INTO watchlist VALUES(?, ?)", (user, new_watchlist))

    db.commit()
    db.close()

def check_exist(user, item ):


def rmv_user(user):
    """Remove the stock rmv_stock_name when the user sells stocks."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("DELETE FROM user_stock WHERE username = '{}'".format(user))

    db.commit()
    db.close()

def remove_stock(user, rmv_stock_name):
    """Remove the stock rmv_stock_name when the user sells stocks."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("DELETE FROM user_stock WHERE username = '{}' and stock_name = '{}'".format(user, rmv_stock_name))

    db.commit()
    db.close()

def remove_watchlist(user, rmv_watchlist_name):
    """Remove the stock rmv_watchlist_name from the watchlist for user."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("DELETE FROM watchlist WHERE username = '{}' and stock_name = '{}'".format(user, rmv_watchlist_name))

    db.commit()
    db.close()
'''
