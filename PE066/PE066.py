import math
##This result uses the fact that the minimal solution of Pell's equation appears in the continued fraction representation of sqrt(D).

#A function to turn a finite continued fraction into a rational number.
def cftorational(cfrep: list):
    cfrev = list(reversed(cfrep))
    runningtotal = [cfrev[0], 1]
    for i in range(1, len(cfrev)):
        numerator = cfrev[i]*runningtotal[0]+runningtotal[1]
        denominator = runningtotal[0]
        runningtotal = [numerator, denominator]
    return runningtotal

#determines the next term in the continued fraction for sqrt(D), assuming earlier terms are accurate.
def nextterm(d: int, cfrep: list):
    cfrep.append(1)
    if len(cfrep) % 2 == 0:
        while cftorational(cfrep)[1]*cftorational(cfrep)[1]*d < cftorational(cfrep)[0]*cftorational(cfrep)[0]:
            cfrep[len(cfrep)-1]+= 1
        cfrep[len(cfrep) - 1] -= 1
    if len(cfrep) % 2 == 1:
        while cftorational(cfrep)[1]*cftorational(cfrep)[1]*d > cftorational(cfrep)[0]*cftorational(cfrep)[0]:
            cfrep[len(cfrep)-1]+= 1
        cfrep[len(cfrep) - 1] -= 1

Dmin = 5
xmin = 9
for D in range(1, 1001):
    if D == math.isqrt(D)*math.isqrt(D):
        continue
    Drep = [math.isqrt(D)]
    while cftorational(Drep)[1]*cftorational(Drep)[1]*D+1 != cftorational(Drep)[0]*cftorational(Drep)[0]:
        nextterm(D, Drep)
    if cftorational(Drep)[0] > xmin:
        xmin = cftorational(Drep)[0]
        Dmin = D
        print(D, Drep)