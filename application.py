import calendar
import os
from datetime import datetime
from tempfile import mkdtemp

import colorama
import png
import pyqrcode
import pytz
import sendgrid
from cs50 import SQL
from flask import (Flask, flash, get_flashed_messages, jsonify, redirect,
                   render_template, request, send_file, session, url_for)
from flask_session import Session
from sendgrid.helpers.mail import *
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import (apology, login_required, lookup, student_login_required,
                     teacher_login_required, usd)
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker    
from table_classes import *


# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

# Ensure environment variable is set
sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# For colored output on terminal
colorama.init()
"""
import logging
logging.basicConfig(filename='error.log', level=logging.DEBUG)
"""




# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")
# p_studs is DB of Students Courses not verified by teacher of course

# Set Current Semester
semester_list = ["Fall", "Spring", "Summer"]
current_semester = str(semester_list[0]) + str(2018)



# Setting up postgres DataBase
# 
# 
db_string = "postgresql://frpswaheyyrcda:cc7c80c84ac73b88483a235dd381eab4e013506eb84c0190676bbc3f16b55e65@ec2-54-235-178-189.compute-1.amazonaws.com:5432/d904mj7g7okbjj" 
pdb = create_engine(db_string)
base = declarative_base()

@app.route("/students/",methods=["GET"])
def all_students_from_pdb():
    pdb_Session = sessionmaker(pdb)
    pdb_session = pdb_Session()
    # base.metadata.create_all(pdb)
    all_students = pdb_session.query(students)
    student_list = []
    s_list = []
    for student in all_students:
        student_list.append(student.data_dict())
        s_list.append(student.student_name)
    # print(student_list)
    return jsonify(student_list)

@app.route('/a_stud',methods=["GET"])
def all_active_stud():
    pdb_Session = sessionmaker(pdb)
    pdb_session = pdb_Session()

    all_active_s = pdb_session.query(a_stud)
    a_stud_list = []
    for active_stud in all_active_s:
       a_stud_list.append(active_stud.data_dict())
    return jsonify(a_stud_list)    

@app.route('/p_stud', methods=['GET'])
def all_pending_stud():
    pdb_Session = sessionmaker(pdb)
    pdb_session = pdb_Session()

    all_pending_s = pdb_session.query(p_stud)
    p_stud_list = []
    for pending_stud in all_pending_s:
        p_stud_list.append(pending_stud.data_dict())
    return jsonify(p_stud_list)

def ret_sec(comb):  # comb is list or string of courses
    if isinstance(comb, list):
        sec_list = []
        for i in comb:
            temp_l = i.split("-")
            sec_list.append(temp_l[1])
        return sec_list
    if isinstance(comb, str):
        temp_l = comb.split("-")
        print("hsdsd" + str(temp_l))
        temp_s = temp_l[1]
        return temp_s

    return

# IDR THIS Returns Courses in list with string input i.e: EL213-E|EE213-E|CS201-E|CL201-E|CS211-E|MT104-E|MG220-GR2 or EL213-E


def ret_cour_list(comb):  # comb is list or string of courses
    if isinstance(comb, list):
        sec_list = []
        for i in comb:
            temp_l = i.split("-")
            sec_list.append(temp_l[0])
        return sec_list
    if isinstance(comb, str):
        temp_l = comb.split("-")
        return temp_l

    return


def ret_index(comb, index=0):  # comb is list or string of courses
    if isinstance(comb, list):
        sec_list = []
        for i in comb:
            temp_l = i.split("-")
            sec_list.append(temp_l[index])
        return sec_list
    if isinstance(comb, str):
        temp_l = comb.split("-")
        print("hsdsd" + str(temp_l))
        temp_s = temp_l[index]
        return temp_s

    return

# Returns list of courses with dictionatry of info such as section,course short etc
# Takes Input of list returned by db.execute when SELECT from students or teachers


def ret_courses(rows):
    # print(rows)
    # print(rows[0])
    cour = rows[0]['courses_reg'].split("|")
    # print(cour)
    course_list = []
    semester_list = []
    course_code_dict = {}
    for each_course in cour:
        temp = each_course.split("-")
        course_code_dict[temp[0]] = temp[1]
        course_list.append(temp[0])
        semester_list.append(temp[2])

    delimit = "\",\""
    course_str = delimit.join(course_list)
    course_str = str("\"" + course_str + "\"")
    # print(course_str)
    # print(ret_sec(cour))
    # print(ret_index(cour,0))

    c_sec_list = ret_sec(cour)
    course_code_list = ret_index(cour, 0)
    all_cour = []
    all_cour = db.execute(
        "SELECT * FROM courses WHERE course_code IN(" + course_str + ")")

    #print("courses: " + str(all_cour))
    cnt = 0
    course_dict_list2 = []
    for x in course_code_list:
        temp_course_list = next(i for i in all_cour if i["course_code"] == x)
        # print(temp_course_list)
        course_dict_list2.append({"id": temp_course_list["id"], "course_name": temp_course_list["course_name"],
                                  "course_short": temp_course_list["course_short"], "course_code": temp_course_list["course_code"],
                                  "course_sec": c_sec_list[cnt], "semester": semester_list[cnt],
                                  "course_unique": str(str(temp_course_list["course_code"]) + "-" + str(c_sec_list[cnt]) + "-" + str(semester_list[cnt]))})
        cnt = cnt+1

    # print(course_dict_list2)
    return course_dict_list2


