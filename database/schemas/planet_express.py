from datetime import datetime
from database.utils import DatabaseUtil
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float

Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employee'

    employee_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    salary = Column(Float, nullable=False)
    remarks = Column(String(255))


class Planet(Base):
    __tablename__ = 'planet'

    planet_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    coordinates = Column(Float, nullable=False)


class Shipment(Base):
    __tablename__ = 'shipment'

    shipment_id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=True)
    manager = Column(Integer, ForeignKey('employee.employee_id'), nullable=False)
    planet = Column(Integer, ForeignKey('planet.planet_id'), nullable=False)


class HasClearance(Base):
    __tablename__ = 'has_clearance'

    employee = Column(Integer, ForeignKey('employee.employee_id'), primary_key=True)
    planet = Column(Integer, ForeignKey('planet.planet_id'), primary_key=True)
    level = Column(Integer, nullable=False)


class Client(Base):
    __tablename__ = 'client'

    account_number = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Package(Base):
    __tablename__ = 'package'

    shipment = Column(Integer, ForeignKey('shipment.shipment_id'), primary_key=True)
    package_number = Column(Integer, primary_key=True)
    contents = Column(String(255), nullable=False)
    weight = Column(Float, nullable=False)
    sender = Column(Integer, ForeignKey('client.account_number'), nullable=False)
    recipient = Column(Integer, ForeignKey('client.account_number'), nullable=False)


def generate():
    db_util = DatabaseUtil(base=Base, db_name='planet_express')

    db_util.delete_database()

    session = db_util.get_session()

    all_clients = [(1, 'Zapp Brannigan'), (2, "Al Gore's Head"), (3, 'Barbados Slim'),
                   (4, 'Ogden Wernstrom'), (5, 'Leo Wong'), (6, 'Lrrr'),
                   (7, 'John Zoidberg'), (8, 'John Zoidfarb'), (9, 'Morbo'),
                   (10, 'Judge John Whitey'), (11, 'Calculon')]

    for client in all_clients:
        account_number = client[0]
        name = client[1]

        new_client = Client(account_number=account_number, name=name)

        session.add(new_client)

    all_employees = [(1, 'Phillip J. Fry', 'Delivery boy', 7500.0, 'Not to be confused with the Philip J. Fry from Hovering Squid World 97a'),
                     (2, 'Turanga Leela', 'Captain', 10000.0, None),
                     (3, 'Bender Bending Rodriguez', 'Robot', 7500.0, None),
                     (4, 'Hubert J. Farnsworth', 'CEO', 20000.0, None),
                     (5, 'John A. Zoidberg', 'Physician', 25.0, None),
                     (6, 'Amy Wong', 'Intern', 5000.0, None),
                     (7, 'Hermes Conrad', 'Bureaucrat', 10000.0, None),
                     (8, 'Scruffy Scruffington', 'Janitor', 5000.0, None)]

    for employee in all_employees:
        employee_id = employee[0]
        name = employee[1]
        position = employee[2]
        salary = employee[3]
        remarks = employee[4]

        new_employee = Employee(employee_id=employee_id, name=name,
                                position=position, salary=salary, remarks=remarks)

        session.add(new_employee)

    all_planets = [(1, 'Omicron Persei 8', 89475345.3545),
                   (2, 'Decapod X', 65498463216.3466),
                   (3, 'Mars', 32435021.65468),
                   (4, 'Omega III', 98432121.5464),
                   (5, 'Tarantulon VI', 849842198.354654),
                   (6, 'Cannibalon', 654321987.21654),
                   (7, 'DogDoo VII', 65498721354.688),
                   (8, 'Nintenduu 64', 6543219894.1654),
                   (9, 'Amazonia', 65432135979.6547)]

    for planet in all_planets:
        planet_id = planet[0]
        name = planet[1]
        coordinates = planet[2]

        new_planet = Planet(planet_id=planet_id, name=name,
                            coordinates=coordinates)

        session.add(new_planet)

    all_has_clearance = [(1, 1, 2), (1, 2, 3), (2, 3, 2),
                         (2, 4, 4), (3, 5, 2), (3, 6, 4),
                         (4, 7, 1)]

    for clearance in all_has_clearance:
        employee = clearance[0]
        planet = clearance[1]
        level = clearance[2]

        new_clearance = HasClearance(
            employee=employee, planet=planet, level=level)

        session.add(new_clearance)

    all_shipments = [(1, datetime.strptime("2024-01-10", "%Y-%m-%d"), 1, 1), (2, datetime.strptime("2024-05-10", "%Y-%m-%d"), 1, 2),
                     (3, None, 2, 3), (4, None, 2, 4), (5, datetime.strptime("2024-03-10", "%Y-%m-%d"), 7, 5)]

    for shipment in all_shipments:
        shipment_id = shipment[0]
        date = shipment[1]
        manager = shipment[2]
        planet = shipment[3]

        new_shipment = Shipment(shipment_id=shipment_id, date=date,
                                manager=manager, planet=planet)

        session.add(new_shipment)

    all_packages = [(1, 1, 'Undeclared', 1.5, 1, 2),
                    (2, 1, 'Undeclared', 10.0, 2, 3),
                    (2, 2, 'A bucket of krill', 2.0, 8, 7),
                    (3, 1, 'Undeclared', 15.0, 3, 4),
                    (3, 2, 'Undeclared', 3.0, 5, 1),
                    (3, 3, 'Undeclared', 7.0, 2, 3),
                    (4, 1, 'Undeclared', 5.0, 4, 5),
                    (4, 2, 'Undeclared', 27.0, 1, 2),
                    (5, 1, 'Undeclared', 100.0, 5, 1)]

    for package in all_packages:
        shipment = package[0]
        package_number = package[1]
        contents = package[2]
        weight = package[3]
        sender = package[4]
        recipient = package[5]

        new_package = Package(shipment=shipment, package_number=package_number,
                              contents=contents, weight=weight, sender=sender, recipient=recipient)

        session.add(new_package)

    session.commit()

    session.close()
