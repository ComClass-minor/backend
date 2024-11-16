# we are given an array made up of 0's and 1's ... 
# we have to find the sum of least distances between the 0's and 1's
# for example [0 , 0 , 1 , 1 , 0 , 0 ,0 , 1]
# distances would be [2 , 1 , 0 , 0 , 1 , 2 , 1 , 0] = 7

arr = [0 , 0 , 1 , 1 , 0 , 0 , 0 , 1]
#  we will first find the indexes of all zeros
zeros = [i for i , v in enumerate(arr) if v == 0]
ones = [i for i , v in enumerate(arr) if v == 1]
ans = []
for i in zeros:
    ans.append(min(abs(i - z) for z in ones))
print(sum(ans))