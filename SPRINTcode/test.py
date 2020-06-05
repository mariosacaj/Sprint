import csv
import re
import numpy as np
from sqlalchemy.dialects.mssql.information_schema import columns

l1=['bus_stop', 'check_point_access']
l2=['railStation', 'fareRule','access list']
l3=['stop_place', 'start_Point']
l4=['stop_place', 'check_startPoint','endPoint','zone']
l5=['stop_place', 'check_startPoint','end_Point','access list']

sl1 = [re.split('[_|\s]+', w) for w in l1]
sl2 = [re.split('[_|\s]+', w) for w in l2]
sl3 = [re.split('[_]', w) for w in l3]
sl4 = [re.split('[_]', w) for w in l4]
sl5 = [re.split('[_]', w) for w in l5]

def checkUnderscore(i):
    flag= bool(re.search(r'[_]', i))
    return flag

op1=[]
sl1 = [re.split('[_|\s]+', w) for w in l1]
for x in sl1:
    cl1 = [re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', i)).split() for i in x]
    flatc=[x for sublist in cl1 for x in sublist]
    op1.append(flatc)

def splitToList(inputList):
    finalList=[]
    split_space=[re.split('[_|\s]+', w) for w in inputList]
    for x in split_space:
        split_CamelCase=[re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', i)).split() for i in x]
        flatten_list=[x for sublist in split_CamelCase for x in sublist]
        finalList.append(flatten_list)
    return finalList

cl2 = [re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', i)).split() for i in sl2]
cl3 = [re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', i)).split() for i in sl3]


import openpyxl
from pathlib import Path
xlsx_file = Path('/Users/safiakalwar/Documents/SprintSVN/POLIMI-Internal/CodeAnalysis/', 'LinkedgtfstogtfsMapping.xlsx')
wb_obj = openpyxl.load_workbook(xlsx_file)
sheet = wb_obj.active

for row in sheet.iter_rows(max_row=6):
    for cell in row:
        print(cell.value, end=" ")
    print()

import pandas as pd
fpath= "/Users/safiakalwar/Documents/SprintSVN/POLIMI-Internal/CodeAnalysis/"
fname= "testfile.csv"

import pandas as pd
my_filtered_csv = pd.read_csv(fname, usecols=[ 'Suggestion','Source', 'Decision'])

import numpy as np
b=np.loadtxt(r'/Users/safiakalwar/Documents/SprintSVN/POLIMI-Internal/CodeAnalysis/testfile.csv',dtype=str,delimiter=';',skiprows=1)
