import io
import re


class LogReader:
    def __init__(self, log_file):
        self.log_file = log_file

    def read_file(self):
        with io.open(self.log_file, 'r') as log_file:
            for line in log_file.readlines():
                print line

    def _tokenize(self, string):
        parts = {}
        parts['date'] = self.get_date(string)
        parts['time'] = self.get_time(string)
        parts['zone_function'] = self.get_zone_function(string)
        parts['card'] = self.get_card(string)
        return parts

    @staticmethod
    def get_date(string):
        return re.search(r'(\d+-\d+-\d+)', string).group(1)

    @staticmethod
    def get_time(string):
        return re.search(r'(\d+:\d+:\d+.\d+)', string).group(1)

    @staticmethod
    def get_zone_function(string):
        return re.search('(?<=ZoneChangeList.)\w+', string).group(0)

    @staticmethod
    def regex_generator(key):
        pattern = '%s=[(A-Z), (_), (0-9)]+' % key
        return pattern

    @staticmethod
    def get_cardId(string):
        pattern = LogReader.regex_generator('cardId')
        match = re.search(pattern, string)
        if match:
            val = match.group().strip()
            return val.split('=')[1]

    def get_card(self, string):
        card_properties = ['name', 'id', 'zone', 'zonePos', 'cardId', 'player']
        card = {}

        start = string.rindex('[') + 1
        end = string.rindex(']')
        card_string = string[start:end]

        for card_property in card_properties:
            card[card_property] = self.get_card_property(card_string, card_property)

        return card

    def get_card_property(self, card_string, card_property):
        m = re.search(LogReader.regex_generator(card_property), card_string)
        return m.group().strip().split('=')[1]