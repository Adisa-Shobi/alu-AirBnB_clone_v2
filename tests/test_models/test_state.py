#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import unittest
from os import environ


STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


class test_state(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    @unittest.skipIf(STORAGE_TYPE == 'db', 'FS tests not for DB')
    def test_name3(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
