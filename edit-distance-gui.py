from tkinter import *
from tkinter.font import Font
from PIL import ImageTk, Image
import numpy as np

def updateBox(background, cell, dpTable):
    ## This function is responsible for chaning the colour of the boxes when we are back tracking for the solution

    ## Declaring some variables
    j,i = cell
    box_size = 50
    padding = 20
    box_gap = 10
    y = (box_gap + box_size)*(j+1) + padding
    x = (box_gap + box_size)*(i+1) + padding
    arrow = {
        'n':'↖',
        'i':'↑',
        'd':'←',
        'r':'↖',
    }

    ## Creating a box with a different colour over lapping the pervious one and writing text on it
    background.create_rectangle(x, y, x + box_size, y + box_size, fill = '#7d5fff', outline = "")
    if i == 0 and j == 0:
        text = dpTable[j,i][:-1]
    else:
        text = dpTable[j,i].replace(dpTable[j,i][-1], arrow[dpTable[j,i][-1]])
    background.create_text(x+box_size/2, y+box_size/2, text = text, font = textFont)   ## Adding Text
    root.update()

def writeInBox(x, y, cell, background):
    ## This function writes texts on screen given the location
    background.create_text(x, y, text = cell, font = textFont)
    root.update()

def printEditDistance(dist, background):
    ## This function display Distance at the end
    background.create_text(w/2 + 360, h/2 - 300, text = "Total Changes Needed: " + str(dist), font = textFont)
    root.update()

def getInput(str1, str2):
    ## This function checks if the inputs are valid or not i.e. if they're strings Only and the fields aren't empty.
    s1 = str1.get()
    s2 = str2.get()
    if s1 == '' or s2 == '': 
        ## Warning for empty string
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Please enter both strings").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    elif not(s1.isalpha()) or not(s2.isalpha()):
        ## Warning for non alphebetical strings
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Both should be Strings only.").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    else:
        ## If all the conditions are valid we go to our second screen which displays the table
        tableCreate(s1.lower(), s2.lower())

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
    return table

def calcChangesInString(table, s1, s2):
    i = len(s1)
    j = len(s2)
    changes = []  ## Initialising changes list: saves all the changes in words
    path = []     ## Initialising path list: this saves all the boxes we trace while backtracking
    flag = 0 ## This will tell when to break out of the loop
    changing_string = list(s2)  ## copying the string to reflect the changes as we go backtracing
    
    while i >= 0:
        if flag == 1:
            break
        while j >= 0:
            if table[i,j][-1] == 'n':  ## If there is an 'n' that means no changes needed simply move diagonally.
                path.append([i,j])
                j-=1
                i-=1
            elif table[i,j][-1] == 'r':
                ## In case of a 'r' i.e. replace, we replace the character in the string, print appropriate statement and move diagonally.
                statement1 = str(s2[j-1]).upper() + ' changes to ' + str(s1[i-1]).upper()
                changing_string[j-1] = s1[i-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                i-=1
                j-=1
            elif table[i,j][-1] == 'i':
                ## In case of a 'i' i.e. insertion, we insert the character in the string, print appropriate statement and move upwards.
                statement1 = 'Insert ' + str(s1[i-1]).upper() + ' at position ' + str(j+1) + ' in string'
                changing_string.insert(j, s1[i-1])
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                i-=1
            elif table[i,j][-1] == 'd':
                ## In case of a 'd' i.e. deletion, we delete the character in the string, print appropriate statement and move leftwards.
                statement1 = 'Remove ' + str(s2[j-1]).upper()
                del changing_string[j-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                path.append([i,j])
                j-=1
            if len(changes) == int(table[len(s1), len(s2)][:-1]):
                ## If total number of changes match the edit distance, we break out of the loop
                flag = 1
                break
    
    return changes, path

def inputScreen():
    ## This function is responsible for the input screen/landing page of the GUI
    ## Setting Background
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)
    ## Heading
    background.create_text(w/2, h/2 - 300, text = "Edit Distance", font = headingFont)

    ## Creating text and input boxes
    background.create_text(w/2 - 310, h/2 - 200, text = "Enter the original string: ", font = textFont)
    str1 = Entry(background)
    background.create_window(w/2 + 120, h/2 - 200, window = str1, width = w/4)

    background.create_text(w/2 - 250, h/2 - 100, text = "Enter the string you want to change: ", font = textFont)
    str2 = Entry(background)
    background.create_window(w/2 + 120, h/2 - 100, window = str2, width = w/4)
    
    ## Button for input
    b1 = Button(background, text = "Enter", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:getInput(str1, str2))
    background.create_window(w/2, h/2, window = b1, width = w/8)

def tableCreate(s1, s2):
    ## This function creates the table on screen and puts all the values in it.

    ## Resetting the background
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)

    ## Declaring some variables
    box_size = 50
    box_gap = 10
    table_width = len(s1) + 2
    table_height = len(s2) + 2
    padding = 20
    animation_gap = 100
    arrow = {
        'n':'↖',
        'i':'↑',
        'd':'←',
        'r':'↖',
    }

    ## Creating the Table
    for i in range(table_height):
        for j in range(table_width):
            if (i,j) == (0,0) or (i,j) == (1,0) or (i,j) == (0,1):
                continue
            else:
                x = (box_gap + box_size)*i + padding
                y = (box_gap + box_size)*j + padding
                background.create_rectangle(x, y, x + box_size, y + box_size, fill = '#9fe9fa', outline = "")

    ## Writing the String Values
    ## To Change String
    for i in range(table_height-2):
        x = (box_gap + box_size)*(i+2) + padding + box_size/2
        background.create_text(x, padding + box_size/2, text = s2[i].upper(), font = textFont)

    ## Orig String
    for i in range(table_width-2):
        y = (box_gap + box_size)*(i+2) + padding + box_size/2
        background.create_text(padding + box_size/2, y, text = s1[i].upper(), font = textFont)
    
    ## Writing formula for refernce with the box image
    formulaOnCanvas = background.create_image(w/2 + 100, h/2 - 250, anchor=NW, image=formula)
    background.update()

    dpTable = calcDpTable(s1, s2)  ## Getting the DP Table from the function

    ## Initialising Table
    for i in range(dpTable.shape[0]):
        for j in range(dpTable.shape[1]):
            if i == 0 or j == 0:
                x = (box_gap + box_size)*(j+1) + padding + box_size/2
                y = (box_gap + box_size)*(i+1) + padding + box_size/2
                if i == 0 and j == 0:
                    cell = dpTable[i,j][:-1]
                else:
                    cell = dpTable[i,j].replace(dpTable[i,j][-1], arrow[dpTable[i,j][-1]])
                background.create_text(x, y, text = cell, font = textFont)

    ## Putting in Numbers through animation
    for i in range(dpTable.shape[0]):
        for j in range(dpTable.shape[1]):
            if not(i == 0 or j == 0):
                x = (box_gap + box_size)*(j+1) + padding + box_size/2
                y = (box_gap + box_size)*(i+1) + padding + box_size/2

                cell = dpTable[i,j].replace(dpTable[i,j][-1], arrow[dpTable[i,j][-1]])
                background.after(animation_gap, writeInBox(x,y,cell,background))

    ## Calling function to print total edit distance
    printEditDistance(dpTable[table_width-2, table_height-2][:-1], background)

    ## Button to display list of changes
    b3 = Button(background, text = "Show Changes in Detail", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:displayChangeList(background, dpTable, s1, s2, formulaOnCanvas, button, animation_gap))
    button = background.create_window(w/2 + 340, h/2 - 60, window = b3, width = w/8)

