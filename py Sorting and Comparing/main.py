import pandas as pd
import sys
from functs import *

# to remove duplicates it's /r
# to append the second list, it's /a
# to only keep duplicates, it's /k
# to use the second list to compare, it's /c
# to verify all emails and keep only verified, it's /v

commands = []
string = ""
workplace = Workspace()
with open("config.txt", 'r') as configFile:
    lineNum = 0
    for line in configFile:
        lineNum+=1
        if not line == "\n":
            workplace.execute(line, lineNum)









