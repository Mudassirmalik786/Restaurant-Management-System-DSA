# Description: This file contains all the sorting algorithms and searching algorithms
from cmath import inf
from pickle import FALSE


# insertion sort function
def InsertionSort(MOVIES, start, end, keyValue):
    for i in range(start + 1, end):
        singleMovie = MOVIES[i][keyValue]
        Temp1 = MOVIES[i]
        j = i - 1
        while j >= start and str(singleMovie) < str(MOVIES[j][keyValue]):
            MOVIES[j + 1] = MOVIES[j]
            j = j - 1
        MOVIES[j + 1] = Temp1
    return MOVIES[start:end]


# Selection sort function
def SelectionSort(Array, start, end, Key):
    for key in range(start, end):
        min_idx = key

        for i in range(key, end):
            if str(Array[i][Key]) < str(Array[min_idx][Key]):
                min_idx = i
        (Array[key], Array[min_idx]) = (Array[min_idx], Array[key])
    return Array


# Bubble sort function
def BubbleSort(Array, start, end, Key):
    i = end
    sorted = False
    while i > start and not sorted:
        sorted = True
        for j in range(start + 1, i):
            if (str(Array[j - 1][Key]) > str(Array[j][Key])):
                temp = Array[j - 1]
                Array[j - 1] = Array[j]
                Array[j] = temp
                sorted = False
        i = i - 1
    return Array

# Merge Sort
def MergeSort(Array, start, end, Key):
    if start != end:
        q = (start + end) // 2
        MergeSort(Array, start, q, Key)
        MergeSort(Array, q + 1, end, Key)
        return Merge(Array, start, end, q, Key)

# Merge function for merge sort
def Merge(Array, p, r, q, Key):
    leftcopy = Array[p:q + 1]
    rightcopy = Array[q + 1:r + 1]

    leftcopyindex = 0
    rightcopyindex = 0
    sortedindex = p

    while leftcopyindex < len(leftcopy) and rightcopyindex < len(rightcopy):

        if str(leftcopy[leftcopyindex][Key]) <= str(rightcopy[rightcopyindex][Key]):
            Array[sortedindex] = leftcopy[leftcopyindex]
            leftcopyindex = leftcopyindex + 1

        else:
            Array[sortedindex] = rightcopy[rightcopyindex]
            rightcopyindex = rightcopyindex + 1

        sortedindex = sortedindex + 1

    while leftcopyindex < len(leftcopy):
        Array[sortedindex] = leftcopy[leftcopyindex]
        leftcopyindex = leftcopyindex + 1
        sortedindex = sortedindex + 1

    while rightcopyindex < len(rightcopy):
        Array[sortedindex] = rightcopy[rightcopyindex]
        rightcopyindex = rightcopyindex + 1
        sortedindex = sortedindex + 1
    return Array

# Hybrid Merge Sort
def HybridMergeSort(Array, start, end, Key):
    if end - start > 250:
        q = (start + end) // 2
        MergeSort(Array, start, q, Key)
        MergeSort(Array, q + 1, end, Key)
        return Merge(Array, start, end, q, Key)
    else:
        return InsertionSort(Array, start, end, Key)

def search_string(MOVIES, search_key, search_value):
    matching_items = []
    non_matching_items = []
    for item in MOVIES:
        if search_value.lower() in item[search_key].lower():
            matching_items.append(item)
        else:
            non_matching_items.append(item)
    result = matching_items + non_matching_items
    return result

# Function to search integer values
def search_int(MOVIES, search_key, search_value):
    matching_items = []
    non_matching_items = []

    for item in MOVIES:
        item_value = str(item[search_key])
        if search_value.isdigit() and search_value in item_value:
            matching_items.append(item)
        elif not search_value.isdigit() and search_value.lower() in item_value.lower():
            matching_items.append(item)
        else:
            non_matching_items.append(item)

    result = matching_items + non_matching_items
    return result
