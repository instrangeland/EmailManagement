import pandas as pd
import sys
import os.path
import os

class Workspace:
    def __init__(self):
        self.tables = {}
        pass
    def execute(self, line, lineNum):
        self.lineNum = lineNum
        sourceFrame, command, args = self.breakdownCommand(line)

        if "new_table" == command:
            self.newFrame(sourceFrame, args)
        elif "delete" == command:
            self.delete(sourceFrame, args)
        elif "open" == command:
            self.openFile(sourceFrame, args)
        elif "save_as" == command:
            self.save(sourceFrame, args)
        elif "copy_over" == command:
            self.copyOver(sourceFrame, args)
        elif "append_to" == command:
            self.fileAppend(sourceFrame, args)
        elif "remove_duplicates" == command:
            self.removeDuplicates(sourceFrame, args)
        elif "keep_only_duplicates" == command:
            self.keepDuplicates(sourceFrame, args)
        elif "remove_lines_matching" == command:
            self.compareFiles(sourceFrame, args)
        else:
            self.error("command "+command+" does not exist")

    

    def save(self, sourceFrame, args):
        self.fileValidExcel(args[0])
        if sourceFrame not in self.tables:
            self.error("table " + sourceFrame + " does not exist!")
        self.tables[sourceFrame].to_excel(args[0], index=False)

    def copyOver(self, sourceFrame, args):
        if sourceFrame not in self.tables:
            self.error("table " + sourceFrame + " does not exist!")
        if args[0] not in self.tables:
            self.error("table " + args[0] + " does not exist!")
        self.tables[args[0]] = self.tables[sourceFrame]

    def delete(self, sourceFrame, args):
        if sourceFrame in self.tables:
            self.tables.pop(sourceFrame)
        else:
            self.fileValidExcel(args)
            os.remove(sourceFrame)

    def openFile(self, sourceFrame, args):
        self.fileExists(args[0])
        self.fileValidExcel(args[0])
        newDF = pd.read_excel(args[0],engine='openpyxl')
        self.tables[sourceFrame] = newDF

    def newFrame(self, sourceFrame, args):
        if sourceFrame in self.tables:
            self.error("dataframe name already exists")
        self.tables[sourceFrame] = pd.DataFrame()

    def compareFiles(self, sourceFrame, args):
        if sourceFrame not in self.tables:
            self.error("table " + sourceFrame + " does not exist!")
        if args[0] not in self.tables:
            self.error("table " + args[0] + " does not exist!")
        for index, row in self.tables[args[0]].iterrows():  # this is really hacky but clever
            self.tables[sourceFrame] = self.tables[sourceFrame].append(row)  # appends a line to self.wb1
            size = len(self.tables[sourceFrame])  # gets the size with an extra added
            self.tables[sourceFrame] = self.tables[sourceFrame].drop_duplicates(subset=['Email'], keep=False)  # removes duplicates
            if size == len(self.tables[sourceFrame]):  # and then checks if the size changed. If yes, it was duplicate If not, remove the appended row
                self.tables[sourceFrame].drop(self.tables[sourceFrame].tail(1).index, inplace=True) # if the size didn't change, remove the appended row


    def fileAppend(self, sourceFrame, args):
        if len(args) >= 1:
            if sourceFrame not in self.tables:
                self.error("table "+sourceFrame+" does not exist!")
            if args[0] not in self.tables:
                self.error("table " + args[0] + " does not exist!")
            self.tables[args[0]] = self.tables[args[0]].append(self.tables[sourceFrame])
        else:
            self.error("Append must have at least 2 files specified")

    def removeDuplicates(self, sourceFrame, args):
        if sourceFrame not in self.tables:
            self.error("table " + sourceFrame + " does not exist!")
        self.tables[sourceFrame] = self.tables[sourceFrame].drop_duplicates(subset=['Email'], keep=False)

    def keepDuplicates(self, sourceFrame, args):
        if sourceFrame not in self.tables:
            self.error("table " + sourceFrame + " does not exist!")
        duplicatesBool = self.tables[sourceFrame].duplicated(subset=['Email'])
        duplicates = self.tables[sourceFrame][duplicatesBool]
        seenDuplicate = []
        singleInstanceDuplicates = pd.DataFrame()
        for index, row in duplicates.iterrows():
            if row[2] not in seenDuplicate:
                seenDuplicate.append(row[2])
                singleInstanceDuplicates = singleInstanceDuplicates.append(row)
        neworder = self.tables[sourceFrame].columns
        singleInstanceDuplicates = singleInstanceDuplicates.reindex(columns=neworder)
        self.tables[sourceFrame] = singleInstanceDuplicates

    def breakdownCommand(self, command: str):
        commandParts = command.split(" ")
        #print(commandParts)
        commandParts = [i.strip("\n ") for i in commandParts]
        return commandParts[0], commandParts[1], commandParts[2:]

    def error(self, text):
        raise SyntaxError("Error on line "+str(self.lineNum)+": "+text)

    def fileValidExcel(self, pathTo):
        fullPath = os.path.abspath(pathTo)
        if not os.path.splitext(fullPath)[1] == ".xlsx":
            self.error("path " + pathTo + " is not an xlsx file")

    def fileExists(self, pathTo):
        fullPath = os.path.abspath(pathTo)
        if not os.path.exists(fullPath):
            self.error("path " + pathTo + " does not exist")
        if not os.path.isfile(fullPath):
            self.error("path " + pathTo + " is not a file")



