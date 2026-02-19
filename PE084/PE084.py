# A program to find the probability of landing on a specific square in a (simplified) version of monopoly, by finding the stationary state of a stochastic matrix.
# This is a slightly simplified form of the actual method, as it doesn't account for the fact that you're slightly more likely to land on certain squares after rolling doubles.

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


def rollcolumn(space: int): #The first transition matrix applied, which calculates the odds of landing on a given space by rolling 2d4.
    newcolumn = [0] * 40
    for roll in range(2,2*DIE+1):
        newcolumn[(space+roll)%40] = (min(2*DIE+1-roll, roll-1))/(DIE*DIE)
    return newcolumn

#The second transition matrix checks to see if you've landed on a special square, and applies its effects.

def idcolumn(space: int): #no effect
    newcolumn = [0] * 40
    newcolumn[space]=1
    return newcolumn

def chancecolumn(space: int): #Gives the effects of landing on a Chance space
    newcolumn = [0] * 40
    newcolumn[space] = 3/8
    newcolumn[0] = newcolumn[5] = newcolumn[10] = newcolumn[11] = newcolumn[24] = newcolumn[39] = 1/16
    newcolumn[nextrailroad(space)] += 1/8
    newcolumn[nextutil(space)] += 1/16
    if space == 36:
        newcolumn[33]+= 7/128
        newcolumn[0]+= 1/256
        newcolumn[10]+= 1/256
    else:
        newcolumn[(space-3)%40] += 1/16
    return newcolumn

def commchestcolumn(space: int): #Gives the effects of landing on a Community Chest space
    newcolumn = [0]*40
    newcolumn[0] = 1/16
    newcolumn[10] = 1/16
    newcolumn[space] = 7/8
    return newcolumn

def gotojailcolumn(space: int): #Gives the effects of landing on the "Go To Jail" space
    newcolumn = [0]*40
    newcolumn[10] = 1
    return newcolumn

#The third transition matrix checks if you've rolled three doubles in a row.
#This is only approximate, as I treated the probability as 1/64 no matter which square you

def tripledoublescolumn(space: int):
    newcolumn = [0]*40
    newcolumn[10] += 1/(DIE**3)
    newcolumn[space] += (DIE**3 - 1)/(DIE**3)
    return newcolumn


tripdubs = []
for col in range(40):
    tripdubs.append(tripledoublescolumn(col))
rollmatrix = []
for col in range(40):
    rollmatrix.append(rollcolumn(col))
specialmatrix = []
for col in range(40):
    if col in [2, 17, 33]:
        specialmatrix.append(commchestcolumn(col))
    elif col in [7,22,36]:
        specialmatrix.append(chancecolumn(col))
    elif col == 30:
        specialmatrix.append(gotojailcolumn(col))
    else:
        specialmatrix.append(idcolumn(col))

transitionmatrix = numpy.matmul(rollmatrix, numpy.matmul(specialmatrix, tripdubs)).transpose()

transitioneigs = LA.eig(transitionmatrix)
for eigindex in range(40):
    if numpy.isclose(1, transitioneigs[0][eigindex]):
        eqcolumn = eigindex
equilibrium = []
for i in range(40):
    equilibrium.append(float(numpy.real(transitioneigs[1][i][eqcolumn])))
eqnormalizer = numpy.sum(equilibrium)
for j in range(40):
    equilibrium[j] /= eqnormalizer
spaces = []
for i in range(40):
    spaces.append(i)
spaces.sort(reverse=True, key=lambda i: equilibrium[i])
print(spaces)