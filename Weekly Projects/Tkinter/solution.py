from tkinter import *
from tokenize import String 

expression = ""

def press(num):
    """function used for presiing numbers"""
    global expression

    expression += str(num)
    equation.set(expression)

def equalpress():
    """function for pressign the equal to sign"""
    try :
        global expression

        total  = str(eval(expression))
        equation.set(total)
        expression = ""

    except :
        equation.set("error")
        expression = ""
    
def clear():
    global expression
    expression = ""
    equation.set("")


# main driver's code
if __name__ == "__main__" :
    root = Tk()
    root.configure(background = "light green")

    root.title("Python calculator")
    root.geometry("500x300")
    
    equation = StringVar()

    expression_field = Entry(root , textvariable = equation)
    expression_field.grid(columnspan = 4 ,  ipadx = 200)

    button = Button(root , text = "1" , fg = "black" , bg = "light blue" , command = lambda : press(1) , height = 2 , width = 16).grid(row = 3 , column = 0)
    button = Button(root , text = "2" , fg = "black" , bg = "light blue" , command = lambda : press(2) , height = 2 , width = 16).grid(row = 3 , column = 1)
    button = Button(root , text = "3" , fg = "black" , bg = "light blue" , command = lambda : press(3) , height = 2 , width = 16).grid(row = 3 , column = 2)
    button = Button(root , text = "4" , fg = "black" , bg = "light blue" , command = lambda : press(4) , height = 2 , width = 16).grid(row = 4 , column = 0)
    button = Button(root , text = "5" , fg = "black" , bg = "light blue" , command = lambda : press(5) , height = 2 , width = 16).grid(row = 4 , column = 1)
    button = Button(root , text = "6" , fg = "black" , bg = "light blue" , command = lambda : press(6) , height = 2 , width = 16).grid(row = 4 , column = 2)
    button = Button(root , text = "7" , fg = "black" , bg = "light blue" , command = lambda : press(7) , height = 2 , width = 16).grid(row = 5 , column = 0)
    button = Button(root , text = "8" , fg = "black" , bg = "light blue" , command = lambda : press(8) , height = 2 , width = 16).grid(row = 5 , column = 1)
    button = Button(root , text = "9" , fg = "black" , bg = "light blue" , command = lambda : press(9) , height = 2 , width = 16).grid(row = 5 , column = 2)
    button = Button(root , text = "0" , fg = "black" , bg = "light blue" , command = lambda : press(0) , height = 2 , width = 16).grid(row = 6 , column = 0)

    plus = Button(root, text=' + ', fg='black', bg='red',
                command=lambda: press("+"), height=2, width = 16)
    plus.grid(row=3, column=3)
 
    minus = Button(root, text=' - ', fg='black', bg='red',
                command=lambda: press("-"), height=2, width=16)
    minus.grid(row=4, column=3)
 
    multiply = Button(root, text=' * ', fg='black', bg='red',
                    command=lambda: press("*"), height=2, width=16)
    multiply.grid(row=5, column=3)
 
    divide = Button(root, text=' / ', fg='black', bg='red',
                    command=lambda: press("/"), height=2, width=16)
    divide.grid(row=6, column=3)
 
    equal = Button(root, text=' = ', fg='black', bg='red',
                command=equalpress, height=2, width=16)
    equal.grid(row=6, column=2)

    clear = Button(root, text='Clear', fg='black', bg='red',
                command=clear, height=2, width=16)
    clear.grid(row=6, column='1')

    Decimal= Button(root ,text='.', fg='black', bg='red',
                    command=lambda: press('.'), height=2, width=16)
    Decimal.grid(row=7, column=0)

    # start the GUI
    root.mainloop()
