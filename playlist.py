import operator

def builtTable (arr, n, target_num):

    # where n+1 because first col is empty set
    # and target+1 because have to consider base case when T = 0
    subset = [True]* (n+1)
    for i in range(n+1):
        subset[i] = [True]* (target_num + 1)

    # Any of the num in the arr will add up to 0 - with empty set
    for i in range(0, n + 1):
        subset[i][0] = True

    for j in range(1, target_num+1):
        subset[0][j] = False

    # Fill the subset table one by one
    for i in range(1, n+1):
        for j in range(1, target_num+1):

            # if the previous row is True, then under same col it will be true
            # by excluding the current element, considering the previous subset
            subset[i][j] = subset[i-1][j]

            if subset[i][j] == False and j >= arr[i-1]:
                subset[i][j] = subset[i-1][j] or subset[i-1][j-arr[i-1]]

    # initialize i and j to start from bottom right corner
    a = n
    b = target_num
    subset_sum = []

    while a >= 0 and b >= 0 and target_num > 0:

        # if the cell is not equal to cell above ( means their sum will equal to target )
        if subset[a][b] != subset[a-1][b]:

            subset_sum.append([a,arr[a-1]])
            target_num = target_num - arr[a-1]                      # deduct the target num with the value at index a-1
            b = b - arr[a-1]                                        # index a-1 because the table size is (m+1)x(n+1) thus there will be one extra column
            a -= 1                                                  # the extra one more column is zero

        else:
            a -= 1

    return subset_sum

#array = [10,3,5,7,2]
#target_num = 14

#array = [2,3,7,8,10]
#target_num = 11

trip_length = int(input("Enter trip length: "))
input = open("songs.txt", "r")
no_songs = int(input.readline())
duration = input.readline().split()

for i in range(no_songs):
    duration[i] = int(duration[i])

set = builtTable(duration, no_songs, trip_length)

# sort the array by according to first index of each row - which is id in this case
set = sorted(set, key=operator.itemgetter(0))

if set == []:
    print("Bad luck Alice!")
else:
    print("Playlist")
    for i in range(len(set)):
        print("ID:",set[i][0]," Duration: ",set[i][1])
