## This python code solves the edit distance problem using dynamic programming. 
## 1. calcDpTable() takes in both string and calculcates the table and prints the total edit distance.
## 2. calcChangesList takes in the table from the previously mentioned function and returns a list of changes (in words) needed to make
##    in the string to convert into the other.

import numpy as np

def calcDpTable(s1, s2):
    ## Initialise the table with zeroes.
    table = np.zeros([len(s1)+1, len(s2)+1], dtype=np.dtype('U3'))

    ## Here 'i' indicated insertion or up arrow and 'd' indicated 'deletion' or left hand side arrow
    ## Further in the code you'll find 'r' indicating 'replacment' or diagonal arrow. 
    ## Also 'n' meaning 'no operation' or diagonal arrow.

    ## Fill in base cases
    for i in range(len(s1)+1):
        table[i,0] = str(i) + 'i'
    for j in range(len(s2)+1):
        table[0,j] = str(j) + 'd'

    ## Start filling the rest of the table with the help of formula
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:  ## If there is no character mismatch then no operation.
                table[i, j] = table[i-1, j-1][:-1] + 'n'
            else:  ## In case of character mismatch we take the minimum among the three and add one.
                if min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i-1, j-1][:-1]):
                    table[i,j] = str(int(table[i-1, j-1][:-1]) + 1) + 'r'
                elif min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i, j-1][:-1]):
                    table[i,j] = str(int(table[i, j-1][:-1]) + 1) + 'd'
                elif min(int(table[i-1, j-1][:-1]), int(table[i-1, j][:-1]), int(table[i, j-1][:-1])) == int(table[i-1, j][:-1]):
                    table[i,j] = str(int(table[i-1, j][:-1]) + 1) + 'i'

    ## Displaying total edit distance i.e. the value in the bottom left corner cell.
    print('Total Edit Distance:', table[len(s1), len(s2)][:-1])

    calcChangesList(s1, s2, table)

def calcChangesList(s1, s2, table):    
    i = len(s1)
    j = len(s2)
    changes = []  ## Initialising changes list
    flag = 0 ## This will tell when to break out of the loop
    changing_string = list(s2)  ## copying the string to reflect the changes as we go backtracing
    
    while i >= 0:
        if flag == 1:
            break
        while j >= 0:
            if table[i,j][-1] == 'n':  ## If there is an 'n' that means no changes needed simply move diagonally.
                j-=1
                i-=1
            elif table[i,j][-1] == 'r':  
                ## In case of a 'r' i.e. replace, we replace the character in the string, print appropriate statement and move diagonally.
                statement1 = str(s2[j-1]) + ' changes to ' + str(s1[i-1])
                changing_string[j-1] = s1[i-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                i-=1
                j-=1
            elif table[i,j][-1] == 'i':
                ## In case of a 'i' i.e. insertion, we insert the character in the string, print appropriate statement and move upwards.
                statement1 = 'Insert ' + str(s1[i-1]) + ' at position ' + str(j+1) + ' in string'
                changing_string.insert(j, s1[i-1])
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                i-=1
            elif table[i,j][-1] == 'd':
                ## In case of a 'd' i.e. deletion, we delete the character in the string, print appropriate statement and move leftwards.
                statement1 = 'Remove ' + str(s2[j-1])
                del changing_string[j-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                j-=1
            if len(changes) == int(table[len(s1), len(s2)][:-1]):
                ## If total number of changes match the edit distance, we break out of the loop
                flag = 1
                break
    
    ## Printing the list of changes
    print("\n\nThe Changes to be made are:\n")
    for i in range(len(changes)):
        print(i+1,".", changes[i][0],'\n', changes[i][1], '\n')

str2 = input("Enter String to be Change: ")
str1 = input("Enter Original String: ")
calcDpTable(str1, str2)
