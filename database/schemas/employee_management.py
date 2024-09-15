from database.utils import DatabaseUtil
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'

    code = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    budget = Column(Integer, nullable=False)


class Employee(Base):
    __tablename__ = 'employees'

    ssn = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    department = Column(Integer, ForeignKey('departments.code'), nullable=False)


def generate():
    db_util = DatabaseUtil(base=Base, db_name='employee_management')

    db_util.delete_database()

    session = db_util.get_session()

    all_departments = [(14, 'IT', 65000), (37, 'Accounting', 15000),
                       (59, 'Human Resources', 24000), (77, 'Research', 55000)]

    for department in all_departments:
        code = department[0]
        name = department[1]
        budget = department[2]

        new_department = Department(code=code, name=name, budget=budget)

        session.add(new_department)

    all_employees = [('123234877', 'Michael', 'Rogers', 14),
                     ('152934485', 'Anand', 'Manikutty', 14),
                     ('222364883', 'Carol', 'Smith', 37),
                     ('326587417', 'Joe', 'Stevens', 37),
                     ('332154719', 'Mary-Anne', 'Foster', 14),
                     ('332569843', 'George', 'ODonnell', 77),
                     ('546523478', 'John', 'Doe', 59),
                     ('631231482', 'David', 'Smith', 77),
                     ('654873219', 'Zacary', 'Efron', 59),
                     ('745685214', 'Eric', 'Goldsmith', 59),
                     ('845657245', 'Elizabeth', 'Doe', 14),
                     ('845657246', 'Kumar', 'Swamy', 14)]

    for employee in all_employees:
        ssn = employee[0]
        name = employee[1]
        last_name = employee[2]
        department = employee[3]

        new_employee = Employee(ssn=ssn, name=name,
                                last_name=last_name, department=department)

        session.add(new_employee)

    session.commit()

    session.close()
