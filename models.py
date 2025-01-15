from sqlalchemy import Column , Integer , String,ForeignKey,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    quantity = Column(Integer, default=1)
    product = relationship('Product', back_populates='carts')
    user = relationship('User', back_populates='carts')
    
    
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    productname = Column(String, nullable=False)
    productDesc = Column(String, nullable=False)
    productPrice = Column(Float, nullable=False)
    img1 = Column(String, nullable=False)
    img2 = Column(String, nullable=False)
    img3 = Column(String, nullable=False)
    img4 = Column(String, nullable=False)
    img5 = Column(String, nullable=False)
    carts = relationship('Cart', back_populates='product')

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(Integer , unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    carts = relationship('Cart', back_populates='user')

     
# class Product(Base):
#      __tablename__ = 'addProducts'
#      id = Column(Integer , primary_key=True)
#      productname =Column(String(150) , nullable=False)
#      productDesc = Column(String(150) , nullable=False)
#      productPrice = Column(Integer , nullable=False)
#      img = Column(String(200))
     
class Blog(Base):
    __tablename__ = 'addblogs'
    id = Column(Integer, primary_key=True)
    blogtitle = Column(String(150), nullable=False)
    blogDesc = Column(String(150), nullable=False)
    bimg = Column(String(200))
    url = Column(String(150), nullable=False)