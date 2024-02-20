#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import console
from contextlib import contextmanager
from datetime import datetime
import inspect
from io import StringIO
import models
import pep8
import sys
from os import environ, stat
import unittest

Place = models.place.Place
State = models.state.State
User = models.user.User
STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')
HBNBCommand = console.HBNBCommand
storage = console.storage
CNC = {
    'BaseModel': models.base_model.BaseModel,
    'Amenity': models.amenity.Amenity,
    'City': models.city.City,
    'Place': models.place.Place,
    'Review': models.review.Review,
    'State': models.state.State,
    'User': models.user.User
}


@contextmanager
def redirect_streams():
    """function redirects streams: stdout & stderr for testing purposes
    first creates StringIO obj, then saves / updates stdout & stderr"""
    new_stdout, new_stderr = StringIO(), StringIO()
    old_stdout, sys.stdout = sys.stdout, new_stdout
    old_stderr, sys.stderr = sys.stderr, new_stderr
    try:
        # returns new file streams
        yield new_stdout, new_stderr
    finally:
        # restore std streams to the previous value
        sys.stdout, sys.stderr = old_stdout, old_stderr


class TestHBNBcmdDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(cls):
        """init: prints output to mark new tests"""
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.......  For the Console  .......')
        print('.................................\n\n')
        cls.all_funcs = inspect.getmembers(console.HBNBCommand,
                                           inspect.isfunction)

    def test_doc_file(self):
        """... documentation for the file"""
        expected = ' Console Module '
        actual = console.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = ' Contains the functionality for the HBNB console'
        actual = HBNBCommand.__doc__
        self.assertEqual(expected, actual)

    def test_all_function_docs(self):
        """... tests for ALL DOCS for all functions in console file"""
        AF = TestHBNBcmdDocs.all_funcs
        for f in AF:
            if "_HBNBCommand_" in f[0]:
                self.assertIsNotNone(f[1].__doc__)

    def test_pep8_console(self):
        """... console.py conforms to PEP8 Style"""
        pep8style = pep8.StyleGuide(quiet=True)
        errors = pep8style.check_files(['console.py'])
        self.assertEqual(errors.total_errors, 0, errors.messages)

    def test_file_is_executable(self):
        """... tests if file has correct permissions so user can execute"""
        file_stat = stat('console.py')
        permissions = str(oct(file_stat[0]))
        actual = int(permissions[5:-2]) >= 5
        self.assertTrue(actual)


@unittest.skipIf(STORAGE_TYPE == 'db', 'FS tests not for DB')
class TestHBNBcmdCreate(unittest.TestCase):
    """testing instantiation of CLI & create() function"""

    @classmethod
    def setUpClass(cls):
        """init: prints output to mark new tests"""
        print('\n\n.................................')
        print('.... Test create() w/ params ....')
        print('..... For HBNBCommand Class .....')
        print('.................................\n\n')
        storage.delete_all()
        print('...creating new Place object: ', end='')
        cls.cli = HBNBCommand()
        cls.cli.do_create('Place '
                          'city_id="0001" '
                          'user_id="0001" '
                          'name="My_little_house" '
                          'number_rooms=4 '
                          'number_bathrooms=2 '
                          'max_guest=10 '
                          'price_by_night=300 '
                          'latitude=37.773972 '
                          'longitude=-122.431297')
        print('')
        cls.storage_objs = storage.all()
        for v in cls.storage_objs.values():
            cls.obj = v

    def setUp(self):
        """initializes new HBNBCommand instance for each test"""
        self.CLI = TestHBNBcmdCreate.cli
        self.obj = TestHBNBcmdCreate.obj

    def test_instantiation(self):
        """... checks if HBNBCommand CLI Object is properly instantiated"""
        self.assertIsInstance(self.CLI, HBNBCommand)

    def test_create(self):
        """... tests creation of class City with attributes"""
        self.assertIsInstance(self.obj, CNC['Place'])

    def test_attr_user_id(self):
        """... checks if proper parameter for user_id was created"""
        actual = self.obj.user_id
        expected = "0001"
        self.assertEqual(expected, actual)

    def test_attr_city_id(self):
        """... checks if proper parameter for city_id was created"""
        actual = self.obj.city_id
        expected = "0001"
        self.assertEqual(expected, actual)

    def test_attr_name(self):
        """... checks if proper parameter for name was created"""
        actual = self.obj.name
        expected = 'My little house'
        self.assertEqual(expected, actual)

    def test_attr_num_rm(self):
        """... checks if proper parameter for number_rooms was created"""
        actual = self.obj.number_rooms
        expected = 4
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), int)

    def test_attr_num_btrm(self):
        """... checks if proper parameter for number_bathrooms was created"""
        actual = self.obj.number_bathrooms
        expected = 2
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), int)

    def test_attr_max_guest(self):
        """... checks if proper parameter for max_guest was created"""
        actual = self.obj.max_guest
        expected = 10
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), int)

    def test_attr_price_bn(self):
        """... checks if proper parameter for price_by_night was created"""
        actual = self.obj.price_by_night
        expected = 300
        self.assertEqual(expected, actual)
        self.assertEqual(type(actual), int)

    def test_attr_lat(self):
        """... checks if proper parameter for latitude was created"""
        actual = self.obj.latitude
        expected = 37.773972
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), float)

    def test_attr_long(self):
        """... checks if proper parameter for longitude was created"""
        actual = self.obj.longitude
        expected = -122.431297
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), float)


