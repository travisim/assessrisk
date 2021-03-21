import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import time
from helpers import apology, login_required, lookup, usd
import re

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True



# Ensure responses aren't cached
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
#db = SQL("sqlite:///database.db")
#or
db = SQL(os.getenv("postgres://olqqcvqhgevtmv:8bf40c6a649bbfdc954f42216a5bdf71c1f4f5842e308f71fd30449ae93b7b92@ec2-52-71-231-37.compute-1.amazonaws.com:5432/d87103joqnghkp"))
db = SQL(os.getenv("DATABASE_URL"))

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        password = request.form.get("password")

        length_error = len(password) < 8
        # searching for digits
        digit_error = re.search(r"\d", password) is None

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None

        # searching for symbols
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

        # overall result
        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

        if password_ok == False:
            return apology("must satisfy password requirements", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match",400)

        try:
            k = db.execute("INSERT INTO users (username,hash) VALUES (?,?)",
            request.form.get("username"),
            generate_password_hash(request.form.get("password")))


        except:
            return apology("user exists already", 400)

        if k is None:
            return apology("registration failed", 403)
        session["user_id"] = k
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        #Ensure username was submitted
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


@app.route("/logout", )
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def form():
    if request.method == "POST":

        if not request.form.get("activity"):
            return apology("must provide activity", 400)
        if not request.form.get("water"):
            return apology("must provide water drank", 400)
        if not request.form.get("temp"):
            return apology("must provide temperature", 400)
        activity = request.form.get("activity")
        water = request.form.get("water")
        temp = request.form.get("temp")
        qlist = list(map(int, request.form.getlist("q")))


        for i in range(1,13,1):
            globals()["q" + str(i)]= "no"
        for i in qlist:
            globals()["q" + str(i)]= "yes"
        db.execute("""
            INSERT INTO history(user_id,activity,water,temp,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            session["user_id"],
            activity,
            water,
            temp,
            q1,
            q2,
            q3,
            q4,
            q5,
            q6,
            q7,
            q8,
            q9,
            q10,
            q11,
            q12
        )


        flash("Form submitted","sucess")
        return  redirect("/")
    else:
        return render_template("index.html")




@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":



        if request.form['submit_button'] != 'Report Sick':
            return apology("must provide activity", 400)

        flash("Reported Sick","sucess")
        return  redirect("/")
    else:
        return render_template("report.html")













@app.route("/history")
@login_required
def history():
    history = db.execute("""
        SELECT activity,water,temp,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12
        FROM history
        WHERE user_id = ?
    """, session["user_id"])
    #j = 1
    #for i in range(len(history)):
      # print(history[i]["q" + str(j)])



    return render_template("history.html",history = history)












def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
#-----------------------------------------------------------------------------













