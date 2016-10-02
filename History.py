VERSION = "v0.1.0"


class SizeException(Exception):
    pass


class NotFoundException(Exception):
    pass


class History:
    queries = []
    maxSize = 100

    @staticmethod
    def add(query):
        if History.getSize() >= History.getMaxSize():
            History.queries.pop(0)
        History.queries.insert(0, query)

    @staticmethod
    def get(index):
        if index < 0 or index > (len(History.queries) - 1):
            raise NotFoundException("No query selected")

        return History.queries[index]

    @staticmethod
    def setMaxSize(size=100):
        if size < 1:
            raise SizeException("Size can't be lower than 1")

        History.maxSize = size
        return History.maxSize

    @staticmethod
    def getMaxSize():
        return History.maxSize

    @staticmethod
    def getSize():
        return len(History.queries)

    @staticmethod
    def all():
        return History.queries

    @staticmethod
    def clear():
        History.queries = []
        return History.queries
