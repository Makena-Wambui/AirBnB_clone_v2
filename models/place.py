#!/usr/bin/python3
""" Place Module for HBNB project """

import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review",
            backref="place",
            cascade="delete, delete-orphan, all")

    else:
        @property
        def reviews(self):
            """
            This attribute returns a list of Review instances
            that have a place_id equal to the current Place instance's id.
            establishes a relationship between the Place instance
            and the Review instances that are associated with it.
            """
            # will hold the Review instances that are associated with the
            # current Place instance.
            myList = []
            reviewList = []  # holds all review instances

            # retrieve all objects from the storage
            # returns a dictionary of all objects currently stored.
            dictionary = models.storage.all()

            # iterate over each key in dictionary
            for k in dictionary:
                # replace the dot separator with a space
                review = k.replace('.', ' ')

                # splits review into a list
                review = shlex.split(review)

                # If the first element of the list is 'Review',
                # the object corresponding to the key is a Review instance.
                # so it is appended to reviewList
                if (review[0] == 'Review'):
                    reviewList.append(dictionary[k])

                    # iterates over reviewList which contains all Review
                    # instances.
            for r in reviewList:
                # For each Review instance, r in reviewList,
                # check if the place_id attribute of the Review instance
                # is equal to the id of the current Place instance (self.id).

                if r.place_id == self.id:
                    myList.append(r)
            return myList