# Returns Pending Courses For Approval for teacher
def ret_p_courses(list_courses):

    course_list_codes = []
    for each_course in list_courses:
        course_list_codes.append(str(each_course['course_code']) + "-" + str(
            each_course['course_sec']) + "-" + str(current_semester))

    delimit = "\",\""
    course_str = delimit.join(course_list_codes)
    course_str = str("\"" + course_str + "\"")

    all_cour = []
    all_cour = db.execute(
        "SELECT * FROM p_stud WHERE course_unique IN(" + course_str + ")")

    print(all_cour)
    return all_cour


# Returns Courses like
"""
[{'id': 15, 'course_name': 'data structures', 'course_short': 'DS', 'course_code': 'CS201', 'section': 'A'},
{'id': 16, 'course_name': 'data structures lab', 'course_short': 'DS Lab', 'course_code': 'CL201', 'section': 'B'},
{'id': 17, 'course_name': 'digital logic design', 'course_short': 'DLD', 'course_code': 'EE227', 'section': 'A'},
{'id': 18, 'course_name': 'digital logic design lab', 'course_short': 'DLD Lab', 'course_code': 'EL227', 'section': 'A'},
{'id': 23, 'course_name': 'marketing management', 'course_short': 'MM', 'course_code': 'MG220', 'section': 'GR2'}]
"""
# Takes input only course Codes


def ret_courses_take_code(list_courses):

    course_list_codes = []
    for each_course in list_courses:
        course_list_codes.append(str(each_course['course_code']))

    delimit = "\",\""
    course_str = delimit.join(course_list_codes)
    course_str = str("\"" + course_str + "\"")

    all_cour = []
    all_cour = db.execute(
        "SELECT * FROM courses WHERE course_code IN(" + course_str + ")")

    cnt = 0
    course_dict_list2 = []
    for x in course_list_codes:
        temp_course_list = next(i for i in all_cour if i["course_code"] == x)
        # print(temp_course_list)
        course_dict_list2.append({"id": temp_course_list["id"], "course_name": temp_course_list["course_name"],
                                  "course_short": temp_course_list["course_short"], "course_code": temp_course_list["course_code"], "section": list_courses[cnt]['section']})
        cnt = cnt+1

    # print(course_dict_list2)
    return course_dict_list2


def ret_courses_section_take_code(list_courses):

    course_list_codes = []
    for each_course in list_courses:
        course_list_codes.append(str(each_course['course_code']))

    delimit = "\",\""
    course_str = delimit.join(course_list_codes)
    course_str = str("\"" + course_str + "\"")

    all_cour = []
    all_cour = db.execute(
        "SELECT * FROM courses WHERE course_code IN(" + course_str + ")")

    cnt = 0
    course_dict_list2 = []
    for x in course_list_codes:
        temp_course_list = next(i for i in all_cour if i["course_code"] == x)
        # print(temp_course_list)
        course_dict_list2.append({"id": temp_course_list["id"], "course_name": temp_course_list["course_name"], "course_short": temp_course_list[
                                 "course_short"], "course_code": temp_course_list["course_code"], "section": list_courses[cnt]['course_sec']})
        cnt = cnt+1

    # print(course_dict_list2)
    return course_dict_list2


# Returns Course name with section in str
"""

"""
# Takes input only course Codes


def ret_course_name_take_code(list_courses):

    course_list_codes = []
    for each_course in list_courses:
        course_list_codes.append(str(each_course['course_code']))

    delimit = "\",\""
    course_str = delimit.join(course_list_codes)
    course_str = str("\"" + course_str + "\"")

    all_cour = []
    all_cour = db.execute(
        "SELECT * FROM courses WHERE course_code IN(" + course_str + ")")

    cnt = 0
    course_dict_list2 = []
    course_name_w_sec = " "
    for x in course_list_codes:
        temp_course_list = next(i for i in all_cour if i["course_code"] == x)
        # print(temp_course_list)
        course_name_w_sec += (str(temp_course_list["course_short"].upper(
        ) + "-" + str(list_courses[cnt]['section']) + "|"))
        cnt = cnt+1

    # print(course_dict_list2)
    return course_name_w_sec


