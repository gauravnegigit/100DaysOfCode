from tkinter import *
import random

# creating a list of all possible colours 
colours = ['Red' , 'Blue' , 'Green' , 'Pink' , 'Black' , 'Yellow' , 'Orange' , 'White' , 'Purple' , 'Brown']

# game variables
score = 0
timeleft = 30

def main(event) :
    if timeleft == 30 :
        countdown()
    
    nextColour()

def nextColour() :
    global score 
    global timeleft 

    if timeleft > 0 :
        entry.focus_set()

        if entry.get().lower() == colours[1].lower() :
            score += 1
        
        entry.delete(0 , END)
        random.shuffle(colours)

        # now changing the label
        label.config(fg = str(colours[1]) , text = str(colours[random.randint(0 , len(colours) - 1)]))
        scoreLabel.config(text = "Score : " + str(score))

def countdown():
    global timeleft 

    if timeleft > 0 :
        timeleft -= 1
        timeLabel.config(text = "Time left : " + str(timeleft))
        timeLabel.after(1000 , countdown)


# main Driver's code
root = Tk()
root.title("Color game")
root.geometry("400x375")

# main GUI logic starts here 
instructions = Label(root , text = "Type in the color of the words \n and not the word text !" , font = ('Arial Black' , 12))
instructions.pack()

#add a score label
scoreLabel = Label(root , text = "\n\nPress enter to start " , font = ('Arial Black' , 12))
scoreLabel.pack()

# adding the time left label
timeLabel = Label(root , text = "Time left : " + str(timeleft) , font = ("Arial Black" , 12))
timeLabel.pack()

# add a label for displaying teh colours 
label  = Label(root , font = ("Arial Black" , 12))
label.pack()

# adding a textentry box for typing in colours
entry = Entry(root)

root.bind('<Return>' , main)
entry.pack()

# setting the focus on the entry box
entry.focus_set()
root.mainloop()