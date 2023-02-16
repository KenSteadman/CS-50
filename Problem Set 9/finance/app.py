import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get the user's ID from the session
    user_id = session["user_id"]

    # Get the user's stock information from the transactions table, grouped by symbol and with the total number of shares for each symbol
    user_stock_info = db.execute(
        "SELECT symbol, name, SUM(shares) as total_shares, price FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)

    # Get the user's current cash balance from the database
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Calculate the user's total net worth (cash + value of stocks)
    total = user_cash
    for stock in user_stock_info:
        total += stock["price"] * stock["total_shares"]

    # Render the index template, passing the user's stock information, cash balance, total net worth, and a few helper functions
    return render_template("index.html", user_stock_info=user_stock_info, user_cash=usd(user_cash),
                           total=usd(total), usd=usd, lookup=lookup, percentage=percentage)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # If the request method is "GET", retrieve the "buy_symbol" parameter from the request query string
    # and pass it to the template as "buy_symbol"
    if request.method == "GET":
        temp = request.args.get("buy_symbol")
        if not temp:
            buy_symbol = ""
        else:
            buy_symbol = temp
        return render_template("buy.html", buy_symbol=buy_symbol)

    # If the request method is "POST", lookup the stock information for the symbol specified in the form
    stock_info = lookup(request.form.get("symbol"))

    # Convert the number of shares to buy from a string to an integer. If it's not a valid integer, return an apology
    try:
        number = int(request.form.get("shares"))
    except ValueError:
        return apology("Shares should be positive integer")

    # If the stock information is not found or the symbol is invalid, return an apology
    if not stock_info:
        return apology("Invalid symbol or This symbol does not exist")

    # If the number of shares is not a positive integer, return an apology
    if number <= 0:
        return apology("Shares should be positive integer")

    # Extract the stock symbol, name, and price from the stock information
    stock_symbol = stock_info["symbol"]
    stock_name = stock_info["name"]
    stock_price = stock_info["price"]

    # Get the user's ID from the session
    user_id = session["user_id"]

    # Get the user's current cash balance from the database
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Calculate the remaining cash balance after buying the shares
    remaining_cash = user_cash - (stock_price * number)

    # If the user doesn't have enough cash, return an apology
    if remaining_cash < 0:
        return apology("Insufficient Funds")

    # If the user has enough cash, update the cash balance in the database and record the transaction in the transactions table
    else:
        db.execute("UPDATE users SET cash = ? WHERE id = ?", remaining_cash, user_id)

        date = datetime.datetime.now()

        db.execute("INSERT INTO transactions(user_id, symbol, name, shares, price, date, type) VALUES(?,?, ?, ?, ?, ?, ?)",
                   user_id, stock_symbol, stock_name, number, stock_price, date, "Buy")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get the user's transaction history from the transactions table, ordered by the timestamp in descending order
    transaction_info = db.execute(
        "SELECT date, type, symbol, price, shares FROM transactions WHERE user_id = ? ORDER BY date DESC", session["user_id"])
    # Render the history template, passing the transaction information and the usd function
    return render_template("history.html", transaction_info=transaction_info, usd=usd)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # If the request method is "GET", render the quote template
    if request.method == "GET":
        return render_template("quote.html")

    # If the request method is "POST"
    else:
        # Get the symbol from the form data
        symbol = request.form.get("symbol")

        # If the symbol is not entered, return an apology message
        if not symbol:
            return apology("Must enter symbol")

        # Look up the stock information for the given symbol
        stock = lookup(symbol.upper())

        # If the stock information is not found, return an apology message
        if stock == None:
            return apology("Symbol Does Not Exist")

        # Render the quoted template with the stock information
        return render_template("quoted.html", name=stock["name"], price=usd(stock["price"]),
                               symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If the request method is "GET", render the registration form template
    if request.method == "GET":
        return render_template("register.html")

    # If the request method is "POST", process the form submission
    else:
        # Get the submitted username, password, and password confirmation from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # If the username is not provided, return an apology
        if not username:
            return apology("Username Required")

        # If the password is not provided, return an apology
        if not password:
            return apology("Password Required")

        # If the password confirmation is not provided, return an apology
        if not confirmation:
            return apology("Confirmation Required")

        # If the password and password confirmation do not match, return an apology
        if password != confirmation:
            return apology("Passwords Do Not Match")

        # Hash the password using a secure hashing function
        hash = generate_password_hash(password)

        # Try to insert the new user into the database. If the username already exists, return an apology.
        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already exists")

        # Store the new user's ID in the session and redirect to the home page
        session["user_id"] = new_user
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get the user's ID from the session
    user_id = session["user_id"]

    # If the request method is "GET", render the sell form template
    if request.method == "GET":
        # Get the selected stock symbol from the query string
        temp = request.args.get("sell_symbol")
        # If no stock symbol was provided, set the sell symbol to an empty string
        if not temp:
            sell_symbol = ""
        # If a stock symbol was provided, set the sell symbol to that value
        else:
            sell_symbol = temp
        # Get a list of the stock symbols that the user owns from the transactions table
        stock_symbol = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", user_id)
        # Render the sell form template, passing the list of stock symbols and the sell symbol
        return render_template("sell.html", stock_symbol=stock_symbol, sell_symbol=sell_symbol)
    # If the request method is "POST", process the form submission
    else:
        # Get the selected stock symbol and the number of shares to sell from the form
        selected_stock_symbol = request.form.get("symbol")
        number = int(request.form.get("shares"))
        # Look up the current price of the selected stock
        selected_stock_price = lookup(selected_stock_symbol)["price"]
        # Look up the name of the selected stock
        selected_stock_name = lookup(selected_stock_symbol)["name"]
        # If the number of shares to sell is not positive, return an apology
        if number <= 0:
            return apology("Shares should be positive integer")
        # Get the total number of shares that the user owns of the selected stock from the transactions table
        current_shares_owned = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
                                          user_id, selected_stock_symbol)[0]["total_shares"]
        # If the user doesn't own enough shares to sell the requested number, return an apology
        if current_shares_owned < number:
            return apology("You don't have enough shares to sell")

        # Get the current cash balance of the user from the users table
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]
        # Update the user's cash balance by adding the proceeds from the sale
        db.execute("UPDATE users SET cash = ? WHERE id =?", (current_cash + (number * selected_stock_price)), user_id)
        # Insert a record into the transactions table to track the sale of the shares
        db.execute("INSERT INTO transactions(user_id, type, symbol, name, shares, price) VALUES(?, ?, ?, ?, ?, ?)",
                   user_id, "SELL", selected_stock_symbol, selected_stock_name, -number, selected_stock_price)
        # Redirect the user back to the index page
        return redirect("/")


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Add Cash"""

    # Get the user's current cash balance from the database
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # If the request method is "GET", render the add cash form template with the current cash balance
    if request.method == "GET":
        return render_template("add_cash.html", user_cash=usd(user_cash))

    # If the request method is "POST", process the form submission
    else:
        # Get the amount of cash to add from the form
        added_cash = request.form.get("added_cash")

        # Convert the current cash balance and the amount to add to floats and add them together
        new_total_cash = float(added_cash) + float(user_cash)

        # Update the user's cash balance in the database and record the cash addition in the transactions table
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_total_cash, session["user_id"])
        db.execute("INSERT INTO transactions(user_id, type, symbol, name, shares, price) VALUES(?, ?, ?, ?, ?, ?)",
                   session["user_id"], "ADD CASH", "N/A", "N/A", 1, float(added_cash))

        # Render the add cash form template with the updated cash balance
        return render_template("add_cash.html", user_cash=usd(new_total_cash))


@app.route("/changepassword", methods=["GET", "POST"])
def change_password():
    """Allow user to change their password"""

    # If the request method is "GET", render the change password form template
    if request.method == "GET":
        return render_template("changepassword.html")

    # If the request method is "POST", process the form submission
    else:
        # Get the current password, new password, and new password confirmation from the form
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        new_password_confirmation = request.form.get("confirm_new_password")

        # If the current password is not provided, return an apology
        if not current_password:
            return apology("You should input your current password")

        # Check that the current password is correct by comparing it to the hashed password stored in the database
        old_password = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])
        if len(old_password) != 1 or not check_password_hash(old_password[0]["hash"], current_password):
            return apology("invalid username and/or password", 403)

        # If the new password is not provided, return an apology
        if not new_password:
            return apology("You should input your new password")
        # If the new password confirmation is not provided, return an apology
        elif not new_password_confirmation:
            return apology("You should input your password in 'Confirmation New Password'")
        # If the new password and new password confirmation do not match, return an apology
        elif new_pw != new_password_confirmation:
            return apology("Password does not match")

    # Hash the new password using a secure hashing function
    hashed_new_password = generate_password_hash(new_password)

    # Update the user's hashed password in the database
    db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_new_password, session["user_id"])

    # Redirect the user to the logout page
    return redirect("/logout")


# Handle percentage output for index page
def percentage(value):
    """Format value as percentage. """
    return f"{value:,.2f}%"