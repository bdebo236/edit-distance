from tkinter import *
from tkinter.font import Font
from PIL import ImageTk, Image
import numpy as np

def writeInBox(x, y, cell, background):
    background.create_text(x, y, text = cell, font = textFont)
    root.update()

def printEditDistance(dist, background):
    ## Display Distance
    background.create_text(w/2 + 360, h/2 - 300, text = "Total Changes Needed: " + str(dist), font = textFont)
    root.update()


def getInput(str1, str2):
    ## Check if the inputs are valid or not ie if they're strings Only and the fields aren't empty
    s1 = str1.get()
    s2 = str2.get()
    if s1 == '' or s2 == '': 
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Please enter both strings").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    elif not(s1.isalpha()) or not(s2.isalpha()):
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Both should be Strings only.").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    else:
        tableCreate(s1, s2)

def calcDpTable(s1, s2):
    table = np.zeros([len(s1)+1, len(s2)+1], dtype=np.dtype('U2'))

    for i in range(len(s1)+1):
        table[i,0] = i

    for j in range(len(s2)+1):
        table[0,j] = j

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

    return table

def calcChangesInString(table, s1, s2):
    i = len(s1)
    j = len(s2)
    changes = []
    flag = 0
    print('s1 = orig string =', s1)
    print('s2 = to be changed =', s2)
    print()
    changing_string = list(s2)
    
    while i >= 0:
        if flag == 1:
            break
        while j >= 0:
            if table[i,j][1] == 'n':
                j-=1
                i-=1
            elif table[i,j][1] == 'r':
                statement1 = str(s2[j-1]) + ' changes to ' + str(s1[i-1])
                changing_string[j-1] = s1[i-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                i-=1
                j-=1
            elif table[i,j][1] == 'i':
                statement1 = 'Insert ' + str(s1[i-1]) + ' at position ' + str(j+1) + ' in string'
                changing_string.insert(j, s1[i-1])
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                i-=1
            elif table[i,j][1] == 'd':
                statement1 = 'Remove ' + str(s2[j-1])
                del changing_string[j-1]
                statement2 = 'Thus, now the string becomes: ' + ''.join(changing_string)
                changes.append([statement1,statement2])
                j-=1
            if len(changes) == int(table[len(s1), len(s2)][0]):
                flag = 1
                break
            
    return changes


def inputScreen():
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
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)

    box_size = 50
    box_gap = 10
    table_width = len(s1) + 2
    table_height = len(s2) + 2
    padding = 50
    animation_gap = 500
    next_box_gap = 1000
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

    dpTable = calcDpTable(s1, s2)
    print(dpTable)

    ## Initialising Table
    for i in range(dpTable.shape[0]):
        for j in range(dpTable.shape[1]):
            if i == 0 or j == 0:
                x = (box_gap + box_size)*(j+1) + padding + box_size/2
                y = (box_gap + box_size)*(i+1) + padding + box_size/2
                cell = dpTable[i,j]
                background.create_text(x, y, text = cell, font = textFont)

    ## Putting in Numbers through animation
    for i in range(dpTable.shape[0]):
        for j in range(dpTable.shape[1]):
            if not(i == 0 or j == 0):
                x = (box_gap + box_size)*(j+1) + padding + box_size/2
                y = (box_gap + box_size)*(i+1) + padding + box_size/2

                cell = dpTable[i,j].replace(dpTable[i,j][1], arrow[dpTable[i,j][1]])
                background.after(100, writeInBox(x,y,cell,background))

    ## Calling function to print total edit distance
    background.after(next_box_gap, printEditDistance(dpTable[table_width-2, table_height-2][0], background))

    ## Button to display list of changes
    b3 = Button(background, text = "Show Changes in Detail", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:displayChangeList(background, dpTable, s1, s2, formulaOnCanvas, button))
    button = background.create_window(w/2 + 340, h/2 - 60, window = b3, width = w/8)

def displayChangeList(background, dpTable, s1, s2, formulaOnCanvas, b3):
    ## Delete the previous image and button
    background.delete(b3)
    background.delete(formulaOnCanvas)
    background.update()

    ## Add the edit-distance backtracking table
    background.create_image(w/2 + 40, h/2 - 300, anchor=NW, image=back_table)

    ## Print all the changes needed in bullets
    changes = calcChangesInString(dpTable, s1, s2)
    background.create_text(w/2 + 350, h/2 - 30, text = "The Changes to be made are:", font = textFont)
    for i in range(len(changes)):
        statement = str(i+1) + ". " + changes[i][0] + '. ' + changes[i][1]
        background.create_text(w/2 + 370, h/2 + i*30, text = statement, font = smallTextFont)

    ## Button for going back to input screen
    b2 = Button(background, text = "Enter Another String", bg = '#84A3FF', activebackground = '#FFE5CC', command=inputScreen)
    background.create_window(w/2 + 250, h/2 + 250, window = b2, width = w/8)

    ## Button to quit and end the program
    b3 = Button(background, text = "Quit", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:root.destroy())
    background.create_window(w/2 + 450, h/2 + 250, window = b3, width = w/8)
  

if __name__ == "__main__":
    root = Tk()

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))
    root.title("Edit Distance")
    smallTextFont = Font(family = 'Bookman Old Style', size = '12')
    textFont = Font(family = 'Bookman Old Style', size = '15')
    headingFont = Font(family = 'Bookman Old Style', size = '30')

    formula = Image.open("edit-distance/img/edit-distance-formula.png")
    #formula = formula.resize((450, 77), Image.ANTIALIAS)
    formula = formula.resize((500, 128), Image.ANTIALIAS)
    formula = ImageTk.PhotoImage(formula)

    back_table = Image.open("edit-distance/img/edit-distance-square.png")
    back_table = back_table.resize((600, 300), Image.ANTIALIAS)
    back_table = ImageTk.PhotoImage(back_table)

    inputScreen()
    
    root.mainloop()
