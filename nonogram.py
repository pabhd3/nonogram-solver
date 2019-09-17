from itertools import product
from numpy import prod


def filterRowsColumns(rows, columns):
    for ci, cPoss in enumerate(columns):
        if(len(cPoss) == 1):
            # print(ci, cPoss)
            for i, v in enumerate(rows):
                # print(v)
                # cpossi = cPoss[0][i]
                # print(f" i = {i}   rPoss[0][{i}] = {cpossi}")
                # print(list(filter(lambda x: x[i] == cPoss[0][i], v)))
                rows[i] = list(filter(lambda x: x[i] == cPoss[0][i], v))

    for ri, rPoss in enumerate(rows):
        if(len(rPoss) == 1):
            # print(ri, rPoss)
            for i, v in enumerate(columns):
                # print(v)
                # rpossi = rPoss[0][i]
                # print(f" i = {i}   rPoss[0][{i}] = {rpossi}")
                # print(list(filter(lambda x: x[i] == rPoss[0][i], v)))
                columns[i] = list(filter(lambda x: x[i] == rPoss[0][i], v))
    return rows, columns



def solve(rows, columns, combos):
    tested = 0
    for p in product(*ROW_POSSIBILITIES):
        print(f"Testing {tested}/{combos}", end="\r")
        found = True
        for i in range(0, len(p[0])):
            pColumns = "".join([r[i] for r in p])
            if(pColumns not in columns[i]):
                found = False
                break
        tested += 1
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
    ROWS = [(0,), (4,), (6,), (2,2), (2,2), (6,), (4,), (2,), (2,), (2,), (0,)]
    COLUMNS = [(0,), (9,), (9,), (2,2), (2,2), (4,), (4,), (0,)]

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

    # Filter Rows
    # ROW_POSSIBILITIES, COLUMN_POSSIBILITIES = filterRowsColumns(rows=ROW_POSSIBILITIES, columns=COLUMN_POSSIBILITIES)

    # Solve
    print("""
    ####################
    ##### solution #####
    ####################
    """)
    combos = prod([len(i) for i in ROW_POSSIBILITIES])
    print(f"Possible Board Combinations = {combos}")
    solution = solve(rows=ROW_POSSIBILITIES, columns=COLUMN_POSSIBILITIES, combos=combos)
    print("\n".join(solution))