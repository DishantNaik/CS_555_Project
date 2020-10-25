"""
Git repo:- https://github.com/DishantNaik/CS_555_Project
Team :- Anurag Aman , Dhruv Patel , Dishant Naik , Deepti Agarwal, Neil Naidu, Pradeep Kumar
"""
from prettytable import PrettyTable
from datetime import datetime,date,timedelta
import collections
import copy
import re


Individuals= PrettyTable()
Families= PrettyTable()

tags={"INDI":"0","FAM":"0"}

head={"NAME":"1",
"SEX":"1",
"BIRT":"1",
"DEAT":"1",
"FAMC":"1",
"FAMS":"1",
"FAM" :"0",
"MARR":"1",
"HUSB":"1",
"WIFE":"1",
"CHIL":"1",
"DIV":"1",
"DATE":"2",
"HEAD":"0",
"TRLR":"0",
"NOTE":"0"}

fp=open('Test_file.ged')
inlines =[]
Individuals.field_names = ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]
Families.field_names = ["ID", "Married", "Divorced", 'Husband ID', 'Husband Name', 'Wife ID', 'Wife Name', 'Children']
for f in fp:
    inlines.append("-->" + f)
    data = f.strip().split(" ")
    if len(data)> 3:
        ss = f.strip().split( " " , 2)
        if ss[1] in head:
            res = head[ss[1]]
            if res == ss[0]:
                    inlines.append("<--"+ss[0]+"|"+ss[1]+"|Y|"+ss[2])
            else:
                    inlines.append("<--"+ss[0]+"|"+ss[1]+"|N|"+ss[2])
        else:
            inlines.append("<--"+ss[0] + "|" + ss[1] + "|N|" + ss[2])

    elif len(data)==2 :
        ss=f.strip().split()
        if ss[1] in head:
            res=head[ss[1]]
            if res==ss[0]:
                inlines.append("<--"+ss[0]+"|"+ss[1]+"|Y|")
            else:
                inlines.append("<--"+ss[0]+"|"+ss[1]+"|N|")
        else:
            inlines.append("<--"+ss[0]+"|"+ss[1]+"|N|")
    elif len(data)== 3:
        ss = f.strip().split(" ", 2)
        if ss[2] in tags:
                inlines.append("<--"+ss[0]+"|"+ss[2]+"|"+"|Y|"+ss[1])
        else:
            if ss[1] in head:
                res=head[ss[1]]
                if res==ss[0]:
                    inlines.append("<--"+ss[0]+"|"+ss[1]+"|Y|"+ss[2])
                else:
                    inlines.append("<--"+ss[0]+"|"+ss[1]+"|N|"+ss[2])
            else:
                inlines.append("<--"+ss[0]+"|"+ss[1]+"|N|"+ss[2])

    else:
        inlines.append("Invalid input")

#************************************************** PROJECT 03 **********************************************************************
details = []
vdetails = []

# Extracting the individual information
for x in inlines:
    if ('Y' in x.split("|")):
        details.append(x)
ndetails = "\n".join(details)
for i in ndetails.split("INDI"):
    vdetails.append(i)


# Retriving the individual details for the table
for x in range(1 , len(vdetails)):
    col=['NA','NA','NA','NA','NA',True,'NA','NA','NA']
    data = vdetails[x].split("\n")
    a =set()
    b = set()
    #Populating the row with the details
    for j in range (0 , len(data)):
        #Getting the id and putting it into the column:- 1
        if data[j].split('|')[0]=='':
            col[0]= ((data[j].split("|")[-1]).replace('@',''))
        #Getting the Name and putting it into the cloumn:- 2
        elif len(data[j].split("|")) >1 and data[j].split("|")[1]=='NAME':
            col[1]=(data[j].split("|")[-1])
        #Getting the sex detail and putting it into the column :-3
        elif len(data[j].split("|")) >1 and data[j].split("|")[1]=='SEX' :
            col[2]=(data[j].split("|")[-1])
        # getting the Birth details and putting it into the column 4
        elif len(data[j].split("|")) >1 and data[j].split("|")[1]=='BIRT' :
            col[3]=(data[j+1].split("|")[-1])
            today=date.today()
            born = datetime.strptime((data[j+1].split("|")[-1]), '%d %b %Y')
            col[4]=(today.year - born.year - ( (born.month, born.day)> (today.month, today.day) ))
        #Getting the Death details and putting it into the coulm 5
        elif len(data[j].split("|")) >1 and data[j].split("|")[1]=='DEAT':
            col[5]=False
            col[6]=(data[j+1].split("|")[-1])
            death=datetime.strptime((data[j+1].split("|")[-1]), '%d %b %Y')
            col[4]=(death.year - born.year - ((born.month, born.day) > (death.month, death.day) ))
        #Getting the Family table and populating the child and spouse.
        elif len(data[j].split("|")) >1 and data[j].split("|")[1]=='FAMC':
            a.add((data[j].split("|")[-1]).replace('@',''))
            col[7]=a
        elif len(data[j].split("|")) >1 and data[j].split("|")[1]=='FAMS':
            b.add((data[j].split("|")[-1]).replace('@',''))
            col[8]=b


    Individuals.add_row(col)

