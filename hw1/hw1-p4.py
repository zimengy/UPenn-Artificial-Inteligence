
class CacheListFunction:

    def __init__(self, f):
        # create the constructor
        self.function = f
        self.cache = {}
        
   	 
    def invoke(self, t):
        # invoke f on t
        leng = len(self.cache)
        if leng==0:
            foutput = self.function(t)
            self.cache[t] = foutput
            return foutput
        else:
            for key in self.cache.keys():
                if key == t:
                # if f on this tuple has been calculated before, return the stored value 
                    return self.cache[key]
            # if not, compute the value, memorize it, and return it        
            foutput = self.function(t)
            self.cache[t] = foutput
            return foutput    
            


def testFunction(t):
    # create you own test function here
    # testfunction: print out the sum of the numbers in the tuple
    sum = 0
    for i in range(len(t)):
        sum = sum+t[i]
    return sum


if __name__ == '__main__':
    # the following statements will be executed if call as main program
    # not imported to other program as module
    
    clf = CacheListFunction(testFunction)
    # call invoke and test
    print clf.invoke((1,2,3))
    print clf.invoke((1,2,3,4))
    print clf.invoke((1,2,3))
  
