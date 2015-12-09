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
        parts = string.split()

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