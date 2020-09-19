from tkinter import *
from tkinter.font import Font
import numpy as np

def getInput(str1, str2):
    s1 = str1.get()
    s2 = str2.get()
    if s1 == '' or s2 == '' or not(s1.isalpha()) or not(s2.isalpha()):
        screenError = Toplevel(root)
        screenError.geometry("250x90")
        screenError.title("Warning!")
        Label(screenError, text = "Please enter both strings").pack()
        Button(screenError, text = "OK", command = screenError.destroy).pack()
    else:
        tableCreate(s1, s2)

def inputScreen():
    ## Setting Background
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)
    
    ## Creating text and input boxes
    background.create_text(w/2 - 200, h/2 - 250, text = "Enter first String: ", font = textFont)
    str1 = Entry(background)
    background.create_window(w/2 + 100, h/2 - 250, window = str1, width = w/4)

    background.create_text(w/2 - 200, h/2 - 150, text = "Enter second String: ", font = textFont)
    str2 = Entry(background)
    background.create_window(w/2 + 100, h/2 - 150, window = str2, width = w/4)
    
    ## Button for input
    b1 = Button(background, text = "Enter", bg = '#84A3FF', activebackground = '#FFE5CC', command=lambda:getInput(str1, str2))
    background.create_window(w/2, h/2, window = b1, width = w/8)


def tableCreate(s1, s2):
    print(s1, s2)
    background = Canvas(root, bg = "#DEF9FF", width = w, height = h)
    background.grid(row=0, column=0)

    box_width = 50
    box_height = 50
    box_gap = 10
    table_width = len(s1) + 2
    table_height = len(s2) + 2

    ## Creating the Table
    for i in range(table_width):
        for j in range(table_height):
            if (i,j) == (0,0) or (i,j) == (1,0) or (i,j) == (0,1):
                continue
            else:
                x = (box_gap + box_height)*i + 100
                y = (box_gap + box_width)*j + 100
                background.create_rectangle(x, y, x + box_height, y + box_width, fill = '#9fe9fa', outline = "")

    ## Writing the String Values
    ## String1
    for i in range(table_width-2):
        x = (box_gap + box_height)*(i+2) + 100 + box_height/2
        background.create_text(x, 100 + box_width/2, text = s1[i].upper(), font = textFont)

    ## String2
    for i in range(table_height-2):
        y = (box_gap + box_width)*(i+2) + 100 + box_width/2
        background.create_text(100 + box_height/2, y, text = s2[i].upper(), font = textFont)

if __name__ == "__main__":
    root = Tk()

    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d+50+30" % (w, h+80))
    root.title("Edit Distance")
    textFont = Font(family = 'Bookman Old Style', size = '15')
    
    inputScreen()
    
    root.mainloop()
