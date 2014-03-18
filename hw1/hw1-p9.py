### CIS 521 HW1-9
### zimeng YANG


def convol(abc):
    '''takes a list of polynomials in coefficient form, return their mulplication'''
    lenOfList = len(abc)
    if lenOfList == 0:
        return []
    else:
        # do convolution to compute the coefficients of the result of the mulplication
        a = abc[0]
        for m in range(lenOfList-1):
            b = abc[m+1]
            c = []
            len1 = len(a)
            len2 = len(b)
            leng = len1 + len2 - 1
            for k in range(abs(leng-len1)):
                a.append(0)
            for i in range(leng):
                sumCol = 0
                for j in range(len2):
                    sumCol = sumCol + a[i-j]*b[j]
                c.append(sumCol)
            a = c
        return a
    
def addMerge(a,b):
    '''takes two list of polynomials, return their sum'''
    len1 = len(a)
    len2 = len(b)
    leng = max(len1, len2)
    c = []
    for i in range(leng):
        if i>=len1:
            c.append(b[i])
        elif i>=len2:
            c.append(a[i])
        
        else:
            c.append(a[i]+b[i])        
    return c

def coefficientForm(poly):
    '''takes polynomial, return result in coefficient form'''
    if poly[0]==1:
        # there is no nested parentheses
        lastTerm = convol(poly[2]);
        solutionPoly =  addMerge(poly[1], lastTerm)
    else:
        # there are nested parentheses
        lastTerm = poly[2]
        length = len(lastTerm)
        lastTermNew = []
        for i in range(length):
            temp = coefficientForm(lastTerm[i])
            lastTermNew.append(temp[1])
        multiTerm = convol(lastTermNew)
        solutionPoly =  addMerge(poly[1], multiTerm)
    solution = []
    solution.append(1)
    solution.append(solutionPoly)
    solution.append([])
    return solution

if __name__ == '__main__':
    # first polynomial
    p1 = [1,[],[[9,0,-1,6],[0,-5,1]]]
    p1_coefficientForm = coefficientForm(p1)
    print p1_coefficientForm

    # second polynomial
    p2 = [1,[],[[1,1,1],[1,1]]]
    p2_coefficientForm = coefficientForm(p2)
    print p2_coefficientForm

    # third polynomials
    p3 = [1, [0,0,9], [[-2,3],[5,-1]]]
    p3_coefficientForm = coefficientForm(p3)
    print p3_coefficientForm
