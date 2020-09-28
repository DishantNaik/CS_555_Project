import unittest
import Team4_Project_File
from prettytable import PrettyTable


class US39_test(unittest.TestCase):

    def test_equal(self):
        """Testing Equal"""
        self.assertEqual(Team4_Project_File.US39(), ['Marty /Smith/', 'Megan /Fox/'])

class fooTest(unittest.TestCase):

    def test_story_us05(self):
        """Testing User Story 05"""
        self.assertEqual(Team4_Project_File.US05(),'US05 - Error : Individual - I1, I11 have marriage before death')


if __name__=='__main__':
    unittest.main(exit=False, verbosity=2)