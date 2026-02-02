# This generates a list of valid six-sided dice, encoded into 10-bit integers i.
# The integer j appears on the die if and only if the 2**j place in the binary representation of i is 1
i = 0
validdice = []
while i < 1024:
    sides = 0
    for j in range(10):
        if i & 2**j > 0:
            sides += 1
    if sides == 6:
        validdice.append(i)
    i+= 1

# Uses bitwise operators to see if a square is possible  with the two dice.
# Note that we are checking if 6 or 9 appears on a die via a bitwise comparison with 576 = 2**6 + 2**9
configurations = 0
for die1 in validdice:
    for die2 in validdice:
        if(die1 & 1 > 0 and die2 & 2 > 0) or (die2 & 1 > 0 and die1 & 2 > 0):
            if( die1 & 1 > 0 and die2 & 16 > 0)or (die2 & 1 > 0 and die1 & 16 > 0):
                if (die1 & 1 > 0 and die2 & 576 > 0) or (die2 & 1 > 0 and die1 & 576 > 0):
                    if(die1 & 2 > 0 and die2 & 576 > 0) or (die2 & 2 > 0 and die1 & 576 > 0):
                        if (die1 & 4 > 0 and die2 & 32 > 0) or (die2 & 4 > 0 and die1 & 32 > 0):
                            if (die1 & 8 > 0 and die2 & 576 > 0) or (die2 & 8 > 0 and die1 & 576 > 0):
                                if (die1 & 16 > 0 and die2 & 576 > 0) or (die2 & 16 > 0 and die1 & 576 > 0):
                                    if (die1 & 2 > 0 and die2 & 256> 0) or (die2 & 2 > 0 and die1 & 256 > 0):
                                        configurations += 1
print(configurations//2) #Accounts for symmetry.
