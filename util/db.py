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

    command = "CREATE TABLE user_stocks (username TEXT, stock_name TEXT, num_stocks INTEGER, price_paid FLOAT)"
    c.execute(command)

    command = "CREATE TABLE watchlist (username TEXT, stock_name TEXT)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

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

def user_exist():
    """Check if a username has already been taken when registering."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for each in c.execute("SELECT user_info.username FROM user_info"):
        if(each[0] == username):
            db.close()
            return True
    db.close()
    return False

def buy_stock(user, stock_name, num_stock, price_paid):
    """Remove the stock rmv_stock_name when the user sells stocks."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

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
