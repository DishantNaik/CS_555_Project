import sys
import os
from datetime import datetime
from datetime import date
import pprint

'''
@Author - Deeptidevi Agrawal FALL 2020 - SSW555
usage GEDCOMProcessor.py <filepath>
Discription - Program to
    Reads each line of a GEDCOM file

    Prints "--> <input line>"
    
    Prints "<-- <level>|<tag>|<valid?> : Y or N|<arguments>"
    <level> is the level of the input line, e.g. 0, 1, 2
    <tag> is the tag associated with the line, e.g. 'INDI', 'FAM', 'DATE', ...
    <valid?> has the value 'Y' if the tag is one of the supported tags or 'N' otherwise.  
    The set of all valid tags for our project is specified in the Project Overview document.
    <arguments> is the rest of the line beyond the level and tag.
'''
pp = pprint.PrettyPrinter(indent=4)
NOT_SUPPORTED_COMBINE_TOKEN = ["1 DATE", "2 NAME"]
SUPPORTED_THIRD_TOKEN = ["INDI", "FAM"]
SUPPORTED_SECOND_TOKEN = ["NAME","SEX","BIRT","DEAT","FAMC","FAMS","MARR","HUSB","WIFE","CHIL","DIV","DATE","HEAD","TRLR","NOTE"]
individuals = {}
families = []

class Individual:
    id = None
    name = None
    sex = None
    birthDate = None
    deathDate = None

    def __init__(self, id):
        self.id = id
        self.childOfFamilyIds = []
        self.spouseOfFamilyIds = []
    
    def isAlive(self):
        if self.deathDate is None:
            return True
        else:
            return False
    
    def calculateAge(self):
        if self.birthDate is not None:
            bd = datetime.strptime(self.birthDate, '%d %b %Y')
            today = date.today() 
            age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day)) 
            return age
        else:
            return 'N/A'
            
            
class Family:
    id = None
    marriageDate = None
    divorcedDate = None
    wifeId = None
    husbandId = None
    def __init__(self, id):
        self.id = id
        self.childIds = []

    def addChild(self, child):
        self.childIds.append(child)

def main(args):
    try:
        filePath = sys.argv[1]
    except:
        print("Usage - GEDCOMProcessor.py <filePath>")
        sys.exit()
        
    if not os.path.isfile(filePath):
        print("File path {} does not exist. Exiting...".format(filePath))
        sys.exit()
    
    #printProject02Assignment(filePath)
    findIndividualsAndFamilies(filePath)
    printIndividuals()
    printFamilies()

def printIndividuals():
    print('Individuals')
    print('-' * 120)
    print('|{:^22s}|{:^15s}|{:^6s}|{:^11s}|{:^3s}|{:^5s}|{:^11s}|{:^22s}|{:^22s}|'.format('ID', 'Name', 'Gender', 'Birthday', 'Age', 'Alive', 'Death', 'Child', 'Spouse'))
    print('-' * 120)
    for id, indiv in individuals.items():
        deathdt = indiv.deathDate if indiv.deathDate is not None else 'NA'
        familySp = indiv.spouseOfFamilyIds if len(indiv.spouseOfFamilyIds) > 0 else 'NA'
        familyCh = indiv.childOfFamilyIds if len(indiv.childOfFamilyIds) > 0 else 'NA'
        print('|{:^22s}|{:^15s}|{:^6s}|{:^11s}|{:^3d}|{:^5s}|{:^11s}|{:^22s}|{:^22s}|'.format(indiv.id, indiv.name,indiv.sex,indiv.birthDate,indiv.calculateAge(),'True' if indiv.isAlive() else 'False', deathdt , ','.join(familyCh), ','.join(familySp)))
    print('-' * 120)

