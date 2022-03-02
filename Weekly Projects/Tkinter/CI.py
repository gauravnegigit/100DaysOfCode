
from tkinter import *

def clear():
    principle_field.delete(0 , END)
    rate_field.delete(0 , END)
    time_field.delete(0 , END)
    compound_field.delete(0 , END)

    principle_field.focus_set()

def calculate():
    try :
        principle = int(principle_field.get())
        rate = float(rate_field.get())
        time = int(time_field.get())

        CI = principle * (pow((1 + rate/100) , time))

        # if the compound field is empty then only we need to fill it 
        '''There may be a case when the user may hit the submit button more than one time'''
        if not compound_field.get() :
            compound_field.insert(10 , CI)
    
    except :
        pass 

if __name__ == "__main__":
    root = Tk()
    root.configure(background= "light green" )
    root.geometry("500x500")
    root.title("COMPOUND INTEREST CALCULATOR")

    label1 = Label(root , text = "Principal Amount (Rs) :" , fg ="black" , bg = "red" , activebackground= "yellow")
    label2 = Label(root , text = "Rate(%) : " , fg = "black" , bg = "red" , activebackground= "yellow")

    label3 = Label(root, text = "Time(years) : ",
                   fg = 'black', bg = 'red' , activebackground= "yellow")
 
    # Create a Compound Interest : label
    label4 = Label(root, text = "Compound Interest : ",
                   fg = 'black', bg = 'red' , activebackground= "yellow")
    
    label1.grid(row = 1, column = 0, padx = 10, pady = 10) 
    label2.grid(row = 2, column = 0, padx = 10, pady = 10) 
    label3.grid(row = 3, column = 0, padx = 10, pady = 10)
    label4.grid(row = 5, column = 0, padx = 10, pady = 10)


    principle_field = Entry(root)
    rate_field = Entry(root)
    time_field = Entry(root)
    compound_field = Entry(root)

    #setting up teh grid 
    principle_field.grid(row = 1, column = 1, padx = 10, pady = 10) 
    rate_field.grid(row = 2, column = 1, padx = 10, pady = 10) 
    time_field.grid(row = 3, column = 1, padx = 10, pady = 10)
    compound_field.grid(row = 5, column = 1, padx = 10, pady = 10)

    button1 = Button(root, text = "Submit", bg = "red", 
                     fg = "black", command = calculate)
   
    # Create a Clear Button and attached 
    # to clear_all function 
    button2 = Button(root, text = "Clear", bg = "red", 
                     fg = "black", command = clear)
   
    button1.grid(row = 4, column = 1, pady = 10)
    button2.grid(row = 6, column = 1, pady = 10)
 
    # Start the GUI 
    root.mainloop()