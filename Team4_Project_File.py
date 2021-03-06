"""
Git repo:- https://github.com/DishantNaik/CS_555_Project
Team :- Anurag Aman , Dhruv Patel , Dishant Naik , Deepti Agarwal, Neil Naidu, Pradeep Kumar
"""
from prettytable import PrettyTable
from datetime import datetime,date,timedelta
import collections
import copy
import re
import operator

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
    col=['NA','NA','NA','NA',-1,True,'NA','NA','NA']
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
            col[4]=int(today.year - born.year - ( (born.month, born.day)> (today.month, today.day) ))
        #Getting the Death details and putting it into the coulm 5
        elif len(data[j].split("|")) >1 and data[j].split("|")[1]=='DEAT':
            col[5]=False
            col[6]=(data[j+1].split("|")[-1])
            death=datetime.strptime((data[j+1].split("|")[-1]), '%d %b %Y')
            col[4]=int(death.year - born.year - ((born.month, born.day) > (death.month, death.day) ))
        #Getting the Family table and populating the child and spouse.
        elif len(data[j].split("|")) >1 and data[j].split("|")[1]=='FAMC':
            a.add((data[j].split("|")[-1]).replace('@',''))
            col[7]=str(a)
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

# COMMON METHODS
def getID(ind):
    #refactor
    id = (ind.get_string(fields = ["ID"]).strip().replace('/',''))
    return id

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

####################################### Story 32 ###########################################

def US32():
    multipleBirths = []
    totalBirths = []
    for row in Individuals:
        row.border = False
        row.header = False
        if((row.get_string(fields=["Birthday"]).strip()=='NA')==False):
            birthstr = row.get_string(fields=["Birthday"]).strip()
            totalBirths.append(birthstr)
    all_freq = {}
    for i in totalBirths:
        if i in all_freq:
            all_freq[i] += 1
        else:
            all_freq[i] = 1
    for i in all_freq:
        if(all_freq[i]>=2):
            multipleBirths.append(f"US32 - Multiple Births - {i} is a multiple birthdate.")

    if multipleBirths:
        return multipleBirths
    else:
        return(['US32 - There are no Multiple Births'])


print('US32 - ',US32())


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

####################################### Story 14 ###########################################
# No more than five siblings should be born at the same time

def US14():
    results = list()
    for i in Families:
        i.border = False
        i.header = False
        siblings = list()

        tmp = i.get_string(fields = ["Children"]).strip()

        tmp = tmp.split(',')

        for j in tmp:
            result = re.sub('[\W_]+', '',j)
            siblings.append(result)

        birth_dates = list()
        for k in Individuals:
            k.border = False
            k.header = False
            tmp = k.get_string(fields = ["ID"]).strip()
            # print(tmp)
            for l in siblings:
                if(tmp == l):
                    if(k.get_string(fields = ["Birthday"]).strip() != 'NA'):
                        birth_dates.append(datetime.strptime((k.get_string(fields = ["Birthday"]).strip()), '%d %b %Y'))
                    else: birth_dates.append('NA')


        results.append(check(birth_dates))

    if(len(results) > 5):
        for m in results:
            if(m == True):
                return('ERROR')
            else: return('NO ERROR FOUND')

    else: return('NO ERROR FOUND')

def check(a):
    return all(i == a[0] for i in a)


print('US14 - ',US14())

####################################### Story 09 ###########################################
# Birth before death of parents
def get_childs(fam_id):

    for j in Families:
        j.border = False
        j.header = False
        if(j.get_string(fields = ["ID"]).strip() == fam_id):
            siblings = list()

            tmp = j.get_string(fields = ["Children"]).strip()
            tmp = tmp.split(',')

            for k in tmp:
                result = re.sub('[\W_]+', '',k)
                siblings.append(result)

            birth_dates = list()
            for k in Individuals:
                k.border = False
                k.header = False
                tmp = k.get_string(fields = ["ID"]).strip()
                # print(tmp)
                for l in siblings:
                    if(tmp == l):
                        if(k.get_string(fields = ["Birthday"]).strip() != 'NA'):
                            tt = datetime.strptime((k.get_string(fields = ["Birthday"]).strip()), '%d %b %Y')
                            tt = tt.now().date()
                            birth_dates.append(tt)

            return(birth_dates)



def US09():

    for i in Families:
        i.border = False
        i.header = False

        # Getting parents data
        parent_id1 = i.get_string(fields = ["Husband ID"]).strip()
        parent_id2 = i.get_string(fields = ["Wife ID"]).strip()
        fam_id = i.get_string(fields = ["ID"]).strip()

        hus_deth, wif_deth = '',''
        for m in Individuals:
            m.border = False
            m.header = False

            if(m.get_string(fields = ["ID"]).strip() == parent_id1):
                if(m.get_string(fields = ["Death"]).strip() != "NA"):
                    hus_deth = datetime.strptime((m.get_string(fields = ["Death"]).strip()), '%d %b %Y')
                    hus_deth = hus_deth.now().date()
                else: hus_deth = 'NA'
                # print(type(hus_deth))

            if(m.get_string(fields = ["ID"]).strip() == parent_id2):
                if(m.get_string(fields = ["Death"]).strip() != "NA"):
                    wif_deth = datetime.strptime((m.get_string(fields = ["Death"]).strip()), '%d %b %Y')
                    wif_deth = wif_deth.now().date()
                else: wif_deth = 'NA'
                # print(wif_deth)

            # tmp = get_childs(fam_id)
            # print(tmp)
            # print('------------')

            flag = list()

            # if(type(hus_deth) is datetime.date):
            #     tmp = get_childs(fam_id)

            #     for x in tmp:
            #         diff_with_dad = (hus_deth - x).days

            #         if(diff_with_dad > 0):
            #             flag.append(True)
            #         else: flag.append(False)

            # if(type(wif_deth) is datetime.date):
            #     tmp = get_childs(fam_id)

            #     for x in tmp:
            #         diff_with_mom = (wif_deth - x).days

            #         if(diff_with_mom > 0):
            #             flag.append(True)
            #         else: flag.append(False)


            if(type(hus_deth) is datetime.date and type(wif_deth) is datetime.date):
                tmp = get_childs(fam_id)

                for x in tmp:

                    diff_with_dad =  abs((hus_deth - x).days)
                    diff_with_mom =  abs((wif_deth - x).days)

                    if(diff_with_dad > 0 and diff_with_mom > 0):
                        flag.append(True)
                    else: flag.append(False)

            elif(type(hus_deth) is datetime.date and type(wif_deth) is not datetime.date):
                tmp = get_childs(fam_id)

                for x in tmp:
                    diff_with_dad =  abs((hus_deth - x).days)

                    if(diff_with_dad > 0):
                        flag.append(True)
                    else: flag.append(False)

            elif(type(hus_deth) is not datetime.date and type(wif_deth) is datetime.date):
                tmp = get_childs(fam_id)

                for x in tmp:

                    diff_with_mom =  abs((wif_deth - x).days)

                    if(diff_with_mom > 0):
                        flag.append(True)
                    else: flag.append(False)

            else: flag.append(True)

            for q in flag:
                if(q == False):
                    return('Error Found')

            return('No Error found')

