from typing import List

def isEmail(line: str) -> bool:
    return "@" in line

def findEmailIndexes(lines: List[str]) -> List[int]:
    indexes = []
    for i in range(0, len(lines)):
        if isEmail(lines[i]):
            indexes.append(i)
    return indexes
