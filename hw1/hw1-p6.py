
def TDapply(g, m):
    # your single statement function
    return [ [g(m[i][j]) for j in range(len(m[0]))] for i in range(len(m))]

def testFunction(x):
    # test function works as g
    return x*2

if __name__ == '__main__':
    m = [[1,2,3],[6,5,4]] # the list used for test
    print TDapply(testFunction, m)

