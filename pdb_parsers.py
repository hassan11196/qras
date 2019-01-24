
from application import current_semester
from application import pdb
from sqlalchemy.orm import sessionmaker
from table_classes import *

def ret_list(query_list):
    dic_list = []
    for x in query_list:
        dic_list.append(x.data_dict())
    return dic_list

def pdb_ret_courses_reg(list_courses):

    course_list_codes = []
    for each_course in list_courses:
        course_list_codes.append(str(each_course['course_code']))
    all_cour = []
    pdb_Session = sessionmaker(pdb)
    pdbs = pdb_Session()
    all_cour = ret_list( pdbs.query(courses).filter(courses.course_code.in_(course_list_codes) ).all())
    another_list = []
    # print(course_dict_list2)
    for i in list_courses:
        print(i['course_code'])
        temp_cour = next(c for c in all_cour if c['course_code'] == i['course_code'])        
        another_list.append({**i,**temp_cour})
        # print(i)
        # print(temp_cour)
    return another_list  


def pdb_ret_courses(rows):
    cour = rows[0]['courses_reg'].split("|")
    course_list = []
    for each_course in cour:
        temp = each_course.split("-")
        course_list.append(temp[0])

    all_cour = []
    pdb_Session = sessionmaker(pdb)
    pdbs = pdb_Session()
    all_cour = ret_list( pdbs.query(courses).filter(courses.course_code.in_(course_list) ).all())
    another_list = []
    for c in cour:
        temp_c = c.split("-")
        print(temp_c[0])
        temp_cour = next(c for c in all_cour if c['course_code'] == temp_c[0])
        temp_dict = {"course_unique" : str(temp_c[0]) + "-" + str(temp_c[1]) + "-" + str(temp_c[2]), 'semester':temp_c[2], 'course_sec':temp_c[1]}
        another_list.append({**temp_dict,**temp_cour})

    return another_list
# Returns Pending Courses For Approval for teacher
def pdb_ret_p_courses(list_courses):

    course_list_codes = []
    for each_course in list_courses:
        course_list_codes.append(str(each_course['course_code']) + "-" + str(
            each_course['course_sec']) + "-" + str(current_semester))

    all_cour = []
    pdb_Session = sessionmaker(pdb)
    pdbs = pdb_Session()
    all_cour = ret_list( pdbs.query(courses).filter(courses.course_code.in_(course_list) ).all())

    return all_cour