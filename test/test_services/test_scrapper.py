import json
import pathlib
from unittest import TestCase
from unittest.mock import patch, PropertyMock, Mock

from pymongo.cursor import Cursor

from flaskr.models import TinderProfile, tinder_profile_from_dict
from flaskr.services.scrapper import ScrapperService


class TestScrapperService(TestCase):

    @patch('pymongo.cursor.Cursor.sort')
    @patch.object(ScrapperService('foo'), '_last_document', return_value=None)
    @patch('pymongo.collection.Collection.find', spec=Cursor)
    def test_last_document_isNone(self, find, sut, sort):
        find().sort().return_value = open(pathlib.Path(__file__).parent.parent / 'fixtures/tinder_profile.json').read()
        sut.last_profile
        find.assert_called()

    @patch.object(ScrapperService('foo'), '_last_document', return_value=json.loads(open(pathlib.Path(__file__).parent.parent / 'fixtures/tinder_profile.json').read()))
    @patch('pymongo.collection.Collection.find', spec=Cursor)
    def test_last_document_isCached(self, mongo_client, sut):
        sut.last_profile
        mongo_client.assert_not_called()

    def test_should_upload(self):
        sut = ScrapperService('foo')
        sut._last_document = open(pathlib.Path(__file__).parent.parent / 'fixtures/tinder_profile.json').read()
        self.assertTrue(sut.should_upload(open(pathlib.Path(__file__).parent.parent / 'fixtures/tinder_profile_2photo.json').read()))

    def test_should_upload_disorder(self):
        sut = ScrapperService('foo')
        sut._last_document = open(pathlib.Path(__file__).parent.parent / 'fixtures/tinder_profile.json').read()
        self.assertTrue(sut.should_upload(open(pathlib.Path(__file__).parent.parent / 'fixtures/tinder_profile_3photo.json').read()))

    def test_should_not_upload(self):
        sut = ScrapperService('foo')
        sut._last_document = open(pathlib.Path(__file__).parent.parent / 'fixtures/tinder_profile.json').read()
        self.assertFalse(sut.should_upload(open(pathlib.Path(__file__).parent.parent / 'fixtures/tinder_profile.json').read()))



    # def test_should_upload(self):
    #     self.fail()
    #
    # def test_upload_to_mongo(self):
    #     self.assertTrue(True)