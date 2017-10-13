# Data preprocessing script for heatly-net bayesian network.
# Using oasis alzheimers data found here: https://www.kaggle.com/jboysen/mri-and-alzheimers/data 

from math import floor,ceil

## HELPER FUNCTIONS ##

def transformSES(val):
    if (val is None):
        return "*"
    else:
        val = float(val)
    
    if (val <= 1):
        return "low"
    elif (val <=3):
        return "middle"
    else: 
        return "upper"

def transformMMSE(val):
    if (val is None):
        return "*"
    else:
        val = float(val)
        
    if (val <= 24):
        return "none"
    elif (val <= 18):
        return "mild"
    else:
        return "severe"

def transformCDR(val):
    if (val is None):
        return "*"
    else:
        val = float(val)
    
    if (val == 0):
        return "none"
    elif (val == 0.5):
        return "very_mild"
    elif (val == 1):
        return "mild"
    elif (val == 2):
        return "moderate"
    else:
        return "severe"

def transformEduc(val):
    if (val is None):
        return "*"
    else:
        val = float(val)
    
    if (val == 0):
        return "none"
    elif (val <= 8):
        return "primary"
    elif (val <= 12):
        return "secondary"
    else:
        return "tertiary"

def transformAge(val):
    # If the value is NaN or below 0 return * as missing val
    if (val is None):
        return "*"
    else:
         val = float(val)
    
    if (val < 25):
        return "under25"
    elif (val > 65):
        return "over65"
    else:
        return "over25"

def transformAlzheimers(val):
    if (val is None):
        return "*"
    elif (val == "Demented"):
        return "true"
    elif (val == "Nondemented"):
        return "false"
    else:
        return "*"

def transformSex(val):
    if (val is None):
        return "*"
    elif (val == "M"):
        return "male"
    else:
        return "female"

def transformHand(val):
    if (val is None):
        return "*"
    elif (val == "R"):
        return "right"
    else:
        return "left"

#This is needed for Neticas format for some reason
HEADER_LINE = "// ~->[CASE-1]->~\n"

COLUMN_HEADINGS = "IDnum\talzheimers\tsex\thand\tage\teduc\tses\tmmse\tcdr\n"

cases = []

num_cases = 0

#Read in csv
with open('data.csv', 'r') as f:
    for line in f:
        temp = line.split(",")
        if(temp[3] == "1"):
            for i in range(0, len(temp)):
                if (len(temp[i]) == 0):
                    temp[i] = None
            cases.append(temp)
            num_cases += 1

print(num_cases)
print(cases[0])

new_cases = []
#Transform values into discrete ranges categories
for i in range(0,num_cases):
    temp = []
    temp.append(transformAlzheimers(cases[i][2]))
    temp.append(transformSex(cases[i][5]))
    temp.append(transformHand(cases[i][6]))
    temp.append(transformAge(cases[i][7]))
    temp.append(transformEduc(cases[i][8]))
    temp.append(transformSES(cases[i][9]))
    temp.append(transformMMSE(cases[i][10]))
    temp.append(transformCDR(cases[i][11]))
    new_cases.append(temp)

#Write to case file
with open('training.casefile', 'w') as outfile:
    outfile.write(HEADER_LINE)
    outfile.write(COLUMN_HEADINGS)
    for i in range(0,floor(num_cases*0.8)):
        print(str(i) + " : ")
        print(new_cases[i])
        case_str = "\t".join(new_cases[i])
        case_str = str(i+1) + "\t" + case_str +"\n"
        outfile.write(case_str)

with open('testing.casefile', 'w') as outfile:
    outfile.write(HEADER_LINE)
    outfile.write(COLUMN_HEADINGS)
    for i in range(ceil(num_cases*0.8),num_cases):
        case_str = "\t".join(new_cases[i])
        case_str = str(i-(ceil(num_cases*0.8))+1) + "\t" + case_str + "\n"
        outfile.write(case_str)

