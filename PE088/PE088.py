#For any k, one can make 2k with k, 2, and (k-2) 1's, so for k <= 12000, N <= 24000.
#Next, any factorization of N corresponds with a specific k.
#We will iterate over all possible factorizations, listed in increasing order.

def product(factorlist: list):
    prod = 1
    for factor in factorlist:
        prod *= factor
    return prod
def kvalue(factorlist: list):
    numberoffactors = 0
    for factor in factorlist:
        if factor > 1:
            numberoffactors += 1
    sumoffactors = 0
    for factor in factorlist:
        if factor > 1:
            sumoffactors += factor
    return product(factorlist) - sumoffactors + numberoffactors

#initializes list with N=2k:
smallestN = [0,0]
for j in range(2, 12001):
    smallestN.append(2*j)

factors = [1,1,1,1,1,1,1,1,1,1,1,1,2,2] #Any number less than 24000 has at most 14 factors, since 2^15 > 24000.
slide = len(factors) - 1
while factors[0]<= 2:
    if kvalue(factors) < 12001 and product(factors) < smallestN[kvalue(factors)]:
        smallestN[kvalue(factors)] = product(factors)
    factors[slide]+=1
    while product(factors) > 24000 and factors[0] <= 2:
        # If the product of factors is >24000, finds the next valid set of factors whose product is <= 24000.
        slide -= 1
        factors[slide] += 1
        for k in range(slide, len(factors)):
            factors[k] = factors[slide]
    slide = len(factors)-1
print(sum(set(smallestN)))
