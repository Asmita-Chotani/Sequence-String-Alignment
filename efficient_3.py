import sys
import time
import math
import numpy as np
import psutil

alpha_values = { 'A' : {'A': 0, 'C': 110, 'G': 48, 'T': 94} , 'C' : {'A': 110, 'C': 0, 'G': 118, 'T': 48} , 'G' : {'A': 48, 'C': 118, 'G': 0, 'T': 110}, 'T' : {'A': 94, 'C': 48, 'G': 110, 'T': 0} }

strings = dict()


def checkString(count, lenX ,input):
    x = math.pow(2, count) * len(input)
    if x != lenX:
        return 0
    return 1

def newString(old_string, line):
    old_string = old_string[:int(line) + 1] + old_string + old_string[int(line) + 1:]
    return old_string

def traceback_string(arr,len1,len2, string1, string2):
    solutionX = list()
    solutionY = list()
    while (len1 != 0) and (len2 != 0):
        val1 = arr[len1 - 1][len2 - 1] + alpha_values[string1[len1 - 1]][string2[len2 - 1]]
        val2 = arr[len1 - 1][len2] + 30
        val3 = arr[len1][len2 - 1] + 30
        if arr[len1][len2] == val1:
            solutionY.append(string2[len2 - 1])
            solutionX.append(string1[len1 - 1])
            len1 -= 1
            len2 -= 1
        elif val2 == arr[len1][len2]:
            solutionX.append(string1[len1 - 1])
            solutionY.append('_')
            len1 -= 1
        elif val3 == arr[len1][len2]:
            solutionX.append('_')
            solutionY.append(string2[len2 - 1])
            len2 -= 1

    while len1 > 0:
        solutionX.append(string1[len1 - 1])
        solutionY.append('_')
        len1 -= 1

    while len2 > 0:
        solutionY.append(string2[len2 - 1])
        solutionX.append('_')
        len2 -= 1

    xData = solutionX[::-1]
    xValue = ''.join(xData)
    yData = solutionY[::-1]
    yValue = ''.join(yData)

    return xValue, yValue
    

def basicAlignment1D(len1,len2,string1, string2):
    s1= len1 + 1
    s2= len2 + 1
    arr = [[0 for j in range(s2)] for i in range(s1)]
    for x, y in ((i, j) for i in range(s1) for j in range(s2)):
        arr[x][0] = 30 * x
        arr[0][y] = 30 * y

    # traverse through matrix
    for i in range(1,s1):
        for j in range(1, s2):
            val1 =  alpha_values[string1[i - 1]][string2[j - 1]] + arr[i - 1][j - 1]
            val2 = min(val1, 30 + arr[i - 1][j])
            arr[i][j] = min(30 + arr[i][j - 1], val2)

    X, Y = traceback_string(arr, len1,len2,string1, string2)
    return X, Y, arr[len1][len2]

def basicAlignment(len1,len2,string1, string2):

    s1= len1 + 1
    s2= len2 + 1
    arr = np.zeros((s1, s2))
    for x, y in ((i, j) for i in range(s1) for j in range(s2)):
        arr[x][0] = 30 * x
        arr[0][y] = 30 * y

    # traverse through matrix
    for i in range(1,s2):
        for j in range(1, s1):
            val1 = arr[i - 1][j - 1] + alpha_values[string1[i - 1]][string2[j - 1]]
            val2 = min(val1, 30 + arr[i - 1][j])
            arr[i][j] = min(30 + arr[i][j - 1], val2)

    X, Y = traceback_string(arr, len1,len2,string1, string2)
    return X, Y, arr[len1][len2]

  
def dnc_alignment(string1, string2):
    len1, len2 = len(string1), len(string2)

    if len1 < 3 or len2 < 3:
        return basicAlignment1D(len1, len2, string1, string2)

    min_var = sys.maxsize

    string1_left, string1_right = string1[0:len1//2], string1[len1//2:]

    string2_left = ""
    string2_right = ""

    temp_var = 0

    min_l = divide(string1_left, string2, len1//2, len2)
    min_r = divide(string1_right[::-1], string2[::-1], (len1 - len1//2), len2)
    
    #temp_var = 0

    for i in range(len2+1):
        min_current = min_l[i] + min_r[len2-i]
        if(min_current < min_var):
            temp_var = i
            min_var = min_current

    if (temp_var>0):
        string2_left = string2[:temp_var]

    if (temp_var<len2):
        string2_right = string2[temp_var:len2]


    left = dnc_alignment(string1_left, string2_left)
    right = dnc_alignment(string1_right, string2_right)

    result0 = left[0] + right[0]
    result1 = left[1] + right[1]
    return result0, result1, min_var
    
def divide(string1, string2, len1, len2):
    
    divide_arr = []

    for i in range(len2+1):
        val = 30 * i
        divide_arr.append(val)
    
    for i in range(1, len1+1):
        prev_val = divide_arr[0]
        divide_arr[0] = i * 30
        for j in range(1, len2+1):
            #change line if still plag
            alpha= alpha_values[string1[i-1]][string2[j - 1]]
            val1 = min(divide_arr[j], divide_arr[j-1])
            temp_var = divide_arr[j]
            divide_arr[j] = min(prev_val + alpha, val1 + 30)
            prev_val = temp_var
    return divide_arr

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

stringA = ''
inputA = ''
stringB = ''
inputB = ''

if len(sys.argv) > 1:
    print("-commandline input-")
    file = sys.argv[1]
    with open(file) as f:
        lines = f.readlines()
    f.close()
else:
    print("-work directory input-")
    with open('input.txt') as f:
        lines = f.readlines()
    f.close()

count1 = 0
count2 = 0
flag = 1

for index, line in enumerate(lines):
    line = line.replace('\n', '', -1)
    choice = line.isnumeric()
    if index == 0:
        # create two copies of the input
        inputA = line
        stringA = line

    elif choice == 1:

        if flag == 0:
            stringB = newString(stringB, line)
            count2 += 1
        else:
            stringA = newString(stringA, line)
            count1 += 1
    else:
        flag = 0
        inputB = line
        stringB = line

if (checkString(count1, len(stringA), inputA) and checkString(count2, len(stringB),inputB)) == True:
    time1 = time.time()
    row1, row2, min_var = dnc_alignment(stringA, stringB)
    memoryValue = process_memory()
    time2 = time.time()
    with open(sys.argv[2], "w") as f:
        print(int(min_var / 1.0), file=f)
        print(row1, file=f)
        print(row2, file=f)
        print((time2 - time1)*1000, file=f)
        print(float(memoryValue), file=f)
else:
    print("Invalid String")
