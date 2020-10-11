import numpy as np

def editDistance(s1, s2):
    table = np.zeros([len(s1)+1, len(s2)+1], dtype=np.dtype('U2'))

    for i in range(len(s1)+1):
        table[i,0] = str(i) + 'i'

    for j in range(len(s2)+1):
        table[0,j] = str(j) + 'd'

    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                table[i, j] = table[i-1, j-1][0] + 'n'
            else:
                if min(table[i-1, j-1][0], table[i-1, j][0], table[i, j-1][0]) == table[i-1, j-1][0]:
                    table[i,j] = str(int(table[i-1, j-1][0]) + 1) + 'r'
                elif min(table[i-1, j-1][0], table[i-1, j][0], table[i, j-1][0]) == table[i, j-1][0]:
                    table[i,j] = str(int(table[i, j-1][0]) + 1) + 'd'
                elif min(table[i-1, j-1][0], table[i-1, j][0], table[i, j-1][0]) == table[i-1, j][0]:
                    table[i,j] = str(int(table[i-1, j][0]) + 1) + 'i'

    print('Total Edits Needed:', table[len(s1), len(s2)][0])
    
    i = len(s1)
    j = len(s2)
    changes = []
    path = []
    flag = 0
    changing_string = list(s2)
    
    while i >= 0:
        if flag == 1:
            break
        while j >= 0:
            if table[i,j][1] == 'n':
                path.append([i,j])
                j-=1
                i-=1
            elif table[i,j][1] == 'r':
                statement1 = str(s2[j-1]) + ' changes to ' + str(s1[i-1])
                changing_string[j-1] = s1[i-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                i-=1
                j-=1
            elif table[i,j][1] == 'i':
                statement1 = 'Insert ' + str(s1[i-1]) + ' at position ' + str(j+1) + ' in string'
                changing_string.insert(j, s1[i-1])
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                i-=1
            elif table[i,j][1] == 'd':
                statement1 = 'Remove ' + str(s2[j-1])
                del changing_string[j-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                j-=1
            if len(changes) == int(table[len(s1), len(s2)][0]):
                flag = 1
                break

    #print(path)
    print("\n\nThe Changes to be made are:\n")
    for i in range(len(changes)):
        print(i+1,".", changes[i][0],'\n', changes[i][1], '\n')

str2 = input("Enter String to be Change: ")
str1 = input("Enter Original String: ")
editDistance(str1, str2)
