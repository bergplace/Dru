class BlockInfo(object):

    def __init__(self, hash, path, index, height=-1):
        self.hash = hash
        self.path = path
        self.index = index
        self.height = height
        self.__next_counter = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.__next_counter += 1
        if self.__next_counter == 4:
            self.__next_counter = -1
            raise StopIteration()
        return self.__getattribute__(
            ('hash', 'path', 'index', 'height')[self.__next_counter]
        )