# Takes input only course Codes RETURNS Registered Courses List
def ret_courses_reg(list_courses):

    course_list_codes = []
    for each_course in list_courses:
        course_list_codes.append(str(each_course['course_code']))

    delimit = "\",\""
    course_str = delimit.join(course_list_codes)
    course_str = str("\"" + course_str + "\"")

    all_cour = []
    all_cour = db.execute(
        "SELECT * FROM courses WHERE course_code IN(" + course_str + ")")

    cnt = 0
    course_dict_list2 = []
    for x in course_list_codes:
        temp_course_list = next(i for i in all_cour if i["course_code"] == x)
        # print(temp_course_list)
        course_dict_list2.append({"id": temp_course_list["id"], "course_name": temp_course_list["course_name"],
                                  "course_short": temp_course_list["course_short"], "course_code": temp_course_list["course_code"],
                                  "section": list_courses[cnt]['section'], 'teacher_name': list_courses[cnt]['teacher_name'], "semester": list_courses[cnt]['semester'], "teacher_mail": list_courses[cnt]['teacher_mail']})
        cnt = cnt+1
    # print(course_dict_list2)
    return course_dict_list2


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
    c = db.execute("SELECT * FROM courses WHERE course_code=:co", co=cour)

    return jsonify(c)


@app.route("/course/<cour>/name", methods=["GET"])
def course_name_detail(cour):
    c = db.execute(
        "SELECT course_name FROM courses WHERE course_code=:co", co=cour)

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


@app.route("/mail", methods=["GET"])
def mail():
    from_email = Email("FASTQRAS@nu.edu.pk")
    to_email = Email("k173654@nu.edu.pk")
    subject = "TEST FROM CS50"
    content = Content("text/plain", "Hello This is COAL QRAS FAST NUCES.")

    mail = Mail(from_email, subject, to_email, content)
    print(mail)
    sg.client.mail.send.post(request_body=mail.get())
    #responses = sg.client.mail.send.post(mail.get())
#   print(responses.status_code)
#    print(responses.body)
#    print(responses.headers)
    return redirect("/")


@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    return render_template("about.html")


@app.route("/active_courses", methods=["GET"])
def active_cour():
    if request.method == "GET":
        active_courses = db.execute("SELECT * FROM active_courses")
        return render_template("active_courses.html", ac=active_courses)


@app.route("/active_students", methods=["GET"])
def active_stud():
    if request.method == "GET":
        active_students = db.execute("SELECT * FROM students")
        return render_template("active_students.html", ac=active_students)


@app.route("/")
@login_required
def index():
    return redirect("/login")


@app.route("/login_mobile/check_login", methods=["GET", "POST"])
def check_login():
    if session.get("user_id"):

        if session.get("student_id"):
            return jsonify(session["student_id"])

        elif session.get("teacher_id"):
            return jsonify(session["teacher_id"])


