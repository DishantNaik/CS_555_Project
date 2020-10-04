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

class US29_test(unittest.TestCase):
    def setUp(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind1","Tia /Meyer/",  "F", "22 Jun 1965","NA" ,"True", "NA","NA", "{f1}" ])
        self.individuals.add_row(["ind2","John /Meyer/",  "M", "NA","NA" ,"False", "25 May 1995","NA", "{f1}" ])
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"True", "NA","NA", "{f1}" ])

    def test_US29_returnedIndividualsAreNotFromAliveIndividuals(self):
        deceasedIndividuals = Team4_Project_File.findDeceasedIndividuals(self.individuals)
        for dIndiv in deceasedIndividuals:
            dIndiv.border,dIndiv.header = False,False
            self.assertIsNot("Tia /Meyer/", dIndiv.get_string(fields=['Name']).strip())
            self.assertIsNot("Maddy /Meyer/", dIndiv.get_string(fields=['Name']).strip())

    def test_US29_returnedIndividualsAreFromDeceasedIndividuals(self):
        deceasedIndividuals = Team4_Project_File.findDeceasedIndividuals(self.individuals)
        for dIndiv in deceasedIndividuals:
            dIndiv.border,dIndiv.header = False,False
            self.assertEqual("John /Meyer/", dIndiv.get_string(fields=['Name']).strip())

class US30_test(unittest.TestCase):
    def setUp(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind2","John /Meyer/",  "M", "NA","NA" ,"False", "25 May 1995","NA", "{f1}" ])
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"True", "NA","NA", "{f1}" ])

    def test_US30_returnedIndividualsAreNotFromAliveMarriedIndividuals(self):
        aliveMarriedIndividuals = Team4_Project_File.findAliveMarried(self.individuals)
        for amIndiv in aliveMarriedIndividuals:
            amIndiv.border,amIndiv.header = False,False
            self.assertIsNot("John /Meyer/", amIndiv.get_string(fields=['Name']).strip())

    def test_US30_returnedIndividualsAreFromAliveMarriedIndividuals(self):
        aliveMarriedIndividuals = Team4_Project_File.findAliveMarried(self.individuals)
        for amIndiv in aliveMarriedIndividuals:
            amIndiv.border,amIndiv.header = False,False
            self.assertEqual("Maddy /Meyer/", amIndiv.get_string(fields=['Name']).strip())

class US31_test(unittest.TestCase):
    def setUp(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind1","Tia /Meyer/",  "F", "22 Jun 1965","55" ,"True", "NA","NA", "NA" ])
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","18" ,"True", "NA","NA", "NA" ])

    def test_US31_returnedIndividualsAreNotFromLivingSingleOver30AgeIndividuals(self):
        livingSingleOver30Age = Team4_Project_File.findLivingSingleOverXAge(self.individuals,30)
        for lsIndiv in livingSingleOver30Age:
            lsIndiv.border,lsIndiv.header = False,False
            self.assertIsNot("Maddy /Meyer/", lsIndiv.get_string(fields=['Name']).strip())

    def test_US31_returnedIndividualsAreFromLivingSingleOver30AgeIndividuals(self):
        livingSingleOver30Age = Team4_Project_File.findLivingSingleOverXAge(self.individuals,30)
        for lsIndiv in livingSingleOver30Age:
            lsIndiv.border,lsIndiv.header = False,False
            self.assertEqual("Tia /Meyer/", lsIndiv.get_string(fields=['Name']).strip())

if __name__=='__main__':
    unittest.main(exit=False, verbosity=2)
