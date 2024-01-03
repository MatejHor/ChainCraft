import logging


class Module:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__)
        self.logger.setLevel(logging.INFO)

    def __str__(self):
        return self.__dict__

    def setup(self):
        pass

    def process(self):
        return None
