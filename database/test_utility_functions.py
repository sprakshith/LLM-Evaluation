import hashlib
from typing import List
from database.utils import get_session
from database.schemas.blogs import User, Post, Comment
from database.schemas.computer_store import Manufacturer, Product
from database.schemas.scientists import Scientist, Project, AssignedTo
from database.schemas.employee_management import Department, Employee as EMP
from database.schemas.hospital import Appointment, Patient, Stay, Procedures, Undergoes
from database.schemas.planet_express import Employee as PEMP, Planet, Shipment, HasClearance, Client, Package


def hash_password(password):
    '''Hashes the given password using SHA-256 algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    '''

    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def get_correct_hashed_password(username):
    '''Returns the correct hashed password for the given username.

    Args:
        username (str): The username for which the password is to be fetched.

    Returns:
        str: The hashed password.
    '''

    return get_session('blogs').query(User).filter(User.username == username).first().password


def fetch_all_users() -> List[User]:
    '''Fetches all the users from the database and returns a list of User objects.

    Args:
        None

    Returns:
        List[User]: A list of User objects. A User object has attributes `id`, `name`, `username`, `email` and `password`.
    '''

    return get_session('blogs').query(User).all()


def fetch_all_posts() -> List[Post]:
    '''Fetches all the posts from the database and returns a list of Post objects.

    Args:
        None

    Returns:
        List[Post]: A list of Post objects. A Post object has attributes `id`, `title`, `date`, `content`, and `author`.
    '''

    return get_session('blogs').query(Post).all()


def fetch_all_comments() -> List[Comment]:
    '''Fetches all the comments from the database and returns a list of Comment objects.

    Args:
        None

    Returns:
        List[Comment]: A list of Comment objects. A Comment object has attributes `id`, `text`, `user_id` and `post_id`.
    '''

    return get_session('blogs').query(Comment).all()


def add_new_user(**kwargs):
    '''Adds a new user to the database.

    Args:
        **kwargs: The attributes of the new user. The attributes are `id`, `name`, `username`, `email` and `password`.

    Returns:
        None
    '''

    session = get_session('blogs')
    session.add(User(**kwargs))
    session.commit()
    session.close()


def add_new_post(**kwargs):
    '''Adds a new post to the database.

    Args:
        **kwargs: The attributes of the new post. The attributes are `id`, `title`, `date`, `content` and `author`.

    Returns:
        None
    '''

    session = get_session('blogs')
    session.add(Post(**kwargs))
    session.commit()
    session.close()


def add_new_comment(**kwargs):
    '''Adds a new comment to the database.

    Args:
        **kwargs: The attributes of the new comment. The attributes are `id`, `text`, `user_id` and `post_id`.

    Returns:
        None
    '''

    session = get_session('blogs')
    session.add(Comment(**kwargs))
    session.commit()
    session.close()


def fetch_all_manufacturers() -> List[Manufacturer]:
    '''Fetches all the manufacturers from the database and returns a list of Manufacturer objects.

    Args:
        None

    Returns:
        List[Manufacturer]: A list of Manufacturer objects. A Manufacturer object has attributes `code` and `name`.
    '''

    return get_session('computer_store').query(Manufacturer).all()


def fetch_all_products() -> List[Product]:
    '''Fetches all the products from the database and returns a list of Product objects.

    Args:
        None

    Returns:
        List[Product]: A list of Product objects. A Product object has attributes `code`, `name`, `price` and `manufacturer`.
    '''

    return get_session('computer_store').query(Product).all()


def fetch_all_departments() -> List[Department]:
    '''Fetches all the departments from the database and returns a list of Department objects.

    Args:
        None

    Returns:
        List[Department]: A list of Department objects. A Department object has attributes `code`, `name` and `budget`
    '''

    return get_session('employee_management').query(Department).all()


def fetch_all_employees() -> List[EMP]:
    '''Fetches all the employees from the database and returns a list of Employee objects.

    Args:
        None

    Returns:
        List[Employee]: A list of Employee objects. An Employee object has attributes `ssn`, `name`, `last_name` and `department`.
    '''

    return get_session('employee_management').query(EMP).all()


def fetch_all_scientists() -> List[Scientist]:
    '''Fetches all the scientists from the database and returns a list of Scientist objects.

    Args:
        None

    Returns:
        List[Scientist]: A list of Scientist objects. A Scientist object has attributes `ssn` and `name`.
    '''

    return get_session('scientists').query(Scientist).all()


