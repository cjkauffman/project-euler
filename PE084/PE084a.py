# A program to find the probability of landing on a specific square in a (simplified) version of monopoly, by finding the stationary state of a stochastic matrix.
# This is a more precise version of the previous method. The problem as stated is imprecise, as it does not state when doubles reset.

import numpy, math
from numpy import linalg as LA

DIE = 4

def nextrailroad(j): #Returns the next railroad
    if 5 < j <= 15:
        return 15
    if 15 < j <= 25:
        return 25
    if 25<j<=35:
        return 35
    else:
        return 5

def nextutil(j): #Returns the next utility
    if 12 < j <= 28:
        return 28
    else:
        return 12

#Now we construct out transition matrix row by row.
#Element j of column(i) gives the probability of moving to space j from space i via a given method (rolling or landing on a special square).
#Note that every column function gives a vector which sums to 1.
#list elements 0-39 refer to spaces 0-39 without doubles having been rolled.
#list elements 40-79 refer to spaces 0-39 (respectively) with doubles having been rolled once.
#list elements 80-119 refer to spaces 0-39 with doubles having been rolled twice.

def rollcolumn(space: int): #The first transition matrix applied, which calculates the odds of landing on a given space by rolling 2d4.
    newcolumn = [0] * 120
    dubs = space//40
    for roll1 in range(1, DIE+1):
        for roll2 in range(1, DIE+1):
            if roll1 != roll2: #returns doubles to 0 and moves.
                newcolumn[(space+roll1+roll2)%40] += 1/(DIE*DIE)
            elif roll1 == roll2 and dubs != 2: #increments doubles by 1 and moves.
                newcolumn[40 * dubs + 40 + (space + roll1 + roll2) % 40] += 1/(DIE * DIE)
            else: #three doubles in a row, sends the token to jail and resets doubles.
                newcolumn[10] += 1/(DIE*DIE)
    return newcolumn

#The second transition matrix checks to see if you've landed on a special square, and applies its effects.

def idcolumn(space: int): #no effect.
    newcolumn = [0] * 120
    newcolumn[space]=1
    return newcolumn

def chancecolumn(space: int): #Gives the effects of landing on a Chance space
    newcolumn = [0] * 120
    dubs = space // 40
    newcolumn[space] = 3/8
    newcolumn[40*dubs+0] = newcolumn[40*dubs+5] = newcolumn[40*dubs+10] = newcolumn[40*dubs+11] = newcolumn[40*dubs+24] = newcolumn[40*dubs+39] = 1/16
    newcolumn[40*dubs+nextrailroad(space%40)] += 1/8
    newcolumn[40*dubs+nextutil(space%40)] += 1/16
    if (space%40) == 36:
        newcolumn[40*dubs+33]+= 7/128
        newcolumn[40*dubs+0]+= 1/256
        newcolumn[40*dubs+10]+= 1/256
    else:
        newcolumn[40*dubs+((space-3)%40)] += 1/16
    return newcolumn

def commchestcolumn(space: int): #Gives the effects of landing on a Community Chest space.
    newcolumn = [0]*120
    dubs = space // 40
    newcolumn[40*dubs + 0] = 1/16
    newcolumn[40*dubs + 10] = 1/16
    newcolumn[space] = 7/8
    return newcolumn

def gotojailcolumn(space: int): #Gives the effects of landing on the "Go To Jail" space.
    newcolumn = [0]*120
    dubs = space // 40
    newcolumn[40*dubs + 10] = 1
    return newcolumn

rollmatrix = []
for col in range(120):
    rollmatrix.append(rollcolumn(col))

specialmatrix = []
for col in range(120):
    if col%40 in [2, 17, 33]:
        specialmatrix.append(commchestcolumn(col))
    elif col%40 in [ 7, 22, 36]:
        specialmatrix.append(chancecolumn(col))
    elif col%40 == 30:
        specialmatrix.append(gotojailcolumn(col))
    else:
        specialmatrix.append(idcolumn(col))

transitionmatrix = numpy.matmul(rollmatrix, specialmatrix).transpose() #Constructs the transition matrix.

transitioneigs = LA.eig(transitionmatrix)
for eigindex in range(120):
    if numpy.isclose(1, transitioneigs[0][eigindex]): #Finds the index of the eigenvector which is constant under the action of the transition matrix.
        eqcolumn = eigindex
equilibrium = []
for i in range(120):
    equilibrium.append(float(numpy.real(transitioneigs[1][i][eqcolumn]))) #Constructs the invariant eigenvector.
eqnormalizer = numpy.sum(equilibrium)
for j in range(120):
    equilibrium[j] /= eqnormalizer #normalizes the eigenvector, noting that the total probability equals 1.
spaces = []
for i in range(40):
    spaces.append(i)
spaces.sort(reverse=True, key=lambda i: (equilibrium[i] + equilibrium[40+i]+equilibrium[80+i])) #sorts by the probability of landing on a square after 0, 1, or 2 doubles.
print(spaces)