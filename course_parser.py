from cs50 import SQL
from application import current_semester
db = SQL("sqlite:///finance.db")

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