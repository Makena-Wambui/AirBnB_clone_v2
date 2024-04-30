#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)
    state = relationship('State', back_populates="cities")

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
