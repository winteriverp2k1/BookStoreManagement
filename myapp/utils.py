import json, os
from myapp import app, db
from myapp.models import Book, Author, Publisher, Book_Category, User, UserRole
import hashlib
import email
from flask_login import current_user
from sqlalchemy import func
from sqlalchemy.sql import extract


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_book_category():
    return Book_Category.query.all()

def load_publisher():
    return Publisher.query.all()
    # return read_json(os.path.join(app.root_path, 'data/publishers.json'))

def load_books(book_cate_id ,pub_id=None, kw=None, from_price=None, to_price=None, page=1):
    books = Book.query.filter(Book.active.__eq__(True))

    if book_cate_id:
        books = books.filter(Book.book_category_id.__eq__(book_cate_id))
    if pub_id:
        books = books.filter(Book.publisher_id.__eq__(pub_id))
    if kw:
        books = books.filter(Book.name.contains(kw))
    if from_price:
        books = books.filter(Book.price.__ge__(from_price))
    if to_price:
        books = books.filter(Book.price.__le__(to_price))
    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return books.slice(start, end).all()
    # books = read_json(os.path.join(app.root_path, 'data/books.json'))
    # #tìm theo nhà xuất bản
    # if pub_id:
    #     books = [b for b in books if b['publisher_id'] == int(pub_id)]
    # #tìm theo tên sách
    # if kw:
    #     books = [b for b in books if b['name'].lower().find(kw.lower()) >= 0]
    # #tìm theo giá
    # if from_price:
    #     books = [b for b in books if b['price'] >= float(from_price)]
    # if to_price:
    #     books = [b for b in books if b['price'] <= float(to_price)]
    #
    # return books

def count_books():
    return Book.query.filter(Book.active.__eq__(True)).count()

def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    # chưa bắt lỗi trên web
    user = User(name=name.strip(), username=username.strip(), password=password, email= kwargs.get('email')
                ,avatar=kwargs.get('avatar'))
    db.session.add(user)
    try:
        db.session.commit()
    except:
        return False
    else:
        return True

def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()

def get_user_by_id(user_id):
     return User.query.get(user_id)


def get_book_by_id(book_id):
    return Book.query.get(book_id)
    # books = read_json(os.path.join(app.root_path, 'data/books.json'))
    # for b in books:
    #     if b['id'] == book_id:
    #         return b

