from tkinter import *
from tkinter import filedialog 

def browseFiles() :
    filename = filedialog.askopenfilename(initialdir = "/" , title = "Select a file" , filetypes = (("Text file" , "*.txt") , ("all files" , "*.*")))

    label.config(text = "File opened : " + filename)

    with open(filename  , "a+") as f :
        print(f.read())

        run = input('\n\nDo you want to manipulate the text ? (ENTER YES OR NO)')

        while run.lower() == "yes" :
            data = input("\nEnter some text : ")
            f.write(data)
            run = input('\n\nDo you want to enter some more text ? (ENTER YES OR NO ) ')


    
# main gui logic 
root = Tk()
root.title("File Explorer")
root.geometry('600x600')
root.config(background= "light blue")

label = Label(root , text = "File Explorer using Tkinter in Python" , width = 45 , height = 4 , fg = "Blue" , font = ("Arial Black" , 15))

button_browse = Button(root , text = "Browse" , font = ("comicsans" , 12) ,command = browseFiles)
browse_exit = Button(root , text = "Exit" , font = ("comicsans" , 12) , command = exit)

label.grid(column = 1 , row = 1)
button_browse.grid(column = 1, row = 2)
browse_exit.grid(column = 1, row = 3)

root.mainloop()