from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from passlib.context import CryptContext
from tempfile import gettempdir
from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # define user currently logged in
    user = session["user_id"]

    # if user reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":

        # select the summary php table and the remaining cash for the user logged in
        table = db.execute("SELECT * FROM summary WHERE id = :user GROUP BY symbol", user=user)
        remain = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user)

        # create the variable total_value for cash on hand + shares value
        total_value = remain[0]["cash"]

        # create the rows current_price for the current price of shares and current_value for the total worth of each of the type
        # of shares owned by iterating through the table and add current_value to the total_value each time
        for row in table:
            row["current_price"] = round(lookup(row["symbol"])["price"], 2)
            row["current_value"] = row["quantity"] * row["current_price"]
            total_value = round(total_value + row["current_value"], 2)

        # render the html index template to display the table
        return render_template("index.html", table=table, remain=remain[0]["cash"], money=total_value)

    # add cash to balance functionality
    # if user reached route via POST (as by submitting a form via POST)
    else:
        # test case for no entry provided
        if request.form.get("cash") == "":
            return apology("You must provide a positive integer amount of money")

        # get cash to add from user input
        cash = request.form.get("cash")

        # verify that the cash to add is a digit
        if not cash.isdigit():
            return apology("You need to provide a number")
        else:
            cash = int(cash)

        # test case for negative number inputed
        if cash < 0:
            return apology("You must provide a positive integer amount of money")

        # update the php table users to reflect the new cash added
        db.execute("UPDATE users SET cash = cash + :cash WHERE id = :user", cash=cash, user=user)

        # render confirmation message
        flash("Cash Successfully Added!")

        # return to index after successfully adding cash
        return redirect(url_for("index"))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # test case for no entry provided
        if request.form.get("symbol") == "" or request.form.get("shares") == "":
            return apology("You must provide a stock symbol and the amount of shares to be bought")

        # grab the list containing the dictionnary with the information of the quote requested through Yahoo Finance
        quote = lookup(request.form.get("symbol"))

        # test case verify that the quote exists on Yahoo Finance
        if quote == None:
            return apology("Must provide valid stock symbol")
        else:
            # get quantity of shares to be bought from user input
            quantity = request.form.get("shares")

            # test case to verify that quantity is a number
            if not quantity.isdigit():
                return apology("You need to provide a number")
            else:
                quantity = int(quantity)

            # test case to prevent buying negative quantities
            if quantity < 0:
                return apology("You must provide a positive integer")

            # get id number (idno) and current cash from users php table for logged in user
            user = session["user_id"]
            cash = db.execute("SELECT cash FROM users WHERE id = :user", user=user)
            idno = db.execute("SELECT id FROM users WHERE id = :user", user=user)
            idno = idno[0]["id"]
            cash = cash[0]["cash"]

            # get information relative to requested share to buy
            symbol = quote["symbol"]
            price = round(quote["price"], 2)
            name = quote["name"]

            # calculate new remaining cash and the total value of the shares bought
            total = round(quantity * price, 2)
            remain = round(cash - total, 2)

            # create variable with $ sign to be displayed on html
            price_t = "${}".format(price)
            total_t = "${}".format(total)
            remain_t = "${}".format(remain)

            # test case to ensure user has enough money to buy the shares
            if total > cash:
               return apology("You don't have enough money!")
            else:
                # insert a new row into transactions php table to reflect the new buying transaction that was completed.
                db.execute("INSERT INTO transactions (id, symbol, name, price, quantity, total, remain) VALUES (:idno, :symbol, :name, :price, :quantity, :total, :remain)", idno=idno, symbol=symbol, name=name, price=price_t, quantity=quantity, total=total_t, remain=remain_t)

                # update users php table to reflect the new remaining cash the user has
                db.execute("UPDATE users SET cash = :remain WHERE id = :user", remain=remain, user=user)

                # check if the user already owns some of the shares just bought in his summary table.
                if len(db.execute("SELECT * FROM summary WHERE symbol = :symbol", symbol=symbol)) != 0:
                    # update the row containing the shares to reflect the new amount of shares owned for this type since
                    db.execute("UPDATE summary SET quantity = quantity + :quantity WHERE symbol = :symbol", quantity=quantity, symbol=symbol)
                else:
                    # create a new row in the summary php table since the user now owns some of these shares
                    db.execute("INSERT INTO summary (id, symbol, name, quantity, buyprice) VALUES (:idno, :symbol, :name, :quantity, :buyprice)", idno=idno, symbol=symbol, name=name, quantity=quantity, buyprice=price_t)

                # render success message
                flash("Bought!")

                # redirect user to main page
                return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    # if user reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":

        # define currently logged in user
        user = session["user_id"]

        # create a table variable containing all the information from the transactions table for the user currently logged in
        table = db.execute("SELECT * FROM transactions WHERE id = :user", user=user)

        # select cash currently owned by user from users php table
        remain = db.execute("SELECT cash from users where id = :user", user=user)

        # create the rows current_price for the current price of shares and current_value for the total worth of each of the type
        # of shares owned by iterating through the table
        for row in table:
            row["current_price"] = round(lookup(row["symbol"])["price"], 2)
            # display a negative cash value for shares bought and positive one for the shares sold
            row["current_value"] = -row["quantity"] * row["current_price"]

        # return html template for history
        return render_template("history.html", table=table)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
