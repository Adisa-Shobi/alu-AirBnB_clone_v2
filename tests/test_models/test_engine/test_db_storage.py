#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import unittest
from datetime import datetime
import models
import inspect
from os import environ, stat
import pep8
from models.base_model import Base
from models.engine.db_storage import DBStorage

STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestDBStorageDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    all_funcs = inspect.getmembers(DBStorage, inspect.isfunction)

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('..... For DB Storage Class .....')
        print('.................................\n\n')

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        models.storage.delete_all()

    def test_doc_file(self):
        """... documentation for the file"""
        expected = 'Definition of engine for db storage\n'
        actual = models.engine.db_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = ('Class definition for database storage\n    ')
        actual = DBStorage.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in db_storage file"""
        all_functions = TestDBStorageDocs.all_funcs
        for function in all_functions:
            self.assertIsNotNone(function[1].__doc__)

    def test_pep8_db(self):
        """... db_storage.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('models/engine/db_storage.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE != 'db', "DB Storage doesn't use FileStorage")
class TestTracebackNullError(unittest.TestCase):
    """testing for throwing Traceback erros:
    missing attributes that Cannot be NULL"""

    @classmethod
    def setUpClass(cls):
        """sets up the class for this round of tests"""
        print('\n\n....................................')
        print('.......... Testing DBStorage .......')
        print('...... Trying to Throw Errors ......')
        print('....................................\n\n')

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        models.storage.delete_all()

    def tearDown(self):
        """tidies up tests that throw errors"""
        models.storage.rollback_session()


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestStateDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing DBStorage .......')
        print('........ For State Class ........')
        print('.................................\n\n')

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        models.storage.delete_all()

    def setUp(self):
        """initializes new BaseModel object for testing"""
        self.state = models.state.State()
        self.state.name = 'California'
        self.state.save()

    def test_state_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = models.storage.all()
        all_state_objs = models.storage.all('State')

        exist_in_all = False
        for k in all_objs.keys():
            if self.state.id in k:
                exist_in_all = True
        exist_in_all_states = False
        for k in all_state_objs.keys():
            if self.state.id in k:
                exist_in_all_states = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_states)

    def test_new_state(self):
        """... checks if new() functions after instantiation and save()"""
        actual = False
        self.s_new = models.state.State(name="Illinois")
        self.s_new.save()
        db_objs = models.storage.all()
        for obj in db_objs.values():
            if obj.id == self.s_new.id:
                actual = True
        self.assertTrue(actual)

    def test_state_delete(self):
        state_id = self.state.id
        models.storage.delete(self.state)
        models.storage.save()
        exist_in_all = False
        for k in models.storage.all().keys():
            if state_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestUserDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing FileStorage ......')
        print('.......... User  Class ..........')
        print('.................................\n\n')

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        models.storage.delete_all()

    def setUp(self):
        """initializes new user for testing"""
        self.user = models.user.User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()

    def test_user_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = models.storage.all()
        all_user_objs = models.storage.all('User')
        exist_in_all = False
        for k in all_objs.keys():
            if self.user.id in k:
                exist_in_all = True
        exist_in_all_users = False
        for k in all_user_objs.keys():
            if self.user.id in k:
                exist_in_all_users = True
        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_users)

    def test_user_delete(self):
        user_id = self.user.id
        models.storage.delete(self.user)
        self.user = None
        models.storage.save()
        exist_in_all = False
        for k in models.storage.all().keys():
            if user_id in k:
                exist_in_all = True
        self.assertFalse(exist_in_all)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestCityDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... City  Class ..........')
        print('.................................\n\n')

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        models.storage.delete_all()

    def setUp(self):
        """initializes new user for testing"""
        self.state = models.state.State()
        self.state.name = 'California'
        self.state.save()
        self.city = models.city.City()
        self.city.name = 'Fremont'
        self.city.state_id = self.state.id
        self.city.save()

    def test_city_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = models.storage.all()
        all_city_objs = models.storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestCityDBInstancesUnderscore(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DB Storage ......')
        print('.......... City Class ..........')
        print('.................................\n\n')

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        models.storage.delete_all()

    def setUp(self):
        """initializes new user for testing"""
        self.state = models.state.State()
        self.state.name = 'California'
        self.state.save()
        self.city = models.city.City()
        self.city.name = 'San_Francisco'
        self.city.state_id = self.state.id
        self.city.save()

    def test_city_underscore_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = models.storage.all()
        all_city_objs = models.storage.all('City')

        exist_in_all = False
        for k in all_objs.keys():
            if self.city.id in k:
                exist_in_all = True
        exist_in_all_city = False
        for k in all_city_objs.keys():
            if self.city.id in k:
                exist_in_all_city = True
        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_city)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestPlaceDBInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing DBStorage ......')
        print('.......... Place  Class ..........')
        print('.................................\n\n')

    def tearDownClass():
        """tidies up the tests removing storage objects"""
        models.storage.delete_all()

    def setUp(self):
        """initializes new user for testing"""
        self.user = models.user.User()
        self.user.email = 'test'
        self.user.password = 'test'
        self.user.save()
        self.state = models.state.State()
        self.state.name = 'California'
        self.state.save()
        self.city = models.city.City()
        self.city.name = 'San_Mateo'
        self.city.state_id = self.state.id
        self.city.save()
        self.place = models.place.Place()
        self.place.city_id = self.city.id
        self.place.user_id = self.user.id
        self.place.name = 'test_place'
        self.place.description = 'test_description'
        self.place.number_rooms = 2
        self.place.number_bathrooms = 1
        self.place.max_guest = 4
        self.place.price_by_night = 100
        self.place.latitude = 120.12
        self.place.longitude = 101.4
        self.place.save()

    def test_place_all(self):
        """... checks if all() function returns newly created instance"""
        all_objs = models.storage.all()
        all_place_objs = models.storage.all('Place')

        exist_in_all = False
        for k in all_objs.keys():
            if self.place.id in k:
                exist_in_all = True
        exist_in_all_place = False
        for k in all_place_objs.keys():
            if self.place.id in k:
                exist_in_all_place = True

        self.assertTrue(exist_in_all)
        self.assertTrue(exist_in_all_place)