@app.route("/send_qr", methods=["POST"])
def s_qr():
    if request.method == "POST":
        if not request.form.get("qr_scan"):
            return jsonify("NULL", 400)
        if request.form.get("rollnumber"):
            print(request.form.get("rollnumber"))

        data_str = request.form.get("qr_scan")
        rollnum = request.form.get("rollnumber")
        data = data_str.split("|")
        student = db.execute(
            "SELECT * FROM STUDENTS where roll_num=:roll", roll=rollnum)
        if not student:
            return jsonify("Rollnumber Not Registered.", 200)
        print("Data Recevied From Mobile : " + str(data))
        print("Rollnumber : " + str(rollnum))

        roll_num = rollnum

        session["user_id"] = student[0]["id"]
        session["student_id"] = student[0]["id"]
        session["student_roll_num"] = roll_num

        active_course_codes = db.execute(
            "SELECT * FROM a_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
        active_courses = ret_courses_reg(active_course_codes)
        pending_course_codes = db.execute(
            "SELECT * FROM p_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
        pending_courses = ret_courses_take_code(pending_course_codes)
        session["courses_student_pending"] = pending_courses
        session["courses_student_registered"] = active_courses
        # print(student[0]['courses_reg'])
        # cour_student = ret_courses(student) #returns list of courses with dictionatry of info such as section,course short etc

        if not session.get("courses_student_registered"):
            print("Student Is Not Registered In This Course. No Courses", 400)
            return jsonify("Course Not Registered")

        cour_student = session["courses_student_registered"]

        course_info = {}

        for x in cour_student:
            if x['course_code'] == data[0] and x['section'] == data[1] and x['semester'] == data[2]:
                print(x)
                print("Course is Registered by Student.")
                course_info = x
                break

        if not course_info:
            print("Student Is Not Registered In This Course.", 200)
            return jsonify("Student Is Not Registered In This Course.", 200)
        print(course_info)
        print("Min Limit :" + str(data[7]))
        curr_time = str(datetime.now(pytz.timezone("Asia/Karachi")).time())
        date_time = str(datetime.now(pytz.timezone("Asia/Karachi")).date())
        course_uni = str(x['course_code']) + "-" + \
            str(x['section']).upper() + "-" + str(x['semester'])

        fmt = '%Y-%m-%d %H:%M:%S'
        print(data[6].split(".")[0])
        d1 = datetime.strptime(
            str(data[4].split(".")[0]) + " " + str(data[6].split(".")[0]), fmt)
        d2 = datetime.strptime(
            date_time + " " + str(curr_time.split(".")[0]), fmt)
        print("d1 d2" + str(d1) + str(d2))
        datetime_start = d1
        datetime_end = d2
        minutes_diff = (datetime_end - datetime_start).total_seconds() / 60.0
        print("Minutes Diff : " + str(minutes_diff))
        if(int(minutes_diff) > int(data[7])):
            print("Time Diff Greate")
            return jsonify("Attendence Closed", 400)

        update_stud = db.execute("UPDATE attendence SET attendence_time=:currtime_t,state=:type_t WHERE course_unique=:cuni_t AND roll_number=:roll_t AND class_date_t=:date_t AND state=:state_t",
                                 currtime_t=curr_time, type_t="P", cuni_t=course_uni, roll_t=session['student_roll_num'], date_t=date_time, state_t="A")

        if not update_stud:
            print("Attendence NOT UPDATED")
            return jsonify("NO Attendence or Attendence Already Marked", 400)

        #print("cour_student = " + str(cour_student))

        return jsonify("Attendence Marked.", 200)


@app.route("/login_mobile/student_attendance", methods=["POST"])
def mobile_student_attendence():
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
            return jsonify("Invalid Roll Number")
        print(rows[0])
        if(len(rows) != 1):
            print("Invalid Roll Number")
            return jsonify("Roll Number Not Registered.")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            print("Invalid password")
            return jsonify("invalid password")

        roll_num = request.form.get("rollnumber")
        course_dict_list2 = ret_courses(rows)
        print("LOGIN BY : " + str(course_dict_list2))
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["student_id"] = rows[0]["id"]
        session["student_roll_num"] = roll_num
        session["courses_student"] = course_dict_list2
        active_course_codes = db.execute(
            "SELECT * FROM a_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
        active_courses = ret_courses_reg(active_course_codes)
        pending_course_codes = db.execute(
            "SELECT * FROM p_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
        pending_courses = ret_courses_take_code(pending_course_codes)
        session["courses_student_pending"] = pending_courses
        session["courses_student_registered"] = active_courses

        return redirect("/student/view")


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
            return jsonify("Invalid Roll Number")
        print(rows[0])
        if(len(rows) != 1):
            print("Invalid Roll Number")
            return jsonify("Roll Number Not Registered.")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            print("Invalid password")
            return jsonify("invalid password")

        roll_num = request.form.get("rollnumber")

        course_dict_list2 = ret_courses(rows)
        print("LOGIN BY : " + str(course_dict_list2))
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["student_id"] = rows[0]["id"]
        session["student_roll_num"] = roll_num
        session["courses_student"] = course_dict_list2
        active_course_codes = db.execute(
            "SELECT * FROM a_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
        active_courses = ret_courses_reg(active_course_codes)
        pending_course_codes = db.execute(
            "SELECT * FROM p_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
        pending_courses = ret_courses_take_code(pending_course_codes)
        session["courses_student_pending"] = pending_courses
        session["courses_student_registered"] = active_courses
        print("Registered Course ->> " +
              str(session["courses_student_registered"]))

        # flash(temp_str)
        # Redirect user to home page
        course_name_w_section_active = ret_course_name_take_code(
            active_course_codes)
        course_name_w_section_pending = ret_course_name_take_code(
            pending_course_codes)

        print(course_name_w_section_active)
        print(course_name_w_section_pending)

        return jsonify(str(rows[0]['student_name']) + "," + str(len(active_course_codes)) + "," + str(course_name_w_section_active)
                       + "," + str(len(pending_course_codes)) + "," + str(course_name_w_section_pending))

    return redirect("/student_home")


@app.route("/student_home", methods=["GET"])
@student_login_required
def stud_home():
    active_course_codes = db.execute(
        "SELECT * FROM a_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
    active_courses = ret_courses_reg(active_course_codes)
    pending_course_codes = db.execute(
        "SELECT * FROM p_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
    pending_courses = ret_courses_take_code(pending_course_codes)

    session["courses_student_pending"] = pending_courses
    session["courses_student_registered"] = active_courses

    courses_complete = session["courses_student"]
    pending_courses = session["courses_student_pending"]
    active_courses = session["courses_student_registered"]
    return render_template("student/index.html", refresh=redirect, cc=courses_complete, ac=active_courses, pc=pending_courses, cinfo=session["courses_student"])


@app.route("/teacher_home", methods=["GET", "POST"])
@teacher_login_required
def teacher_home():
    """LEGACY CODE OBSELETE BY ret_courses() func"""
    """
    rows = db.execute("SELECT * FROM teachers WHERE id = :t",
                          t=session['teacher_id'])


    p_courses = ret_p_courses(rows)
    print(rows)
    """
    if request.method == "GET":
        courses_complete = session["courses_teacher"]
        return render_template("teacher/index.html", refresh=redirect, cc=courses_complete)


@app.route("/teacher/approve", methods=["GET", "POST"])
@teacher_login_required
def teacher_approve():
    if request.method == "POST":
        if not request.form.get("student_name"):
            return apology("NO NAME", 400)
        sname = request.form.get("student_name")
        if not request.form.get("rollnumber"):
            return apology("NO ROLLNUMBER", 400)
        roll_num = request.form.get("rollnumber")
        if not request.form.get("course_code"):
            return apology("NO CODE", 400)
        ccode = request.form.get("course_code")
        if not request.form.get("section"):
            return apology("NO SECTION", 400)
        csec = request.form.get("section")
        if not request.form.get("semester"):
            return apology("NO SEMESTER", 400)
        csem = request.form.get("semester")
        if not request.form.get("batch"):
            return apology("NO BATCH", 400)
        sbatch = request.form.get("batch")

        course_uni = str(ccode) + "-" + str(csec).upper() + "-" + str(csem)

        from_p = db.execute(
            "SELECT * FROM p_stud WHERE roll_num=:roll_t AND course_unique=:cuni_t", roll_t=roll_num, cuni_t=course_uni)
        db.execute("INSERT INTO a_stud (student_name,roll_num,batch,course_code,semester,course_unique,teacher_name,section,teacher_mail) VALUES(:sname_t,:roll_t,:batch_t,:ccode_t,:csem_t,:cuni_t,:tname_t,:csec_t,:tmail_t)",
                   sname_t=sname, roll_t=roll_num, batch_t=sbatch, ccode_t=ccode, csem_t=csem, cuni_t=course_uni, tname_t=session['teacher_name'], csec_t=csec, tmail_t=session['teacher_mail'])
        db.execute("DELETE FROM p_stud WHERE roll_num=:roll_t AND course_unique=:cuni_t",
                   roll_t=roll_num, cuni_t=course_uni)

        courses_complete = session["courses_teacher"]
        course_to_approve = ret_p_courses(courses_complete)
        return render_template("teacher/approve.html", refresh=redirect, cc=courses_complete, ac=course_to_approve)

    if request.method == "GET":
        courses_complete = session["courses_teacher"]
        course_to_approve = ret_p_courses(courses_complete)
        return render_template("teacher/approve.html", refresh=redirect, cc=courses_complete, ac=course_to_approve)


@app.route("/teacher/view", methods=["GET"])
@teacher_login_required
def teacher_view():
    if request.method == "GET":
        courses_complete = session['courses_teacher']
        attendence_courses = []
        sadi_attendence = []
        for x in courses_complete:
            temp = db.execute("SELECT * FROM attendence WHERE teacher_mail=:tmail_t AND course_unique=:cunit_t",
                              tmail_t=session['teacher_mail'], cunit_t=str(x['course_code'] + "-" + x['course_sec'] + "-" + x['semester']))
            sadi_attendence.append(temp)
            date_list = {}
            if temp:
                i = 0
                while i < len(temp):
                    flag = 0
                    t_list = []
                    date_temp = temp[i]['class_date_t']
                    while i < len(temp) and date_temp == temp[i]['class_date_t']:
                        print(temp[i])
                        t_list.append(temp[i])
                        i = i+1
                        flag = 1
                    date_list[date_temp] = t_list
                    if flag == 0:
                        i = i+1
                print("date list : " + str(date_list))
            attendence_courses.append(date_list)
        # print("Course_complete :")
        # print(courses_complete)
        # print("NEW ATT : ")
        # print(attendence_courses)
        # print("SADI ATT:")
        # print(sadi_attendence)
        key_list = []
        for i in range(0, len(attendence_courses)):
            key_list.append(list(attendence_courses[i].keys()))

        return render_template("teacher/view.html", cc=courses_complete, ac=sadi_attendence, nc=attendence_courses, kl=key_list)


@app.route("/teacher/my_students", methods=["GET"])
@teacher_login_required
def teacher_students():
    if request.method == "GET":
        only_courses = session['courses_teacher']
        print(only_courses)
        my_list = []
        for x in only_courses:
            temp = db.execute("SELECT * FROM a_stud WHERE teacher_mail=:tmail_t AND semester=:tsem_t AND course_unique=:ccode_t",
                              tmail_t=session["teacher_mail"], tsem_t=current_semester, ccode_t=x['course_unique'])
            my_list.append(temp)
        all_info = ret_courses_section_take_code(only_courses)
        print(all_info)
        print("nc: " + str(my_list))
        my = db.execute("SELECT * FROM a_stud WHERE teacher_mail=:tmail_t AND semester=:tsem_t",
                        tmail_t=session["teacher_mail"], tsem_t=current_semester)

        return render_template("teacher/students.html", ac=my, cc=only_courses, nc=my_list)


@app.route("/student/view", methods=["GET"])
@student_login_required
def student_view():
    if request.method == "GET":
        courses_complete = session['courses_student']
        attendence_courses = []
        sadi_attendence = []
        for x in courses_complete:
            temp = db.execute("SELECT * FROM attendence WHERE roll_number=:troll_t AND course_unique=:cunit_t",
                              troll_t=session['student_roll_num'], cunit_t=str(x['course_code'] + "-" + x['course_sec'] + "-" + x['semester']))
            sadi_attendence.append(temp)
            date_list = {}
            if temp:
                i = 0
                while i < len(temp):
                    flag = 0
                    t_list = []
                    date_temp = temp[i]['class_date_t']
                    while i < len(temp) and date_temp == temp[i]['class_date_t']:
                        print(temp[i])
                        t_list.append(temp[i])
                        i = i+1
                        flag = 1
                    date_list[date_temp] = t_list
                    if flag == 0:
                        i = i+1
                print("date list : " + str(date_list))
            attendence_courses.append(date_list)
        # print("Course_complete :")
        # print(courses_complete)
        # print("NEW ATT : ")
        # print(attendence_courses)
        # print("SADI ATT:")
        # print(sadi_attendence)
        key_list = []
        for i in range(0, len(attendence_courses)):
            key_list.append(list(attendence_courses[i].keys()))

        return render_template("student/view.html", cc=courses_complete, ac=sadi_attendence, nc=attendence_courses, kl=key_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if session.get("user_id"):

        if session.get("student_id"):
            return redirect("/student_home")

        elif session.get("teacher_id"):
            return redirect("/teacher_home")

    # Forget any user_id
    session.clear()
    # User reached route via GET (as by clicking a link or via redirect)
    flash("Welcome")
    return render_template("login.html")


@app.route("/login/student", methods=["GET", "POST"])
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
        if(len(rows) != 1):
            return apology("Roll Number Not Registered.", 400)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid roll number and/or password", 400)

        course_dict_list2 = []
        course_dict_list2 = ret_courses(rows)

        roll_num = request.form.get("rollnumber")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["student_id"] = rows[0]["id"]
        session["student_roll_num"] = roll_num
        session["courses_student"] = course_dict_list2

        active_course_codes = db.execute(
            "SELECT * FROM a_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
        active_courses = ret_courses_reg(active_course_codes)
        pending_course_codes = db.execute(
            "SELECT * FROM p_stud WHERE roll_num=:roll_t", roll_t=session['student_roll_num'])
        pending_courses = ret_courses_take_code(pending_course_codes)

        session["courses_student_pending"] = pending_courses
        session["courses_student_registered"] = active_courses

        temp_str = ("Welcome back " +
                    str(rows[0]["student_name"]).title() + ".")
        flash(temp_str)
        # Redirect user to home page
        return redirect("/student_home")
    else:
        if session.get("student_id"):
            return redirect("/student_home")
        return render_template("student/login_student.html")


@app.route("/login/teacher", methods=["GET", "POST"])
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
        if(len(rows) != 1):
            return apology("Teacher Not Registered.", 400)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("invalid NU mail id and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["teacher_id"] = rows[0]["id"]
        session['teacher_mail'] = rows[0]['teacher_mail']

        stud = db.execute("SELECT * FROM teachers WHERE id=:id_",
                          id_=session['teacher_id'])

        """
        #print(stud[0])
        cour = stud[0]['courses_reg'].split("|")
        #print(cour)
        c_sec_list = ret_sec(cour)
        #print(c_sec_list)
        course_list=[]
        course_dict_list = []
        course_dict_list2 = []
        course_code_dict = {}
        course_code_list = []
        course_sec = {}
        for each_course in cour:
            temp = each_course.split("-")
            course_code_dict[(temp[0])] = temp[1]
            course_code_list.append(temp[0])
            course_dict_list.append({temp[0]:temp[1]})
            course_list.append(temp[0])

        #print("course_dict_list: " + str(course_dict_list))
        #print("course_list: " + str(course_dict_list))
        #print("course_code_dict : " + str(course_code_dict))
        #print("course_code_list : " + str(course_code_list))
        #print("courses:")
        delimit="\",\""
        course_str=delimit.join(course_list)
        course_str=str("\"" + course_str + "\"")
        print(course_str)
        all_cour=[]
        all_cour = db.execute("SELECT * FROM courses WHERE course_code IN(" + course_str + ")")
        print("courses: " + str(all_cour))
        cnt=0
        for x in course_code_list:
            temp_course_list=next(i for i in all_cour if i["course_code"]==x)
            #print(temp_course_list)
            course_dict_list2.append({"id":temp_course_list["id"],"course_name":temp_course_list["course_name"],"course_short":temp_course_list["course_short"],"course_code":temp_course_list["course_code"],"course_sec":c_sec_list[cnt]})
            cnt=cnt+1
        print(course_dict_list2)
        """
        course_dict_list2 = []
        course_dict_list2 = ret_courses(rows)
        session["teacher_name"] = (rows[0]["teacher_name"]).lower()
        session["courses_teacher"] = course_dict_list2

        temp_str = ("Welcome back " +
                    str(rows[0]["teacher_name"]).title() + ".")
        flash(temp_str)
        # Redirect user to home page
        return redirect("/teacher_home")
    else:
        if session.get("teacher_id"):
            return redirect("/teacher_home")
        return render_template("teacher/login_teacher.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/mark_attendence", methods=["POST"])
@teacher_login_required
def mart_att():
    if request.method == "POST":
        if not request.form.get("course_c"):
            return apology("must provide course name.", 400)
        if not request.form.get("course_sec"):
            return apology("must provide course section.", 400)

        course_semester = current_semester  # To be removed

        course_short = request.form.get("course_c")
        course_sec = request.form.get("course_sec")
        hours = request.form.get("hours")
        date = request.form.get("date_class")
        time_limit = request.form.get("time_limit")
        print(course_short)
        print(hours)

        temp_str = "Attendence For " + str(course_short) + ", section " + str(
            course_sec) + ", Duration : " + str(hours) + " hour(s)" + " On " + date

        at_str = str(course_short)+"|" + str(course_sec) + "|" + str(course_semester) + "|" + str(hours) + "|" + date + \
            "|" + str(session['teacher_id']) + "|" + str(datetime.now(
                pytz.timezone("Asia/Karachi")).time()) + "|" + time_limit
        qr_url = pyqrcode.create(at_str)
        file_ad = "static/" + str(course_short) + ".png"
        file_name = str(course_short) + ".png"
        qr_url.png(file_ad, scale=20)
        pic = url_for('static', filename=file_name)

        course_code = str(course_short)

        course_uni = str(course_code) + "-" + \
            str(course_sec) + "-" + str(course_semester)
        curr_date = str(datetime.now(pytz.timezone("Asia/Karachi")).date())
        curr_time = str(datetime.now(pytz.timezone("Asia/Karachi")).time())

        students = db.execute("SELECT * FROM a_stud where course_unique=:cuni_t AND teacher_mail=:tmail_t",
                              cuni_t=course_uni, tmail_t=session['teacher_mail'])
        check_if_already_open = db.execute("SELECT * FROM attendence WHERE course_unique=:cuni_t AND teacher_mail=:tmail_t AND class_date_t=:date_t",
                                           cuni_t=course_uni, tmail_t=session['teacher_mail'], date_t=curr_date)

        if check_if_already_open:
            temp_str = temp_str + " Opened Earlier"
            flash(temp_str)
            return render_template("teacher/mark_attendence.html", qr_c=pic)
        for x in students:
            db.execute("INSERT INTO attendence (id,roll_number,student_name,student_class,class_date_t,section,class_teacher,state,attendence_time,semester,course_unique,teacher_mail,duration)\
            VALUES(:id_t,:roll_t,:sname_t,:scode_t,:c_datet_t,:csec_t,:tname,:type_t,:att_t,:csem_t,:cuni_t,:tmail_t,:cdur_t)",
                       id_t=str(curr_time) + "|" + str(x['roll_num']), roll_t=x['roll_num'], sname_t=x['student_name'], scode_t=x['course_code'], c_datet_t=str(curr_date), csec_t=x['section'],
                       tname=x['teacher_name'], att_t=str("Not Marked"), type_t="A", csem_t=x['semester'], cuni_t=course_uni, tmail_t=x['teacher_mail'], cdur_t=int(hours))

        flash(temp_str)
        return render_template("teacher/mark_attendence.html", qr_c=pic)


@app.route("/register/student", methods=["GET", "POST"])
def register_student():
    print("STUDENT CLICKED")
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("rollnumber"):
            return apology("must provide rollnumber", 400)

        elif not request.form.get("student_name"):
            return apology("must provide name", 400)

        elif not request.form.get("batch"):
            return apology("must provide batch year", 400)

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
                course_code_w_section_temp.append(str(x['course_code']) + "-" + str(
                    request.form.get(str(x['course_code']))).upper() + "-" + current_semester)
                cunique = str(x['course_code']) + "-" + str(request.form.get(
                    str(x['course_code']))).upper() + "-" + current_semester
                db.execute("INSERT INTO p_stud (student_name,course_code,section,roll_num,batch,semester,course_unique) VALUES(:sname_t,:ccode_t,:csec_t,:sroll_t,:sbatch_t,:sem_t,:cuni_t)",
                           sname_t=sname, ccode_t=str(x['course_code']), csec_t=str(request.form.get(str(x['course_code']))).upper(), sroll_t=rnum, sbatch_t=batch, sem_t=current_semester, cuni_t=cunique)
                course_cnt = course_cnt + 1
        if(not course_code_w_section_temp):
            return apology("No Courses Selected.", 400)
        delimit = '|'
        course_code_w_section = delimit.join(course_code_w_section_temp)

        if course_cnt < 2 or course_cnt > 9:
            return apology("Invalid Number Of Courses. Please Select in range Min:2 Max:9", 400)

        # Query database for username
        db.execute("INSERT INTO students (id,roll_num,student_name,num_courses,year,password,courses_reg) VALUES(:id_,:roll,:name,:cour,:y,:hash_pass,:cg)",
                   id_=(unique_id), roll=(str(rnum)).lower(), name=(sname).lower(), cour=course_cnt, y=int(batch), hash_pass=generate_password_hash(password), cg=str(course_code_w_section))

        rows = db.execute(
            "SELECT * FROM students WHERE roll_num =:roll", roll=(str(rnum)).lower())
        temp_str = (str(rows[0]["student_name"]).title() +
                    " is Registered. Please Login")
        print(temp_str)
        flash(temp_str)
        return redirect("/login/student")

        """ LEGACY CODE """
        """
        # For login
        session["user_id"] = rows[0]['id']
        session["student_id"] = rows[0]['id']

        # Redirect user to home page
        temp_str = (str(rows[0]["student_name"]).title() + " is Registered.")
        print(temp_str)
        flash(temp_str)
        return redirect("/student_home")
        """
    else:
        courses_data = db.execute("SELECT * FROM courses")

        return render_template("student/register_student.html", courses=courses_data, semester=current_semester)
    return render_template("student/register_student.html", courses=courses_data, semester=current_semester)
    # return redirect("/register")


@app.route("/register/teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "POST":
        # Ensure username was submitted

        str_name = "n"
        str_code = "c"
        str_short = "s"
        str_section = "sec"

        str_course = "courser"
        str_course_cnt = 0
        course_cnt = 0
        course_code_w_section_temp = []

        while request.form.get(str_name + str(str_course + str(str_course_cnt))):
            #print(request.form.get( str_name + str( str_course + str(str_course_cnt))))
            #print(request.form.get( str_code + str( str_course + str(str_course_cnt))))
            #print(request.form.get( str_short + str( str_course + str(str_course_cnt))))
            #print(request.form.get( str_section + str( str_course + str(str_course_cnt))))
            course_code_w_section_temp.append(request.form.get(str_code + str(str_course + str(str_course_cnt))) + "-" + str(
                request.form.get(str_section + str_course + str(str_course_cnt))).upper() + "-" + str(current_semester))
            str_course_cnt = str_course_cnt + 1
            course_cnt = course_cnt + 1

        print(course_code_w_section_temp)
        delimit = '|'
        course_code_w_section = delimit.join(course_code_w_section_temp)
        print(course_code_w_section)

        if not request.form.get("teacher_mail"):
            return apology("must provide Valid NU mail", 400)

        elif not request.form.get("teacher_name"):
            return apology("must provide name", 400)

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

        # Where course_code_w_section_temp = e.g ['NS101-A-Fall2018', 'MT119-B-Fall2018']
        for x in course_code_w_section_temp:
            course_reg = db.execute(
                "SELECT * FROM active_courses WHERE course_unique =:uni", uni=x)
            if course_reg:

                return apology(str(course_reg[0]['course_name']) + " Section : " + str(course_reg[0]['section']) + " Already Registered")
            else:
                # Where course_contents = e.g ['NS101','A','Fall2018']
                course_contents = x.split("-")
                db.execute("INSERT INTO active_courses (course_code,section,semester,teacher,course_unique,teacher_mail) VALUES(:ccode_t,:csec_t,:csem_t,:tname_t,:cunique_t,:tmail_t)",
                           ccode_t=course_contents[0], csec_t=course_contents[1], csem_t=current_semester, tname_t=tname, cunique_t=x, tmail_t=tmail)

        #course = db.execute("SELECT * FROM courses")

        """
        for x in course:
            if request.form.get(str(x['course_code'])):
                course_code_w_section_temp.append(str(x['course_code']) + "-" + str(request.form.get(str(x['course_code']))))
                course_cnt = course_cnt + 1
                flag=0
        if(flag):
            return apology("Must Select Atleast One Course.",400)
        """

        # Query database for username
        db.execute("INSERT INTO teachers (teacher_mail,teacher_name,course_cnt,courses_reg,password) VALUES(:tm,:name,:cour,:cr,:hash_pass)",
                   tm=tmail, name=tname, cour=course_cnt, cr=course_code_w_section, hash_pass=generate_password_hash(request.form.get("password")))

        rows = db.execute(
            "SELECT * FROM teachers WHERE teacher_mail =:m", m=tmail)
        temp_str = (str(rows[0]["teacher_name"]).title() +
                    " is Registered. Please Login")
        print(temp_str)
        flash(temp_str)
        return redirect("login/teacher")
    else:
        courses_data = db.execute("SELECT * FROM courses")
        return render_template("teacher/register_teacher.html", courses=courses_data, semester=current_semester)


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_file("favicon.ico")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if isinstance(e, ValueError):
        return apology("ValueError", 400)

    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

