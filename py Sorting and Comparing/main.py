import pandas as pd
import os
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
script = sys.argv[1]
NORMAL, ARG_DESC, HIGH_LEVEL_DESC = 0, 1, 2
mode = 0

if script == "desc":
    if len(sys.argv) < 3:
        raise SyntaxError("Cannot ask nonexistant script for description")
    mode = ARG_DESC
    script = sys.argv[2]

if script == "desc":
    if len(sys.argv) < 3:
        raise SyntaxError("Cannot ask nonexistant script for argument description")
    mode = HIGH_LEVEL_DESC
    script = sys.argv[2]



foundFile = False
if not ".txt" in script:
    files = os.listdir()
    txtfiles = [fileName for fileName in files if ".txt" in fileName]
    for fileName in txtfiles:
        with open(fileName, "r") as file:
            firstLine = file.readline().strip(" \n")
            if "title" in firstLine: #we know it's one of our scripts!
                splitTitleLine = firstLine.split()

                if len(splitTitleLine)<2:
                    continue
                else:
                    if splitTitleLine[1] == script: #we found it!!
                        script = fileName
                        foundFile = True
                        break
                    else:
                        continue
    if not foundFile:
        raise ImportError(name=script)

try:
    with open(script, 'r') as configFile:
        lineNum = 0
        for line in configFile:
            lineNum += 1
            if mode == NORMAL:
                command, arg = breakdownCommand(line)
                if command == "args":

                    #TODO: it will need to read in args, check if right number of args on the system stack, and put them into mem

                if not line == "\n":
                    #TODO: will need to replace possible args
                    workplace.execute(line, lineNum)
            elif mode == ARG_DESC:
                command, arg = breakdownCommand(line)
                if command == "arg_desc":
                    print(line)
                    break
            elif mode == HIGH_LEVEL_DESC:
                command, arg = breakdownCommand(line)
                if command == "high_level_desc":
                    print(line)
                    break
            else:
                raise RuntimeError("mode should not be any value other than those!")


except OSError:
    raise ImportError(name=script)

def breakdownCommand(command: str):
    commandParts = command.split(" ")
    #print(commandParts)
    commandParts = [i.strip("\n ") for i in commandParts]
    if len(commandParts) > 1:
        return commandParts[0], commandParts[1:]
    else:
        return commandParts[0]
print("Hit enter to exit")
input()





