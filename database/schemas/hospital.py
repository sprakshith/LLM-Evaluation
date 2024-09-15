from datetime import datetime
from database.utils import DatabaseUtil
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date

Base = declarative_base()


class Physician(Base):
    __tablename__ = 'physicians'

    employee_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    position = Column(String(30), nullable=False)
    ssn = Column(Integer, nullable=False)


class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    head = Column(Integer, ForeignKey('physicians.employee_id'), nullable=False)


class AffiliatedWith(Base):
    __tablename__ = 'affiliated_with'

    physician = Column(Integer, ForeignKey('physicians.employee_id'), primary_key=True)
    department = Column(Integer, ForeignKey('departments.department_id'), primary_key=True)
    primary_affiliation = Column(Integer, nullable=False)


class Procedures(Base):
    __tablename__ = 'procedures'

    code = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    cost = Column(Float, nullable=False)


class TrainedIn(Base):
    __tablename__ = 'trained_in'

    physician = Column(Integer, ForeignKey('physicians.employee_id'), primary_key=True)
    treatment = Column(Integer, ForeignKey('procedures.code'), primary_key=True)
    certification_date = Column(Date, nullable=False)
    certification_expires = Column(Date, nullable=False)


class Patient(Base):
    __tablename__ = 'patients'

    ssn = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    address = Column(String(30), nullable=False)
    phone = Column(String(30), nullable=False)
    insurance_id = Column(Integer, nullable=False)
    pcp = Column(Integer, ForeignKey('physicians.employee_id'), nullable=False)


class Nurse(Base):
    __tablename__ = 'nurses'

    employee_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    position = Column(String(30), nullable=False)
    registered = Column(Integer, nullable=False)
    ssn = Column(Integer, nullable=False)


class Appointment(Base):
    __tablename__ = 'appointments'

    appointment_id = Column(Integer, primary_key=True)
    patient = Column(Integer, ForeignKey('patients.ssn'), nullable=False)
    prep_nurse = Column(Integer, ForeignKey('nurses.employee_id'))
    physician = Column(Integer, ForeignKey('physicians.employee_id'), nullable=False)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=False)
    examination_room = Column(String(30), nullable=False)


class Medication(Base):
    __tablename__ = 'medications'

    code = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    brand = Column(String(30), nullable=False)
    description = Column(String(30), nullable=False)


class Prescribes(Base):
    __tablename__ = 'prescribes'

    physician = Column(Integer, ForeignKey('physicians.employee_id'), primary_key=True)
    patient = Column(Integer, ForeignKey('patients.ssn'), primary_key=True)
    medication = Column(Integer, ForeignKey('medications.code'), primary_key=True)
    date = Column(Date, primary_key=True)
    appointment = Column(Integer, ForeignKey('appointments.appointment_id'))
    dose = Column(String(30), nullable=False)


class Block(Base):
    __tablename__ = 'blocks'

    block_floor = Column(Integer, primary_key=True)
    block_code = Column(Integer, primary_key=True)


class Room(Base):
    __tablename__ = 'rooms'

    room_number = Column(Integer, primary_key=True)
    room_type = Column(String(30), nullable=False)
    block_floor = Column(Integer, ForeignKey('blocks.block_floor'), nullable=False)
    block_code = Column(Integer, ForeignKey('blocks.block_code'), nullable=False)
    unavailable = Column(Integer, nullable=False)


class OnCall(Base):
    __tablename__ = 'on_call'

    nurse = Column(Integer, ForeignKey('nurses.employee_id'), primary_key=True)
    block_floor = Column(Integer, ForeignKey('blocks.block_floor'), primary_key=True)
    block_code = Column(Integer, ForeignKey('blocks.block_code'), primary_key=True)
    on_call_start = Column(Date, primary_key=True)
    on_call_end = Column(Date, primary_key=True)


