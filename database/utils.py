import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseUtil:
    def __init__(self, base=None, db_name='database'):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.db_path = os.path.join(self.dir_path, f'sqlite_db/{db_name}.db')
        self.engine = create_engine('sqlite:///' + self.db_path)
        self.base = base

    def __create_tables(self):
        self.base.metadata.create_all(self.engine)

    def delete_database(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def get_session(self):
        if self.base is None:
            Session = sessionmaker(bind=self.engine)
        else:
            self.__create_tables()
            Session = sessionmaker(bind=self.engine)

        return Session()


def get_session(db_name):
    db_util = DatabaseUtil(db_name=db_name)
    return db_util.get_session()
