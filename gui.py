#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import filedialog
from sys import exit

sys.path.append(".")
from functions import *
from doseClass import *
from rootFolderFolderClass import *
from calibrationClass import *
from fitResultsSingleChannel import *

def setBool(): 
    medianFilter.set(True)
    print(medianFilter.get())
    
def selectDirectory():
    global path
    browse = Tk()
    browse.withdraw()
    browse.attributes('-topmost', True)
    path = filedialog.askdirectory(title='select rootFolderFolder folder') + '/'
    info_label['text'] = path
    # browse.mainloop()
    
path = ''
window = Tk()

window.title('CHROMO')
window.geometry("700x700")
window.config(background = "white")
window.resizable(True, True)
# window['background']='#8c52ff'
   
medianFilter = BooleanVar()
medianFilter.set(False)
medianFilter.trace('w', lambda *_: print("The value was changed"))

label_file_explorer = Label(window, text = "File Explorer", width = 100, height = 4, fg = "blue")      
button_explore = Button(window, text = "Browse Files", activebackground='white', command = selectDirectory)
medianFilterButton = Checkbutton(window, text="Median Filter", variable = medianFilter, command=setBool)
info_label = ttk.Label(window, text= path)

label_file_explorer.grid(column = 1, row = 1)
button_explore.grid(column = 1, row = 2)
medianFilterButton.grid()
info_label.grid(column = 1, row = 3)

rootFolderFolder = rootFolderFolderClass(path)
cleanOutputDirectory(rootFolderFolder)
createOutputDirectories(rootFolderFolder)

window.mainloop()


      


    
