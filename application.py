import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, get_flashed_messages, jsonify, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
import pyqrcode
import png
from datetime import datetime
import pytz
import calendar


from helpers import apology, login_required, lookup, usd, student_login_required, teacher_login_required


# Ensure environment variable is set

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
semester = "Spring 2018"





@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return render_template("about.html")


@app.route("/")
@login_required
def index():
    return redirect("/login")

@app.route("/login_mobile/check_login", methods=["GET","POST"])
def check_login():
    if session.get("user_id"):

        if session.get("student_id"):
            return jsonify(session["student_id"])

        elif session.get("teacher_id"):
            return jsonify(session["teacher_id"])

@app.route("/send_qr",methods=["POST"])
def s_qr():
    if request.method == "POST":
        if not request.form.get("qr_scan"):
            return jsonify("NULL",400)
        print(request.form.get("qr_scan"))
        return jsonify("Attendence Marked.",200)

@app.route("/login_mobile/student_post", methods=["POST"])
def login_mobile_student_post():

    if request.method == "POST":

        if request.form.get("rollnumber"):
            print(request.form.get("rollnumber"))
        # Ensure username was submitted
        if not request.form.get("rollnumber"):
            return apology("must provide roll number", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        print(request.form.get("password"))

        # Query database for username
        rows = db.execute("SELECT * FROM students WHERE roll_num = :username",
                          username=(request.form.get("rollnumber")).lower())

        if(not rows):
            print("Invalid Roll Number")
            return jsonify("Invalid Roll Number");
        print(rows[0])
        if(len(rows)!=1):
            print("Invalid Roll Number")
            return jsonify("Roll Number Not Registered.")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            print("Invalid password")
            return jsonify("invalid password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["student_id"] = rows[0]["id"]

        temp_str = ("Welcome back " + str(rows[0]["student_name"]).title() + ".")
        #flash(temp_str)
        # Redirect user to home page
        return jsonify(rows[0]);
    return redirect("/student_home")



@app.route("/login_mobile/student", methods=["POST"])
def login_mobile_student():

    if request.headers.method == "POST":


        if request.headers.get("rollnumber"):
            print(request.headers.get("rollnumber"))
        # Ensure username was submitted
        if not request.headers.get("rollnumber"):
            return apology("must provide roll number", 400)

        # Ensure password was submitted
        elif not request.headers.get("password"):
            return apology("must provide password", 400)
        print(request.headers.get("password"))

        # Query database for username
        rows = db.execute("SELECT * FROM students WHERE roll_num = :username",
                          username=(request.headers.get("rollnumber")).lower())

        print(rows[0])
        if(len(rows)!=1):
            return apology("Roll Number Not Registered.", 400)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.headers.get("password")):
            return apology("invalid password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["student_id"] = rows[0]["id"]

        temp_str = ("Welcome back " + str(rows[0]["student_name"]).title() + ".")
        #flash(temp_str)
        # Redirect user to home page
        return jsonify(rows[0]);
    return redirect("/student_home")

@app.route("/student_home",methods=["GET"])
@student_login_required
def stud_home():

    stud = db.execute("SELECT * FROM students WHERE id=:id_", id_=session['student_id'])
    print(stud)
    print(stud[0])
    cour = stud[0]['courses_reg'].split("|")
    print(cour)
    course_list = []
    course_code_dict = {}
    for each_course in cour:
        temp = each_course.split("-")
        course_code_dict[temp[0]] = temp[1]

        course_list.append(temp[0])

    delimit="\",\""
    course_str=delimit.join(course_list)
    course_str=str("\"" + course_str + "\"")
    print(course_str)
    all_cour=[]
    all_cour = db.execute("SELECT * FROM courses WHERE course_code IN(" + course_str + ")")
    return render_template("student_index.html", refresh=redirect,all_courses=all_cour, courses=all_cour, cd=course_code_dict)

@app.route("/teacher_home",methods=["GET"])
@teacher_login_required
def teacher_home():

    stud = db.execute("SELECT * FROM teachers WHERE id=:id_", id_=session['teacher_id'])
    print(stud)
    print(stud[0])
    cour = stud[0]['courses_reg'].split("|")
    print(cour)
    course_list = []
    course_code_dict = {}
    for each_course in cour:
        temp = each_course.split("-")
        course_code_dict[temp[0]] = temp[1]

        course_list.append(temp[0])

    delimit="\",\""
    course_str=delimit.join(course_list)
    course_str=str("\"" + course_str + "\"")
    print(course_str)
    all_cour=[]
    all_cour = db.execute("SELECT * FROM courses WHERE course_code IN(" + course_str + ")")
    return render_template("teacher_index.html", refresh=redirect,all_courses=all_cour, courses=all_cour, cd=course_code_dict)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if session.get("user_id"):

        if session.get("student_id"):
            return redirect("/student_home")

        elif session.get("teacher_id"):
            return redirect("teacher_home")

    # Forget any user_id
    session.clear()
    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")

@app.route("/login/student", methods=["GET","POST"])
def login_student():

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
        if(len(rows)!=1):
            return apology("Roll Number Not Registered.", 400)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid roll number and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["student_id"] = rows[0]["id"]

        temp_str = ("Welcome back " + str(rows[0]["student_name"]).title() + ".")
        flash(temp_str)
        # Redirect user to home page
        return redirect("/student_home")
    else:
        return render_template("login_student.html")

@app.route("/login/teacher", methods=["GET","POST"])
def login_teacher():

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("teacher_mail"):
            return apology("must provide NU mail id", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM teachers WHERE teacher_mail = :t",
                          t=(request.form.get("teacher_mail")).lower())
        if(len(rows)!=1):
            return apology("Teacher Not Registered.", 400)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid NU mail id and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["teacher_id"] = rows[0]["id"]

        temp_str = ("Welcome back " + str(rows[0]["teacher_name"]).title() + ".")
        flash(temp_str)
        # Redirect user to home page
        return redirect("/teacher_home")
    else:
        return render_template("login_teacher.html")





@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/mark_attendence",methods=["POST"])
@teacher_login_required
def mart_att():
    if request.method == "POST":
        if not request.form.get("course_c"):
            return apology("must provide course name.",400)

        course_short=request.form.get("course_c")
        hours=request.form.get("hours")
        date = request.form.get("date_class")
        print(course_short)
        print(hours)

        temp_str = "Attendence For " + str(course_short) + " Duration : "  +str(hours) + " On " + date

        at_str = str(course_short) + "|" + str(hours) + "|" + date + "|" + str(session['teacher_id']) + "|" + str(datetime.now(pytz.timezone("Asia/Karachi")).time())
        qr_url = pyqrcode.create(at_str)
        file_ad = "static/" + str(course_short) +".png"
        file_name = str(course_short) +".png"
        qr_url.png(file_ad,scale=20)
        pic = url_for('static',filename=file_name)
        flash(temp_str)
        return render_template("mark_attendence.html",qr_c=pic)




@app.route("/register/student",methods=["GET","POST"])
def register_student():
    print("STUDENT CLICKED")
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("rollnumber"):
            return apology("must provide rollnumber", 400)

        elif not request.form.get("student_name"):
            return apology("must provide name",400)

        elif not request.form.get("batch"):
            return apology("must provide batch year",400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password Again", 400)

        elif (request.form.get("password") != request.form.get("confirmation")):
            return apology("Passwords are not same.", 400)

        elif (db.execute("SELECT * FROM students WHERE roll_num = :roll", roll=request.form.get("rollnumber").lower())):
            return apology("Roll Number is already registered.", 400)

        rnum = request.form.get("rollnumber").lower()
        sname = request.form.get("student_name").lower()
        batch = request.form.get("batch")
        password = request.form.get("password")
        unique_id = int(rnum[4:]) + (int(rnum[:2])*1000000)

        course = db.execute("SELECT * FROM courses")
        course_cnt = 0
        course_code_w_section_temp = []
        for x in course:
            if request.form.get(str(x['course_code'])):
                course_code_w_section_temp.append(str(x['course_code']) + "-" + str(request.form.get(str(x['course_code']))))
                db.execute("UPDATE courses SET students_reg=students_reg + 1 WHERE course_code=:c_code", c_code=(x['course_code']))
                course_cnt = course_cnt + 1
        if(not course_code_w_section_temp):
            return apology("No Courses Selected.", 400)
        delimit = '|'
        course_code_w_section = delimit.join(course_code_w_section_temp)


        # Query database for username
        db.execute("INSERT INTO students (id,roll_num,student_name,num_courses,year,password,courses_reg) VALUES(:id_,:roll,:name,:cour,:y,:hash_pass,:cg)",
                   id_=(unique_id), roll=(str(rnum)).lower(), name=(sname).lower(), cour=course_cnt, y=int(batch), hash_pass=generate_password_hash(password), cg = str(course_code_w_section))

        rows = db.execute("SELECT * FROM students WHERE roll_num =:roll", roll=(str(rnum)).lower())
        # For login
        session["user_id"] = rows[0]['id']
        session["student_id"] = rows[0]['id']

        # Redirect user to home page
        temp_str = (str(rows[0]["student_name"]).title() + " is Registered.")
        flash(temp_str)
        return redirect("/student_home")
    else:
        courses_data = db.execute("SELECT * FROM courses")
        return render_template("register_student.html",courses=courses_data)
    return render_template("register_student.html",courses=courses_data)
        #return redirect("/register")

@app.route("/register/teacher",methods=["GET","POST"])
def register_teacher():
    if request.method == "POST":
        # Ensure username was submitted

        if not request.form.get("teacher_mail"):
            return apology("must provide Valid NU mail",400)

        elif not request.form.get("teacher_name"):
            return apology("must provide name",400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide password Again", 400)

        elif (request.form.get("password") != request.form.get("confirmation")):
            return apology("Passwords are not same.", 400)

        elif (db.execute("SELECT * FROM teachers WHERE teacher_mail = :ma", ma=request.form.get("teacher_mail").lower())):
            return apology("Teacher is already registered.", 400)

        tmail = request.form.get("teacher_mail").lower()
        tname = request.form.get("teacher_name").lower()
        password = request.form.get("password")


        course = db.execute("SELECT * FROM courses")
        course_cnt = 0
        course_code_w_section_temp = []
        str_course = "ncourser"
        str_course_cnt = 0;
        print(str_course + str(str_course_cnt))
        print(request.form.get(str_course + str(str_course_cnt)))
        while request.form.get(str_course + str(str_course_cnt)):
            print(str_course + str(str_course_cnt))

        for x in course:
            if request.form.get(str(x['course_code'])):
                course_code_w_section_temp.append(str(x['course_code']) + "-" + str(request.form.get(str(x['course_code']))))
                course_cnt = course_cnt + 1

        delimit = '|'
        course_code_w_section = delimit.join(course_code_w_section_temp)


        # Query database for username
        db.execute("INSERT INTO teachers (teacher_mail,teacher_name,course_cnt,courses_reg,password) VALUES(:tm,:name,:cour,:cr,:hash_pass)",
                   tm=tmail, name=tname, cour=course_cnt, cr=course_code_w_section, hash_pass=generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM teachers WHERE teacher_mail =:m", m=tmail)
        # For login
        session["user_id"] = rows[0]['id']
        session["teacher_id"] = rows[0]['id']

        # Redirect user to home page
        temp_str = (str(rows[0]["teacher_name"]).title() + " is Registered.")
        flash(temp_str)
        return redirect("/teacher_home")
    else:
        courses_data = db.execute("SELECT * FROM courses")
        return render_template("register_teacher.html",courses=courses_data)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
