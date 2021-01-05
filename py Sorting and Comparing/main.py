import os
import sys
from functs import *



def breakdownCommand(command: str):
    commandParts = command.split(" ")
    #print(commandParts)
    commandParts = [i.strip("\n ") for i in commandParts]
    if len(commandParts) > 1:
        return commandParts[0], commandParts[1:]
    else:
        return commandParts[0], None


commands = []
string = ""
workplace = Workspace()
script = sys.argv[1]
NORMAL, ARG_DESC, HIGH_LEVEL_DESC = 0, 1, 2
mode = 0

remainingSysArgs = sys.argv[2:]
if script in ["desc", "arg_desc"]:
    script = sys.argv[2]
    remainingSysArgs = remainingSysArgs[1:]
    if len(sys.argv) < 3:
        raise SyntaxError("No name of script for description")
    if script == "desc":
        mode = ARG_DESC
    elif script == "arg_desc":
        mode = HIGH_LEVEL_DESC




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
    argNames = []
    with open(script, 'r') as configFile:
        lineNum = 0
        for line in configFile:
            lineNum += 1
            if mode == NORMAL:
                command, arg = breakdownCommand(line)
                if command == "args":
                    if arg is None:
                        raise SyntaxError("No arguments found!")
                    else:
                        argNames = arg
                        if len(remainingSysArgs) < len(arg):
                            raise SyntaxError("Not enough arguments specified by caller: asks for " + str(len(arg)) +
                                              ", got" + str(len(remainingSysArgs)))
                if not line == "\n":
                    if len(argNames) > 0:
                        for index, arg in enumerate(argNames):
                            line = line.replace(arg, remainingSysArgs[index])
                    print(line)
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


print("Hit enter to exit")
input()





