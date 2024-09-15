from datetime import datetime
from database.utils import DatabaseUtil
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(1024), nullable=False)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    content = Column(Text, nullable=False)
    author = Column(Integer, ForeignKey('users.id'), nullable=False)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


def generate():
    db_util = DatabaseUtil(base=Base, db_name='blogs')

    db_util.delete_database()

    session = db_util.get_session()

    all_users = [(1, 'John Doe', 'john_doe', 'johndoe@fake_company.com', 'c2713b62c903791bdefc5a6a99df04d4330de491bbc7a0ca6a5007337e4a6028'),
                 (2, 'Jane Doe', 'jane_doe', 'janedoe@fake_company.com', '7618385caea382f562305468e586330381aae549829075b78dca7cb0d0aefac6'),
                 (3, 'Alice Smith', 'alice_smith', 'alicesmith@fake_company.com', 'fbb4e2d6c0fe89f7056ab38609f30052ced0e07b33dd16ad5bc1a06da5997cb2'),
                 (4, 'Bob Cat', 'bob_cat', 'bobcat@fake_company.com', '3bfaf7682094d482efb878617e14b9a0326568bc7a64e024a31dfdc1d52a5744'),
                 (5, 'Charlie Brown', 'charlie_brown', 'charliebrown@fake_company.com', '56a4e2de5fa7a0db241606502556bcfb19c30f905979b43ae4dc8ce2334021ec')]

    for user in all_users:
        id = user[0]
        name = user[1]
        username = user[2]
        email = user[3]
        password = user[4]

        new_user = User(id=id, name=name, username=username, email=email, password=password)

        session.add(new_user)

    all_posts = [(1, 'Post 1', datetime.strptime('2024-05-05', '%Y-%m-%d'), 'This is the content of post 1.', 1),
                 (2, 'Post 2', datetime.strptime('2024-05-10', '%Y-%m-%d'), 'This is the content of post 2.', 1),
                 (3, 'Post 3', datetime.strptime('2024-05-15', '%Y-%m-%d'), 'This is the content of post 3.', 2),
                 (4, 'Post 4', datetime.strptime('2024-05-20', '%Y-%m-%d'), 'This is the content of post 4.', 2),
                 (5, 'Post 5', datetime.strptime('2024-05-25', '%Y-%m-%d'), 'This is the content of post 5.', 2)]

    for post in all_posts:
        id = post[0]
        title = post[1]
        date = post[2]
        content = post[3]
        author = post[4]

        new_post = Post(id=id, title=title, date=date, content=content, author=author)

        session.add(new_post)

    all_comments = [(1, 'This is the comment for post 1.', 1, 3), (2, 'This is the comment for post 2.', 2, 3),
                    (3, 'This is the comment for post 3.', 3, 4), (4, 'This is the comment for post 4.', 4, 4),
                    (5, 'This is the comment for post 5.', 5, 5)]

    for comment in all_comments:
        id = comment[0]
        text = comment[1]
        user_id = comment[2]
        post_id = comment[3]

        new_comment = Comment(id=id, text=text, user_id=user_id, post_id=post_id)

        session.add(new_comment)

    session.commit()

    session.close()
