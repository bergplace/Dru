"""
Utilities for block-engine.
"""


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
