
def not_neighbor_sale(arr, n, k):

    current_max = 0
    # array declaration
    memo = [0]*n

    # bottom up while comparing each index with previous memo
    for i in range(len(arr)):
        # append the first value if max is empty - nothing to compare with
        if current_max == 0:
            current_max = arr[0]

        # if there is no neighbors with k distance to compare with, then compare current value with previous max
        elif i <= k:
            current_max = max(current_max, arr[i])

        # if there exist neighbors under restriction k, then compare the previous index with (current + (not neighbor))
        else:
            current_max = max(memo[i-1], (arr[i] + memo[i-(k+1)]))

        memo[i] = current_max

    # save the total profit as the current_max will be used for back tracking later on
    total_profit = current_max

    houses = []
    j = len(arr) - 1                                    # to get the last index to perform back tracking

    while current_max > 0:

        if memo[j] != memo[j-1]:
            houses.append(j+1)                          # j+1 because index 0 = house 1
            current_max = current_max - arr[j]          # minus the current value from max to find the rest
            j = j - (k+1)

        else:
            j -= 1

    print("Houses: ")
    for j in range((len(houses)-1), -1, -1):

        if j != 0:
            print(str(houses[j]) + ' ', end='')

        else:
            print(str(houses[j]))

    print("Total Sale: " + str(total_profit))


# main code
# prompt input for k
k = int(input("Enter value of k: "))
input = open("test.txt", "r")
no_houses = int(input.readline())           # read the first line as length
profit = input.readline().split()           # split all the values in 2nd line

for i in range(no_houses):
    profit[i] = int(profit[i])

not_neighbor_sale(profit, no_houses, k)