@unittest.skipIf(STORAGE_TYPE != 'db', 'DB tests made for DBStorage not FS')
class TestHBNBcmdCreateDB(unittest.TestCase):
    """testing instantiation of CLI & create()
    for Classes State, User, City, Place"""

    @classmethod
    def setUpClass(cls):
        """init: prints output to mark new tests"""
        print('\n\n.................................')
        print('.... Test create() w/ params ....')
        print('... State, User, City, Place ....')
        print('.................................\n\n')
        storage.delete_all()
        print('...creating new Place object: ', end='')
        cls.cli = HBNBCommand()
        CLI = cls.cli
        with redirect_streams() as (std_out, std_err):
            CLI.do_create('State '
                          'name="California"')
        cls.test_state_id = std_out.getvalue()[:-1]
        with redirect_streams() as (std_out, std_err):
            CLI.do_create('User '
                          'email="bettyholbertn@gmail.com" '
                          'password="apass" '
                          'first_name="a_name" '
                          'last_name="a_last_name" ')
        cls.test_user_id = std_out.getvalue()[:-1]
        with redirect_streams() as (std_out, std_err):
            CLI.do_create('City '
                          'state_id="{}" '
                          'name="SanFrancisco"'.format(cls.test_state_id))
        cls.test_city_id = std_out.getvalue()[:-1]
        with redirect_streams() as (std_out, std_err):
            CLI.do_create('Place '
                          'city_id="{}" '
                          'user_id="{}" '
                          'name="A_humble_home" '
                          'number_rooms=4 '
                          'number_bathrooms=2 '
                          'max_guest=10'.format(cls.test_city_id,
                                                cls.test_user_id))
        cls.test_place_id = std_out.getvalue()[:-1]
        print('... done creating')
        storage_objs = storage.all()
        for v in storage_objs.values():
            if v.id == cls.test_place_id:
                cls.obj = v

    def setUp(self):
        """initializes new HBNBCommand instance for each test"""
        self.CLI = TestHBNBcmdCreateDB.cli
        self.obj = TestHBNBcmdCreateDB.obj
        self.state_id = TestHBNBcmdCreateDB.test_state_id
        self.user_id = TestHBNBcmdCreateDB.test_user_id
        self.city_id = TestHBNBcmdCreateDB.test_city_id
        self.place_id = TestHBNBcmdCreateDB.test_place_id

    def test_instantiation(self):
        """... checks if HBNBCommand CLI Object is properly instantiated"""
        self.assertIsInstance(self.CLI, HBNBCommand)

    def test_create(self):
        """... tests creation of class City with attributes"""
        self.assertIsInstance(self.obj, CNC['Place'])

    def test_attr_user_id(self):
        """... checks if proper parameter for user_id was created"""
        actual = self.obj.user_id
        expected = self.user_id
        self.assertEqual(expected, actual)

    def test_attr_city_id(self):
        """... checks if proper parameter for city_id was created"""
        actual = self.obj.city_id
        expected = self.city_id
        self.assertEqual(expected, actual)

    def test_attr_name(self):
        """... checks if proper parameter for name was created"""
        actual = self.obj.name
        expected = 'A humble home'
        self.assertEqual(expected, actual)

    def test_attr_num_rm(self):
        """... checks if proper parameter for number_rooms was created"""
        actual = self.obj.number_rooms
        expected = 4
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), int)

    def test_attr_num_btrm(self):
        """... checks if proper parameter for number_bathrooms was created"""
        actual = self.obj.number_bathrooms
        expected = 2
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), int)

    def test_attr_max_guest(self):
        """... checks if proper parameter for max_guest was created"""
        actual = self.obj.max_guest
        expected = 10
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), int)


