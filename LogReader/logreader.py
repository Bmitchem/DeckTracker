import io


class LogReader:
    def __init__(self, log_file):
        self.log_file = log_file

    def read_file(self):
        with io.open(self.log_file, 'r') as log_file:
            for line in log_file.readlines():
                print line

    def _tokenize(self, string):
        parts = string.split()

