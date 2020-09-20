import sys
import os
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
NOT_SUPPORTED_COMBINE_TOKEN = ["1 DATE", "2 NAME"]
SUPPORTED_THIRD_TOKEN = ["INDI", "FAM"]
SUPPORTED_SECOND_TOKEN = ["NAME","SEX","BIRT","DEAT","FAMC","FAMS","MARR","HUSB","WIFE","CHIL","DIV","DATE","HEAD","TRLR","NOTE"]

def main(args):
	try:
		filepath = sys.argv[1]
	except:
		print("Usage - GEDCOMProcessor.py <filepath>")
		sys.exit()
		
	if not os.path.isfile(filepath):
		print("File path {} does not exist. Exiting...".format(filepath))
		sys.exit()
	
	with open(filepath) as fp:
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
	
main("args")