def count_sort_letters(Array, col, base):
    Temp = Array
    Temp1 = []
    # for Key in range(0,len(Array)):
    #     Temp.append({Key:Array[Key]})
    # print(Temp)
    # Array=Temp
    output = [0] * len(Array)
    count = [0] * (base + 1)
    min_base = ord('a') - 1
    Key = 0
    for item in (Array):
        letter = ord(item[col]) - min_base if col < len(item) else 0
        count[letter] += 1
        Temp1.append(item)
        Key = Key + 1
    print(Temp1)
    for Key in range(len(count) - 1):
        count[Key + 1] += count[Key]
    for item in reversed(Array):
        letter = ord(item[col]) - min_base if col < len(item) else 0
        output[count[letter] - 1] = item
        count[letter] -= 1
    return output

# Radix Sort
def radix_sort_letters(Array):
    max_col = len(max(Array, key=len))
    for col in range(max_col - 1, -1, -1):
        Array = count_sort_letters(Array, col, 26)
    return Array


# Quick Sort
def partition(MOVIES, low, high, Key):
    pivot = MOVIES[high][Key]
    i = low - 1
    for j in range(low, high):
        if str(MOVIES[j][Key]) <= str(pivot):
            i = i + 1
            MOVIES[i], MOVIES[j] = MOVIES[j], MOVIES[i]
    MOVIES[i + 1], MOVIES[high] = MOVIES[high], MOVIES[i + 1]
    return i + 1

def QuickSort(MOVIES, Start, End, Key):
    End=End-1
    if Start < End:  # Change ">=" to "<" here
        p = partition(MOVIES, Start, End, Key)
        QuickSort(MOVIES, Start, p - 1, Key)
        QuickSort(MOVIES, p + 1, End, Key)
    return MOVIES


# def QuickSort(Array, Key):
#     if len(Array) == 0:
#         return []
#     else:
#         pivot = Array[0]
#         lesser = QuickSort([Text for Text in Array[1:] if str(Text[Key]) < str(pivot[Key])], Key)
#         greater = QuickSort([Text for Text in Array[1:] if str(Text[Key]) >= str(pivot[Key])], Key)
#         return lesser + [pivot] + greater


# Shell sort
def ShellSort(Array, Key):
    interval = len(Array) // 2
    while interval > 0:
        for i in range(interval, len(Array)):
            temp = Array[i]
            j = i
            while j >= interval and str(Array[j - interval][Key]) > str(temp[Key]):
                Array[j] = Array[j - interval]
                j -= interval

            Array[j] = temp
        interval //= 2
    return Array


# Comb Sort
def CombSort(Array, Key):
    shrink_fact = 1.3
    gaps = len(Array)
    swapped = True
    i = 0

    while gaps > 1 or swapped:
        gaps = int(float(gaps) / shrink_fact)

        swapped = False
        i = 0

        while gaps + i < len(Array):
            if str(Array[i][Key]) > str(Array[i + gaps][Key]):
                Array[i], Array[i + gaps] = Array[i + gaps], Array[i]
                swapped = True
            i += 1
    return Array

# Hepify function for heap sort
def Heapify(Array, n, i, Key):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and str(Array[i][Key]) < str(Array[l][Key]):
        largest = l

    if r < n and str(Array[largest][Key]) < str(Array[r][Key]):
        largest = r

    if largest != i:
        Array[i], Array[largest] = Array[largest], Array[i]
        Heapify(Array, n, largest, Key)