#Retrieving the family details
col1 = ['NA','NA','NA','NA','NA','NA','NA','NA']
fam=vdetails[-1].split("0|FAM")[1:]

for i in range(0, len(fam)):
    member = fam[i].split("\n")
    c = set()
    for j in range(0,len(member)):
        mb = member[j].split('|')
        #Getting all the ids
        if '' == mb[0]:
            col1[0]  = mb[-1].replace('@','')
        #Getting all husband id and their names
        elif 'HUSB' in mb:
            husid = mb[-1].replace('@','')
            col1[3] = husid
            for x in Individuals:
                x.border , x.header = False , False
                if (x.get_string(fields=["ID"]).strip()) == husid:
                    col1[4]=(x.get_string(fields=["Name"]).strip())
        #Getting all the wife ids and their name
        elif 'WIFE' in mb:
            wifeid = mb[-1].replace('@','')
            col1[5] = wifeid
            for i in Individuals:
                i.border , i.header = False , False
                if (i.get_string(fields=["ID"]).strip()) == wifeid:
                    col1[6]=(i.get_string(fields=["Name"]).strip())
        #Getting all the Children ids and storing it in the set
        elif 'CHIL' in mb:
            chilid = mb[-1].replace('@','')
            c.add(chilid)
            col1[7] = c
        #Getting all the divorce information
        elif 'DIV' in mb:
            col1[2] = member[j+1].split('|')[-1]
        #Getting all the marriage infirmation.
        elif 'MARR' in mb:
            col1[1] = member[j+1].split('|')[-1]
    Families.add_row(col1)

# Printing the prettytable and populating the value
print("Individual")
print(Individuals)
print("Families")
print(Families)

###################################### Dishant Naik #######################################
####################################### Story 39 ###########################################

def isAlive_1(ind):  #refactored
	return ind.get_string(fields=['Alive']).strip()

def hasSpouse_1(ind): #refactored
	return ind.get_string(fields=['Spouse']).strip()

def US39():
    tmp = set()
    names = []
    dates = []

    yy = date.today()
    yy = yy.year
    present = datetime.now()
    next_day = present + timedelta(days=30)

    for i in Individuals:
        i.border,i.header = False,False
        if(isAlive_1(i) == 'True' and hasSpouse_1(i) != 'NA'):
            names.append(i.get_string(fields=['Name']).strip())

    for i in names:
        for j in Families:
            j.header,j.border = False,False
            if(i == j.get_string(fields=['Husband Name']).strip() or i == j.get_string(fields=['Wife Name']).strip() ):
                marDate = datetime.strptime((j.get_string(fields=['Married']).strip()), '%d %b %Y')
                marDate = marDate.replace(year=yy)
                dates.append(marDate)
                break

    tempDate = copy.deepcopy(dates)

    res = {}
    for key in names:
        for value in tempDate:
            res[key] = value
            tempDate.remove(value)
            break

    for i in dates:
        if present <= i <= next_day:
            tmp.add(i)

    finalList = []
    for key, value in res.items():
        if value in tmp:
            finalList.append(key)

    return finalList
print('US39 - ', US39())

####################################### Story 10 ###########################################

def US10():
    valid_age = []
    invalid_age = []
    for i in Families:
        i.border = False
        i.header = False
        tmp_marry = datetime.strptime((i.get_string(fields = ["Married"]).strip()), '%d %b %Y')
        hus_id = (i.get_string(fields = ["Husband ID"])).strip()
        wife_id = (i.get_string(fields = ["Wife ID"])).strip()

        for j in Individuals:
            j.border = False
            j.header = False
            if (j.get_string(fields = ["ID"]).strip() == hus_id):
                br_date = datetime.strptime((j.get_string(fields = ["Birthday"]).strip()), '%d %b %Y')
                # print('---------------------------------------------------------------------------------')
                if((tmp_marry.year - br_date.year) >= 14):
                    valid_age.append(j.get_string(fields = ["Name"]).strip())
                else: invalid_age.append(j.get_string(fields = ["Name"]).strip())

            if(j.get_string(fields = ["ID"]).strip() == wife_id):
                br_date = datetime.strptime((j.get_string(fields = ["Birthday"]).strip()), '%d %b %Y')
                # print('---------------------------------------------------------------------------------')
                if((tmp_marry.year - br_date.year) >= 14):
                    valid_age.append(j.get_string(fields = ["Name"]).strip())
                else: invalid_age.append(j.get_string(fields = ["Name"]).strip())

    return list(dict.fromkeys(valid_age))