@unittest.skipIf(STORAGE_TYPE == 'db', 'not designed for DB yet')
class TestHBNBcmdErr(unittest.TestCase):
    """Tests create method -> attempts to throw errors with strange params"""

    @classmethod
    def setUpClass(cls):
        """init: prints output to mark new tests"""
        print('\n\n.................................')
        print('... Can I Kill your program ? ...')
        print('..... For HBNBCommand Class .....')
        print('.................................\n\n')
        storage.delete_all()
        print('...creating new Place object: ', end='')
        cls.cli = HBNBCommand()
        cls.cli.do_create('Place '
                          'city_id="0001" '
                          'user_id="00_01" '
                          'name="My____little____house" '
                          'number_rooms="4" '
                          'number_bathrooms="2.0" '
                          'max_guest="0"')
        print('')
        storage_objs = storage.all()
        for v in storage_objs.values():
            cls.obj = v

    def setUp(self):
        """initializes new HBNBCommand instance for each test"""
        self.CLI = TestHBNBcmdErr.cli
        self.obj = TestHBNBcmdErr.obj

    def test_create(self):
        """... tests creation of class City with attributes"""
        self.assertIsInstance(self.obj, CNC['Place'])

    def test_attr_user_id(self):
        """... checks if proper parameter for user_id was created"""
        actual = self.obj.user_id
        expected = '00 01'
        self.assertEqual(expected, actual)

    def test_attr_city_id(self):
        """... checks if proper parameter for city_id was created"""
        actual = self.obj.city_id
        expected = '0001'
        self.assertEqual(expected, actual)

    def test_attr_name(self):
        """... checks if proper parameter for name was created"""
        actual = self.obj.name
        expected = 'My    little    house'
        self.assertEqual(expected, actual)

    def test_attr_num_rm(self):
        """... checks if proper parameter for number_rooms was created"""
        actual = self.obj.number_rooms
        expected = '4'
        self.assertEqual(expected, actual)

    def test_attr_num_btrm(self):
        """... checks if proper parameter for number_bathrooms was created"""
        actual = self.obj.number_bathrooms
        expected = '2.0'
        self.assertEqual(expected, actual)
        self.assertIs(type(actual), str)

    def test_attr_max_guest(self):
        """... checks if proper parameter for max_guest was created"""
        actual = self.obj.max_guest
        expected = '0'
        self.assertEqual(expected, actual)


class TestHBNBcmdFunc(unittest.TestCase):
    """Test CLI for create, update, destroy Standard Notation"""

    @classmethod
    def setUpClass(cls):
        """init: prints output to mark new tests"""
        print('\n\n.................................')
        print('.. Testing All other Functions ..')
        print('..... For HBNBCommand Class .....')
        print('.................................\n\n')
        # storage.delete_all()
        print('...creating new State object: ', end='')
        cls.cli = HBNBCommand()
        cls.cli.do_create('State name="California"')
        print('')
        storage_objs = storage.all()
        for v in storage_objs.values():
            cls.obj = v

    def setUp(self):
        """initializes new HBNBCommand instance for each test"""
        self.CLI = TestHBNBcmdFunc.cli
        self.obj = TestHBNBcmdFunc.obj

    def test_create(self):
        """... tests creation of class City with attributes"""
        self.assertNotIsInstance(type(self.obj), CNC['Place'])

    def test_destroy(self):
        """... checks if object can be destroyed"""
        self.CLI.do_destroy('State {}'.format(self.obj.id))
        try:
            self.obj
            self.assertTrue(False)
        except Exception:
            self.assertIsNone(None)


@unittest.skipIf(STORAGE_TYPE == 'db', 'not designed for DB yet')
class TestHBNBcmdAll(unittest.TestCase):
    """Tests .all() method for all Classes"""

    @classmethod
    def setUpClass(cls):
        """init: prints output to mark new tests
        This setup creates an instance of each class"""
        print('\n\n.................................')
        print('..            .all()           ..')
        print('..... Tests for all classes .....')
        print('..... For HBNBCommand Class .....')
        print('.................................\n\n')
        storage.delete_all()
        cls.cli = HBNBCommand()
        for k in CNC.keys():
            print('...creating new {} object: '.format(k), end='')
            cls.cli.do_create(k)
        print('')
        cls.storage_objs = storage.all()
        cls.all_ids = list(v.id for v in
                           TestHBNBcmdAll.storage_objs.values())

    def setUp(self):
        """initializes new HBNBCommand instance & storage obj for each test"""
        self.CLI = TestHBNBcmdAll.cli
        self.storage_objs = TestHBNBcmdAll.storage_objs
        self.all_ids = TestHBNBcmdAll.all_ids


class TestHBNBcmdQuit(unittest.TestCase):
    """Tests Quit, EOF, and unknown input / RTN [Enter] button"""

    @classmethod
    def setUpClass(cls):
        """init: prints output to mark new tests
        This simply tests quit"""
        print('\n\n.................................')
        print('.... quit, EOF & newline CLI ....')
        print('..... For HBNBCommand Class .....')
        print('.................................\n\n')

    def setUp(self):
        """initializes new HBNBCommand instance & storage obj for each test"""
        self.CLI = HBNBCommand()

    def test_carriage_return_cli(self):
        """... tests carriage return should simply print '\n'"""
        with redirect_streams() as (std_out, std_err):
            self.CLI.default('')
        actual = std_out.getvalue()
        expected = ''
        self.assertEqual(expected, actual)

    def test_unknown_cli(self):
        """... tests unknown command should simply print '\n'"""
        with redirect_streams() as (std_out, std_err):
            self.CLI.default('giggly goop magrouple')
        actual = std_out.getvalue()
        expected = ('')
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main
