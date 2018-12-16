"""
Utilities for block-engine.
"""
import traceback


def split_list(lst, number):
    """splits list to n lists as equally as possible"""
    splitted = []
    for i in reversed(range(1, number + 1)):
        split_point = len(lst) // i
        splitted.append(lst[:split_point])
        lst = lst[split_point:]
    return splitted


class FakeMongoCollection:
    """
    Mongo collection mockup
    """
    def insert_one(self, sth):
        """insert_one mockup"""
        pass

    def find(self, sth):
        """find mockup"""
        sth = sth
        return self

    def sort(self, sth):
        """sort mockup"""
        sth = sth
        return self

    def limit(self, sth):
        """limit mockup"""
        sth = sth
        return self

    def count(self):  # pylint: disable=no-self-use
        """count mockup"""
        return 0


class SafeGetter:
    def __init__(self, collection, logger, default=None):
        self.collection = collection
        self.logger = logger
        self.items = []
        self.default = default

    def __getitem__(self, item):
        self.items.append(item)
        return self

    def exec(self):
        try:
            result = self.collection
            for i, item in enumerate(self.items):
                result = result.__getitem__(item)
            return result
        except Exception as e:
            self.logger.error(f'{traceback.format_exc()} for items {self.items[:i + 1]}')
            return self.default


