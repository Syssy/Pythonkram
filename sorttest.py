import numpy as np
 
 
class Testdings:
    def __init__(self, name, number, number2):
        self.name = name
        self.number = number
        self.number2 = number2
 
    def __repr__(self):
        return '{} {} {} '.format(self.name,
                                  self.number,
                                  self.number2)
 
    #def __cmp__(self, other):
    #    if hasattr(other, 'number'):
    #        return self.number.__cmp__(other.number)
	
def getKeyNumber(testdings):
    return testdings.number

def getKeyNumber2(testdings):
    return testdings.number2

def main():
     
    aList = [] 
    
    for i in range(10):
	zz = int(10*np.random.random())
	zz2 = int(100*np.random.random())
	aList.append(Testdings(" S"+str(zz)+str(zz2), zz, zz2))
    print aList  
    aList = sorted(aList, key=getKeyNumber2)
    print sorted(aList,key=getKeyNumber )
    
    '''n = 20*1000*1000  # number of random values to draw
    tests = [test_std_global, test_np_global, test_std_local, test_np_local,
             test_np_prefetch_rand_1, test_np_prefetch_rand_2,
             test_np_prefetch_bool, test_all_np,
             test_np_prefetch_rand_list_direct, test_np_prefetch_rand_list_range]
    print("Times are for {} random numbers".format(n))
    for t in tests:
        start = clock()
        result = t(n)
        time = clock() - start
        print("{}: {:.2f} seconds".format(t.__name__, time))'''


if __name__ == "__main__":
    main()