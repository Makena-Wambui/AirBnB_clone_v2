#!/usr/bin/python3
"""
Supplies class DBStorage.
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.base_model import Base, BaseModel
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.state import State
from models.review import Review


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """
        create the engine (self.__engine)
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        # drop all tables if the environment variable HBNB_ENV is equal to test
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        Public instance method: all

        Optional param, cls
        If cls:
        query on the current database session all objects depending
        on the class name (argument cls)

        If cls is None:
        query all types of objects ie
        (User, State, City, Amenity, Place and Review)

        Returns: a dictionary -> key = <class-name>.<object-id> and
        value = object
        """
        objDict = {}

        if cls is None:
            """
            return all objects for each class.
            """
            # returns a list of User objects
            myList = self.__session.query(User).all()

            # add to the users list, all the other lists
            # use extend method.
            myList.extend(self.__session.query(City).all())
            myList.extend(self.__session.query(State).all())
            myList.extend(self.__session.query(Amenity).all())
            myList.extend(self.__session.query(Review).all())
            myList.extend(self.__session.query(Place).all())
        # logic for when a class name has been provided
        else:
            if type(cls) is str:
                cls = eval(cls)

            myList = self.__session.query(cls).all()

        # iterate through myList
        for obj in myList:
            # etract objects class name and id to be key in our dict
            key = f"{obj.__class__.__name__}.{obj.id}"

            # set value for each key to be the object itself
            objDict[key] = obj

        return objDict

    def new(self, obj):
        """
        adds the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        commits all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes from the current database session obj if not None
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        creates all tables in the database.
        create the current database session (self.__session)
        from the engine (self.__engine) by using a sessionmaker.
        """
        Base.metadata.create_all(self.__engine)

        sesh = sessionmaker(bind=self.__engine, expire_on_commit=False)

        # a scoped session provides a convenient way to manage sessions
        # within a specific context, making it easier to work with SQLAlchemy,
        # in web applications or other multi-threaded scenarios.

        # create a scoped session
        Session = scoped_session(sesh)

        self.__session = Session()