print('US10 - ',US10())


####################################### Story 22 ###########################################
# All individual IDs should be unique and all family IDs should be unique
def US22():
    ind_ids = []
    fam_ids = []
    
    for i in Individuals:
        i.border = False
        i.header = False
        ind_ids.append(i.get_string(fields = ["ID"]).strip())

    for i in Families:
        i.border = False
        i.header = False
        fam_ids.append(i.get_string(fields = ["ID"]).strip())

    if(len(ind_ids) == len(set(ind_ids)) and len(fam_ids) == len(set(fam_ids))):
        return('NO ERROR found')
    else: return('ERROR: All IDs are not unique')
    
    

print('US22 - ',US22())

#************************************************** DHRUV_PATEL **********************************************************************
#************************************************** USER STORY - 05 **********************************************************************

def getMarriage(ind):
    #refactor
    marriageDate = (datetime.strptime((ind.get_string(fields = ["Married"]).strip()), '%d %b %Y'))
    return marriageDate

def getID(ind):
    #refactor
    id = (ind.get_string(fields = ["ID"]).strip().replace('/',''))
    return id
def US05():
    errors = set()
    for ix in Families:
        ix.border = False
        ix.header = False

        if ((ix.get_string(fields = ["Married"]).strip()) != 'NA'):
            marriage = getMarriage(ix) #refactor
            husid = (ix.get_string(fields = ["Husband ID"])).strip()
            wifeid = (ix.get_string(fields = ["Wife ID"])).strip()

            for jx in Individuals:
                jx.border = False
                jx.header = False

                id = getID(jx) #refactor

                if (husid == id or wifeid == id):
                    if((jx.get_string(fields = ["Death"]).strip()) != 'NA'):
                        death = (datetime.strptime((jx.get_string(fields = ["Death"]).strip()), '%d %b %Y'))
                        if(datetime.date(marriage) < datetime.date(death)):
                            errors.add(id)

    if(len(errors) != 0):
        errors = sorted(errors)
        strerror=", ".join(errors)
        return f'US05 - Error : Individual - {strerror} have marriage before death'
    else:
        return "US05 - No errors found "
print('US05 - ',US05())

#************************************************** USER STORY - 04 **********************************************************************

def US04():
    errors = set()
    for iy in Families:
        iy.border = False
        iy.header = False

        id = getID(iy) #refactor

        if((iy.get_string(fields = ["Married"]).strip()) != 'NA'):
            married = getMarriage(iy) #refactor
            if((iy.get_string(fields = ["Divorced"]).strip()) != 'NA'):
                divorce = (datetime.strptime((iy.get_string(fields = ["Divorced"]).strip()), '%d %b %Y'))
                if(datetime.date(married) > datetime.date(divorce)):
                        errors.add(id)

    if(len(errors) != 0):
        errors = sorted(errors)
        strerror=", ".join(errors)
        return f"US04 - Error : Family - {strerror} have been divorced before marriage"
    else:
        return " US04 - No errors found "
print('US04 - ',US04())

#************************************************** START - DEEPTIDEVI AGRAWAL  ********************************************************************
def getIndividualRow(ind):
	id = ind.get_string(fields = ["ID"]).strip()
	name = ind.get_string(fields = ["Name"]).strip()
	gender = ind.get_string(fields = ["Gender"]).strip()
	birthdate = ind.get_string(fields = ["Birthday"]).strip()
	age = ind.get_string(fields = ["Age"]).strip()
	alive = ind.get_string(fields = ["Alive"]).strip()
	death = ind.get_string(fields = ["Death"]).strip()
	child = ind.get_string(fields = ["Child"]).strip()
	spouse = ind.get_string(fields = ["Spouse"]).strip()
	return [id,name,gender,birthdate,age,alive,death,child,spouse]

def getIndividualHeader():
	return ["ID", "Name", "Gender", "Birthday","Age","Alive","Death","Child","Spouse"]

def createIndividualsPrettyTable():
	individuals = PrettyTable()
	individuals.field_names = getIndividualHeader()
	return individuals

def isAlive(ind):  #refactored
	return ind.get_string(fields=['Alive']).strip() == 'True'