def fetch_all_projects() -> List[Project]:
    '''Fetches all the projects from the database and returns a list of Project objects.

    Args:
        None

    Returns:
        List[Project]: A list of Project objects. A Project object has attributes `code`, `name` and `hours`.
    '''

    return get_session('scientists').query(Project).all()


def fetch_all_assignments() -> List[AssignedTo]:
    '''Fetches all the assignments from the database and returns a list of AssignedTo objects.

    Args:
        None

    Returns:
        List[AssignedTo]: A list of AssignedTo objects. An AssignedTo object has attributes `scientist` and `project`.
    '''

    return get_session('scientists').query(AssignedTo).all()


def fetch_all_planet_employees() -> List[PEMP]:
    '''Fetches all the employees from the database and returns a list of Employee objects.

    Args:
        None

    Returns:
        List[Employee]: A list of Employee objects. An Employee object has attributes `employee_id`, `name`, `position`, `salary` and `remarks`.
    '''

    return get_session('planet_express').query(PEMP).all()


def fetch_all_planets() -> List[Planet]:
    '''Fetches all the planets from the database and returns a list of Planet objects.

    Args:
        None

    Returns:
        List[Planet]: A list of Planet objects. A Planet object has attributes `planet_id`, `name` and `coordinates`.
    '''

    return get_session('planet_express').query(Planet).all()


def fetch_all_shipments() -> List[Shipment]:
    '''Fetches all the shipments from the database and returns a list of Shipment objects.

    Args:
        None

    Returns:
        List[Shipment]: A list of Shipment objects. A Shipment object has attributes `shipment_id`, `date`, `manager` and `planet`.
    '''

    return get_session('planet_express').query(Shipment).all()


def fetch_all_clearances() -> List[HasClearance]:
    '''Fetches all the clearances from the database and returns a list of HasClearance objects.

    Args:
        None

    Returns:
        List[HasClearance]: A list of HasClearance objects. A HasClearance object has attributes `employee`, `planet` and `level`.
    '''

    return get_session('planet_express').query(HasClearance).all()


def fetch_all_clients() -> List[Client]:
    '''Fetches all the clients from the database and returns a list of Client objects.

    Args:
        None

    Returns:
        List[Client]: A list of Client objects. A Client object has attributes `account_number` and `name`.
    '''

    return get_session('planet_express').query(Client).all()


def fetch_all_packages() -> List[Package]:
    '''Fetches all the packages from the database and returns a list of Package objects.

    Args:
        None

    Returns:
        List[Package]: A list of Package objects. A Package object has attributes `shipment`, `package_number`, `contents`, `weight`, `sender` and `recipient`.
    '''

    return get_session('planet_express').query(Package).all()


def fetch_all_appointments() -> List[Appointment]:
    '''Fetches all the appointments from the database and returns a list of Appointment objects.

    Args:
        None

    Returns:
        List[Appointment]: A list of Appointment objects. An Appointment object has attributes `appointment_id`, `patient`, `prep_nurse`, `physician`, `start`, `end` and `examination_room`.
    '''

    return get_session('hospital').query(Appointment).all()


def fetch_all_patients() -> List[Patient]:
    '''Fetches all the patients from the database and returns a list of Patient objects.

    Args:
        None

    Returns:
        List[Patient]: A list of Patient objects. A Patient object has attributes `ssn`, `name`, `address`, `phone`, `insurance_id` and `pcp`.
    '''

    return get_session('hospital').query(Patient).all()


def fetch_all_stays() -> List[Stay]:
    '''Fetches all the stays from the database and returns a list of Stay objects.

    Args:
        None

    Returns:
        List[Stay]: A list of Stay objects. A Stay object has attributes `stay_id`, `patient`, `room`, `stay_start` and `stay_end`.
    '''

    return get_session('hospital').query(Stay).all()


def fetch_all_procedures() -> List[Procedures]:
    '''Fetches all the procedures from the database and returns a list of Procedures objects.

    Args:
        None

    Returns:
        List[Procedures]: A list of Procedures objects. A Procedures object has attributes `code`, `name` and `cost`.
    '''

    return get_session('hospital').query(Procedures).all()


def fetch_all_undergoes() -> List[Undergoes]:
    '''Fetches all the undergoes from the database and returns a list of Undergoes objects.

    Args:
        None

    Returns:
        List[Undergoes]: A list of Undergoes objects. An Undergoes object has attributes `patient`, `procedures`, `stay`, `date_undergoes`, `physician` and `assisting_nurse`.
    '''

    return get_session('hospital').query(Undergoes).all()


if __name__ == '__main__':
    print(fetch_all_employees())
