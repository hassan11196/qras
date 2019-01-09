
from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker  

base = declarative_base()
class students(base):
    __tablename__ = "students"

    id = Column(Integer, primary_key = True)
    roll_num = Column(String)
    student_name = Column(String)
    num_courses = Column(Integer)
    password = Column(String)
    username = Column(String)
    courses_reg = Column(String)
    def data_dict(self):
        d = {x:y for x,y in vars(self).items() if not x.startswith('_')}
        return d

class a_stud(base):
    __tablename__ = "a_stud"
    id = Column(Integer, primary_key = True)
    student_name = Column(String)
    roll_num = Column(String)
    batch = Column(Integer)
    course_code = Column(String)
    semester = Column(String)
    course_unique = Column(String) 
    teacher_name = Column(String)
    section = Column(String)
    teacher_mail = Column(String)
    def data_dict(self):
        d = {x:y for x,y in vars(self).items() if not x.startswith('_')}
        return d

class active_courses(base):

    __tablename__ = "active_courses"
    id = Column(Integer)
    course_code = Column(String)
    section = Column(String)
    semester = Column(String)
    teacher = Column(String)
    course_unique = Column(String, primary_key = True)
    teacher_mail = Column(String)
    def data_dict(self):
        d = {x:y for x,y in vars(self).items() if not x.startswith('_')}
        return d

class attendance():
    __tablename__ = "attendance"
    id = Column(String, primary_key = True)
    roll_number = Column(String)
    student_name = Column(String)
    student_class = Column(String)
    class_date_t = Column(Date)
    section = Column(String)
    class_teacher = Column(String)
    state = Column(String)
    attendance_time = Column(String)
    semester = Column(String)
    course_unique = Column(String)
    teacher_mail = Column(String)
    duration = Column(Integer)
    def data_dict(self):
        d = {x:y for x,y in vars(self).items() if not x.startswith('_')}
        return d

class courses(base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key = True)
    course_name = Column(String)
    course_short = Column(String)
    course_code = Column(String)
    secrions = Column(Integer)
    students_reg = Column(Integer)
    def data_dict(self):
        d = {x:y for x,y in vars(self).items() if not x.startswith('_')}
        return d

class p_stud(base):
    __tablename__ = "p_stud"
    id = Column(Integer ,primary_key = True)
    student_name = Column(String)
    course_code = Column(String)
    section = Column(String)
    roll_num = Column(String)
    batch = Column(Integer)
    semester = Column(String)
    course_unique = Column(String)

    def data_dict(self):
        d = {x:y for x,y in vars(self).items() if not x.startswith('_')}
        return d

