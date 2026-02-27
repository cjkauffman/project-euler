import itertools, copy

class SudokuSquare:
    def __init__(self, row, column, input):
        self.value = input
        self.known = (input != 0)
        self.row = row
        self.column = column
        self.square = 3*(row//3) + (column//3)
        if input != 0:
            self.options = [0]*10
            self.options[input] = 1
        else:
            self.options = [0]+[1]*9
        self.rcs = [self.row, self.column, self.square]
        self.valid = True
        self.asserted = False #This can be changed by outside functions.
    def check(self):
        changeflag = False
        if self.options.count(1) == 0:
            self.valid = False
        if self.options.count(1) == 1:
            if not self.known:
                changeflag = True
                self.known = True
            if self.value != self.options.index(1):
                changeflag = True
                self.value = self.options.index(1)
        return changeflag
    def setvalue(self, val):
        if self.value != 0 and self.value != val:
            self.valid = False
        self.value = val
        self.known = True
        for i in range(10):
            if i != val:
                self.options[i] = 0
    def optionlist(self):
        olist = []
        for i in range(1,10):
            if self.options[i] > 0:
                olist.append(i)
        return olist




class Sudoku:
    def __init__(self, sudokumatrix):
        self.grid = []
        self.squarelist = []
        self.rcslist = [[], [], []]
        self.blocklist = [[], [], []]
        self.guesses = []
        self.solved = True
        self.depth = 0      #Equals 0 for the base Sudoku, >0 if any guesses must be made.
        for i in range(3):
            for j in range(9):
                self.rcslist[i].append([])
                self.blocklist[i].append([[]])
        for sudokurow in range(9):
            for sudokucolumn in range(9):
                newsquare = SudokuSquare(sudokurow, sudokucolumn, sudokumatrix[sudokurow][sudokucolumn])
                if not newsquare.known:
                    self.solved = False
                self.squarelist.append(newsquare)
                for k in range(3):
                    self.rcslist[k][newsquare.rcs[k]].append(newsquare)
                    if newsquare.known:
                        self.blocklist[k][newsquare.rcs[k]].append([newsquare])
                    self.blocklist[k][newsquare.rcs[k]][0].append(newsquare)

    # checksolved() returns True if every square has a nonzero value, False otherwise.

    def checksolved(self):
        if not self.solved:
            for sq in self.squarelist:
                if not sq.known:
                    return False
        self.solved = True
        return True

    # checkvalid() Returns True if every square has at least one possible value and
    # no value shows up more than once in a row, column, or 3x3 square.
    # Returns False otherwise.

    def checkvalid(self):
        for sq in self.squarelist:
            if not sq.valid:
                return False
        for val in range(1,10):
            for rcstype in range(3):
                for rcsindex in range(9):
                    valcount = 0
                    for sqindex in range(9):
                        if self.rcslist[rcstype][rcsindex][sqindex] == val:
                            valcount += 1
                    if valcount > 1:
                        return False
        return True

    # cutblocklist(rcstype, rcsnum, squaresinblock) partitions a subset of squares.
    # rcstype and rcsnum determine a set of 9 squares (rows, columns, or 3x3 squares)
    # blocklist[rcstype][rcsnum] is a partition of that set.
    # squaresinblock searches for a subset of those squares in a list of blocks which contains itself
    def cutblocklist(self, rcstype, rcsnum, squaresinblock):
        assert len(squaresinblock) > 0, "Error: not enough squares in the block."
        outerblock = []
        blocks = self.blocklist[rcstype][rcsnum]
        for currentblock in blocks:
            if squaresinblock[0] in currentblock:
                outerblock = currentblock
                break
        assert len(outerblock) > 0, "Error: no block chosen."
        for sq in squaresinblock:
            if sq not in outerblock:
                return False
        if len(outerblock) == len(squaresinblock):
            return False
        for sq in squaresinblock:
            outerblock.remove(sq)
        blocks.append(squaresinblock)
        return True

    def basicupdate(self):
        changeflag = False
        for square in self.squarelist:
            if square.known and not square.asserted:
                if self.assertvalue(square, square.value):
                    changeflag = True


    # This checks to see if, given a value, a row or column, and a 3x3 square, the elements of the row or column containing that value
    # are all within that 3x3 square and vice versa, and updates the grid accordingly.

    def checkagainstsquare(self, value, rctype, rcnum, squarenum):
        changeflag = False
        if (rctype == 0 and rcnum//3 == squarenum//3) or (rctype == 1 and rcnum//3 == squarenum%3):
            rc = []
            for sq in self.rcslist[2][squarenum]:
                if sq.options[value] > 0:
                    if sq.rcs[rctype] not in rc:
                        rc.append(sq.rcs[rctype])
            if len(rc) == 1:
                for sq in self.rcslist[rctype][rc[0]]:
                    if sq.square != squarenum:
                        if sq.options[value] != 0:
                            changeflag = True
                            sq.options[value] = 0
            squares = []
            for sq in self.rcslist[rctype][rcnum]:
                if sq.options[value] > 0:
                    if sq.rcs[2] not in squares:
                        squares.append(sq.rcs[2])
            if len(squares) == 1:
                for sq in self.rcslist[2][squares[0]]:
                    if sq.rcs[rctype] != rcnum:
                        if sq.options[value] != 0:
                            changeflag = True
                            sq.options[value] = 0

    # Updates a square to a given value, partitions it to its own block,
    # and removes it as a possibility in all other squares in its row, column, and 3x3 block

    def assertvalue(self, square, val):
        changeflag = False
        if square.asserted:
            return False
        else:
            if square.options[val] == 0:
                square.valid = False
                return False
            else:
                square.asserted = True
                if square.setvalue(val):
                    changeflag = True
                for rcstype in range(3):
                    if self.cutblocklist(rcstype, square.rcs[rcstype], [square]):
                        changeflag = True
                for othersquare in self.squarelist:
                    for i in range(3):
                        if square.rcs[i] == othersquare.rcs[i] and square != othersquare:
                            if othersquare.options[val] != 0:
                                changeflag = True
                                othersquare.options[val] = 0







    # A function to determine if a subset of empty squares in a row, column, or 3x3 square must contain a subset of values.
    # rcstype = 0 for rows, 1 for columns, 2 for 3x3 squares.
    # rcsnumber should be in the range 0-8
    # block should be a subset of list[rcstype][rcsnumber]
    # comb should be a combination of digits in the range 1-9
    # Returns True if any changes are made, False otherwise.



    def block(self, rcstype, rcsnumber, outerblock, comb):
        assert rcstype in [0,1,2], "Error, type must be 0 for rows, 1 for columns, or 2 for squares."
        assert rcsnumber in range(9), "Error: number must be between 0 and 8"
        squaresincomb = []
        changeflag = False
        for square in outerblock:
            incomb = True
            for i in range(1, 10):
                if i not in comb and square.options[i] != 0:
                    incomb = False
            if incomb:
                squaresincomb.append(square)
        if len(squaresincomb) == len(comb):
            for square in outerblock:
                if square not in squaresincomb:
                    for value in comb:
                        if square.options[value] != 0:
                            changeflag = True
                            square.options[value] = 0
            self.cutblocklist(rcstype, rcsnumber, squaresincomb)
        return changeflag



    def updateall(self):
        updated = False
        if self.solved:
            return False
        while self.basicupdate():
            updated = True
        for val in range(1,10):
            for rcindex in range(9):
                for sqindex in range(9):
                    for type in range(2):
                        if self.checkagainstsquare(val, type, rcindex, sqindex):
                            updated = True
        for value in range(1,10):
            for type in range(3):
                for entry in range(9):
                    squareswithvalue = []
                    for square in self.squarelist:
                        if square.rcs[type] == entry and square.options[value] == 1:
                            squareswithvalue.append(square)
                    if len(squareswithvalue) == 1:
                        if not squareswithvalue[0].known:
                            squareswithvalue[0].setvalue(value)
                            updated = True
        for rcstype in range(3):
            for rcsindex in range(9):
                for block in self.blocklist[rcstype][rcsindex]:
                    for lrange in range(2, len(block)-1):
                        for comb in itertools.combinations(range(1,10), lrange):
                            if self.block(rcstype, rcsindex, block, comb):
                                updated = True
        self.checksolved()
        return updated

    def solve(self):
        while not self.solved:
            while self.updateall():
                if not self.checkvalid():
                    return False
                if self.solved:
                    return True
            if self.depth < 2:
                guessindex = 0
                while self.squarelist[guessindex].known:
                    guessindex += 1
                for guess in self.squarelist[guessindex].optionlist():
                    guesssudoku = copy.deepcopy(self)
                    guesssudoku.depth = self.depth+1
                    guesssudoku.squarelist[guessindex].setvalue(guess)
                    if not guesssudoku.solve():
                        self.squarelist[guessindex].options[guess] = 0
            else:
                Print("Error: problem requires too many guesses.")
                return False






    def __str__(self):
        string = ""
        for i in range(9):
            for j in range(9):
                string += str(self.squarelist[9*i+j].value) + " "
            string += "\n"
        return string



def tosudokuline(line):
    sudokuline = []
    for char in line:
        if char.isdigit():
            sudokuline.append(int(char))
    return sudokuline

matrix = []
with open("sudoku.txt") as sfile:
    counter = 0
    for line in sfile:
        formattedline = line.strip(" \n")
        if formattedline.isnumeric():
            print(formattedline)
            matrix.append(tosudokuline(formattedline))
        counter += 1
sudokus = []
for i in range(50):
    sudokus.append(Sudoku(matrix[9*i:9*i+9]))
for i in range(50):
    sudokus[i].solve()
for i in range(50):
    if not sudokus[i].solved:
        print(i)
        print(sudokus[i])
        for sq in sudokus[i].squarelist:
            print(sq.row, sq.column, sq.optionlist())
sum = 0
for i in range(50):
    sum += 100*(sudokus[i].squarelist[0].value)+10*(sudokus[i].squarelist[1].value)+(sudokus[i].squarelist[2].value)
print(sum)
