#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""

import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        if kwargs:
            for key, val in kwargs.items():
                if key == 'updated_at':
                    val = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f')

                elif key == 'created_at':
                    val = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S.%f')

                elif key == "__class__":
                    del val
                else:
                    setattr(self, key, val)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        # lets change logic for removing this key:_sa_instance_state
        d = self.__dict__.copy()
        
        for key in d.keys():
            if key == "_sa_instance_state":
                del d["_sa_instance_state"]
        d['__class__'] = str(self.__class__.__name__)
        d['created_at'] = self.created_at.isoformat()
        d['updated_at'] = self.updated_at.isoformat()
        return d

    def delete(self):
        """
        Add a new public instance method: def delete(self),
        to delete the current instance from the storage (models.storage),
        by calling the method delete.
        """
        models.storage.delete(self)
