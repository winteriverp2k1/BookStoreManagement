from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from myapp import db
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin



class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    MANAGER = 2
    STORE_MANAGER = 3
    BOOK_SELLER = 4
    USER = 5

class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    active = Column(Boolean, default=True)
    email = Column(String(100))
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    def str(self):
        return self.name

class Book_Category(BaseModel):
    __tablename__ = 'book_category'
    name = Column(String(30), nullable=False)
    books = relationship('Book', backref='Book_Category', lazy=False)
    def __str__(self):
        return self.name


class Publisher(BaseModel):
    tablename = 'publisher'
    name = Column(String(50), nullable=False)
    books = relationship('Book', backref='publisher', lazy=False)
    def __str__(self):
        return self.name

class Author(BaseModel):
    tablename = 'author'
    name = Column(String(50), nullable=False)
    releases = relationship('Book_Author', backref='author', lazy=True)
    def str(self):
        return self.name

class Book(BaseModel):
    tablename = 'book'
    name = Column(String(50), nullable=False)
    image = Column(String(100))
    type = Column(String(50), nullable=False)
    publish_date = Column(DateTime, default=datetime.now())
    price = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    in_stock = Column(Integer)
    publisher_id = Column(Integer, ForeignKey(Publisher.id), nullable=False)
    book_category_id = Column(Integer, ForeignKey(Book_Category.id), nullable=False)
    author_details = relationship('Book_Author', backref='book', lazy=True)
    def str(self):
        return self.name

class Book_Author(db.Model):
    author_id = Column(Integer, ForeignKey(Author.id), nullable=False, primary_key=True)
    book_id = Column(Integer, ForeignKey(Book.id), nullable=False, primary_key=True)


if __name__ == '__main__':
    db.create_all()
