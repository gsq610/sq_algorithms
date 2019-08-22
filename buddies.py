
def countingSort(arr, exp1, digit, type):

    if type == 1:
        n = len(arr)

    # The output array elements that will have sorted arr
        output = [0] * n

    # initialize count array as 0
        count = [0] * (10)

    # Store count of occurrences in count[]
        for i in range(0, n):
            index = (arr[i]/exp1)
            count[ int(index%10) ] += 1

    # Change count[i] so that count[i] now contains actual
    #  position of this digit in output array
        for i in range(1,10):
            count[i] += count[i-1]

    # Build the output array
        i = n-1
        while i>=0:
            index = (arr[i]/exp1)
            output[ count[ int(index%10) ] - 1] = arr[i]
            count[ int(index%10) ] -= 1
            i -= 1

    # Copying the output array to arr[],
    # so that arr now contains sorted numbers
        i = 0
        for i in range(0,len(arr)):
            arr[i] = output[i]

    else:
        n = len(arr)

    # initialize count array as 0
        count = [0] * exp1

        digitbag = [[] for i in range(digit)]

        #print(digitbag)

    # Store count of occurrences in count[]

        for i in range(n):
            if exp1 < len(arr[i][1]):
                digitbag[arr[i][1][exp1]].append(arr[i])
            else:
                digitbag[50].append(arr[i])
        #print(digitbag)

    # update original array
        k =0
        for i in range(digit-1, -1, -1):
            for j in range(len(digitbag[i])):
                arr[k] = digitbag[i][j]
                k+=1

def findmax(arr):
    max = 0
    for i in range(len(arr)):
        if max < len(arr[i][1]):
            max = len(arr[i][1])
    return max

# Method to do Radix Sort
def radixSort(arr, digit):

    # Find the maximum number to know number of digits
    if isinstance(arr[0], list):
        max1 = findmax(arr)
        print(max1)
        i=0
        while i < max1:
            countingSort(arr,i,digit,2)
            i += 1
        return arr

    else:
        max1 = max(arr)

    # Do counting sort for every digit. Note that instead
    # of passing digit number, exp is passed. exp is 10^i
    # where i is current digit number
        exp = 1
        while max1/exp > 0:
            countingSort(arr,exp, 0,1)
            exp *= 10
        return arr

file01 = open("favouriteMovie.txt")
templist = []
for line in file01:
    pairs = line.strip("\n")
    value = pairs.split(":")
    value[1:] = value[1].split(",")
    templist.append(value)
file01.close()
#print(templist[0][2])

movie_list = []
for i in range(len(templist)):
    for j in range(1, len(templist[i])):
        if templist[i][j].replace('\r', '') not in movie_list:
            movie_list.append(templist[i][j].replace('\r', ''))

print(len(movie_list))
for z in range(len(movie_list)):
    for a in range(len(templist)):
        for b in range(1, len(templist[a])):
            if not isinstance (templist[a][b], int):
                if templist[a][b].replace('\r', '') == movie_list[z]:
                    templist[a][b] = z

templist1=[]
for a in range(len(templist)):
    alist1 = []
    alist1.append(templist[a][0])
    alist = []
    for b in range(1, len(templist[a])):
        alist.append(templist[a][b])
    alist = radixSort(alist, 0)
    alist1.append(alist)
    templist1.append(alist1)


radixSort(templist1, len(movie_list))
print(templist1)

temp=[]
index =-1
movieset=[]
moviesetidlist=[]
for a in range(len(templist1)):
    if templist1[a][1]==temp:
        moviesetidlist[index].append(templist1[a][0])
    else:
        temp = templist1[a][1]
        movieset.append(templist1[a][1])
        index +=1
        alist = []
        alist.append(templist1[a][0])
        moviesetidlist.append(alist)

print(movieset)
#print(moviesetidlist)

for i in range(len(movieset)):
    if (len(moviesetidlist[i])>1):
        print("Movies:")
        for j in range (len(movieset[i])):
            print(movie_list[movieset[i][j]])
        print("Buddies:")
        for j in range (len(moviesetidlist[i])):
            print(str(moviesetidlist[i][j]))

