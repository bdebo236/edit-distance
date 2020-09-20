from tkinter import *
from tkinter.font import Font
import numpy as np

def getInput(str1, str2):
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
    table = np.zeros([len(s1)+1, len(s2)+1], dtype=int)

    for i in range(len(s1)+1):
        table[i,0] = i

    for j in range(len(s2)+1):
        table[0,j] = j

    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                table[i, j] = table[i-1, j-1]
            else:
                table[i, j] = min(table[i-1, j-1], table[i-1, j], table[i, j-1]) + 1
    
    return table


def inputScreen():
    ## Setting Background
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)
    ## Heading
    background.create_text(w/2, h/2 - 300, text = "Edit Distance", font = headingFont)

    ## Creating text and input boxes
    background.create_text(w/2 - 325, h/2 - 200, text = "Enter the original string: ", font = textFont)
    str1 = Entry(background)
    background.create_window(w/2 + 120, h/2 - 200, window = str1, width = w/4)

    background.create_text(w/2 - 250, h/2 - 100, text = "Enter the string you want to change: ", font = textFont)
    str2 = Entry(background)
    background.create_window(w/2 + 120, h/2 - 100, window = str2, width = w/4)
    
    ## Button for input
    b1 = Button(background, text = "Enter", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:getInput(str1, str2))
    background.create_window(w/2, h/2, window = b1, width = w/8)

def tableCreate(s1, s2):
    #print('tableCreate()', s1, s2)
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)

    box_size = 50
    box_gap = 10
    table_width = len(s1) + 2
    table_height = len(s2) + 2
    padding = 50

    ## Creating the Table
    for i in range(table_height):
        for j in range(table_width):
            if (i,j) == (0,0) or (i,j) == (1,0) or (i,j) == (0,1):
                continue
            else:
                x = (box_gap + box_size)*j + padding
                y = (box_gap + box_size)*i + padding
                background.create_rectangle(x, y, x + box_size, y + box_size, fill = '#9fe9fa', outline = "")

    ## Writing the String Values
    ## To Change String
    for i in range(table_width-2):
        x = (box_gap + box_size)*(i+2) + padding + box_size/2
        background.create_text(x, padding + box_size/2, text = s1[i].upper(), font = textFont)

    ## Orig String
    for i in range(table_height-2):
        y = (box_gap + box_size)*(i+2) + padding + box_size/2
        background.create_text(padding + box_size/2, y, text = s2[i].upper(), font = textFont)

    dpTable = calcDpTable(s1, s2)
    #print(dpTable)

    ## Putting numbers in the table
    for i in range(table_width-1):
        for j in range(table_height-1):
            x = (box_gap + box_size)*(i+1) + padding + box_size/2
            y = (box_gap + box_size)*(j+1) + padding + box_size/2
            cell = dpTable[i,j]
            background.create_text(x, y, text = cell, font = textFont)



    background.create_text(w/2 + 250, h/2 - 200, text = "Total Changes Needed: " + str(dpTable[table_width-2, table_height-2]), font = textFont)


if __name__ == "__main__":
    root = Tk()

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d" % (w, h))
    root.title("Edit Distance")
    textFont = Font(family = 'Bookman Old Style', size = '15')
    headingFont = Font(family = 'Bookman Old Style', size = '30')
    inputScreen()
    
    root.mainloop()
