from database.utils import DatabaseUtil
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Scientist(Base):
    __tablename__ = 'scientists'

    ssn = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)


class Project(Base):
    __tablename__ = 'projects'

    code = Column(String(4), primary_key=True)
    name = Column(String(50), nullable=False)
    hours = Column(Integer, nullable=False)


class AssignedTo(Base):
    __tablename__ = 'assigned_to'

    scientist = Column(Integer, ForeignKey('scientists.ssn'), primary_key=True)
    project = Column(String(4), ForeignKey('projects.code'), primary_key=True)


def generate():
    db_util = DatabaseUtil(base=Base, db_name='scientists')

    db_util.delete_database()

    session = db_util.get_session()

    all_scientists = [(123234877, 'Michael Rogers'),
                      (152934485, 'Anand Manikutty'),
                      (222364883, 'Carol Smith'),
                      (326587417, 'Joe Stevens'),
                      (332154719, 'Mary-Anne Foster'),
                      (332569843, 'George ODonnell'),
                      (546523478, 'John Doe'),
                      (631231482, 'David Smith'),
                      (654873219, 'Zacary Efron'),
                      (745685214, 'Eric Goldsmith'),
                      (845657245, 'Elizabeth Doe'),
                      (845657246, 'Kumar Swamy')]

    for scientist in all_scientists:
        ssn = scientist[0]
        name = scientist[1]

        new_scientist = Scientist(ssn=ssn, name=name)

        session.add(new_scientist)

    all_projects = [('AeH1', 'Winds: Studying Bernoullis Principle', 156),
                    ('AeH2', 'Aerodynamics and Bridge Design', 189),
                    ('AeH3', 'Aerodynamics and Gas Mileage', 256),
                    ('AeH4', 'Aerodynamics and Ice Hockey', 789),
                    ('AeH5', 'Aerodynamics of a Football', 98),
                    ('AeH6', 'Aerodynamics of Air Hockey', 89),
                    ('Ast1', 'A Matter of Time', 112),
                    ('Ast2', 'A Puzzling Parallax', 299),
                    ('Ast3', 'Build Your Own Telescope', 6546),
                    ('Bte1', 'Juicy: Extracting Apple Juice with Pectinase', 321),
                    ('Bte2', 'A Magnetic Primer Designer', 9684),
                    ('Bte3', 'Bacterial Transformation Efficiency', 321),
                    ('Che1', 'A Silver-Cleaning Battery', 545),
                    ('Che2', 'A Soluble Separation Solution', 778)]

    for project in all_projects:
        code = project[0]
        name = project[1]
        hours = project[2]

        new_project = Project(code=code, name=name, hours=hours)

        session.add(new_project)

    all_assigned_to = [(123234877, 'AeH1'),
                       (152934485, 'AeH3'),
                       (222364883, 'Ast3'),
                       (326587417, 'Ast3'),
                       (332154719, 'Bte1'),
                       (546523478, 'Che1'),
                       (631231482, 'Ast3'),
                       (654873219, 'Che1'),
                       (745685214, 'AeH3'),
                       (845657245, 'Ast1'),
                       (845657246, 'Ast2'),
                       (332569843, 'AeH4')]

    for assigned_to in all_assigned_to:
        scientist = assigned_to[0]
        project = assigned_to[1]

        new_assigned_to = AssignedTo(scientist=scientist, project=project)

        session.add(new_assigned_to)

    session.commit()

    session.close()
