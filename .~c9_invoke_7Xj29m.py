import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)
"""
import logging
logging.basicConfig(filename='error.log', level=logging.DEBUG)
"""

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
"""
 endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']

    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user)


# endpoint to show all users
@app.route("/user", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)

"""
"""
# endpoint to get user detail by id
@app.route("/user/<id_>", methods=["GET"])
def user_detail(id_):
    user=db.execute("SELECT * FROM users WHERE id=:idx", idx=id_)

    return jsonify(user)

"""
@app.route("/course/<cour>", methods=["GET"])
def course_detail(cour):
    c=db.execute("SELECT * FROM courses WHERE course_code=:co",co=cour)

    return jsonify(c)

@app.route("/course/<cour>/name", methods=["GET"])
def course_name_detail(cour):
    c=db.execute("SELECT course_name FROM courses WHERE course_code=:co",co=cour)

    return jsonify(c)

"""
# endpoint to update user
@app.route("/user/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']

    user.email = email
    user.username = username

    db.session.commit()
    return user_schema.jsonify(user)



# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)
"""


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return render_template("about.html")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    current_stocks = db.execute("SELECT * FROM s_numbers WHERE id=:user_id AND stock_quantity!=0", user_id=int(session['user_id']))
    rows = db.execute("SELECT * FROM users WHERE id=:user_id", user_id=int(session['user_id']))
    common_s_names = ["TSLA", "NFLX", "MSFT", "PG", "AAPL"]
    common_s = []
    for name in common_s_names:
        temp = lookup(name)
        if(temp):
            common_s.append(temp)
    return render_template("index.html", refresh=redirect, common_stocks=common_s, stack=(current_stocks), ac_cash=round(rows[0]['cash'], 2), stock_cash=round(rows[0]['cash_in_stocks'], 2))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        try:
            share_int = int(request.form.get("shares"))
        except:
            return apology("shares must be a positive integer", 400)

        if not request.form.get("symbol"):
            return apology("Enter Symbol of Stock", 400)
        if not request.form.get("shares"):
            return apology("Enter number of Stocks", 400)
        if (float(request.form.get("shares")) < 0):
            return apology("Invalid No. of shares", 400)
        if not (float(request.form.get("shares")).is_integer):
            return apology("Invalid No. of shares", 400)

        quotation = lookup(request.form.get("symbol"))
        if not quotation:
            return apology("Invalid Stock Name", 400)
        total_price = float(request.form.get("shares")) * float(quotation['price'])
        rows = db.execute("SELECT * FROM users WHERE id=:user_id", user_id=int(session['user_id']))

        if (total_price > rows[0]['cash']):
            return apology("Not Enough Cash In Account", 400)

        rows[0]['cash'] = rows[0]['cash'] - total_price

        db.execute("UPDATE users SET cash=:new_total,cash_in_stocks= cash_in_stocks + :s_cash  WHERE id=:user_id",
                   new_total=float(rows[0]['cash']), s_cash=total_price, user_id=int(rows[0]['id']))

        db.execute("INSERT INTO stocks (id,stock_name,stock_price,stock_quantity,stock_total_price) VALUES (:user_id,:s_name,:s_price,:s_quantity,:s_total)", user_id=int(rows[0]['id']), s_name=quotation['symbol'], s_price=quotation['price'],
                   s_quantity=request.form.get("shares"), s_total=total_price)
        second_db = db.execute("SELECT * FROM s_numbers WHERE stock_name=:s_name AND id=:user_id",
                               s_name=quotation['symbol'], user_id=int(rows[0]['id']))
        if second_db:
            db.execute("UPDATE s_numbers SET stock_price =:s_price,stock_quantity = stock_quantity + :s_quantity,stock_total_price = (stock_quantity + :s_quantity)* :s_price,times_purchased = times_purchased + 1 WHERE stock_name=:s_name AND id=:user_id",
                       s_price=quotation['price'], s_quantity=request.form.get("shares"),
                       s_name=quotation['symbol'], user_id=int(rows[0]['id']))
        else:
            db.execute("INSERT INTO s_numbers (id,stock_name,stock_price,stock_quantity,stock_total_price,times_purchased,times_sold) VALUES (:user_id,:s_name,:s_price,:s_quantity,:s_total,1,0)",
                       user_id=int(rows[0]['id']), s_name=quotation['symbol'], s_price=quotation['price'],
                       s_quantity=request.form.get("shares"), s_total=total_price)

        temp_str = (str(rows[0]["username"]).title() +
                    " has successfully bought " + str(request.form.get("shares")) + " " + str(request.form.get("symbol")) +
                    " share(s) worth " + (usd((total_price))) +
                    " - Price of one share is " + usd(quotation['price']) +
                    " - Remaining Balance : " + usd(rows[0]['cash'])
                    )
        flash(temp_str)
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    if request.method == "POST":
        db.execute("DELETE FROM stocks WHERE id=:user_id", user_id=int(session['user_id']))

    all_stocks = db.execute("SELECT * FROM stocks WHERE id=:user_id", user_id=int(session['user_id']))
    rows = db.execute("SELECT * FROM users WHERE id=:user_id", user_id=int(session['user_id']))

    return render_template("history.html", stack=all_stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    if session.get("user_id"):
        return redirect("/")

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("rollnumber"):
            return apology("must provide roll number", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM students WHERE roll_num = :username",
                          username=(request.form.get("rollnumber")).lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid roll number and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        temp_str = ("Welcome back " + str(rows[0]["student name"]).title() + ".")
        flash(temp_str)
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
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        quotation = lookup(request.form.get("symbol"))
        if not quotation:
            return apology("Invalid Stock Name", 400)
        some_str = "A share of " + str(quotation['symbol']) + " costs $ " + usd(quotation['price'])

        return render_template("quote.html", sstr=some_str)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("rollnumber"):
            return apology("must provide rollnumber", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password Again", 400)

        elif (request.form.get("password") != request.form.get("confirmation")):
            return apology("Passwords are not same.", 400)
        elif (db.execute("SELECT * FROM students WHERE roll_num = :username", username=request.form.get("rollnumber"))):
            return apology("Roll Number is already registered.", 400)






        # Query database for username
        db.execute("INSERT INTO students (roll_num,password) VALUES(:username,:hash_pass)", username=(request.form.get("rollnumber")).lower(),
                   hash_pass=generate_password_hash(request.form.get("password")))
        rows = db.execute("SELECT * FROM students WHERE roll_num = :username", username=(request.form.get("rollnumber")).lower())

        # For login
        session["user_id"] = 

        # Redirect user to home page
        temp_str = (str(rows[0]["student_name"]).title() + " is Registered.")
        flash(temp_str)
        return redirect("/")studstudents

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        courses_data = db.execute("SELECT * FROM courses")
        return render_template("register.html",courses=courses_data)
    #return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("No Symbol Selected", 406)
        if not request.form.get("shares"):
            return apology("Select Valid No. of Stocks", 400)
        if (float(request.form.get("shares")) < 0):
            return apology("Invalid No. of shares", 400)
        if not (float(request.form.get("shares")).is_integer):
            return apology("Invalid No. of shares", 400)

        quantity = int(request.form.get("shares"))
        symbol = request.form.get("symbol")

        sell_stock = db.execute("SELECT * FROM s_numbers WHERE id=:user_id AND stock_name=:s_name",
                                user_id=int(session['user_id']), s_name=symbol)
        if (quantity > sell_stock[0]["stock_quantity"]):
            return apology("Greater Number of Stocks selected", 400)

        quotation = lookup(request.form.get("symbol"))

        if not quotation:
            return apology("Market is DOWN. Try Again.", 500)

        total_price = float(request.form.get("shares")) * float(quotation['price'])

        rows = db.execute("SELECT * FROM users WHERE id=:user_id", user_id=int(session['user_id']))

        rows[0]['cash'] = rows[0]['cash'] + total_price

        db.execute("UPDATE users SET cash=:new_total,cash_in_stocks= cash_in_stocks - :s_cash  WHERE id=:user_id",
                   new_total=float(rows[0]['cash']), s_cash=total_price, user_id=int(rows[0]['id']))

        db.execute("INSERT INTO stocks (id,stock_name,stock_price,stock_quantity,stock_total_price) VALUES (:user_id,:s_name,:s_price,:s_quantity,:s_total)", user_id=int(
            rows[0]['id']), s_name=quotation['symbol'], s_price=quotation['price'], s_quantity=quantity * (-1), s_total=total_price)

        second_db = db.execute("SELECT * FROM s_numbers WHERE stock_name=:s_name AND id=:user_id",
                               s_name=quotation['symbol'], user_id=int(rows[0]['id']))
        if second_db:
            db.execute("UPDATE s_numbers SET stock_price =:s_price,stock_quantity = stock_quantity -:s_quantity ,stock_total_price = (stock_quantity - :s_quantity) * :s_price, times_sold = times_sold + 1 WHERE stock_name=:s_name AND id=:user_id",
                       s_price=quotation['price'], s_quantity=quantity, s_name=quotation['symbol'], user_id=int(rows[0]['id']))
        else:
            db.execute("INSERT INTO s_numbers (id,stock_name,stock_price,stock_quantity,stock_total_price,times_sold) VALUES (:user_id,:s_name,:s_price,:s_quantity,:s_total,1)", user_id=int(
                rows[0]['id']), s_name=quotation['symbol'], s_price=quotation['price'], s_quantity=quantity * (-1), s_total=total_price)

        temp_str = str(str(rows[0]["username"]).title() + " has successfully SOLD " + str(quantity) + " " + str(request.form.get("symbol")) +
                       " share(s) worth $" + usd(total_price) + " - Price of one share is " + usd(quotation['price']) + " - Remaining Balance : " + usd(rows[0]['cash']))
        flash(temp_str)
        return redirect("/")

    else:
        rows = db.execute("SELECT * FROM s_numbers WHERE id=:user_id AND stock_quantity!=0", user_id=int(session['user_id']))

    return render_template("sell.html", stack=rows)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