def HeapSort(Array, Key):
    n = len(Array)

    for i in range(n // 2, -1, -1):
        Heapify(Array, n, i, Key)

    for i in range(n - 1, 0, -1):
        Array[i], Array[0] = Array[0], Array[i]

        Heapify(Array, i, 0, Key)
    return Array


# Brick Sort
def BrickSort(Array, Key):
    isSorted = 0
    while isSorted == 0:
        isSorted = 1
        temp = 0
        for i in range(1, len(Array) - 1, 2):
            if str(Array[i][Key]) > str(Array[i + 1][Key]):
                Array[i], Array[i + 1] = Array[i + 1], Array[i]
                isSorted = 0

        for i in range(0, len(Array) - 1, 2):
            if str(Array[i][Key]) > str(Array[i + 1][Key]):
                Array[i], Array[i + 1] = Array[i + 1], Array[i]
                isSorted = 0

    return Array


# Counting Sort
def CountingSort(Array, Key):
    size = len(Array)
    Temp = [0] * size
    Max = 0
    for i in range(0, len(Array)):
        if Max <= Array[i][Key]:
            Max = Array[i][Key]
    count = [0] * (Max + 1)

    for i in range(0, size):
        count[Array[i][Key]] += 1

    for i in range(1, Max):
        count[i] += count[i - 1]

    j = size - 1
    while j >= 0:
        Temp[count[Array[j][Key]] - 1] = Array[j]
        count[Array[j][Key]] -= 1
        j -= 1

    for j in range(0, size):
        Array[j] = Temp[j]
    return Array[1:len(Array) - 1]

# Bucket Sort
def MultilevalHeapify(Array, n, i, Key, Previous):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and str(Array[i][Key]) < str(Array[l][Key]) and str(Array[i][Previous]) == str(Array[l][Previous]):
        largest = l
    if r < n and str(Array[largest][Key]) < str(Array[r][Key]) and str(Array[largest][Previous]) == str(
            Array[r][Previous]):
        largest = r
    if largest != i:
        Array[i], Array[largest] = Array[largest], Array[i]
        MultilevalHeapify(Array, n, largest, Key, Previous)


# Multilevel Sorting
def MultilevalSort(Array, Key, Previous):
    n = len(Array)
    for i in range(n // 2, -1, -1):
        MultilevalHeapify(Array, n, i, Key, Previous)
    for i in range(n - 1, 0, -1):
        Array[i], Array[0] = Array[0], Array[i]
        MultilevalHeapify(Array, i, 0, Key, Previous)
    return Array


# Searching Algorithms
def LinearSearchthatcontain(Array, Key, text):
    Temp = []
    for j in range(0, len(Array)):
        if str(Array[j][Key]).find(text) != -1:
            Temp.append(Array[j])
    return Temp


def LinearSearchthatStarts(Array, Key, text):
    Temp = []
    for j in range(0, len(Array)):
        if str(Array[j][Key]).startswith(text) == True and str(Array[j][Key]).find(text) != -1:
            Temp.append(Array[j])
    return Temp


def LinearSearchthatEnds(Array, Key, text):
    Temp = []
    for j in range(0, len(Array)):
        if str(Array[j][Key]).endswith(text) == True and str(Array[j][Key]).find(text) != -1:
            Temp.append(Array[j])
    return Temp


def BooleanSearchwithAnd(Array, Key1, Key2, text):
    Temp = []
    text1 = text.split(' & ')
    for j in range(0, len(Array) - 2):
        if str(Array[j][Key1]).find(text1[0]) != -1 and str(Array[j][Key2]).find(text1[1]) != -1:
            Temp.append(Array[j])
    return Temp


def BooleanSearchwithOr(Array, Key1, Key2, text):
    Temp = []
    text1 = text.split(' | ')
    for j in range(0, len(Array) - 2):
        if str(Array[j][Key1]).find(text1[0]) != -1 or str(Array[j][Key2]).find(text1[1]) != -1:
            Temp.append(Array[j])
    return Temp


def BooleanSearchwithNot(Array, Key1, text):
    Temp = []
    for j in range(0, len(Array) - 2):
        if not str(Array[j][Key1]).find(text) != -1:
            Temp.append(Array[j])
    return Temp


# Binary Search
# def BinarySearch(Array, Text, Low, High,Key):
#     if High <= Low:
#         mid = Low + (High - Low)//2
#         if str(Array[mid][Key]) == Text:
#             return mid
#         elif str(Array[mid][Key]) > Text:
#             return BinarySearch(Array, Text, Low, mid-1,Key)
#         else:
#             return BinarySearch(Array, Text, mid + 1, High,Key)
#     else:
#         return -1


# Binary Search
def BinarySearch(Array, Text, Low, High, Key):
    Array = MergeSort(Array, 0, len(Array) - 1, Key)
    Temp = []
    mid = Low + ((High - Low) // 2)
    mid1 = mid
    count = 0
    print(Array[mid][Key])

    while (mid >= Low and mid1 <= High):
        # print(Text, Array[mid][Key])
        if count == 0:
            if (Text == str(Array[mid][Key])):
                Temp.append(Array[mid])
                mid -= 1
        if count == 1:
            if (Text == str(Array[mid1 - 1][Key])):
                Temp.append(Array[mid1 - 1])
                mid1 += 1
        if (Text < str(Array[mid][Key])):
            mid -= 1
        if (Text > str(Array[mid][Key])):
            count = 1
            mid1 += 1

    return Temp
