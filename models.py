from sqlalchemy import Column , Integer , String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
     __tablename__ = 'users'
     id = Column(Integer , primary_key=True)
     username = Column(String(150) , nullable=False)
     email = Column(String(150) , nullable=False, unique=True)
     phone = Column(Integer , nullable=False, unique=True)
     role = Column(String(150))
     password = Column(String(150) , nullable=False)
     
     
class Product(Base):
     __tablename__ = 'addProducts'
     id = Column(Integer , primary_key=True)
     productname =Column(String(150) , nullable=False)
     productDesc = Column(String(150) , nullable=False)
     productPrice = Column(Integer , nullable=False)
     img = Column(String(200))
     
class Blog(Base):
    __tablename__ = 'addblogs'
    id = Column(Integer, primary_key=True)
    blogtitle = Column(String(150), nullable=False)
    blogDesc = Column(String(150), nullable=False)
    bimg = Column(String(200))
    url = Column(String(150), nullable=False)