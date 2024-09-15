from database.utils import DatabaseUtil
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class Manufacturer(Base):
    __tablename__ = 'manufacturers'

    code = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Product(Base):
    __tablename__ = 'products'

    code = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    manufacturer = Column(Integer, ForeignKey(
        'manufacturers.code'), nullable=False)


def generate():
    db_util = DatabaseUtil(base=Base, db_name='computer_store')

    db_util.delete_database()

    session = db_util.get_session()

    all_manufacturers = [(1, 'Sony'), (2, 'Creative Labs'), (3, 'Hewlett-Packard'),
                         (4, 'Iomega'), (5, 'Fujitsu'), (6, 'Winchester')]

    for manufacturer in all_manufacturers:
        code = manufacturer[0]
        name = manufacturer[1]

        new_manufacturer = Manufacturer(code=code, name=name)

        session.add(new_manufacturer)

    all_products = [(1, 'Hard drive', 240, 5), (2, 'Memory', 120, 6), (3, 'ZIP drive', 150, 4), (4, 'Floppy disk', 5, 6), (5, 'Monitor', 240, 1),
                    (6, 'DVD drive', 180, 2), (7, 'CD drive', 90, 2), (8, 'Printer', 270, 3), (9, 'Toner cartridge', 66, 3), (10, 'DVD burner', 180, 2)]

    for product in all_products:
        code = product[0]
        name = product[1]
        price = product[2]
        manufacturer = product[3]

        new_product = Product(code=code, name=name,
                              price=price, manufacturer=manufacturer)

        session.add(new_product)

    session.commit()

    session.close()
