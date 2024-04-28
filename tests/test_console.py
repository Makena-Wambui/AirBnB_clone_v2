#!/usr/bin/python3

"""
This module contains tests for the console.
"""

import unittest
import os
import uuid
import models
from io import StringIO
from console import HBNBCommand
from unittest.mock import patch
from models.engine.file_storage import FileStorage


class TestConsole(unittest.TestCase):
    """
    Tests the HBNB Console.
    """

    @classmethod
    def setUpClass(cls):
        """
        THis method is executed once before any of the tests are run.
        Prepares the test environment.

        cls is a reference to the test class.

        First, temporarily renames the file accordingly.
        Then instantiates HBNBCommand class,
        and assigns it to the test class HBNB attribute.
        This instance will be used in the test methods
        to interact with the command interpreter.
        """

        try:
            os.rename("file.json", "temp")
        except Exception:
            pass

        cls.HBNB = HBNBCommand()

    def tearDownClass(cls):
        """
        This method is executed once after all the tests have run.
        For clean up operations after all tests are run.

        the file is given its old name.

        the HBNBCommand object is deleted.
        """
        try:
            os.rename("temp", "file.json")
        except Exception:
            pass

        del cls.HBNB

    def setUp(self):
        """
        This method is executed before each test

        Set the dictionary that stores all objects to empty.
        """

        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """
        This instance method is run after each test has been executed.

        Removes the specified file.
        """
        os.remove("file.json")

    def test_errors(self):
        """
        Here we test for errors when no class name is passed,
        of when the class name does not exist.

        We use patching to redirect sys.stdout to a StringIO object,
        allowing it to capture the output of commands executed by
        HBNBCommand for assertion purposes.
        """

        # onecmd extracts the command and finds the appropriate do_ method
        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("create")

            # getvalue returns the entire content ogf the StringIO object
            self.assertEqual(out.getvalue(), "** class name missing **\n")

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("create Makena")

            self.assertEqual(out.getvalue(), "** class doesn't exist **\n")

    def test_all(self):
        """
        Create instances of each class.
        Then test if the all command will return all the instances
        for their respective class.
        """

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("create User")
            userObject = out.getvalue().strip()

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("create Place")
            placeObject = out.getvalue().strip()

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("create City")
            cityObject = out.getvalue().strip()

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("create Review")
            reviewObject = out.getvalue().strip()

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("create BaseModel")
            baseModel = out.getvalue().strip()

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("create State")
            stateObject = out.getvalue().strip()

        # then we test if each instance created will reflect in all.
        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("all User")
            users = out.getvalue().strip()
            message = "userObject not in users"
            self.assertIn(userObject, users, message)

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("all City")
            cities = out.getvalue().strip()
            message = "cityObject not in cities"
            self.assertIn(cityObject, cities, message)

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("all Place")
            places = out.getvalue().strip()
            message = "placeObject not in places"
            self.assertIn(placeObject, places, message)

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("all Review")
            reviews = out.getvalue().strip()
            message = "reviewObject not in reviews"
            self.assertIn(reviewObject, reviews, message)

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("all BaseModel")
            basemodels = out.getvalue().strip()
            message = "baseModel not in basemodels"
            self.assertIn(baseModel, basemodels, message)

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("all State")
            states = out.getvalue().strip()
            message = "stateObject not in states"
            self.assertIn(stateObject, states, message)

    def test_create_with_arguments(self):
        """
        Test when the create method is passed arguments.
        For example:
        create Place city_id="0001" user_id="0001" name="My_little_house"
        number_rooms=4 number_bathrooms=2 max_guest=10
        price_by_night=300 latitude=37.773972 longitude=-122.431297

        So if i run all Place, this object should be present,
        plus each attribute name and value.
        """
        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd(
                'create User email="iamakena@gmail.com" '
                'password="ghssggwn_sgj" '
                'first_name="Alicia" '
                'age="40"')

            userObj = out.getvalue().strip()

        with patch("sys.stdout", output=StringIO()) as out:
            self.HBNB.onecmd("all User")
            users = out.getvalue().strip()
            msg = "userObj not in users"
            self.assertIn(userObj, users, msg)
            email = "'email': 'iamakena@gmail.com'"
            password = "'password': 'ghssggwn_sgj'"
            first_name = "'first_name': 'Alicia'"
            age = "'age': '40'"
            self.assertIn(email, users)
            self.assertIn(password, users)
            self.assertIn(first_name, users)
            self.assertNotIn(age, users)
