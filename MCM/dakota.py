import sys

from numpy import empty

class DpMCMNoRecursion:
    m = []
    s = []

    def matrix_chain_order(self, dimensions):
        n = len(dimensions) - 1
        self.m = [[0 for i in range(n)] for j in range(n)]
        self.s = [[0 for i in range(n)] for j in range(n)]
        out = dict()
        for start in range(1, n):
            for i in range(n - start):
                j = i + start
                self.m[i][j] = sys.maxsize
                for k in range(i, j):
                    cost = self.m[i][k] + self.m[k + 1][j] + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                    if cost < self.m[i][j]:
                        self.m[i][j] = cost
                        self.s[i][j] = k
                        outx = [i,k]
                        outy = [k+1, j]
                        outi = [i,j]
                out[str(outi)] = [outx,outy]
        res = list(sorted(out.keys()))
        print(res)
        print(res[0])
        print(out.get(res[0]))
        for i in out.get(res[0]):
            if i in res:
                res2 = list(out.get(i))
                print(res2)


            

    def print_optimal_parenthesizations(self):
        print(self.s)
        in_a_result = [False for i in range(len(self.s))]
        print(in_a_result)
        self.print_parenthesizations(self, 0, len(self.s) - 1, in_a_result)

    def print_parenthesizations(self, i, j, in_a_result):
       
        if i != j:
            self.print_parenthesizations(self, i, self.s[i][j], in_a_result)
            self.print_parenthesizations(self, self.s[i][j] + 1, j, in_a_result)
            istr = "_result " if in_a_result[i] else " "
            jstr = "_result " if in_a_result[j] else " "
            print(" A_" + str(i) + istr + "* A_" + str(j) + jstr + " = " + str(self.m[i][j]))
            in_a_result[i] = True
            in_a_result[j] = True