@unittest.skipIf(STORAGE_TYPE != 'db', 'skip if environ is not db')
class TestCountGet(unittest.TestCase):
    """testing Count and Get methods"""

    @classmethod
    def setUpClass(cls):
        """sets up the class for this round of tests"""
        print('\n\n....................................')
        print('.......... Testing DBStorage .......')
        print('. State, City, User, Place Amenity .')
        print('....................................')
        models.storage.delete_all()
        cls.s = models.state.State(name="California")
        cls.c = models.city.City(state_id=cls.s.id,
                            name="San Francisco")
        cls.u = models.user.User(email="betty@holbertonschool.com",
                            password="pwd")
        cls.p1 = models.place.Place(user_id=cls.u.id,
                              city_id=cls.c.id,
                              name="a house")
        cls.p2 = models.place.Place(user_id=cls.u.id,
                              city_id=cls.c.id,
                              name="a house two")
        cls.a1 = models.amenity.Amenity(name="Wifi")
        cls.a2 = models.amenity.Amenity(name="Cable")
        cls.a3 = models.amenity.Amenity(name="Bucket Shower")
        objs = [cls.s, cls.c, cls.u, cls.p1, cls.p2, cls.a1, cls.a2, cls.a3]
        for obj in objs:
            obj.save()

    def setUp(self):
        """initializes new user for testing"""
        self.s = TestCountGet.s
        self.c = TestCountGet.c
        self.u = TestCountGet.u
        self.p1 = TestCountGet.p1
        self.p2 = TestCountGet.p2
        self.a1 = TestCountGet.a1
        self.a2 = TestCountGet.a2
        self.a3 = TestCountGet.a3

    def test_all_reload_save(self):
        """... checks if all(), save(), and reload function
        in new instance.  This also tests for reload"""
        actual = 0
        db_objs = models.storage.all()
        for obj in db_objs.values():
            for x in [self.s.id, self.c.id, self.u.id, self.p1.id]:
                if x == obj.id:
                    actual += 1
        self.assertTrue(actual == 4)


if __name__ == '__main__':
    unittest.main
