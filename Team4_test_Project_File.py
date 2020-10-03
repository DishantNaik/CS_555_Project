import unittest
import Team4_Project_File
from prettytable import PrettyTable


class US39_test(unittest.TestCase):

    def test_equal(self):
        """Testing Equal"""
        self.assertEqual(Team4_Project_File.US39(), [])

class US10_test(unittest.TestCase):

    def test_equal(self):
        """Testing Equal"""
        self.assertEqual(Team4_Project_File.US10(), ['Kim /Kardashian/', 'Kim /Kardashian/', 'Kris /Humphries/', 'Kim /Kardashian/', 'Robert /Kardashian/', 'Kris /Jenner/', 'Travis /Scott/'])

class US05_test(unittest.TestCase):

    def test_story_us05(self):
        """Testing User Story 05"""
        self.assertEqual(Team4_Project_File.US05(),'US05 - Error : Individual - I3, I6, I6 have marriage before death')

class US04_test(unittest.TestCase):

    def test_story_us05(self):
        """Testing User Story 05"""
        self.assertEqual(Team4_Project_File.US04(),'US04 - Error : Family - F3, F6 have been divorced before marriage')


if __name__=='__main__':
    unittest.main(exit=False, verbosity=2)