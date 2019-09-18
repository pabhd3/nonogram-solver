from itertools import product
from numpy import prod


def filterRowsColumns(rows, columns):
    # Filter when only 1 possible row or column
    oneRow, checkedOneRows = True, []
    oneColumn, checkedOneColumns = True, []
    while(oneRow or oneColumn):
        oneRow, oneColumn = False, False
        # Check Rows
        for oRowIndex, oRow in enumerate(rows):
            if(len(oRow) == 1 and oRowIndex not in checkedOneRows):
                oneRow = True
                checkedOneRows.append(oRowIndex)
                for oneRowColIndex, oneRowColumns in enumerate(columns):
                    columns[oneRowColIndex] = [c for c in oneRowColumns if c[oRowIndex] == oRow[0][oneRowColIndex]]
        # Check Columns
        for oColumnIndex, oColumn in enumerate(columns):
            if(len(oColumn) == 1 and oColumnIndex not in checkedOneColumns):
                oneColumn = True
                checkedOneColumns.append(oColumnIndex)
                for oneColumnRowIndex, oneColumnRows in enumerate(rows):
                    rows[oneColumnRowIndex] = [r for r in oneColumnRows if r[oColumnIndex] == oColumn[0][oneColumnRowIndex]]

    # Updated rows/columns
    print("""
    ##########################
    ##### 'One' ROW DATA #####
    ##########################
    """)
    for i, row in enumerate(rows):
        l = len(row)
        print(f"{i}th Column ({l}) = {row}")
    print("""
    #############################
    ##### 'One' COLUMN DATA #####
    #############################
    """)
    for i, column in enumerate(columns):
        l = len(column)
        print(f"{i}th Column ({l}) = {column}")

    # Filter overlapping rows or columns
    overlapRow, checkedOverlapRows = True, []
    overlapColumn, checkedOverlapColumns = True, []
    while(overlapRow or overlapColumn):
        overlapRow, overlapColumn = False, False
        # Check rows
        for ovRowIndex, ovRow in enumerate(rows):
            overlapRowIndexes = []
            for i in range(0, len(ovRow[0])):
                if(all([int(ovr[i]) for ovr in ovRow])):
                    overlapRowIndexes.append(i)
            if(overlapRowIndexes and ovRowIndex not in checkedOverlapRows):
                overlapRow = True
                checkedOverlapRows.append(ovRowIndex)
                for ovIndex in overlapRowIndexes:
                    columns[ovIndex] = [c for c in columns[ovIndex] if int(c[ovRowIndex])]
        # Check columns
        for ovColIndex, ovCol in enumerate(columns):
            overlapColIndexes = []
            for i in range(0, len(ovCol[0])):
                if(all([int(ovc[i]) for ovc in ovCol])):
                    overlapColIndexes.append(i)
            if(overlapColIndexes and ovColIndex not in checkedOverlapColumns):
                overlapColumn = True
                checkedOverlapColumns.append(ovColIndex)
                for ovIndex in overlapColIndexes:
                    rows[ovIndex] = [r for r in rows[ovIndex] if int(r[ovColIndex])]

    return rows, columns



def solve(rows, columns, combos):
    tested = 0
    ftested = None
    for p in product(*ROW_POSSIBILITIES):
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
            return p


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
    # Determine known and unknown values
    KNOWN = sum(values)
    UNKNOWN = length - KNOWN
    # print(f"Known = {KNOWN}   UNKNOWN = {UNKNOWN}")
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
    return possibilities


if __name__ == "__main__":
    # Constant Grid Input
    ROWS = [(11,2),(3,2,5,1),(13,),(1,3,7),(7,4,1),(11,2),(15,),(4,10),(3,2,5),(2,6),(1,7,3),(15,),(11,2),(10,),(11,1)]
    COLUMNS = [(15,),(3,6,4),(9,5),(1,6,5),(7,5),(3,4,5),(1,7,5),(4,4,5),(8,5),(8,1,4),(10,2,1),(4,4,1),(2,6),(1,8,1),(2,9)]

    # Find all row possibilities
    print("""
    ####################
    ##### ROW DATA #####
    ####################
    """)
    ROW_POSSIBILITIES = [possibilities(values=r, length=len(COLUMNS)) for r in ROWS]
    for i, row in enumerate(ROW_POSSIBILITIES):
        l = len(row)
        print(f"{i}th Column ({l}) = {row}")

    # Find all column possibilities
    print("""
    #######################
    ##### COLUMN DATA #####
    #######################
    """)
    COLUMN_POSSIBILITIES = [possibilities(values=c, length=len(ROWS)) for c in COLUMNS]
    for i, column in enumerate(COLUMN_POSSIBILITIES):
        l = len(column)
        print(f"{i}th Column ({l}) = {column}")

    # Solve
    print("""
    ####################
    ##### solution #####
    ####################
    """)
    allCombos = "{:,}".format(prod([len(i) for i in ROW_POSSIBILITIES]))
    print(f"Total Board Combinations = {allCombos}")

    # Filter Rows
    ROW_POSSIBILITIES, COLUMN_POSSIBILITIES = filterRowsColumns(rows=ROW_POSSIBILITIES, columns=COLUMN_POSSIBILITIES)

    filteredCombos = "{:,}".format(prod([len(i) for i in ROW_POSSIBILITIES]))
    print(f"Filtered Board Combinations = {filteredCombos}")

    # print("\n".join([r[0] for r in ROW_POSSIBILITIES]))
    solution = solve(rows=ROW_POSSIBILITIES, columns=COLUMN_POSSIBILITIES, combos=filteredCombos)
    print("\n".join(solution))