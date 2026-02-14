from tkinter import *
from tkinter import filedialog
import sys
import os
import BatterStats as bs
import CatcherStats as cs
global filestring
filestring = ""
root = Tk()

def genBatters():
    if filestring=="":
        csvNameTextField.delete(0,END)
        csvNameTextField.insert(0,"ERROR: FILENAME NOT DEFINED OR FOUND. ENTER FILE NAME TO IMPORT HERE")
        return
    print(filestring)
    bs.genStats(filestring,outputNameTextField.get()+"_batters.pdf")

def genCatchers():
    if filestring=="":
        csvNameTextField.delete(0,END)
        csvNameTextField.insert(0,"ERROR: FILENAME NOT DEFINED OR FOUND. ENTER FILE NAME TO IMPORT HERE")
        return
    print(filestring)
    cs.genStats(filestring,outputNameTextField.get()+"_catchers.pdf")


def changeInputName():
    global filestring
    filestring = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select CSV File",filetypes=[("CSV FILES",".csv")])
    csvNameTextField.delete(0,END)
    csvNameTextField.insert(0,filestring)
    #filestring = csvNameTextField.get()
    print("Is now",filestring)


myLabel = Label(root,text="University of Houston Baseball Stats Generator",font=("Arial",25))
myLabel2 = Label(root,text="2026 - Sammy Tawakkol - github.com/strakerak",font=("Arial",10))
myLabel3 = Label(root,text = "Enter output name below, will autmatically generate to  name_batters.pdf and name_catchers.pdf",font=("Arial",14))

outputNameTextField = Entry(root,width=100)
outputNameTextField.insert(0,"Enter output name here")

csvNameTextField = Entry(root,width=100)
csvNameTextField.insert(0,"Enter full CSV name here")

batterButton = Button(root,text="Generate Batter Report",command=genBatters)
catcherButton = Button(root,text="Generate Catcher Report",command=genCatchers)
changeButton = Button(root,text="Select CSV File",command=changeInputName)
quitButton = Button(root,text="QUIT PROGRAM",command=root.quit)

myLabel.grid(row=0,column=0)
batterButton.grid(row=2,column=0,padx=150)
catcherButton.grid(row=3,column=0,padx=150)
changeButton.grid(row=4,column=0,padx=150)
csvNameTextField.grid(row=5,column=0)
myLabel3.grid(row=6,column=0,padx=150)
outputNameTextField.grid(row=7,column=0)
myLabel2.grid(row=8,column=0)
quitButton.grid(row=9,column=0,padx=150)

root.title("UH Baseball Stat Generator")
root.mainloop()
#if __name__=="__main__":
#    filestring = sys.argv[1]
#    battername = sys.argv[2] + ".pdf"
#    catchername = sys.argv[3] + ".pdf"
#    bs.genStats(filestring,battername,catchername)


#batterButton.bind('<Button-1>',genBatters)
#catcherButton.bind('<Button-2>',genCatchers)
#changeButton.bind('<Button-3>',changeName(filestring))
