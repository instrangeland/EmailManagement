# steps to divide up the thing

from typing import List
#define some functs

# <editor-fold desc="necessaryFunctions">
def isEmail(line: str) -> bool:
    return "@" in line

def findEmailIndexes(lines: List[str]) -> List[int]:
    indexes = []
    for i in range(0, len(lines)):
        if isEmail(lines[i]):
            indexes.append(i)
    return indexes
# </editor-fold>


# read in the file
with open("exampleDirectory.txt", "r") as file:
    lines = [line for line in file]

# let's do some basic cleanup. First, change everything to ascii (I don't wanna deal with unicode
nonUnicodeLines = [line.encode(encoding="ascii", errors="ignore") for line in lines]

linesAsStr = [line.decode("ascii") for line in nonUnicodeLines]

# next, any blank lines
skipBlankLines = [line for line in linesAsStr if not line == ""]
skipEmptyLines = [line for line in skipBlankLines if not line.isspace()] # lines that are only whitespace

# we honestly don't care about any line that contains numbers... unless they're also an email
skipNumericalLines = [line for line in skipEmptyLines
                      if "@" in line or # so if it has the @ symbol we let it through automatically
                      not any(char.isdigit() for char in line)] # otherwise NONE of the characters can be digits

with open("cleanedFile.txt", "w") as writeFile:
    for i in skipNumericalLines:
        writeFile.write(i)

cleanedLines = skipNumericalLines

print("Autodetecting record lengths")

indexes = findEmailIndexes(cleanedLines)



# look at how many lines are after the last instance of an email
estimatedLinesAfterEmail = len(cleanedLines)-1 - indexes[-1]

# the first record is the most likely to be mutant and be missing a line



