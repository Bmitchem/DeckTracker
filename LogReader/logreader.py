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
        parts['card'] = self.get_card(string)
        print parts['card']
        return parts

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
        m = re.search('(?<=%s=)\w+' % card_property, card_string)
        return m.group(0)