import os
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
# from application import pdb
from table_classes import *
from pdb_parsers import *
from course_parser import *
import colorama
colorama.init()

if __name__ == "__main__":
    db_string = str(os.environ.get('POSTGRESQL_DB_URI'))
    #db_string = "sqlite:///finance.db"
    pdb = create_engine(db_string)
    # db_string = "postgresql://frpswaheyyrcda:cc7c80c84ac73b88483a235dd381eab4e013506eb84c0190676bbc3f16b55e65@ec2-54-235-178-189.compute-1.amazonaws.com:5432/d904mj7g7okbjj"
    # #db_string = "sqlite:///finance.db"
    # pdb = create_engine(db_string)
    pdb_Session = sessionmaker(pdb)
    pdbs = pdb_Session()
    unique_id = 19003612
    rnum = "19k-3612"
    sname = "krazzwalla"
    course_cnt = 5
    batch = 2019
    password=str(123)
    course_code_w_section="NS101-A-Fall2018|MT119-A-Fall2018|SS150-C-Fall2018|SL150-D-Fall2018"

    # active_course_codes = ret_list(pdbs.query(p_stud).filter(p_stud.roll_num == "17k-3654").all())
    # print("before pdb_ret_Courses_reg " + str(active_course_codes))
    # active_courses = pdb_ret_courses_reg(active_course_codes)
    # print(active_courses)

    # new_student = students(id=unique_id, roll_num=(str(rnum)).lower(), student_name=sname, num_courses=course_cnt, batch=int(batch), password=generate_password_hash(password), courses_reg=str(course_code_w_section))
    # print(new_student.data_dict())
    # dir(new_student)
    # pdb_session.add(new_student)
    # pdb_session.commit()
    rows = ret_list(pdbs.query(students).filter(students.roll_num == "17k-3654").all())
    print(rows)
    ret_c = pdb_ret_courses(rows)
    print(ret_c)
