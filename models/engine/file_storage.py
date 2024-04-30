#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import json
from models.base_model import BaseModel


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        cls, ie the class name is an optional parameter.
        if it is not provided, then the method returns the entire
        __objects dict, which contains all models in storage.

        if cls is provided, we create a dictionary, class_dict.
        This will hold the filtered models.
        """
        # if cls is provided eg all State:
        if cls:
            class_dict = {}
            if type(cls) is str:
                cls = globals().get(cls)
                # iterate over the items (key, value pairs)
                # in the __objects dictionary
                for k, v in self.__objects.items():
                    # For each item, check whether the type of the value
                    # matches the provided cls type.
                    if cls == v.__class__ or cls == v.__class__.__name__:
                        # If the type of value matches the provided cls type,
                        # the method adds the item to class_dict.
                        class_dict[k] = v

                        # then return class_dict, which contains only the
                        # models of the specified class type.
                    return class_dict

        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Add a new public instance method: def delete(self, obj=None)
        to delete obj from __objects if it’s inside
        if obj is equal to None, the method should not do anything.
        """
        if obj is None:
            return

        # if obj is not None, delete it
        # extract that object's class name and id
        # and use that to search for it in the dictionary
        # of objects __objects.

        obj = f"{obj.__class__.__name__}.{obj.id}"
        if obj in self.__objects:
            del FileStorage.__objects
