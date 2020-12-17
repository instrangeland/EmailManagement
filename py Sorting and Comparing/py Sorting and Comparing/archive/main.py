import pandas as pd
import sys



# to remove duplicates it's /r
# to append the second list, it's /a
# to only keep duplicates, it's /k
# to use the second list to compare, it's /c
commands = []
string = ""
with open("config.txt", 'r') as configFile:
    files = []
    extensions = []
    string = configFile.read()
commands = string.split(" ")
for i in commands:
    if i[0] != "/":
        files.append(i)
    else:
        extensions.append(i)

twoReadFiles = False
wb1 = pd.read_excel(files[0])
saveFileName = files[1]
if len(files) < 2:
    raise ValueError("Must specify output file name!!")
if len(files) == 3:
    wb2 = pd.read_excel(files[1])
    twoReadFiles = True
    saveFileName = files[2]

if "/a" in extensions:
    if twoReadFiles:
        wb1 = wb1.append(wb2)
    else:
        raise TypeError("Cannot append with only one file!!")

if "/r" in extensions:
    print(wb1)
    wb1 = wb1.drop_duplicates(subset=['Email'], keep=False)
    print(wb1)
elif "/k" in extensions:
    duplicatesBool = wb1.duplicated(subset=['Email'])
    duplicates = wb1[duplicatesBool]
    seenDuplicate = []
    singleInstanceDuplicates = pd.DataFrame()
    for index, row in duplicates.iterrows():
        if row[2] not in seenDuplicate:
            seenDuplicate.append(row[2])
            singleInstanceDuplicates = singleInstanceDuplicates.append(row)
    neworder = ['First Name', 'Last Name', 'Email']
    singleInstanceDuplicates = singleInstanceDuplicates.reindex(columns=neworder)
    wb1 = singleInstanceDuplicates
elif "/c" in extensions:
    if not twoReadFiles:
        raise TypeError("To compare, need two readable filenames!")
    else:
        for index, row in wb2.iterrows():  # this is really hacky but clever... I think
            tryWB1 = wb1.append(row)
            size = len(wb1)  # so yeah it appends a line
            tryWB1 = tryWB1.drop_duplicates(subset=['Email'], keep=False)  # removes duplicates
            if size != len(tryWB1):  # and then checks if anything was removed. If not, remove the appended row
                wb1 = tryWB1

wb1.to_excel(saveFileName)
