from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///phones.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = relationship("Surname", back_populates="user")
    fathername = relationship("FathersName", back_populates="user")
    phones = relationship("Phone", back_populates="user")
    organizations = relationship("NameOrganization", back_populates='user')

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, name):
        user = cls(name=name)
        session.add(user)
        session.commit()
        return user

    @classmethod
    def all(cls):
        return session.query(cls).all()

class Surname(Base):
    __tablename__ = 'surname'
    id = Column(Integer, primary_key=True)
    sur = Column(String, nullable = False) #быть пустым запрещено
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="surname")

    def __str__(self):
        return self.sur

    @classmethod
    def add(cls, sur, user):
        sur = cls(sur=sur, user=user)
        session.add(sur)
        session.commit()
        return sur

class FathersName(Base):
    __tablename__ = 'fathername'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="fathername")

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, name, user):
        name = cls(name=name, user=user)
        session.add(name)
        session.commit()
        return name

class Phone(Base):
    __tablename__ = 'phones'
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="phones")

    def __str__(self):
        return self.phone

    @classmethod
    def add(cls, phone, user):
        phone = cls(phone=phone, user=user)
        session.add(phone)
        session.commit()
        return phone


class NameOrganization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="organizations")

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, name, user):
        name = cls(name=name, user=user)
        session.add(name)
        session.commit()
        return name


Base.metadata.create_all(engine)