def hasSpouse(ind): #refactored
	return ind.get_string(fields=['Spouse']).strip() != 'NA' and len(ind.get_string(fields=['Spouse']).strip()) > 0

def isAliveMarried(ind): #refactored
	return isAlive(ind) and hasSpouse(ind)

def isLivingSingle(ind): #refactored
	return isAlive(ind) and not hasSpouse(ind)

def isOverAge(ind, age):
	return ind.get_string(fields=['Age']).strip() != 'NA' and int(ind.get_string(fields=['Age']).strip()) > age

def isLivingSingleOverAge(ind, age):
	return isLivingSingle(ind) and isOverAge(ind, age)

def disableHeader(ind): #refactored
	ind.header = False
	return ind

def disableBorder(ind): #refactored
	ind.border = False
	return ind

def disableHeaderBorder(ind): #refactored
	ind = disableHeader(ind)
	ind = disableBorder(ind)
	return ind

def addRowToPreetyTable(prettyTable, ind): #refactored
	prettyTable.add_row(getIndividualRow(ind))

def filterIndividuals(Individuals, filter, age): #refactored
	newIndividuals = createIndividualsPrettyTable()
	for ind in Individuals:
		ind = disableHeaderBorder(ind)
		if(filter == 'DECEASED'):
			if not isAlive(ind):
				addRowToPreetyTable(newIndividuals, ind)
		if(filter == 'ALIVE_MARRIED'):
			if isAliveMarried(ind):
				addRowToPreetyTable(newIndividuals, ind)
		if(filter == 'LIVINGSINGLE_OVERXAGE'):
			if isLivingSingleOverAge(ind, age):
				addRowToPreetyTable(newIndividuals, ind)
	return newIndividuals

def findDeceasedIndividuals(Individuals):
	return filterIndividuals(Individuals, 'DECEASED', None)

def findAliveMarried(Individuals):
	return filterIndividuals(Individuals, 'ALIVE_MARRIED', None)

def findLivingSingleOverXAge(Individuals, age):
	return filterIndividuals(Individuals, 'LIVINGSINGLE_OVERXAGE', age)

def US29(Individuals):
	print('US29 - Deceased Individuals')
	print(findDeceasedIndividuals(Individuals))
US29(Individuals)

def US30(Individuals): #Homework05-UserStory Implemented alone
	print('US30 - Alive Married Individuals')
	print(findAliveMarried(Individuals))
US30(Individuals)

def US31(Individuals, ageOver): # Homework 05-Paired programming partner with Anurag Aman
	print('US31 - Living Single Over 30')
	print(findLivingSingleOverXAge(Individuals, ageOver))
US31(Individuals, 30)

#************************************************** END - DEEPTIDEVI AGRAWAL  **********************************************************************

#************************************************** START- ANURAG AMAN *****************************************************************************
#*************************************************** USER STORY - 17 ***********************************************************************

def US17():
    nf ={}
    error = []
    for x in Families:
        x.border = False
        x.header = False
        val = []
        id=(x.get_string(fields=["ID"]).strip().replace('/',''))
        val.append(x.get_string(fields=["Husband ID"]).strip().replace('/','').split(" ")[0])
        val.append(x.get_string(fields=["Wife ID"]).strip().replace('/','').split(" ")[0])
        val.append(x.get_string(fields=["Children"]).strip().replace('/',''))
        nf[id]=val
    for i in nf:
        childern= nf[i][-1]
        patterns= r'\w+'
        if childern != 'N/A':
            match= re.findall(patterns, childern)
            nf[i].pop()
            nf[i].append(match)
        if (nf[i][0] in nf[i][-1]) or (nf[i][1] in nf[i][-1]):
            error.append(f"US17 - Error : In Family {i} has parents who are married to their children ")
    if error:
        return error
    else:
        return "US17 - No Parents are married to their children"



#*********************** USER STORY - 21 Homework 05-Paired programming partner with Deepti Agarwal ***************************************

def US21():
    nf={}
    error=[]
    for x in Families:
        x.border , x.header  = False , False
        val=[]
        id=(x.get_string(fields=["ID"]).strip().replace('/',''))
        val.append(x.get_string(fields=["Husband ID"]).strip().replace('/','').split(" ")[0])
        val.append(x.get_string(fields=["Wife ID"]).strip().replace('/','').split(" ")[0])
        nf[id]=val
    for i in nf:
        for y in Individuals:
            y.border , y.header = False , False
            if ((y.get_string(fields=["ID"]).strip()) == nf[i][0]) and (y.get_string(fields=["Gender"]).strip()) != 'M' :
                error.append(f"US21 - Error : In Family {i} have parents of wrong gender")
            elif ((y.get_string(fields=["ID"]).strip()) == nf[i][1]) and (y.get_string(fields=["Gender"]).strip()) != 'F':
                error.append(f"US21 - Error : In Family {i} have parents of wrong gender")
    if error:
        return sorted(list(set(error)))
    else:
        return "US21 - No Errors"