print('US09 - ',US09())

####################################### Story 08 ###########################################
# Birth after marriage of parents

def US08():

    for i in Families:
        i.border = False
        i.header = False

        # Getting parents data
        # parent_id1 = i.get_string(fields = ["Husband ID"]).strip()
        # parent_id2 = i.get_string(fields = ["Wife ID"]).strip()
        parant_mrg = datetime.strptime((i.get_string(fields = ["Married"]).strip()), '%d %b %Y')
        fam_id = i.get_string(fields = ["ID"]).strip()

        tmp = get_childs(fam_id)

        for j in tmp:
            for k in Individuals:
                if(k.get_string(fields = ["ID"]).strip() == j):
                    tmp1 = datetime.strptime((k.get_string(fields = ["Married"]).strip()), '%d %b %Y')

                    if(abs((parant_mrg - tmp1).days) <= 0):
                        return('Error found at ', k)

    return('No error found')



print('US08 - ',US08())

####################################### Story 42 ###########################################
# Reject illegitimate dates
def US42():
    error = list()
    mon_30 = ['APR','JUN','SEP','NOV']
    mon_31 = ['JAN','MAR','MAY','JUL','AUG','OCT','DEC']
    for i in Individuals:
        i.border = False
        i.header = False

        if(i.get_string(fields = ["Birthday"]).strip() != 'NA'):
            tmp = (datetime.strptime((i.get_string(fields = ["Birthday"]).strip()), '%d %b %Y'))
            tmp_mon = tmp.month
            tmp_day = tmp.day

            if (tmp_mon in mon_30):
                if(tmp_day >= 1 and tmp_day <= 30):
                    continue
                else: error.append(tmp)
            if (tmp_mon in mon_31):
                if(tmp_day >= 1 and tmp_day <= 31):
                    continue
                else: error.append(tmp)
            if (tmp_mon == 'FEB'):
                if(tmp_day >= 1 and tmp_day <= 29):
                    continue
                else: error.append(tmp)


        if(i.get_string(fields = ["Death"]).strip() != 'NA'):
            tmp2 = (datetime.strptime((i.get_string(fields = ["Death"]).strip()), '%d %b %Y'))
            tmp1_mon = tmp2.month
            tmp1_day = tmp2.day

            if (tmp1_mon in mon_30):
                if(tmp1_day >= 1 and tmp1_day <= 30):
                    continue
                else: error.append(tmp)
            if (tmp1_mon in mon_31):
                if(tmp1_day >= 1 and tmp1_day <= 31):
                    continue
                else: error.append(tmp)
            if (tmp1_mon == 'FEB'):
                if(tmp1_day >= 1 and tmp1_day <= 29):
                    continue
                else: error.append(tmp)

    for j in Families:
        j.border = False
        j.header = False

        if(j.get_string(fields = ["Married"]).strip() != 'NA'):
            tmp = (datetime.strptime((j.get_string(fields = ["Married"]).strip()), '%d %b %Y'))
            tmp_mon = tmp.month
            tmp_day = tmp.day

            if (tmp_mon in mon_30):
                if(tmp_day >= 1 and tmp_day <= 30):
                    continue
                else: error.append(tmp)
            if (tmp_mon in mon_31):
                if(tmp_day >= 1 and tmp_day <= 31):
                    continue
                else: error.append(tmp)
            if (tmp_mon == 'FEB'):
                if(tmp_day >= 1 and tmp_day <= 29):
                    continue
                else: error.append(tmp)

        if(j.get_string(fields = ["Divorced"]).strip() != 'NA'):
            tmp = (datetime.strptime((j.get_string(fields = ["Divorced"]).strip()), '%d %b %Y'))
            tmp1_mon = tmp.month
            tmp1_day = tmp.day

            if (tmp1_mon in mon_30):
                if(tmp1_day >= 1 and tmp1_day <= 30):
                    continue
                else: error.append(tmp)
            if (tmp1_mon in mon_31):
                if(tmp1_day >= 1 and tmp1_day <= 31):
                    continue
                else: error.append(tmp)
            if (tmp1_mon == 'FEB'):
                if(tmp1_day >= 1 and tmp1_day <= 29):
                    continue
                else: error.append(tmp)

    if(len(error) != 0):
        return('ERROR -',error)
    else: return('NO ERROR found')

print('US42 - ',US42())
#************************************************** DHRUV_PATEL **********************************************************************
#************************************************** USER STORY - 05 **********************************************************************

