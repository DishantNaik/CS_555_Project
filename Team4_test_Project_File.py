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
        self.assertEqual(Team4_Project_File.US10(), ['Kim /Kardashian/', 'Kris /Humphries/', 'Robert /Kardashian/', 'Kris /Jenner/', 'Travis /Scott/'])

class US05_test(unittest.TestCase):

    def test_story_us05(self):
        """Testing User Story 05"""
        self.assertEqual(Team4_Project_File.US05(),'US05 - Error : Individual - I3, I6 have marriage before death')

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

    def test_US29_isNotAlive(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind2","John /Meyer/",  "M", "NA","NA" ,"False", "25 May 1995","NA", "{f1}" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertFalse(Team4_Project_File.isAlive(indiv))

    def test_US29_isAlive(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind1","Tia /Meyer/",  "F", "22 Jun 1965","NA" ,"True", "NA","NA", "{f1}" ])
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"True", "NA","NA", "{f1}" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertTrue(Team4_Project_File.isAlive(indiv))

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

    def test_US29_returnIndividualsInstanceType(self):
        deceasedIndividuals = Team4_Project_File.findDeceasedIndividuals(self.individuals)
        self.assertIsInstance(deceasedIndividuals,PrettyTable)
        for dIndiv in deceasedIndividuals:
            dIndiv.border,dIndiv.header = False,False
            self.assertIsInstance(dIndiv,PrettyTable)

    def test_US29_returnedIndividualIsNotAlive(self):
        deceasedIndividuals = Team4_Project_File.findDeceasedIndividuals(self.individuals)
        for dIndiv in deceasedIndividuals:
            dIndiv.border,dIndiv.header = False,False
            self.assertEqual('False',dIndiv.get_string(fields=['Alive']).strip())

    def test_US29_returnedIndividualsDeathDateisNotNone(self):
        deceasedIndividuals = Team4_Project_File.findDeceasedIndividuals(self.individuals)
        for dIndiv in deceasedIndividuals:
            dIndiv.border,dIndiv.header = False,False
            self.assertIsNot("NA",dIndiv.get_string(fields=['Death']).strip())

class US30_test(unittest.TestCase):
    def setUp(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind2","John /Meyer/",  "M", "NA","NA" ,"False", "25 May 1995","NA", "{f1}" ])
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"True", "NA","NA", "{f1}" ])

    def test_US30_hasSpouse(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind1","Tia /Meyer/",  "F", "22 Jun 1965","NA" ,"True", "NA","NA", "{f1}" ])
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"True", "NA","NA", "{f1}" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertTrue(Team4_Project_File.hasSpouse(indiv))

    def test_US30_hasNoSpouse(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind1","Tia /Meyer/",  "F", "22 Jun 1965","NA" ,"True", "NA","NA", "NA" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertFalse(Team4_Project_File.hasSpouse(indiv))

    def test_US30_isAliveMarried(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"True", "NA","NA", "{f1}" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertTrue(Team4_Project_File.isAliveMarried(indiv))

    def test_US30_isNotAliveMarried(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"False", "NA","NA", "{f1}" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertFalse(Team4_Project_File.isAliveMarried(indiv))

    def test_US30_isNotAliveNotMarried(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"False", "NA","NA", "NA" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertFalse(Team4_Project_File.isAliveMarried(indiv))

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

    def test_US30_returnIndividualsInstanceType(self):
        aliveMarriedIndividuals = Team4_Project_File.findAliveMarried(self.individuals)
        self.assertIsInstance(aliveMarriedIndividuals,PrettyTable)
        for amIndiv in aliveMarriedIndividuals:
            amIndiv.border,amIndiv.header = False,False
            self.assertIsInstance(amIndiv,PrettyTable)

class US31_test(unittest.TestCase):
    def setUp(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind1","Tia /Meyer/",  "F", "22 Jun 1965","55" ,"True", "NA","NA", "NA" ])
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","18" ,"True", "NA","NA", "NA" ])

    def test_US31_isLivingSingle(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"True", "NA","NA", "NA" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertTrue(Team4_Project_File.isLivingSingle(indiv))

    def test_US31_isLivingNotSingle(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"True", "NA","NA", "{f1}" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertFalse(Team4_Project_File.isLivingSingle(indiv))

    def test_US31_isNotLivingNotSingle(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","NA" ,"False", "NA","NA", "{f1}" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertFalse(Team4_Project_File.isLivingSingle(indiv))

    def test_US31_isLivingSingleOver15Age(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","18" ,"True", "NA","NA", "NA" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertTrue(Team4_Project_File.isLivingSingleOverAge(indiv, 15))

    def test_US31_isNotLivingSingleOver25Age(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 1992","28" ,"False", "NA","NA", "NA" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertFalse(Team4_Project_File.isLivingSingleOverAge(indiv, 25))

    def test_US31_isNotLivingSingleNotOver25Age(self):
        self.individuals = PrettyTable()
        self.individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
        self.individuals.add_row(["ind3","Maddy /Meyer/",  "M", "14 Jan 2000","20" ,"False", "NA","NA", "{f1}" ])

        for indiv in self.individuals:
            indiv.border,indiv.header = False,False
            self.assertFalse(Team4_Project_File.isLivingSingleOverAge(indiv, 25))

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

    def test_US31_returnIndividualsInstanceType(self):
        livingSingleOver30Age = Team4_Project_File.findLivingSingleOverXAge(self.individuals, 30)
        self.assertIsInstance(livingSingleOver30Age,PrettyTable)
        for lsIndiv in livingSingleOver30Age:
            lsIndiv.border,lsIndiv.header = False,False
            self.assertIsInstance(lsIndiv,PrettyTable)
            
class US43_test(unittest.TestCase):

    def test(self):

        """Testing Equal"""
        self.assertEqual(Team4_Project_File.US43(), "US43 --> Flagged Individual(s): I5 are recorded as being born after their death.")

class US43_testRaises(unittest.TestCase):
    def test(self):
        """Testing Raises"""
        self.assertIsNot(Team4_Project_File.US43(), "US43 --> Flagged Individual(s): I5, I8, I7, I8 has/have birthday after death." )

class US43_testIsNotNone(unittest.TestCase):
    def test(self):
        """Testing IsNotNone"""
        self.assertIsNotNone(Team4_Project_File.US43())

class US43_testTrue(unittest.TestCase):
    def test(self):
        """Testing True"""
        self.assertTrue(Team4_Project_File.US43())

class US43_testIsNot(unittest.TestCase):
    def test(self):
        """Testing IsNot"""
        self.assertIsNot(Team4_Project_File.US43(), "US43 --> No fraudulent entries found.")

class US13_test(unittest.TestCase):

    def test(self):

        """Testing Equal"""
        self.assertEqual(Team4_Project_File.US13(), "US13 --> No infant mortalities found.")

class US44_testRaises(unittest.TestCase):
    def test(self):
        """Testing Raises"""
        output = Team4_Project_File.US44()
        for i in output:
            i.border,i.header = False,False
            self.assertIsNot("Tia /Meyer/", i.get_string(fields=['Name']).strip())


#all test methods above this line

if __name__=='__main__':
    unittest.main(exit=False, verbosity=2)