class Stay(Base):
    __tablename__ = 'stays'

    stay_id = Column(Integer, primary_key=True)
    patient = Column(Integer, ForeignKey('patients.ssn'), nullable=False)
    room = Column(Integer, ForeignKey('rooms.room_number'), nullable=False)
    stay_start = Column(Date, nullable=False)
    stay_end = Column(Date, nullable=False)


class Undergoes(Base):
    __tablename__ = 'undergoes'

    patient = Column(Integer, ForeignKey('patients.ssn'), primary_key=True)
    procedures = Column(Integer, ForeignKey('procedures.code'), primary_key=True)
    stay = Column(Integer, ForeignKey('stays.stay_id'), primary_key=True)
    date_undergoes = Column(Date, primary_key=True)
    physician = Column(Integer, ForeignKey('physicians.employee_id'), primary_key=True)
    assisting_nurse = Column(Integer, ForeignKey('nurses.employee_id'))


def generate():
    db_util = DatabaseUtil(base=Base, db_name='hospital')

    db_util.delete_database()

    session = db_util.get_session()

    all_physicians = [(1, 'John Dorian', 'Staff Internist', 111111111),
                      (2, 'Elliot Reid', 'Attending Physician', 222222222),
                      (3, 'Christopher Turk', 'Surgical Attending Physician', 333333333),
                      (4, 'Percival Cox', 'Senior Attending Physician', 444444444),
                      (5, 'Bob Kelso', 'Head Chief of Medicine', 555555555),
                      (6, 'Todd Quinlan', 'Surgical Attending Physician', 666666666),
                      (7, 'John Wen', 'Surgical Attending Physician', 777777777),
                      (8, 'Keith Dudemeister', 'MD Resident', 888888888),
                      (9, 'Molly Clock', 'Attending Psychiatrist', 999999999)]

    for physician in all_physicians:
        employee_id = physician[0]
        name = physician[1]
        position = physician[2]
        ssn = physician[3]

        new_physician = Physician(employee_id=employee_id,
                                  name=name,
                                  position=position,
                                  ssn=ssn)

        session.add(new_physician)

    all_departments = [(1, 'General Medicine', 4),
                       (2, 'Surgery', 7),
                       (3, 'Psychiatry', 9)]

    for department in all_departments:
        department_id = department[0]
        name = department[1]
        head = department[2]

        new_department = Department(department_id=department_id,
                                    name=name,
                                    head=head)

        session.add(new_department)

    all_affiliated_with = [(1, 1, 1), (2, 1, 1), (3, 1, 0),
                           (3, 2, 1), (4, 1, 1), (5, 1, 1),
                           (6, 2, 1), (7, 1, 0), (7, 2, 1),
                           (8, 1, 1), (9, 3, 1)]

    for affiliation in all_affiliated_with:
        physician = affiliation[0]
        department = affiliation[1]
        primary_affiliation = affiliation[2]

        new_affiliation = AffiliatedWith(physician=physician,
                                         department=department,
                                         primary_affiliation=primary_affiliation)

        session.add(new_affiliation)

    all_procedures = [(1, 'Reverse Rhinopodoplasty', 1500.0),
                      (2, 'Obtuse Pyloric Recombobulation', 3750.0),
                      (3, 'Folded Demiophtalmectomy', 4500.0),
                      (4, 'Complete Walletectomy', 10000.0),
                      (5, 'Obfuscated Dermogastrotomy', 4899.0),
                      (6, 'Reversible Pancreomyoplasty', 5600.0),
                      (7, 'Follicular Demiectomy', 25.0)]

    for procedure in all_procedures:
        code = procedure[0]
        name = procedure[1]
        cost = procedure[2]

        new_procedure = Procedures(code=code,
                                   name=name,
                                   cost=cost)

        session.add(new_procedure)

    all_patients = [(100000001, 'John Smith', '42 Foobar Lane', '555-0256', 68476213, 1),
                    (100000002, 'Grace Ritchie', '37 Snafu Drive', '555-0512', 36546321, 2),
                    (100000003, 'Random J. Patient', '101 Omgbbq Street', '555-1204', 65465421, 2),
                    (100000004, 'Dennis Doe', '1100 Foobaz Avenue', '555-2048', 68421879, 3)]

    for patient in all_patients:
        ssn = patient[0]
        name = patient[1]
        address = patient[2]
        phone = patient[3]
        insurance_id = patient[4]
        pcp = patient[5]

        new_patient = Patient(ssn=ssn,
                              name=name,
                              address=address,
                              phone=phone,
                              insurance_id=insurance_id, pcp=pcp)

        session.add(new_patient)

    all_nurses = [(101, 'Carla Espinosa', 'Head Nurse', 1, 111111110),
                  (102, 'Laverne Roberts', 'Nurse', 1, 222222220),
                  (103, 'Paul Flowers', 'Nurse', 0, 333333330)]

    for nurse in all_nurses:
        employee_id = nurse[0]
        name = nurse[1]
        position = nurse[2]
        registered = nurse[3]
        ssn = nurse[4]

        new_nurse = Nurse(employee_id=employee_id,
                          name=name,
                          position=position,
                          registered=registered,
                          ssn=ssn)

        session.add(new_nurse)

    all_appointments = [(13216584, 100000001, 101, 1, datetime.strptime('2008-04-24 10:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-24 11:00', '%Y-%m-%d %H:%M'), 'A'),
                        (26548913, 100000002, 101, 2, datetime.strptime('2008-04-24 10:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-24 11:00', '%Y-%m-%d %H:%M'), 'B'),
                        (36549879, 100000001, 102, 1, datetime.strptime('2008-04-25 10:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-25 11:00', '%Y-%m-%d %H:%M'), 'A'),
                        (46846589, 100000004, 103, 4, datetime.strptime('2008-04-25 10:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-25 11:00', '%Y-%m-%d %H:%M'), 'B'),
                        (59871321, 100000004, None, 4, datetime.strptime('2008-04-26 10:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-26 11:00', '%Y-%m-%d %H:%M'), 'C'),
                        (69879231, 100000003, 103, 2, datetime.strptime('2008-04-26 11:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-26 12:00', '%Y-%m-%d %H:%M'), 'C'),
                        (76983231, 100000001, None, 3, datetime.strptime('2008-04-26 12:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-26 13:00', '%Y-%m-%d %H:%M'), 'C'),
                        (86213939, 100000004, 102, 9, datetime.strptime('2008-04-27 10:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-21 11:00', '%Y-%m-%d %H:%M'), 'A'),
                        (93216548, 100000002, 101, 2, datetime.strptime('2008-04-27 10:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-04-27 11:00', '%Y-%m-%d %H:%M'), 'B')]

    for appointment in all_appointments:
        appointment_id = appointment[0]
        patient = appointment[1]
        prep_nurse = appointment[2]
        physician = appointment[3]
        start = appointment[4]
        end = appointment[5]
        examination_room = appointment[6]

        new_appointment = Appointment(appointment_id=appointment_id,
                                      patient=patient,
                                      prep_nurse=prep_nurse,
                                      physician=physician,
                                      start=start,
                                      end=end,
                                      examination_room=examination_room)

        session.add(new_appointment)

    all_medications = [(1, 'Procrastin-X', 'X', 'N/A'),
                       (2, 'Thesisin', 'Foo Labs', 'N/A'),
                       (3, 'Awakin', 'Bar Laboratories', 'N/A'),
                       (4, 'Crescavitin', 'Baz Industries', 'N/A'),
                       (5, 'Melioraurin', 'Snafu Pharmaceuticals', 'N/A')]

    for medication in all_medications:
        code = medication[0]
        name = medication[1]
        brand = medication[2]
        description = medication[3]

        new_medication = Medication(code=code,
                                    name=name,
                                    brand=brand,
                                    description=description)

        session.add(new_medication)

    all_prescribes = [(1, 100000001, 1, datetime.strptime('2008-04-24 10:47', '%Y-%m-%d %H:%M'), 13216584, '5'),
                      (9, 100000004, 2, datetime.strptime('2008-04-27 10:53', '%Y-%m-%d %H:%M'), 86213939, '10'),
                      (9, 100000004, 2, datetime.strptime('2008-04-30 16:53', '%Y-%m-%d %H:%M'), None, '5')]

    for prescribes in all_prescribes:
        physician = prescribes[0]
        patient = prescribes[1]
        medication = prescribes[2]
        date = prescribes[3]
        appointment = prescribes[4]
        dose = prescribes[5]

        new_prescribes = Prescribes(physician=physician,
                                    patient=patient,
                                    medication=medication,
                                    date=date,
                                    appointment=appointment,
                                    dose=dose)

        session.add(new_prescribes)

    all_blocks = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3),
                  (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3)]

    for block in all_blocks:
        block_floor = block[0]
        block_code = block[1]

        new_block = Block(block_floor=block_floor,
                          block_code=block_code)

        session.add(new_block)

    all_rooms = [(101, 'Single', 1, 1, 0), (102, 'Single', 1, 1, 0),
                 (103, 'Single', 1, 1, 0), (111, 'Single', 1, 2, 0),
                 (112, 'Single', 1, 2, 1), (113, 'Single', 1, 2, 0),
                 (121, 'Single', 1, 3, 0), (122, 'Single', 1, 3, 0),
                 (123, 'Single', 1, 3, 0), (201, 'Single', 2, 1, 1),
                 (202, 'Single', 2, 1, 0), (203, 'Single', 2, 1, 0),
                 (211, 'Single', 2, 2, 0), (212, 'Single', 2, 2, 0),
                 (213, 'Single', 2, 2, 1), (221, 'Single', 2, 3, 0),
                 (222, 'Single', 2, 3, 0), (223, 'Single', 2, 3, 0),
                 (301, 'Single', 3, 1, 0), (302, 'Single', 3, 1, 1),
                 (303, 'Single', 3, 1, 0), (311, 'Single', 3, 2, 0),
                 (312, 'Single', 3, 2, 0), (313, 'Single', 3, 2, 0),
                 (321, 'Single', 3, 3, 1), (322, 'Single', 3, 3, 0),
                 (323, 'Single', 3, 3, 0), (401, 'Single', 4, 1, 0),
                 (402, 'Single', 4, 1, 1), (403, 'Single', 4, 1, 0),
                 (411, 'Single', 4, 2, 0), (412, 'Single', 4, 2, 0),
                 (413, 'Single', 4, 2, 0), (421, 'Single', 4, 3, 1),
                 (422, 'Single', 4, 3, 0), (423, 'Single', 4, 3, 0)]

    for room in all_rooms:
        room_number = room[0]
        room_type = room[1]
        block_floor = room[2]
        block_code = room[3]
        unavailable = room[4]

        new_room = Room(room_number=room_number,
                        room_type=room_type,
                        block_floor=block_floor,
                        block_code=block_code,
                        unavailable=unavailable)

        session.add(new_room)

    all_on_call = [(101, 1, 1, datetime.strptime('2008-11-04 11:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-11-04 19:00', '%Y-%m-%d %H:%M')),
                   (101, 1, 2, datetime.strptime('2008-11-04 11:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-11-04 19:00', '%Y-%m-%d %H:%M')),
                   (102, 1, 3, datetime.strptime('2008-11-04 11:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-11-04 19:00', '%Y-%m-%d %H:%M')),
                   (103, 1, 1, datetime.strptime('2008-11-04 19:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-11-05 03:00', '%Y-%m-%d %H:%M')),
                   (103, 1, 2, datetime.strptime('2008-11-04 19:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-11-05 03:00', '%Y-%m-%d %H:%M')),
                   (103, 1, 3, datetime.strptime('2008-11-04 19:00', '%Y-%m-%d %H:%M'), datetime.strptime('2008-11-05 03:00', '%Y-%m-%d %H:%M'))]

    for on_call in all_on_call:
        nurse = on_call[0]
        block_floor = on_call[1]
        block_code = on_call[2]
        on_call_start = on_call[3]
        on_call_end = on_call[4]

        new_on_call = OnCall(nurse=nurse,
                             block_floor=block_floor,
                             block_code=block_code,
                             on_call_start=on_call_start,
                             on_call_end=on_call_end)

        session.add(new_on_call)

    all_stays = [(3215, 100000001, 111, datetime.strptime('2008-05-01', '%Y-%m-%d'), datetime.strptime('2008-05-04', '%Y-%m-%d')),
                 (3216, 100000003, 123, datetime.strptime('2008-05-03', '%Y-%m-%d'), datetime.strptime('2008-05-14', '%Y-%m-%d')),
                 (3217, 100000004, 112, datetime.strptime('2008-05-02', '%Y-%m-%d'), datetime.strptime('2008-05-03', '%Y-%m-%d'))]

    for stay in all_stays:
        stay_id = stay[0]
        patient = stay[1]
        room = stay[2]
        stay_start = stay[3]
        stay_end = stay[4]

        new_stay = Stay(stay_id=stay_id,
                        patient=patient,
                        room=room,
                        stay_start=stay_start,
                        stay_end=stay_end)

        session.add(new_stay)

    all_undergoes = [(100000001, 6, 3215, datetime.strptime('2008-05-02', '%Y-%m-%d'), 3, 101),
                     (100000001, 2, 3215, datetime.strptime('2008-05-03', '%Y-%m-%d'), 7, 101),
                     (100000004, 1, 3217, datetime.strptime('2008-05-07', '%Y-%m-%d'), 3, 102),
                     (100000004, 5, 3217, datetime.strptime('2008-05-09', '%Y-%m-%d'), 6, None),
                     (100000001, 7, 3217, datetime.strptime('2008-05-10', '%Y-%m-%d'), 7, 101),
                     (100000004, 4, 3217, datetime.strptime('2008-05-13', '%Y-%m-%d'), 3, 103)]

    for undergoes in all_undergoes:
        patient = undergoes[0]
        procedures = undergoes[1]
        stay = undergoes[2]
        date_undergoes = undergoes[3]
        physician = undergoes[4]
        assisting_nurse = undergoes[5]

        new_undergoes = Undergoes(patient=patient,
                                  procedures=procedures,
                                  stay=stay,
                                  date_undergoes=date_undergoes,
                                  physician=physician,
                                  assisting_nurse=assisting_nurse)

        session.add(new_undergoes)

    all_trained_in = [(3, 1, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (3, 2, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (3, 5, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (3, 6, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (3, 7, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (6, 2, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (6, 5, datetime.strptime('2007-01-01', '%Y-%m-%d'), datetime.strptime('2007-12-31', '%Y-%m-%d')),
                      (6, 6, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (7, 1, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (7, 2, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (7, 3, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (7, 4, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (7, 5, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (7, 6, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d')),
                      (7, 7, datetime.strptime('2008-01-01', '%Y-%m-%d'), datetime.strptime('2008-12-31', '%Y-%m-%d'))]

    for trained_in in all_trained_in:
        physician = trained_in[0]
        treatment = trained_in[1]
        certification_date = trained_in[2]
        certification_expires = trained_in[3]

        new_trained_in = TrainedIn(physician=physician,
                                   treatment=treatment,
                                   certification_date=certification_date,
                                   certification_expires=certification_expires)

        session.add(new_trained_in)

    session.commit()

    session.close()
