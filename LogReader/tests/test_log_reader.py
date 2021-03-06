import os

import unittest

from django.test import TestCase
from django.conf import settings

from LogReader.logreader import LogReader

LOG_LOCATION = os.path.join(os.pardir, 'match.log')


class LogReaderTestCase(unittest.TestCase):
    def setUp(self):
        self.logReader = LogReader(log_file=LOG_LOCATION)


class RegexTestCase(unittest.TestCase):
    def setUp(self):
        self.test_string = "2015-12-03 21:53:33.355: [Zone] ZoneChangeList.ProcessChanges() - id=104 local=False [name=Mechanical Yeti id=35 zone=PLAY zonePos=3 cardId=GVG_078 player=2] pos from 4 -> 3"


class TestCardIDRead(RegexTestCase):
    def setUp(self):
        super(TestCardIDRead, self).setUp()
        self.card_id = LogReader.get_cardId(self.test_string)

    def test_card_id_no_fail(self):
        self.assertTrue(self.card_id)

    def test_correct_id(self):
        self.assertEquals(self.card_id, 'GVG_078')


class TestCard(RegexTestCase):
    def setUp(self):
        super(TestCard, self).setUp()
        self.card = LogReader.get_card(self.test_string)

    def test_card_name(self):
        self.assertEqual(self.card['name'], "Mechanical Yeti")

    def test_id(self):
        self.assertEqual(self.card['id'], "35")

    def test_card_zone(self):
        self.assertEqual(self.card['zone'], "PLAY")

    def test_card_zone_pos(self):
        self.assertEqual(self.card['zonePos'], "3")

    def test_card_id(self):
        self.assertEqual(self.card['cardId'], "GVG_078")

    def test_card_player(self):
        self.assertEqual(self.card['player'], "2")


class TestTokenize(LogReaderTestCase):
    def setUp(self):
        super(TestTokenize, self).setUp()
        test_string = "2015-12-03 21:53:33.355: [Zone] ZoneChangeList.ProcessChanges() - id=104 local=False [name=Mechanical Yeti id=35 zone=PLAY zonePos=3 cardId=GVG_078 player=2] pos from 4 -> 3"
        self.test_string = test_string
        self.tokens = self.logReader._tokenize(test_string)

    def test_tokens_created(self):
        self.assertTrue(self.tokens)

    def test_number_of_tokens(self):
        self.assertEqual(len(self.tokens), 4)

    def test_date_token(self):
        self.assertEqual(self.tokens.get('date'), '2015-12-03')
        self.assertEqual(self.logReader.get_date(self.test_string), '2015-12-03')

    def test_time_token(self):
        self.assertEqual(self.tokens.get('time'), '21:53:33.355')
        self.assertEqual(self.logReader.get_time(self.test_string), '21:53:33.355')

    def test_zone_function_token(self):
        self.assertEqual(self.tokens.get('zone_function'), 'ProcessChanges')
        self.assertEqual(self.logReader.get_zone_function(self.test_string), 'ProcessChanges')

    def test_card_token(self):
        self.assertEqual(self.tokens.get('card'),
                         {'name': 'Mechanical Yeti', 'zone': 'PLAY', 'player': '2', 'zonePos': '3', 'cardId': 'GVG_078',
                          'id': '35'})
        self.assertEqual(self.logReader.get_card(self.test_string),
                         {'name': 'Mechanical Yeti', 'zone': 'PLAY', 'player': '2', 'zonePos': '3', 'cardId': 'GVG_078',
                          'id': '35'})