#****************************************************** ANURAG AMAN - END ***********************************************************************

#*********************************************** Pradeep Kumar ************************************************************************************


def marriedMale(Individuals):
	marriedMaleAlive = createIndividualsPrettyTable()
	for ind in Individuals:
		ind.border,ind.header = False,False
		if (ind.get_string(fields=['Alive']).strip() == 'True' and ind.get_string(fields=['Spouse']).strip() != 'NA' and ind.get_string(fields=['Gender']).strip() == 'M' and len(ind.get_string(fields=['Spouse']).strip()) > 0):
			marriedMaleAlive.add_row(getIndividualRow(ind))
	return marriedMaleAlive

def marriedFemale(Individuals):
	marriedFemaleAlive = createIndividualsPrettyTable()
	for ind in Individuals:
		ind.border,ind.header = False,False
		if (ind.get_string(fields=['Alive']).strip() == 'True' and ind.get_string(fields=['Spouse']).strip() != 'NA' and ind.get_string(fields=['Gender']).strip() == 'F' and len(ind.get_string(fields=['Spouse']).strip()) > 0):
			marriedFemaleAlive.add_row(getIndividualRow(ind))
	return marriedFemaleAlive

#Homework05 - UserStory Implemented alone
def US46(Individuals):
	print('US46 - Living Married Male')
	print(marriedMale(Individuals))
US46(Individuals)

#Homework05 - -Paired programming with Neil Naidu
def US48(Individuals):
	print('US46 - Living Married Female')
	print(marriedFemale(Individuals))
US48(Individuals)
#####################################################################
##########CODE FOR USER STORY 43##############
def US43():
    cases = []
    fraud = []

    for i in Individuals:

        i.border, i.header = False, False

        if((i.get_string(fields = ["Death"]).strip()) != "NA"):

            id = (i.get_string(fields = ["ID"]).strip().replace('/', ''))
            birthday = datetime.strptime((i.get_string(fields = ["Birthday"]).strip()), '%d %b %Y')
            death = datetime.strptime((i.get_string(fields = ["Death"]).strip()), '%d %b %Y')

            if(datetime.date(birthday) >= datetime.date(death)):
                fraud.append(id)

    if(len(fraud) != 0):
        cases = ", ".join(fraud)
        return 'US43 --> Flagged Individual(s): '+cases+' are recorded as being born after their death.'
    else:
        return "US43 --> No fraudulent entries found."

print(US43())
####### code for User Story 43 ends here #######


##########CODE FOR USER STORY 13##############
def US13():
    cases = []
    infantMortality = []

    for i in Individuals:

        i.border, i.header = False, False

        if((i.get_string(fields = ["Death"]).strip()) != "NA"):

            id = (i.get_string(fields = ["ID"]).strip().replace('/', ''))
            birthday = datetime.strptime((i.get_string(fields = ["Birthday"]).strip()), '%d %b %Y')
            death = datetime.strptime((i.get_string(fields = ["Death"]).strip()), '%d %b %Y')
            daysInYear = 365.2425
            ageAtDeath = datetime.date(death).year - datetime.date(birthday).year
            if(ageAtDeath < 5 and ageAtDeath > 0):
                infantMortality.append(id)

    if(len(infantMortality) != 0):
        cases = ", ".join(infantMortality)
        return 'US13 --> Individual(s) were flagged as infant mortality(ies):'+ cases
    else:
        return "US13 --> No infant mortalities found."
print(US13())
####### code for User Story 13 ends here #######

#*********************** USER STORY - 44 Homework 05-Paired programming with partner: Pradeep Kannabiran ***************************************
##########CODE FOR USER STORY 44##############
def US44():
	deceasedUnmarriedAdults = createIndividualsPrettyTable()
	for i in Individuals:
		i.border,i.header = False,False
		if (i.get_string(fields=['Alive']).strip() == 'False' and i.get_string(fields=['Spouse']).strip() == 'NA' and i.get_string(fields=['Age']).strip() != 'NA' and int(i.get_string(fields=['Age']).strip()) >= 18):
			deceasedUnmarriedAdults.add_row(getIndividualRow(i))
	return deceasedUnmarriedAdults

print("US44 --> Listing all deceased adults who died unmarried:")
print(US44())
####### code for User Story 44 ends here #######

