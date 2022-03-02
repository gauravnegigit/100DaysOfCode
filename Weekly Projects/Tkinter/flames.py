
from tkinter import *


def remove_matches(list1 , list2):
    for i in list1 :
        for j in list2 :
            if i == j :
                c = i 
                
                list1.remove(c)
                list2.remove(c)

                list3 = list1 + ["*"] + list2
                return [list3 , True]
    
    list3 = list1 + ["*"] + list2 
    return [list3 , False]

def tell_status():
    p1 = player1_field.get()
    p1 = p1.lower()
    p1.replace(" " , "")

    p2 = player2_field.get()
    p2 = p2.lower()
    p2.replace(" " , "")

    p1_list = list(p1)
    p2_list = list(p2)

    run = True 
    while run :
        ret_list = remove_matches(p1_list , p2_list)
        con_list = ret_list[0]
        run = ret_list[1]
        start_index = con_list.index("*")

        p1_list = con_list[: start_index]
        p2_list = con_list[start_index + 1 : ]
    # print(p1_list , p2_list)
    
    count = len(p1_list) + len(p2_list)
    result = ["Friends" , "Love"  , "Affection" , "Marriage" , "Enemy" , "Siblings"]


    while len(result) > 1 :
        split_index = (count % len(result) - 1)

        if split_index >= 0 :
            right = result[split_index + 1 : ]
            left = result[:split_index]
            result = right + left 
        else :
            result = result[: len(result) - 1]

    answer.set(result[0])

def clear():
    player1_field.delete(0 , END)
    player2_field.delete(0 , END)
    status_field.delete(0 , END)

    player1_field.focus_set()


# main driver's code
if __name__ == "__main__":
    root = Tk()

    # main Tkinter GUI logic
    root.configure(background = "light green")
    root.geometry("500x500")
    root.title("PYTHON FLAMES")

    label1 = Label(root , text = "Player 1 Name : " , fg = "black" , bg = "dark green")
    label2 = Label(root , text = "Player 2 Name : " , fg = "black" , bg = "dark green")

    # creating teh label for teh status
    label3 = Label(root , text = "Relationship status : " , fg = "black" , bg = 'red')

    # creating the grid for teh text 
    label1.grid(row = 1, column = 0, sticky ="E") 
    label2.grid(row = 2, column = 0, sticky ="E") 
    label3.grid(row = 5, column = 0, sticky ="E")

    # creating entries for teh game
    player1_field = Entry(root)
    player2_field = Entry(root)

    answer = StringVar()
    status_field = Entry(root , textvariable = answer)


    player1_field.grid(row = 1, column = 1 , ipadx = "100")
    player2_field.grid(row = 2, column = 1 , ipadx = "100")
    status_field.grid(row = 5, column = 1 , ipadx = "100")

    # creating buttons
    button1 = Button(root , text = "Submit" , bg = "red" , fg = "black" , command = tell_status , activebackground= "yellow" )
    button2 = Button(root , text = "clear" , bg ="red" , fg = "black" , command = clear , activebackground= "yellow")

    # griding the buttons
    button1.grid(row = 7 , column = 1)
    button2.grid(row = 10 , column = 1)


    root.mainloop()