"""
Git repo:- https://github.com/DishantNaik/CS_555_Project
Team :- Anurag Aman , Dhruv Patel , Dishant Naik , Deepti Agarwal
"""

from prettytable import PrettyTable
from datetime import datetime,date,timedelta
import copy
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

fp=open('Testing.ged')
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
    b= set()
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

#Retriving the family details
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
####################################### Story 1 ###########################################
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
        if(i.get_string(fields=['Alive']).strip() == 'True' and i.get_string(fields=['Spouse']).strip() != 'NA'):
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
print(US39())

#************************************************** DHRUV_PATEL **********************************************************************

def US05():
    errors = []
    for i in Families:
        i.border = False
        i.header = False

        if ((i.get_string(fields = ["Married"]).strip()) != 'NA'):
            marriage = (datetime.strptime((i.get_string(fields = ["Married"]).strip()), '%d %b %Y'))
            husid = (i.get_string(fields = ["Husband ID"])).strip()
            wifeid = (i.get_string(fields = ["Wife ID"])).strip()

            for j in Individuals:
                j.border = False
                j.header = False
                id = (j.get_string(fields = ["ID"]).strip().replace('/',''))

                if (husid == id or wifeid == id):
                    if((j.get_string(fields = ["Death"]).strip()) != 'NA'):
                        death = (datetime.strptime((j.get_string(fields = ["Death"]).strip()), '%d %b %Y'))
                        if(datetime.date(marriage) < datetime.date(death)):
                            errors.append(id)
    
    if(len(errors) != 0):
        strerror=", ".join(errors)
        return f'US05 - Error : Individual - {strerror} have marriage before death'
    else:
        return "US05 - No errors found "
print(US05())

