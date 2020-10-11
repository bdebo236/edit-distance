def editDistance(s1, s2):
    ## If one of the string is empty then the edit distance will be equal to the length of the other because in that case we just have to
    ## insert all the letters in that string to duplicate it or remove all from the other to make it empty like the other
    if len(s1) == 0:
        return len(s2)
    elif len(s2) == 0:
        return len(s1)
    elif s1[-1] == s2[-1]:
        ## The Edit Distance of two string with the same last alphabet will be the same the distance of the two strings without the last alphabet
        ## This is cause the last alphabet being same won't provide any input, as they are already same    
        return editDistance(s1[:-1], s2[:-1])
    else:
        ## If last letter isn't the same then we have to perform one of the three operations i.e. insertion, deletion or replacing letter.
        return 1 + min(
            editDistance(s1, s2[:-1]),              ## Insertion
            editDistance(s1[:-1], s2[:-1]),         ## Replacing letter
            editDistance(s1[:-1], s2)               ## Deletion
        )

## Input and accept string only if they're purely alphabetical
while True:
    s1 = input("\nEnter the string you wish to change: ")
    if s1.isalpha():
        break
    else:
        print("Strings should be alphabets only.")

while True:
    s2 = input("\nEnter the original string: ")
    if s2.isalpha():
        break
    else:
        print("Strings should be alphabets only.")

## Call function
totalDistance = editDistance(s1.lower(), s2.lower())

## Printing the result
print("\nEdit Distance to convert " + s1 + " to " + s2 + " is: " + str(totalDistance))