#            print(request.form.get("password"))
#            print(rows[0]["hash"])
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # test case for no entry provided
        if not request.form.get("quote"):
            return apology("Must provide quote")
        else:
            # get quote information from Yahoo Finance using lookup
            quote = lookup(request.form.get("quote"))

            # test case for quote entry not existing
            if quote == None:
                return apology("Must provide an existing quote symbol")
            else:
                # define text to be outputted and render it in html
                text = "A share of {} ({}) costs ${}.".format(quote["name"], quote["symbol"], quote["price"])
                return render_template("quoted.html", display_text=text)

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # test case for no entry provided
        if request.form.get("username") == "" or request.form.get("password") == "" or request.form.get("confirmation") == "":
            return apology("Must provide username and password!")

        # test for passwords not matching
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords don't match!")

        # test case to verify that the username is not already taken
        elif len(db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))) != 0:
            return apology("Username already taken")
        else:
            # get password from user entry and encrypt it
            password=request.form.get("password")

            hash_password = pwd_context.hash(password)
#            hash_password = CryptContext.hash(password, scheme=None)

            # insert into users php table the username from user input and the hash of the password
            db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash_pass)", username=request.form.get("username"), hash_pass=hash_password)

            # return to main page
            return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # test case for no entry entered
        if request.form.get("symbol") == "" or request.form.get("shares") == "":
            return apology("You must provide a stock symbol and the amount of shares to be sold")

        # get quote information from Yahoo Finance using lookup and get the quantity to be sold from user input
        quote = lookup(request.form.get("symbol"))
        quantity = request.form.get("shares")

        # test case to verify that the quantity to be sold is a number
        if not quantity.isdigit():
            return apology("You need to provide a number")
        else:
            quantity = int(quantity)

        # select amount of the type of shares requested the user already owns
        amount_owned = db.execute("SELECT quantity FROM summary WHERE symbol = :symbol", symbol=quote["symbol"])

        # test case to verify that the user owns this type of shares
        if amount_owned == []:
            return apology("You don't own any of these shares!")

        # get value from list and dictionnary of the table
        amount_owned = amount_owned[0]["quantity"]

        # verify that the share requested exist
        if quote == None:
            return apology("Must provide valid stock symbol")
        else:
            # test case to verify that the quantity of shares to be sold is positive
            if quantity < 0:
                return apology("You must provide a positive integer")

            # test case to verify that the user is not selling more shares than he owns
            if quantity > amount_owned:
                return apology("You don't own that many shares!")

            # get id number (idno) and current cash from users php table for logged in user
            user = session["user_id"]
            cash = db.execute("SELECT cash FROM users WHERE id = :user", user=user)
            idno = db.execute("SELECT id FROM users WHERE id = :user", user=user)
            idno = idno[0]["id"]
            cash = cash[0]["cash"]

            # get information relative to requested share to sell
            symbol = quote["symbol"]
            price = quote["price"]
            name = quote["name"]

            # calculate new remaining cash and the total value of the shares sold
            total = round(quantity * price, 2)
            remain = round(cash + total, 2)

            # create variable with $ sign to be displayed on html
            price_t = "${}".format(price)
            total_t = "${}".format(total)
            remain_t = "${}".format(remain)

            # set quantity negative to reflect the fact that they have been sold and the number owned by user has decreased
            quantity = -quantity

            # insert into transactions php table a new row to reflect the new transaction that was completed
            db.execute("INSERT INTO transactions (id, symbol, name, price, quantity, total, remain) VALUES (:idno, :symbol, :name, :price, :quantity, :total, :remain)", idno=idno, symbol=symbol, name=name, price=price_t, quantity=quantity, total=total_t, remain=remain_t)

            # update users php table to reflect the new cash on hand of the user
            db.execute("UPDATE users SET cash = :remain WHERE id = :user", remain=remain, user=user)

            # update summary php table to reflect the new quantity of shares owned by user
            db.execute("UPDATE summary SET quantity = quantity + :quantity WHERE symbol = :symbol", quantity=quantity, symbol=symbol)

            # check if the quantity after transaction of the type of shares sold is 0 and delete the row from the table if it is
            if db.execute("SELECT quantity FROM summary WHERE symbol = :symbol", symbol=symbol)[0]["quantity"] == 0:
                db.execute("DELETE FROM summary WHERE symbol = :symbol", symbol=symbol)

            # render confirmation message
            flash("Sold!")

            # redirect to main page
            return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("sell.html")
