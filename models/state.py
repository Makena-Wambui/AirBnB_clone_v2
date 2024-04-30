#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship('City', back_populates='state', cascade="delete")

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """
            returns the list of City instances with state_id equals to
            the current State.id
            => It will be the FileStorage relationship between State and City.
            """
            cityObjects = models.storage.all(City).values()
            cityObjects = list(cityObjects)
            citiesList = []

            for city in cityObjects:
                if city.state_id == self.id:
                    citiesList.append(city)
            return citiesList
