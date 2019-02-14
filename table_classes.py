
from sqlalchemy import create_engine, Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

base = declarative_base()


class students(base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    roll_num = Column(String)
    student_name = Column(String)
    num_courses = Column(Integer)
    year = Column(Integer)
    password = Column(String)
    username = Column(String)
    courses_reg = Column(String)

    def __init__(self, **kwargs):
        if len(kwargs.keys()) >= 7 :
            self.id = kwargs['id']
            self.roll_num = kwargs['roll_num']
            self.student_name = kwargs['student_name']
            self.num_courses = kwargs['num_courses']
            self.password = kwargs['password']
            self.year = kwargs['batch']
            self.courses_reg = kwargs['courses_reg']
        else:
            raise ValueError("INVALID NUMBER OF INPUTS")

    def data_dict(self):
        d = {x: y for x, y in vars(self).items() if not x.startswith('_')}
        return d


class a_stud(base):
    __tablename__ = "a_stud"
    id = Column(Integer, primary_key=True)
    student_name = Column(String)
    roll_num = Column(String)
    batch = Column(Integer)
    course_code = Column(String)
    semester = Column(String)
    course_unique = Column(String)
    teacher_name = Column(String)
    section = Column(String)
    teacher_mail = Column(String)

    def __init__(self, **kwargs):
        if len(kwargs.keys() >= 9):
            self.student_name = kwargs['student_name']
            self.roll_num = kwargs['roll_num']
            self.batch = kwargs['batch']
            self.course_code = kwargs['course_code']
            self.semester = kwargs['semester']
            self.course_unique = kwargs['course_unique']
            self.teacher_name = kwargs['teacher_name']
            self.section = kwargs['section']
            self.teacher_mail = kwargs['teacher_mail']
        else :
            raise ValueError("INVALID NUMBER OF INPUTS")

    def data_dict(self):
        d = {x: y for x, y in vars(self).items() if not x.startswith('_')}
        return d


class active_courses(base):

    __tablename__ = "active_courses"
    id = Column(Integer)
    course_code = Column(String)
    section = Column(String)
    semester = Column(String)
    teacher_name = Column(String)
    course_unique = Column(String, primary_key=True)
    teacher_mail = Column(String)

    def __init__(self, **kwargs):
        if len(kwargs.keys() >= 6):
            self.course_code = kwargs['course_code']
            self.section = kwargs['section']
            self.semester = kwargs['semester']
            self.teacher_name = kwargs['teacher_name']
            self.course_unique = kwargs['course_unique']
            self.teacher_mail = kwargs['teacher_mail']
        else :
            raise ValueError("INVALID NUMBER OF INPUTS")

    def data_dict(self):
        d = {x: y for x, y in vars(self).items() if not x.startswith('_')}
        return d


class attendance(base):
    __tablename__ = "attendance"
    id = Column(String, primary_key=True, unique=True)
    roll_num = Column(String)
    student_name = Column(String)
    student_class = Column(String)
    class_date_t = Column(Date)
    section = Column(String)
    teacher_name = Column(String)
    state = Column(String)
    attendance_time = Column(String)
    semester = Column(String)
    course_unique = Column(String)
    teacher_mail = Column(String)
    duration = Column(Integer)

    def __init__(self, **kwargs):
        if len(kwargs.keys()) >= 9:
            self.id = kwargs['id']
            self.student_name = kwargs['student_name']
            self.roll_num = kwargs['roll_num']
            self.student_class = kwargs['student_class']
            self.class_date_t = kwargs['class_date_t']
            self.section = kwargs['section']
            self.teacher_name = kwargs['teacher_name']
            self.state = kwargs['state'] 
            self.attendance_time = kwargs['attendance_time']
            self.semester = kwargs['semester']            
            self.course_unique = kwargs['course_unique']
            self.teacher_mail = kwargs['teacher_mail']
            self.duration = kwargs['duration']
        else :
            raise ValueError("INVALID NUMBER OF INPUTS")

    def data_dict(self):
        d = {x: y for x, y in vars(self).items() if not x.startswith('_')}
        return d


class courses(base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    course_short = Column(String)
    course_code = Column(String)
    sections = Column(Integer)
    students_reg = Column(Integer)

    def __init__(self, **kwargs):
        if len(kwargs.keys() >= 5):
            self.sections = kwargs['sections']
            self.students_reg = kwargs['students_reg']            
            self.course_code = kwargs['course_code']
            self.course_name = kwargs['course_name']
            self.course_short = kwargs['course_short']
        else :
            raise ValueError("INVALID NUMBER OF INPUTS")

    def data_dict(self):
        d = {x: y for x, y in vars(self).items() if not x.startswith('_')}
        return d


class p_stud(base):
    __tablename__ = "p_stud"
    id = Column(Integer, primary_key=True)
    student_name = Column(String)
    course_code = Column(String)
    section = Column(String)
    roll_num = Column(String)
    batch = Column(Integer)
    semester = Column(String)
    course_unique = Column(String)

    
    def __init__(self, **kwargs):
        if len(kwargs.keys()) >= 7:
            self.student_name = kwargs['student_name']
            self.course_code = kwargs['course_code']
            self.section = kwargs['section']
            self.roll_num = kwargs['roll_num']
            self.batch = kwargs['batch']
            self.semester = kwargs['semester']
            self.course_unique = kwargs['course_unique']
        else:
            raise ValueError("INVALID NUMBER OF INPUTS")    


    def data_dict(self):
        d = {x: y for x, y in vars(self).items() if not x.startswith('_')}
        return d

class teachers(base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    teacher_name = Column(String)
    username = Column(String)
    password = Column(String)
    courses_reg = Column(String)
    course_cnt = Column(String)
    teacher_mail = Column(String)

    def __init__(self,**kwargs):
        if len(kwargs.keys()) >= 7:
            self.id = kwargs['id']
            self.username = kwargs['username']
            self.password = kwargs['password']
            self.teacher_name = kwargs['teacher_name']
            self.course_cnt = kwargs['course_cnt']
            self.courses_reg = kwargs['courses_reg']
            self.teacher_mail = kwargs['teacher_mail']
        else:
            raise ValueError("INVALID NUMBER OF INPUTS")

    def data_dict(self):
        d = {x: y for x, y in vars(self).items() if not x.startswith('_')}
        return d