# Pip Imports
from functools import reduce
from itertools import product


def findBlanks(base, maxVal):
    blanks = []
    possibility = list("0" * base)
    while("".join(possibility) < str(max) * base):
        possibility[0] = str(int(possibility[0]) + 1)
        for i, v in enumerate(possibility):
            if(v == str(maxVal)):
                try:
                    possibility[i] = "0"
                    possibility[i + 1] = str(int(possibility[i + 1]) + 1)
                except:
                    pass
        blanks.append(tuple([int(i) for i in possibility[::-1]]))
        if("".join(possibility) == str(maxVal - 1) * base):
            break
    return blanks


def filterBlanks(blanks, blankSum):
    return list(filter(lambda b: sum(b) == blankSum and all(b[1:-1]), blanks))


def possibilities(values, length):
    print(values)
    # Determine known and unknown values
    KNOWN = sum(values)
    UNKNOWN = length - KNOWN
    print(f"Known = {KNOWN}   UNKNOWN = {UNKNOWN}")
    # If all known of unknown
    if(KNOWN == length or UNKNOWN == length):
        return ["0" * length if UNKNOWN == length else "1" * length]
    # Find number of possibilities
    BASE = len(values) + 1
    power, i = 0, 1
    while(power < UNKNOWN):
        power += BASE
        i += 1
    # Find all blanks, then filter possible ones
    blanks = findBlanks(base=BASE, maxVal=UNKNOWN+1)
    filteredBlanks = filterBlanks(blanks=blanks, blankSum=UNKNOWN)
    # Create the possible structure of the row
    possibilities = []
    for possibleBlank in filteredBlanks:
        possibility = ""
        for i, _ in enumerate(possibleBlank):
            try:
                possibility += "0" * possibleBlank[i]
                possibility += "1" * values[i]
            except:
                pass
        possibilities.append(possibility)
    lenBlanks = "{:,}".format(len(blanks))
    lenPossibilities = "{:,}".format(len(possibilities))
    print(f"{values} -> Possibilities {lenBlanks} -> Filtered {lenPossibilities}")
    return possibilities


def filterRowsColumns(rows, columns):
    allCombosR = "{:,}".format(reduce(lambda x, y: x*y, [len(i) for i in rows]))
    allCombosC = "{:,}".format(reduce(lambda x, y: x*y, [len(i) for i in columns]))
    print(f"Total Board Combinations = { allCombosR } & { allCombosC }")
    unfilteredRows = sum([len(r) for r in rows])
    unfilteredColumns = sum([len(c) for c in columns])
    while(True):
        for ri, r in enumerate(rows):
            overlap = ""
            for i in range(0, len(r[0])):
                ithVal = [int(rr[i]) for rr in r]
                overlap += str(ithVal[0]) if len(ithVal) == 1 or all(ithVal) else "-"
            if("0" in overlap or "1" in overlap):
                for oi, o in enumerate(overlap):
                    if(o == "-"):
                        continue
                    columns[oi] = list(filter(lambda x: x[ri] == o, columns[oi]))
        for ci, c in enumerate(columns):
            overlap = ""
            for i in range(0, len(c[0])):
                ithVal = [int(cc[i]) for cc in c]
                overlap += str(ithVal[0]) if len(ithVal) == 1 or all(ithVal) else "-"
            if("0" in overlap or "1" in overlap):
                for oi, o in enumerate(overlap):
                    if(o == "-"):
                        continue
                    rows[oi] = list(filter(lambda x: x[ci] == o, rows[oi]))
        filteredRows = sum([len(r) for r in rows])
        filteredColumns = sum([len(c) for c in columns])
        print(unfilteredRows, filteredRows, unfilteredColumns, filteredColumns)
        if(unfilteredRows == filteredRows and unfilteredColumns == filteredColumns):
            break
        else:
            unfilteredRows = filteredRows
            unfilteredColumns = filteredColumns
    allCombosR2 = "{:,}".format(reduce(lambda x, y: x*y, [len(i) for i in rows]))
    allCombosC2 = "{:,}".format(reduce(lambda x, y: x*y, [len(i) for i in columns]))
    print(f"Total Board Combinations = { allCombosR2 } & { allCombosC2 }")


def solve(rows, columns):
    tested = 0
    ftested = 0
    combos = "{:,}".format(reduce(lambda x, y: x*y, [len(i) for i in rows]))
    for p in product(*rows):
        print(f"Testing {ftested}/{combos}", end="\r")
        found = True
        for i in range(0, len(p[0])):
            pColumns = "".join([r[i] for r in p])
            if(pColumns not in columns[i]):
                found = False
                break
        tested += 1
        ftested = "{:,}".format(tested)
        if(found):
            print("\n")
            return list(p)


if __name__ == "__main__":
    # Constant Grid Input
    ROWS = [(2,2),(13,),(7,7),(4,4),(1,3,3,1),(2,2,1,1,2,2),(2,4,4,2),(1,4,4,1),(2,2,1,2,2),(2,1,2),(2,2,2,2),(2,3,2),(3,1,3),(11,),(5,)]
    COLUMNS = [(2,7),(6,5),(3,2),(4,3,2),(3,5,1),(2,1,3,1,2),(2,4,2,2),(1,2,4),(2,4,2,2),(2,1,3,1,2),(3,5,1),(4,3,2),(3,2),(6,5),(2,7)]

    # Find all row possibilities
    print("\n####################\n##### ROW DATA #####\n####################")
    ROW_POSSIBILITIES = [possibilities(values=r, length=len(COLUMNS)) for r in ROWS]

    # Find all column possibilities
    print("\n#######################\n##### COLUMN DATA #####\n#######################\n")
    COLUMN_POSSIBILITIES = [possibilities(values=c, length=len(ROWS)) for c in COLUMNS]

    # Filter columns/rows on overlapping "certain" values
    print("\n#####################\n##### FILTERING #####\n#####################")
    filterRowsColumns(rows=ROW_POSSIBILITIES, columns=COLUMN_POSSIBILITIES)

    # Brute force remaining possibilities
    print("\n###################\n##### SOLVING #####\n###################")
    solution = solve(rows=ROW_POSSIBILITIES, columns=COLUMN_POSSIBILITIES)
    for ri, r in enumerate(solution):
        solution[ri] = r.replace("0", ".")
    print("\n".join(solution))