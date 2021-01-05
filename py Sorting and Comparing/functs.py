import pandas as pd
import sys
import os.path
import os

skippables = ["title", "note", "desc", "args", "arg_desc"]

class Workspace:
    def __init__(self):
        self.tables = {}
        self.pythonSource = []  # this is used for embedding python source into the main program
        self.pythonMode = False # python mode means it'll be executing the following lines as python code
        pass
    def execute(self, line, lineNum):
        self.lineNum = lineNum
        if self.pythonMode:
            if "python_end" in line:
                self.pythonMode = False
                source = ""
                for line in self.pythonSource:
                    source += line
                exec(source)
                self.pythonSource = []
            else:
                self.pythonSource.append(line)
        else:
            sourceFrame, command, args = self.breakdownCommand(line)
            print(command)
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
            elif "python_begin" == sourceFrame:
                self.pythonMode = True
            elif "copy_column" == command:
                self.copyColumn(sourceFrame, args)
            elif "remove_blank_in" == command:
                self.removeBlankIn(sourceFrame, args)
            elif "swap" == command:
                self.swap(sourceFrame, args)
            elif "build_from" == command:
                self.buildFrom(sourceFrame,args)
            elif sourceFrame in skippables:
                pass
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
        if ".csv" in args[0]:
            newDF = pd.read_csv(args[0])
        else:
            newDF = pd.read_excel(args[0], engine='openpyxl')
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
        table1 = self.tables[sourceFrame]
        table2 = self.tables[args[0]]
        table1 = table1[~table1.Email.isin(table2.Email)]
        self.tables[sourceFrame] = table1


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
        self.tables[sourceFrame] = self.tables[sourceFrame].sort_values("First Name")
        self.tables[sourceFrame] = self.tables[sourceFrame].drop_duplicates(subset=['Email'], keep="first")

    def keepDuplicates(self, sourceFrame, args):
        self.tables[sourceFrame] = self.tables[sourceFrame].sort_values("First Name")
        if sourceFrame not in self.tables:
            self.error("table " + sourceFrame + " does not exist!")
        table = self.tables[sourceFrame]
        duplicatesBool = table.duplicated(subset=['Email'])
        duplicates = table[duplicatesBool]
        seenDuplicate = []
        indexOfEmailKey = table.columns.get_loc("Email")

        singleInstanceDuplicates = pd.DataFrame()
        for index, row in duplicates.iterrows():
            if row[indexOfEmailKey] not in seenDuplicate:
                seenDuplicate.append(row[indexOfEmailKey])
                singleInstanceDuplicates = singleInstanceDuplicates.append(row)
        neworder = table.columns
        singleInstanceDuplicates = singleInstanceDuplicates.reindex(columns=neworder)
        self.tables[sourceFrame] = singleInstanceDuplicates

    def breakdownCommand(self, command: str):
        commandParts = command.split(" ")
        #print(commandParts)
        commandParts = [i.strip("\n ") for i in commandParts]
        if len(commandParts) > 1:
            return commandParts[0], commandParts[1], commandParts[2:]
        else:
            return commandParts[0], None, None

    def error(self, text):
        raise SyntaxError("Error on line "+str(self.lineNum)+": "+text)

    def fileValidExcel(self, pathTo):
        fullPath = os.path.abspath(pathTo)
        if not os.path.splitext(fullPath)[1] == ".xlsx" and not os.path.splitext(fullPath)[1] == ".csv":
            self.error("path " + pathTo + " is not an xlsx or csv file")

    def fileExists(self, pathTo):
        fullPath = os.path.abspath(pathTo)
        if not os.path.exists(fullPath):
            self.error("path " + pathTo + " does not exist")
        if not os.path.isfile(fullPath):
            self.error("path " + pathTo + " is not a file")
    def parseColumn(self, lines, start = 0, end = None):
        colName = ""
        if end:
            for i in range(start, end):
                colName += lines[i] + " "
            colName = colName.strip()
        else:
            for line in lines:
                colName += line + " "
            colName = colName.strip()
        return colName
    def copyColumn(self, dataframe, args):
        if len(args) < 3:
            self.error("copy_column requires a source and destination columnn, seperated by \"to\"!")
        else:
            frame = self.tables[dataframe]
            toLocation = args.index("to")


            col1Name = self.parseColumn(args, end=toLocation)
            col2Name = self.parseColumn(args, start = toLocation+1, end=len(args))
            frame[col2Name] = frame[col1Name]

    def removeBlankIn(self, dataframe, args):
        colName = self.parseColumn(args)
        table = self.tables[dataframe]
        table = table.dropna(how = "any", subset = ["Contact2"])
        self.tables[dataframe] = table
        print("Ho")
    def swap(self, dataframe, args):
        if len(args) < 3:
            self.error("swap requires a source and destination columnn, seperated by \"and\"!")
        else:
            frame = self.tables[dataframe]
            toLocation = args.index("and")



            col1Name = self.parseColumn(args, end=toLocation)
            col2Name = self.parseColumn(args, start = toLocation+1, end=len(args))
            a = frame[col1Name].copy()
            b = frame[col2Name].copy()
            frame[col1Name] = b
            frame[col2Name] = a
            self.tables[dataframe] = frame
    def buildFrom(self, sourceFrame, args):
        if sourceFrame not in self.tables:
            self.error("table " + sourceFrame + " does not exist!")
        self.newFrame("temp", None)
        frameExists = False
        for file in args:
            self.openFile("temp", [file])
            if not frameExists:
                self.tables[sourceFrame] = self.tables["temp"]
                frameExists = True
            else:
                self.tables[sourceFrame] = self.tables[sourceFrame].append(self.tables["temp"])



ta = open("testemails_Optinsurvey2.xlsx")