def getMarriage(ind):
    #refactor
    marriageDate = (datetime.strptime((ind.get_string(fields = ["Married"]).strip()), '%d %b %Y'))
    return marriageDate


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

#************************************************** USER STORY - 16 **********************************************************************
def US16():
    family={}
    errors=[]

    for row in Families:
        row.border = False
        row.header = False
        fam=[]

        id = getID(row)

        fam.append(row.get_string(fields=["Husband Name"]).strip().replace('/','').split(" ")[-1].lower())
        fam.append(row.get_string(fields=["Children"]).strip().replace('/',''))

        family[id]=fam

    for i in family:
        childern = family[i][-1]
        patterns = r'\w+'

        if childern != 'NA':
            match = re.findall(patterns, childern)
            child = []

            if (match[0]!='NA'):
                for j in range(0,len(match)):
                    for row in Individuals:
                        row.border = False
                        row.header = False

                        if ((row.get_string(fields=["ID"]).strip()) == match[j]) and (row.get_string(fields=["Gender"]).strip()) == 'M' :
                            child.append(row.get_string(fields=["Name"]).strip().replace('/','').split(" ")[-1].lower())


            family[i].pop()
            family[i] = family[i]+child

    for i in family:
        if(len(family[i])>1):
            if(len(list(set(family[i])))==len(family[i])):
                errors.append(f"US16 - Error : Family {i} has male members with different last names")

    if(len(errors)>0):
        return sorted(errors)
    else:
        return "US16 - No Family has male members with different last names"


print('US16 - ', US16())

#************************************************** USER STORY - 27 **********************************************************************
def US27():
    error=[]
    for row in Individuals:
        row.border = False
        row.header = False

        id = getID(row)

        if(int(row.get_string(fields=["Age"]).strip()) == -1):
            error.append(id)

    error=sorted(error)
    if error:
        str = " ".join(error)
        return f"US27 - Error : Individual {str} has no ages displayed"
    else:
        return "US27 - No errors found"

print('US27 - ', US27())

#************************************************** USER STORY - 15 **********************************************************************
def US15():
    error = set()
    family = {}

    for row in Families:
        row.header = False
        row.border = False

        fam = []
        id = getID(row)

        tmp = row.get_string(fields=["Children"]).strip().replace('/','')
        tmp = tmp.split(',')

        for i in tmp:
            res = re.sub('[\W_]+', '',i)
            fam.append(res)
        family[id] = fam

        for k,v in family.items():
            if len(v) > 15:
                error.add(f"US15 - Family {k} has more than 15 sibiling")

    if error:
        return list(error)
    else:
        return "No error detected"

print('US15 - ',US15())

#************************************************** USER STORY - 34 **********************************************************************
def US34():
    error = []
    lrg_age = set()

    for row in Families:
        row.header = False
        row.border = False

        id = getID(row)
        husid = (row.get_string(fields = ["Husband ID"])).strip()
        wifeid = (row.get_string(fields = ["Wife ID"])).strip()

        h_age, w_age = 0, 0

        for y in Individuals:
            y.header = False
            y.border = False
            if getID(y) == husid:
                h_age = int(y.get_string(fields = ["Age"]).strip())
            if getID(y) == wifeid:
                w_age = int(y.get_string(fields = ["Age"]).strip())

            older = max(h_age, w_age)
            young = min(h_age, w_age)

            if young >= (older/2):
                lrg_age.add(id)

    error.append(f'US34 - Family {sorted(lrg_age)} has a large age difference')
    if error:
        return error
    else:
        return 'No couples with large age difference'

print('US34 - ',US34())

