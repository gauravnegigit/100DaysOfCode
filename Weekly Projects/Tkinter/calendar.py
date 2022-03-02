from tkinter import *
from calendar import *


def showCal():
    new_root = Tk()
    new_root.configure(background= "light green")
    new_root.title("PYTHON CALENDAR")
    new_root.geometry("600x600")
    fetch_year = int(year_field.get())

    cal_content = calendar(fetch_year)
    
    cal_year = Label(new_root , text =  cal_content , font = "Consolas 10 bold")
    cal_year.grid(row = 5 , column = 1 , padx = 20)
    new_root.mainloop()

# main Driver's code
if __name__ == "__main__":
    root = Tk()
    root.config(background = "white")
    root.title("PYTHON CAALENDAR")
    root.geometry("250x150")
    
    cal = Label(root , text = "CALENDAR" , bg = "dark gray" , font = ("comicsans" , 28 , "bold"))
    year = Label(root , text = "ENTER YEAR" , bg = "light green")
    year_field = Entry(root)
    Show = Button(root , text = "Show Calendar" , fg = "black" , bg = "Red" , command = showCal , activebackground= "yellow")
    Exit = Button(root , text = "Exit" , fg = "black" , bg = "red" , activebackground= "yellow" , command = quit)
    cal.grid(row = 1 , column = 1)
    year.grid(row = 2 , column = 1)
    year_field.grid(row = 3 , column = 1)
    Show.grid(row = 4 , column = 1)
    Exit.grid(row = 6 , column = 1)

    root.mainloop()