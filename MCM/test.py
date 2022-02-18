from dakota import *

DP = DpMCMNoRecursion
test_arr = [2,3,1,3,2,3,1]
DP.matrix_chain_order(DP, test_arr)

print(test_arr, end= "\n\n")
for i in DP.m:
    for j in i:
        print("%2d" % j, end = " " )
    print()


print(DP.m[0][len(DP.m)-1])


    