#************************************************** USER STORY - 23 **********************************************************************
def US23():
    names=[]
    dob=[]
    id=[]

    for row in Individuals:
        row.border = False
        row.header = False
        names.append(row.get_string(fields=["Name"]).strip().replace('/',''))
        if (row.get_string(fields=["Birthday"]).strip()) != 'NA':
            dob.append(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
        else:
            dob.append('N/A')
        id.append(row.get_string(fields=["ID"]).strip().replace('/',''))
    error=[]
    for i in range(0,len(names)):
        for j in range(i+1, len(names)):
            if(names[i]==names[j]):
                if(dob[i]==dob[j]):
                    error.append(f"US23 - Error : Individual {id[i]} and {id[j]} Might be the same")
                else:
                    error.append(f"US23 - Error : Individual {id[i]} and {id[j]} Might be the same")


            elif(names[i]!=names[j]):
                if(dob[i]==dob[j]):
                    error.append(f"US23 - Error : Individual {id[i]} and {id[j]} Might be the same")


    if len(error)!=0:
        return (error)
    else:
        return ("US23 - No errors found")

print('US23 - ',US23())

#************************************************** USER STORY - 40 **********************************************************************
def US40():
    no_children = set()
    error = []
    for rw in Individuals:
        rw.header = False
        rw.border = False

        ind_id = getID(rw)
        if(rw.get_string(fields=["Child"]).strip() == 'NA'):
            no_children.add(ind_id)

    error.append(f'US40 - Individual {sorted(no_children)} has no children')

    if (len(no_children) != 0):
        return error
    else:
        return 'No Error Found'

print('US40 - ',US40())
#************************************************** START - DEEPTIDEVI AGRAWAL  ********************************************************************
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

def getId(row):  #refactored
	return row.get_string(fields=['ID']).strip()

indsDict = dict()
familyDict = dict()
def populateIndividualDict(Individuals):
	for ind in Individuals:
		ind = disableHeaderBorder(ind)
		indsDict[getId(ind)] = ind

def populateFamiliesDict(Families):
	for family in Families:
		fam = disableHeaderBorder(family)
		familyDict[getId(fam)] = fam

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

def getHusbandId(fam):  #refactored
	return fam is not None and fam.get_string(fields = ["Husband ID"]).strip()

def getWifeId(fam):  #refactored
	return fam is not None and fam.get_string(fields = ["Wife ID"]).strip()

def getAge(ind):  #refactored
	age = ind.get_string(fields = ["Age"]).strip()
	if age != -1:
		return int(age)
	else:
		return -1

def getFamilyOfChild(ind):  #refactored
	return ind.get_string(fields = ["Child"]).strip().replace('{','').replace('}','').replace('\'','')

def isAlive(ind):  #refactored
	return ind.get_string(fields=['Alive']).strip() == 'True'

def hasDeathDate(ind):  #refactored
	return ind.get_string(fields=['Death']).strip() != 'NA'

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

def hasBirthday(ind):
	return ind.get_string(fields=['Birthday']).strip() != 'NA'

def getdate(ind, dateType):
	return (datetime.strptime((ind.get_string(fields = [dateType]).strip()), '%d %b %Y'))

def isRecentBirthWithinDays(ind, days):
	return isAlive(ind) and hasBirthday(ind) and (datetime.now() - getdate(ind, "Birthday")).days < days and not ((datetime.now() - getdate(ind, "Birthday")).days < 0 )

def daysLeftForNextBirthday(ind):
	try:
		indBirthday = getdate(ind, "Birthday")
		today = datetime.now()
		if(today.month == indBirthday.month and today.day >= indBirthday.day or today.month > indBirthday.month):
			nextBirthdayYear = today.year + 1
		else:
			nextBirthdayYear = today.year
		nextBirthday = datetime.strptime(('%d %d %d' % ( indBirthday.day , indBirthday.month, nextBirthdayYear)), '%d %m %Y')
		return (nextBirthday - today).days
	except:
		return -1

def isUpcomingBirthdayWithinDays(ind, days):
	daysLeft = daysLeftForNextBirthday(ind)
	return hasBirthday(ind) and daysLeft <= days and daysLeft >= 0

def isAgeYoungerThanXAge(ind, days):
	return getAge(ind) >=0 and getAge(ind) < days

def areBothParentsDead(ind):
	areDead = False
	father = None
	mother = None
	if(getFamilyOfChild(ind) != 'NA'):
		fam = familyDict.get(getFamilyOfChild(ind))
		if fam is not None and getHusbandId(fam) != 'NA':
			father = indsDict[getHusbandId(fam)]
		if fam is not None and  getWifeId(fam) != 'NA':
			mother = indsDict[getWifeId(fam)]
		areDead =  (father is None or (father is not None and not isAlive(father))) and ( mother is None or (mother is not None and not isAlive(mother)))
	return areDead

def isOrphansYoungerThanAge(ind, days):
	return isAgeYoungerThanXAge(ind, days) and areBothParentsDead(ind)

def isRecentDeathWithinDays(ind, days):
	return not isAlive(ind) and hasDeathDate(ind) and (datetime.now() - getdate(ind, "Death")).days < days and not ((datetime.now() - getdate(ind, "Death")).days < 0 )

def addRowToPreetyTable(prettyTable, ind): #refactored
	prettyTable.add_row(getIndividualRow(ind))

def filterIndividuals(Individuals, filter, n): #refactored
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
			if isLivingSingleOverAge(ind, n):
				addRowToPreetyTable(newIndividuals, ind)
		if(filter == 'RECENTBIRTH_WITHINXDAYS'):
			if isRecentBirthWithinDays(ind, n):
				addRowToPreetyTable(newIndividuals, ind)
		if(filter == 'RECENTDEATHS_WITHINXDAYS'):
			if isRecentDeathWithinDays(ind, n):
				addRowToPreetyTable(newIndividuals, ind)
		if(filter == 'UPCOMINGBIRTHDAY_WITHINXDAYS'):
			if isUpcomingBirthdayWithinDays(ind, n):
				addRowToPreetyTable(newIndividuals, ind)
		if(filter == 'ORPHANS_YOUNGERTHANXAGE'):
			if isOrphansYoungerThanAge(ind, n):
				addRowToPreetyTable(newIndividuals, ind)

	return newIndividuals

def findDeceasedIndividuals(Individuals):
	return filterIndividuals(Individuals, 'DECEASED', None)

def findAliveMarried(Individuals):
	return filterIndividuals(Individuals, 'ALIVE_MARRIED', None)

def findLivingSingleOverXAge(Individuals, age):
	return filterIndividuals(Individuals, 'LIVINGSINGLE_OVERXAGE', age)

def findRecentBirthsWithinLastNDays(Individuals, days):
	return filterIndividuals(Individuals, 'RECENTBIRTH_WITHINXDAYS', days)

def findRecentDeathsWithinLastNDays(Individuals, days):
	return filterIndividuals(Individuals, 'RECENTDEATHS_WITHINXDAYS', days)

def findUpcomingBirthdaysInNextNDays(Individuals, days):
	return filterIndividuals(Individuals, 'UPCOMINGBIRTHDAY_WITHINXDAYS', days)

def findOrphansYoungerThan(Individuals, childAge):
	return filterIndividuals(Individuals, 'ORPHANS_YOUNGERTHANXAGE', childAge)

def orderSiblingsByDecAgeInFamily(Individuals):
	Individuals = Individuals.get_string(sort_key=operator.itemgetter(8,5), sortby="Age", reversesort = True)
	return Individuals

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

def US35(Individuals, birthsWithinLastNDays):
	print('US35 - Recent Births Within Last 30 Days')
	print(findRecentBirthsWithinLastNDays(Individuals, birthsWithinLastNDays))
US35(Individuals, 30)

def US36(Individuals, deathsWithinLastNDays):
	print('US36 - Recent Deaths Within Last 30 Days')
	print(findRecentDeathsWithinLastNDays(Individuals, deathsWithinLastNDays))
US36(Individuals, 30)

def US38(Individuals, birthdaysInNextNDays):
	print('US38 - Upcoming birthdays in next 30 Days')
	print(findUpcomingBirthdaysInNextNDays(Individuals, birthdaysInNextNDays))
US38(Individuals, 30)

def US33(Individuals, Families, childAge):
	print('US33 - Orphans(both parents dead and child < 18 years old)')
	populateIndividualDict(Individuals)
	populateFamiliesDict(Families)
	print(findOrphansYoungerThan(Individuals, childAge))
US33(Individuals, Families, 18)

def US28(Individuals):
	print('US28 - Order siblings in families by decreasing age, i.e. oldest siblings first')
	print(orderSiblingsByDecAgeInFamily(Individuals))
US28(Individuals)
#************************************************** END - DEEPTIDEVI AGRAWAL  **********************************************************************

#************************************************** START- ANURAG AMAN *****************************************************************************

#************************************************** USER STORY-07 **********************************************************************************
def US07():
    errors=[]
    for row3 in Individuals:
        row3.border , row3.header = False , False
        id = (row3.get_string(fields = ["ID"]).strip().replace('/',''))
        if((row3.get_string(fields = ["Age"]).strip()) != 'NA'):
            age = int((row3.get_string(fields = ["Age"]).strip()))
            if(age >= 150):
                errors.append(id)

    if(len(errors) != 0):
        strerror=" ".join(errors)
        return f'US07 - Error : Individual - {strerror} have age more than 150 years old'
    else:
        return "US07 - No errors found "
#******************************************************USER STORY 25 *********************************************************************************

def US25():
    family={}
    errors=[]
    for row in Families:
        row.border , row.header = False , False
        fam=[]
        id=(row.get_string(fields=["ID"]).strip().replace('/',''))
        fam.append(row.get_string(fields=["Children"]).strip().replace('/',''))
        family[id]=fam

    for i in family:
        childern= family[i][0]
        patterns= r'\w+'
        if childern != 'NA':
            match= re.findall(patterns, childern)
            child=[]
            dob=[]
            if (match[0]!='NA'):
                for j in range(0,len(match)):
                    for row in Individuals:
                        row.border ,row.header = False , False
                        if (row.get_string(fields=["ID"]).strip()) == match[j]:
                            if((row.get_string(fields=["Birthday"]).strip())!='NA'):
                                child.append(row.get_string(fields=["Name"]).strip().replace('/','').split(" ")[0].lower())
                                dob.append(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
            for k in range(0,len(child)):
                for l in range(k+1,len(child)):
                    if(child[k]==child[l]):
                        if(dob[k]==dob[l]):
                            errors.append(f"US25 - Error : Family {i} have children with same name and dob")

    if(len(errors)==0):
        return ("US25 - No error detected.")
    else:
        return (sorted(errors))
#########################################################USER STORY - 02###############################################################################
def US02():
    errors=[]
    for row in Families:
        row.border ,row.header = False , False
        married=(datetime.strptime((row.get_string(fields=["Married"]).strip()), '%d %b %Y'))
        Husband = (row.get_string(fields=["Husband ID"]).strip())
        Wife = (row.get_string(fields=["Wife ID"]).strip())
        for x in Individuals:
            x.border, x.header = False , False
            if x.get_string(fields=["ID"]).strip() == Husband:
                if (x.get_string(fields=["Birthday"]).strip())!='N/A':
                    husbanddate=(datetime.strptime((x.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
                if(husbanddate>married):
                    errors.append(f"US02 - Error : individual {Husband} birthdate {husbanddate} occurs after marriage {married}")
            if x.get_string(fields=["ID"]).strip() == Wife:
                if (x.get_string(fields=["Birthday"]).strip())!='N/A':
                    wifebdate=(datetime.strptime((x.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
                if(wifebdate>married):
                    errors.append(f"US02 - Error : individual {Wife} birthdate-{wifebdate} occurs after marriage {married}")
    return errors

###########################################################USER STORY -01 ###########################################################

def US01():
    dates=[]
    errors=[]
    for row in Individuals:
        row.border ,row.header = False , False
        if((row.get_string(fields=["Birthday"]).strip()=='NA')==False):
            birthstr=row.get_string(fields=["Birthday"]).strip()
            birth=(datetime.strptime((row.get_string(fields=["Birthday"]).strip()), '%d %b %Y'))
            if(datetime.date(birth) > date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                errors.append(f"US01 - Error : Individual - {id} Birthday {birthstr} occurs in the future")

        if((row.get_string(fields=["Death"]).strip()=='NA')==False):
            birthstr=row.get_string(fields=["Death"]).strip()
            birth=(datetime.strptime((row.get_string(fields=["Death"]).strip()), '%d %b %Y'))
            if(datetime.date(birth) > date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                errors.append(f"US01 - Error : Individual - {id} Death {birthstr} occurs in the future")
    for row in Families:
        row.border ,row.header = False , False
        if((row.get_string(fields=["Married"]).strip()=='NA')==False):
            marriedstr=row.get_string(fields=["Married"]).strip()
            married=(datetime.strptime((row.get_string(fields=["Married"]).strip()), '%d %b %Y'))
            if(datetime.date(married) > date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                errors.append(f"US01 - Error : Family ID - {id} Married {marriedstr} occurs in the future")
        if((row.get_string(fields=["Divorced"]).strip()=='NA')==False):
            deathstr=row.get_string(fields=["Divorced"]).strip()
            death=(datetime.strptime((row.get_string(fields=["Divorced"]).strip()), '%d %b %Y'))
            if(datetime.date(death) > date.today()):
                id=(row.get_string(fields=["ID"]).strip().replace('/',''))
                errors.append(f"US01 - Error : Family ID - {id} Divorced {deathstr} occurs in the future")


    for i in dates:
        if(datetime.date(i) > date.today()):
            errors.append(i)


    return errors

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

#*************************************** US03 ********************************************************************************************
def US03():
    errors=[]
    for x in Individuals:
            x.border ,x.header = False , False
            id=(x.get_string(fields = ["ID"]).strip().replace('/',''))
            if((x.get_string(fields = ["Birthday"]).strip()) != 'NA'):
                birthdays = (datetime.strptime((x.get_string(fields = ["Birthday"]).strip()), '%d %b %Y'))
                if((x.get_string(fields = ["Death"]).strip()) != 'NA'):
                    death = (datetime.strptime((x.get_string(fields = ["Death"]).strip()), '%d %b %Y'))
                    if(datetime.date(birthdays)>datetime.date(death) or datetime.date(birthdays) > date.today()):
                        errors.append(id)
    if(len(errors) != 0):
        strerror=" ".join(errors)
        return f'US03 - Error : Individual - {strerror} have death before birthday'
    else:
        return " US03 - No errors found "
print(US03())

#************************************* US06 ***********************************************************************************************
def US06():
    errors=[]
    for y in Families:
        y.border ,y.header = False , False
        if((y.get_string(fields = ["Divorced"]).strip()) != 'NA'):
            divorce = (datetime.strptime((y.get_string(fields = ["Divorced"]).strip()), '%d %b %Y'))
            husid = (y.get_string(fields = ["Husband ID"])).strip()
            wifeid = (y.get_string(fields = ["Wife ID"])).strip()
            for x in Individuals:
                x.border , x.header = False , False
                id = (x.get_string(fields = ["ID"]).strip().replace('/',''))
                if(husid==id or wifeid==id ):
                    if((x.get_string(fields = ["Death"]).strip()) != 'NA'):
                        death = (datetime.strptime((x.get_string(fields = ["Death"]).strip()), '%d %b %Y'))
                        if(datetime.date(divorce) > datetime.date(death)):
                            errors.append(id)

    if(len(errors) != 0):
        strerror=" ".join(errors)
        return f'US06 - Error : Individual - {strerror} have death before divorce'
    else:
        return "US06 - No errors found "
print(US06())



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
	print('US48 - Living Married Female')
	print(marriedFemale(Individuals))
US48(Individuals)

#************************************************** USER STORY - 47 **********************************************************************

def US47():
    print('US47 - Children with Single parent')
    singleParentChild = createIndividualsPrettyTable()
    bad_chars = ['{\'', '\'', '{', '}','\'}']
    childSP = set()
    for ab in Families:
        ab.border,ab.header = False,False
        if (ab.get_string(fields=['Children']).strip() != 'NA' and ab.get_string(fields=['Divorced']).strip() != 'NA'):
            temp = ab.get_string(fields=['Children']).strip()
            for i in bad_chars :
                temp = temp.replace(i, '')
            temp_1 = temp.split(", ")
            for j in temp_1 :
                childSP.add(j)
    for ab in Individuals:
        ab.border,ab.header = False,False
        if(ab.get_string(fields=['ID']).strip() in childSP):
            singleParentChild.add_row(getIndividualRow(ab))
    print(singleParentChild)
US47()


def checkSiblings(sibID, spouse_ID):
    for x in Families:
        x.border,x.header = False,False
        flag = True
        sibHusID = x.get_string(fields=['Husband ID']).strip()
        sibWifeID = x.get_string(fields=['Wife ID']).strip()
        if(sibHusID == sibID or sibWifeID == sibID):
            sibChildren = x.get_string(fields=['Children']).strip()
            if(sibChildren.find(spouse_ID) != -1):
                flag = False
                return flag
    return flag

#************************************************** USER STORY - 20 **********************************************************************

def US20() :
    print('US20 - Aunts and Uncles')
    for ab in Families:
        flag = True
        ab.border,ab.header = False,False
        hus_ID = ab.get_string(fields=['Husband ID']).strip()
        wife_ID = ab.get_string(fields=['Wife ID']).strip()
        for h in Families:
            h.border,h.header = False,False
            sib = h.get_string(fields=['Children']).strip()
            if(hus_ID in sib):
                bad_chars = ['{\'', '\'', '{', '}','\'}']
                for i in bad_chars :
                    sib = sib.replace(i, '')
                    temp = sib.split(", ")
                for i in temp:
                    if(i == hus_ID): continue
                    flag = checkSiblings(i, wife_ID)
        for h in Families:
            h.border,h.header = False,False
            sib = h.get_string(fields=['Children']).strip()
            if(wife_ID in sib):
                bad_chars = ['{\'', '\'', '{', '}','\'}']
                for i in bad_chars :
                    sib = sib.replace(i, '')
                    temp = sib.split(", ")
                for i in temp:
                    if(i == wife_ID): continue
                    flag = checkSiblings(i, hus_ID)
        if(flag == False):
            print(hus_ID, "and ", wife_ID, " have avunculate marriage")
            break
    if(flag == True):
        print("No one in the family have avunculate marriage")
US20()

#************************************************** USER STORY - 24 **********************************************************************

def US24() :
    print('US24 - Unique families by spouses')
    for ab in Families:
        flag = True
        ab.border,ab.header = False,False
        hus = ab.get_string(fields=['Husband Name']).strip()
        wife = ab.get_string(fields=['Wife Name']).strip()
        mar_date = ab.get_string(fields=['Married']).strip()
        fam_id = ab.get_string(fields=['ID']).strip()
        for h in Families:
            h.border,h.header = False,False
            hus_test = h.get_string(fields=['Husband Name']).strip()
            wife_test = h.get_string(fields=['Wife Name']).strip()
            fam_id_test = h.get_string(fields=['ID']).strip()
            mar_date_test = h.get_string(fields=['Married']).strip()
            if(fam_id == fam_id_test):
                continue
            if(hus_test == hus and wife == wife_test and mar_date == mar_date_test) :
                flag = False
                print("Family : ", fam_id, " and ", fam_id_test, " are having same spouses by name and marriage date ")
                break
        if(flag == False):
            break
    if(flag):
        print("All the families in the GEDCOM file are unique")
US24()

#************************************************** USER STORY - 26 **********************************************************************

def US26():
    print('US26 - Corresponding entries')
    entriesIndividual = createIndividualsPrettyTable()
    entriesFamilies = createIndividualsPrettyTable()
    count = True
    for ind in Individuals:
        flag = True
        ind.border,ind.header = False,False
        ind_ID = ind.get_string(fields=['ID']).strip()
        ind_child = ind.get_string(fields=['Child']).strip()
        ind_spouse = ind.get_string(fields=['Spouse']).strip()
        ind_name = ind.get_string(fields=['Name']).strip()
        for f in Families:
            f.border,f.header = False,False
            fam_ID = f.get_string(fields=['ID']).strip()
            fam_hus = f.get_string(fields=['Husband Name']).strip()
            fam_wife = f.get_string(fields=['Wife Name']).strip()
            fam_child = f.get_string(fields=['Children']).strip()
            if fam_ID in ind_spouse :
                if(fam_hus != ind_name and fam_wife != ind_name) :
                    flag = False
            if(fam_ID in ind_child) :
                if ind_ID not in fam_child :
                    flag = False
        if(flag == False):
            entriesIndividual.add_row(getIndividualRow(ind))
            count = False
    if(count):
        print("All family roles specified in an individual record have their corresponding entries in the corresponding family records")
    else:
        print("The Individuals without their corresponding entries in family records")
        print(entriesIndividual)
    count = True
    for f in Families:
        flag = True
        f.border,f.header = False,False
        fam_ID = f.get_string(fields=['ID']).strip()
        fam_child = f.get_string(fields=['Children']).strip()
        fam_husID = f.get_string(fields=['Husband ID']).strip()
        fam_wifeID = f.get_string(fields=['Wife Name']).strip()
        for ind in Individuals:
            ind.border,ind.header = False,False
            ind_ID = ind.get_string(fields=['ID']).strip()
            ind_child = ind.get_string(fields=['Child']).strip()
            ind_spouse = ind.get_string(fields=['Spouse']).strip()
            ind_name = ind.get_string(fields=['Name']).strip()
            if fam_husID == ind_ID :
                if fam_ID not in ind_spouse :
                    flag = False
                    count = False
                    entriesFamilies.add_row(getIndividualRow(ind))
            if fam_wifeID == ind_ID :
                if fam_ID not in ind_spouse :
                    flag = False
                    count = False
                    entriesFamilies.add_row(getIndividualRow(ind))
    if(count):
        print("All Individual roles specified in Family record have their corresponding entries in the corresponding individual records")
    else:
        print("The Individuals without their corresponding entries in Individual records")
        print(entriesFamilies)
US26()

#************************************************** USER STORY - 37 **********************************************************************

def US37():
    result = set()
    indi = []
    yy = date.today()
    yy = yy.year
    present = datetime.now()
    lastMonth = present - timedelta(days=30)
    for i in Individuals:
        i.border,i.header = False,False
        if(i.get_string(fields=['Alive']).strip() != "True"):
            deathDate = datetime.strptime((i.get_string(fields=['Death']).strip()), '%d %b %Y')
            if(deathDate > lastMonth ):
                spouseFam = i.get_string(fields=['Spouse']).strip()
                indivID = i.get_string(fields=['ID']).strip()
                for j in spouseFam:
                    for f in Families:
                        if(f.get_string(fields=['ID']).strip() == j):
                            if(f.get_string(fields=['Husband ID']).strip() == indivID):
                                wifeID = f.get_string(fields=['Wife ID']).strip()
                                indi.append(wifeID)
                            else :
                                husbandID = f.get_string(fields=['Husband ID']).strip()
                                indi.append(husbandID)
                            childrn = f.get_string(fields=['Children']).strip()
                            bad_chars = ['{\'', '\'', '{', '}','\'}']
                            for b in bad_chars :
                                childrn = childrn.replace(b, '')
                                temp = childrn.split(", ")
                            for t in temp :
                                indi.append(t)
                            break
    for i in Individuals:
        i.border,i.header = False,False
        for j in indi:
            if(i.get_string(fields=['ID']).strip() == j and i.get_string(fields=['Alive']).strip() == "True"):
                result.add(j)

    if(result == set()):
        return "No one in the GEDCOM file died in the last 30days"
    return result

print("US37 - ", US37())

#************************************************** USER STORY - 41 **********************************************************************

def US41():
    for i in Individuals:
        i.border,i.header = False,False
        flag = 0
        if(i.get_string(fields = ["Birthday"]).strip() != 'NA'):
            temp = (datetime.strptime((i.get_string(fields = ["Birthday"]).strip()), '%d %b %Y'))
            temp_month = temp.month
            temp_day = temp.day
            temp_year = temp.year
            if(temp_year == 0000):
                print(i.get_string(fields = ["ID"]).strip(), " has no year in the Birthdate")
            if(temp_day == 00 or temp_month == 00):
                flag = 1
        if(i.get_string(fields = ["Death"]).strip() != 'NA'):
            temp1 = (datetime.strptime((i.get_string(fields = ["Death"]).strip()), '%d %b %Y'))
            temp_month1 = temp1.month
            temp_day1 = temp1.day
            temp_year1 = temp1.year
            if(temp_year1 == 0000):
                print(i.get_string(fields = ["ID"]).strip(), " has no year in the Death date")
            if(temp_day1 == 00 or temp_month1 == 00):
                flag = 1
    
    for f in Families:
        f.border,f.header = False,False
        if(f.get_string(fields = ["Married"]).strip() != 'NA'):
            temp = (datetime.strptime((f.get_string(fields = ["Married"]).strip()), '%d %b %Y'))
            temp_month = temp.month
            temp_day = temp.day
            temp_year = temp.year
            if(temp_year == 0000):
                print(f.get_string(fields = ["ID"]).strip(), " has no year in the Marriage date")
            if(temp_day == 00 or temp_month == 00):
                flag = 1
        if(f.get_string(fields = ["Divorced"]).strip() != 'NA'):
            temp1 = (datetime.strptime((f.get_string(fields = ["Divorced"]).strip()), '%d %b %Y'))
            temp_month1 = temp1.month
            temp_day1 = temp1.day
            temp_year1 = temp1.year
            if(temp_year1 == 0000):
                print(f.get_string(fields = ["ID"]).strip(), " has no year in the Divorce date")
            if(temp_day1 == 00 or temp_month1 == 00):
                flag = 1
    if(flag == 1):
        return "Partial dates without days and months are Included"
    else :
        return "All dates in the GEDCOM file are complete "

print("US41 - ", US41())


#*********************************************** Pradeep Kumar END ************************************************************************************
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

##########CODE FOR USER STORY 18##############

def US18() :
    count = 0
    for i in Families:
        i.border,i.header = False,False
        husband = i.get_string(fields=['Husband ID']).strip()
        wife = i.get_string(fields=['Wife ID']).strip()

        for j in Families:
            j.border, j.header = False,False
            listOfSiblings = j.get_string(fields=['Children']).strip()

            """ fam1= " ", fam2= " "
            for k in Individuals:
                k.border, k.header = False,False
                if(husband == k.get_string(fields=['ID']).strip()):
                    fam1 = k.get_string(fields=['Children']).strip()
                if(husband == k.get_string(fields=['ID']).strip()):
                    fam2 = k.get_string(fields=['Children']).strip()
            if(fam1 == fam2): """

            if((husband in listOfSiblings) and (wife in listOfSiblings)):
                		flaggedMarriage = husband + " and " + wife
                		print(flaggedMarriage)
                		count+= 1

    if(count == 0):
        print("None found")
    else:
        print(str(count) + " incestuous marriages found.")

print("US18 --> Listing all couples with incestuous marriages:")
###### code for User Story 18 ends here ######
US18()

##########CODE FOR USER STORY 19##############
def US19():
    family={}
    flag = False

    for i in Families:
        i.border = False
        i.header = False
        entry=[]
        id=getID(i)
        entry.append(i.get_string(fields=["Husband Name"]).strip().replace('/','').split(" ")[-1].lower())
        entry.append(i.get_string(fields=["Children"]).strip().replace('/',''))
        family[id]=entry

    for i in family:
        childern= family[i][-1]
        patterns= r'\w+'

        if childern != 'NA':
            match= re.findall(patterns, childern)
            child=[]
            if (match[0]!='NA'):
                for j in range(0,len(match)):
                    for k in Individuals:
                        k.border = False
                        k.header = False

                        if ((k.get_string(fields=["ID"]).strip()) == match[j]) and (k.get_string(fields=["Gender"]).strip()) == 'F' :
                            child.append(k.get_string(fields=["Name"]).strip().replace('/','').split(" ")[-1].lower())

            family[i].pop()
            family[i] = family[i] + child

    for i in family:
        if(len(family[i]) > 1):
            if(len(list(set(family[i]))) == len(family[i])):
                print("Family (ID:"+ i +") has female members with different last names")
                flag = True

    if(flag == False):
        print("No different names found")
print("US19 --> Last name verification of females:")
###### code for User Story 19 ends here ######
US19()


def US11():
    count = 0

    for i in Families:
        i.border = False
        i.header = False
        husband = i.get_string(fields=["Husband Name"]).strip().replace('/','')
        wife = i.get_string(fields=["Wife Name"]).strip().replace('/','')
        iD = i.get_string(fields=["ID"]).strip().replace('/','')
        for j in Families:
            j.border = False
            j.header = False
            pCheckH = j.get_string(fields=["Husband Name"]).strip()
            pCheckW = j.get_string(fields=["Wife Name"]).strip()
            pCheckId = j.get_string(fields=["ID"]).strip()
            divorce_status = j.get_string(fields=['Divorced']).strip()
            if pCheckId == iD:
                continue
            if (pCheckH == husband and wife == pCheckW):
                if (divorce_status != 'NA'):
                    count+=1
                    print(pCheckId,": is a marriage that violates the polygamy law")
                    break

    if count == 0:
        print('None Found')

print('US11 --> Listing all polygamous marriage:')
##### code for User Story 11 ends here #####
US11()

# ##########CODE FOR USER STORY 12##############
def US12():
    cases = []
    flagged = []
    ageDiff = 0

    for i in Individuals:
        i.border, i.header = False, False
        if((i.get_string(fields = ["ID"]).strip()) != "NA"):
            id = (i.get_string(fields=['ID']).strip().replace('/', ''))
            if (i.get_string(fields=['Birthday']).strip() != 'NA'):
                birthday = datetime.strptime((i.get_string(fields=['Birthday']).strip()), '%d %b %Y')
                if (i.get_string(fields=['Death']).strip() != 'NA'):
                    parent = datetime.strptime((i.get_string(fields=['Death']).strip()), '%d %b %Y')
                    ageDiff = datetime.date(parent).year - datetime.date(birthday).year
            if(ageDiff < 0 or ageDiff > 80):
                flagged.append(id)

    if(len(flagged) != 0):
        cases = ', '.join(flagged)
        print('US12 --> Individual(s) were flagged:' + cases)
    else:
        print('US12 --> No cases found.')

###### code for User Story 12 ends here ######
print("US12 --> Age verification of offspring:")
US12()

##########CODE FOR USER STORY 45##############
def US45():
    flag = False

    for i in Families:
        i.border = False
        i.header = False
        wife_name = i.get_string(fields=["Wife Name"]).strip()
        index = wife_name.index('/')
        maiden_name = wife_name[index:]
        print(maiden_name)
        flag = True

    if(flag == False):
        print("No maiden names found")

###### code for User Story 45 ends here ######
print("US45 --> Maiden names of married females:")
US45()