def printFamilies():
    print('Families')
    print('-' * 120)
    print('|{:^22s}|{:^11s}|{:^8s}|{:^22s}|{:^13s}|{:^22s}|{:^13s}|{:^11s}|'.format('ID', 'Married', 'Divorced', 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children'))
    print('-' * 120)
    for family in families:
        marrDt = family.marriageDate if family.marriageDate is not None else 'NA'
        divDt = family.divorcedDate if family.divorcedDate is not None else 'NA'
        chIds = family.childIds if len(family.childIds) > 0 else 'NA'
        print('|{:^22s}|{:^11s}|{:^8s}|{:^22s}|{:^13s}|{:^22s}|{:^13s}|{:^11s}|'.format(family.id, marrDt,divDt,family.husbandId,individuals[family.husbandId].name, family.wifeId,individuals[family.wifeId].name, ','.join(chIds)))
    print('-' * 120)


def printProject02Assignment(filePath):
    with open(filePath) as fp:
        for line in fp:
            try:
                gedcomLine = line.strip()
                print("--> "+gedcomLine); #print input line 
                
                st = gedcomLine.split(' ', 2 )
                firstToken = st[0] if len(st) > 0 else None
                secondToken = st[1] if len(st) > 1 else None
                thirdToken = st[2] if len(st) > 2 else None
                
                print(convertGedComLine(firstToken, secondToken, thirdToken)) #print output line
            except EOFError:
                break
                
'''
    validate if token is valid or not
    <valid?> has the value 'Y' if the tag is one of the supported tags or 'N' otherwise.  
    The set of all valid tags for our project is specified in the Project Overview document
'''
def isValidToken(firstToken, secondToken, thirdToken):
    if ((secondToken in SUPPORTED_SECOND_TOKEN 
        and firstToken+" "+secondToken not in NOT_SUPPORTED_COMBINE_TOKEN)
        or thirdToken in SUPPORTED_THIRD_TOKEN):
        return 'Y'
    else:
        return 'N'    

'''
    prepare output line
'''
def convertGedComLine(firstToken, secondToken, thirdToken):
    finalLine = []
    finalLine.append("<-- "+firstToken+"|"+secondToken+"|"+isValidToken(firstToken, secondToken, thirdToken))
    
    if thirdToken is not None:  
        finalLine.append("|"+thirdToken)
    
    return ''.join(finalLine)
    
def findIndividualsAndFamilies(filePath):
    processing = None
    processingDateType = None
    individual = None
    family = None
    with open(filePath) as openFile:
        for line in openFile:
            try:
                line = line.strip()
                st = line.split(' ', 2 )
                firstToken = st[0] if len(st) > 0 else None
                secondToken = st[1] if len(st) > 1 else None
                thirdToken = st[2] if len(st) > 2 else None
                if isValidToken(firstToken, secondToken, thirdToken) == 'Y':
                    if secondToken in ['BIRT', 'DEAT', 'DIV', 'MARR']:
                        processingDateType = secondToken
                    if thirdToken in ['INDI', 'FAM']:
                        if processing == 'INDI':
                            individuals[individual.id] = individual
                        if processing == 'FAM':
                            families.append(family)
                        processing = thirdToken
                        if thirdToken == 'INDI':
                            individual = Individual(secondToken)
                        if thirdToken == 'FAM': 
                            family = Family(secondToken)
                    if processing == 'INDI':
                        if secondToken == 'NAME':
                            individual.name = thirdToken
                        if secondToken == 'SEX':
                            individual.sex = thirdToken
                        if secondToken == 'FAMC':
                            individual.childOfFamilyIds.append(thirdToken)
                        if secondToken == 'FAMS':
                            individual.spouseOfFamilyIds.append(thirdToken)
                        if secondToken == 'DATE':
                            if processingDateType == 'BIRT':
                                individual.birthDate = thirdToken
                            if processingDateType == 'DEAT':
                                individual.deathDate = thirdToken
                            processingDateType = None
                    if processing == 'FAM':
                        if secondToken == 'WIFE':
                            family.wifeId = thirdToken
                        if secondToken == 'HUSB':
                            family.husbandId = thirdToken
                        if secondToken == 'CHIL':
                            family.addChild(thirdToken)
                        if secondToken == 'DATE':
                            if processingDateType == 'DIV':
                                family.divorcedDate = thirdToken
                            if processingDateType == 'MARR':
                                family.marriageDate = thirdToken
                            processingDateType = None
            except EOFError:
                break
        if processing == 'INDI':
            individuals[individual.id] = individual
        if processing == 'FAM':
            families.append(family)
main("args")