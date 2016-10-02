import unittest

from History import *


class HistoryTests(unittest.TestCase):
    def testEmpty(self):
        History.clear()
        self.assertEqual(History.all(), [])

    def testAdd(self):
        self.testEmpty()

        History.add("query")
        self.assertEqual(History.all(), ["query"])
        self.assertEqual(History.getSize(), 1)

        History.add("query2")
        self.assertEqual(History.all(), ["query2", "query"])
        self.assertEqual(History.getSize(), 2)

    def testGet(self):
        self.testEmpty()
        self.assertRaises(NotFoundException, History.get, 0)

        self.testAdd()

        self.assertEqual(History.get(0), "query2")
        self.assertEqual(History.get(1), "query")

    def testSetMaxSize(self):
        History.setMaxSize(2)
        self.assertEqual(History.getMaxSize(), 2)

        self.testAdd()
        History.add("query3")

        self.assertRaises(SizeException, History.setMaxSize, 0)


unittest.main()