def displayChangeList(background, dpTable, s1, s2, formulaOnCanvas, b3, animation_gap):
    ## This function is responsible for our third screen i.e. displaying all the changes to be made.

    ## Delete the formula image and button
    background.delete(b3)
    background.delete(formulaOnCanvas)
    background.update()

    ## Add the edit-distance backtracking chart
    background.create_image(w/2 + 40, h/2 - 300, anchor=NW, image=back_table)

    ## Finding all the changes needed in bullets
    changes, path = calcChangesInString(dpTable, s1, s2)

    ## Making the back tracking path a different colour
    for cell in path:
        background.after(animation_gap, updateBox(background, cell, dpTable))


    ## Printing the changes in words
    if len(changes) == 0: ## If no changes we print a statement accordingly
        background.create_text(w/2 + 350, h/2 - 30, text = "The strings are same, so no changes.", font = smallTextFont)
        i=1
    else:
        background.create_text(w/2 + 350, h/2 - 30, text = "The changes to be made in '" + s2 + "' are:", font = textFont)
        for i in range(len(changes)):
            statement = str(i+1) + ". " + changes[i][0] + '. ' + changes[i][1]
            background.create_text(w/2 + 370, h/2 + i*30, text = statement, font = smallTextFont)
        i+=1

    ## Button for going back to input screen
    b2 = Button(background, text = "Enter Another String", bg = '#84A3FF', activebackground = '#FFE5CC', command=inputScreen)
    background.create_window(w/2 + 250, h/2 + i*32, window = b2, width = w/8)

    ## Button to quit and end the program
    b3 = Button(background, text = "Quit", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:root.destroy())
    background.create_window(w/2 + 450, h/2 + i*32, window = b3, width = w/8)
  

if __name__ == "__main__":
    root = Tk()

    ## Adjusting screen size, name, etc
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))
    root.title("Edit Distance")

    ## Declaring some font variable
    smallTextFont = Font(family = 'Bookman Old Style', size = '12')
    textFont = Font(family = 'Bookman Old Style', size = '15')
    headingFont = Font(family = 'Bookman Old Style', size = '30')

    ## Importing all the images
    formula = Image.open(r"C:\Users\deboparna\Desktop\college\Sem5\design and analysis of algorithm\assignment\edit-distance-formula.png")
    formula = formula.resize((500, 128), Image.ANTIALIAS)
    formula = ImageTk.PhotoImage(formula)

    back_table = Image.open(r"C:\Users\deboparna\Desktop\college\Sem5\design and analysis of algorithm\assignment\edit-distance-square.png")
    back_table = back_table.resize((600, 300), Image.ANTIALIAS)
    back_table = ImageTk.PhotoImage(back_table)

    ## Calling the Input Screen function which is responsible for the GUI of the landing page
    inputScreen()
    
    root.mainloop()
