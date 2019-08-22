import heapq

file01 = open("timeSpent.txt")
value_list = []
for line in file01:
    pairs = line.strip("\n")
    value = pairs.split(":")
    value_list.append(value)
file01.close()

# swapping the index 0 and index 1
for i in range(len(value_list)):
    tmp = value_list[i][0]
    value_list[i][0] = value_list[i][1]
    value_list[i][1] = tmp

def heapSearch(alist, k):
    heap = []
    for item in alist:
        # create a heap with k items
        # if the heap has length of k already
        # AND the next item in the list passed as argument is bigger than the first element in the heap
        # which, in this case, the first element of the heap is the smallest element in min-heap
        if len(heap) < k or item > heap[0]:
            # If the heap is full, remove the smallest element on the heap.
            if len(heap) == k:
                heapq.heappop(heap)
            # add the elements from the list into the heap
            # heap push will sort the heap again to have smallest on top
            heapq.heappush(heap, item)
    return heap

k = int(input("Enter value k:"))
the_heap = heapSearch(value_list, k)

def mergeSort(alist):

    if len(alist) > 1:
        mid = len(alist)//2
        left = alist[:mid]
        right = alist[mid:]

        mergeSort(left)
        mergeSort(right)

        i=0
        j=0
        k=0
        while i < len(left) and j < len(right):
            if left[i] > right[j]:
                alist[k]=left[i]
                i=i+1
            else:
                alist[k]=right[j]
                j=j+1
            k=k+1

        while i < len(left):
            alist[k]=left[i]
            i=i+1
            k=k+1

        while j < len(right):
            alist[k]=right[j]
            j=j+1
            k=k+1

mergeSort(the_heap)

# go through the list to check whether there are similar items
for k in range(len(the_heap)-1):
    if the_heap[k][0] == the_heap[k + 1][0] and the_heap[k + 1][1] < the_heap[k][1]:
        tmp = the_heap[k]
        the_heap[k] = the_heap[k + 1]
        the_heap[k + 1] = tmp

for i in range(len(the_heap)):
    print("#",i,": User ID:",the_heap[i][1]," Time Spent:",the_heap[i][0])
