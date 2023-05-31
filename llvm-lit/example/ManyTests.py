from lit import Test

import time

class ManyTests(object):
    def __init__(self, N=10000):
        self.N = N

    def getTestsInDirectory(self, testSuite, path_in_suite, litConfig, localConfig):
        for i in range(self.N):
            test_name = "test-%04d" % (i,)
            yield Test.Test(testSuite, path_in_suite + (test_name,), localConfig)

    def execute(self, test, litConfig):
        # Do a "non-trivial" amount of Python work.
        sum = 0
        for i in range(10000):
            sum += i
        test_output = str(int(time.time()))
        return Test.PASS, test_output
