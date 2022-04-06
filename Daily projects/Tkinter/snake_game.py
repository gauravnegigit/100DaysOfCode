from logging import root
from tkinter import * 
import random
from PIL import Image , ImageTk

# main variables and constants 
FPS = 10 
movement = 25
speed = 1100// FPS 

class Snake(Canvas):
    def __init__(self):
        super().__init__(
            width = 700 ,
            height = 700 ,
            background = '#53ff1a' , 
            highlightthickness=0
        )
    
        self.snake_pos = [(100 , 80) , (80 , 100) , (80 , 100)]
        self.food_pos = self.set_new_food_pos()
        self.direction = "Right"
        self.score = 0
        self.load_img()
        self.create_objects()

        self.bind_all('<Key>' , self.on_key_press)
        self.pack()
        self.after(speed , self.perform_actions)
    
    def load_img(self):
        try:
            self.snake_body = ImageTk.PhotoImage(Image.open('game.png'))
            self.food = ImageTk.PhotoImage(Image.open('game.png'))
        except IOError as error:
            root.destroy()
            raise

    def create_objects(self):
        self.create_text(
            35 , 
            12 , 
            text = f'Score : {self.score}' , 
            tag = "score" , 
            fill = "black" , 
            font = 10
        )

        for x , y in self.snake_pos :
            self.create_image(x , y , image = self.snake_body , tag = 'snake')
        
        self.create_image(*self.food_pos , image = self.food , tag = 'food')
        self.create_rectangle(10 , 30 , 690 , 690 , outline = 'white')
    
    def finish_game(self):
        self.delete(ALL)
        self.create_text(self.winfo_width() /2 , self.winfo_height()/2 , text = f'Game Over ! Your current score is {self.score} !' , fill = 'black' , font = ('Arial Black' , 20))
    

    def consume_food(self):
        if abs(self.snake_pos[0][0] - self.food_pos[0]) < 10 and  abs(self.snake_pos[0][1] - self.food_pos[1]) < 10 :
            self.score += 10 
            self.snake_pos.append(self.snake_pos[-1])

            self.create_image(*self.snake_pos[-1] , image = self.snake_body , tag = 'snake')

            self.food_pos = self.set_new_food_pos()
            self.coords(self.find_withtag('food') , *self.food_pos)

            score = self.find_withtag("score")
            self.itemconfigure(score , text = f'Score : {self.score}' , tag = 'score')

    
    def snake_movement(self):
        head_x , head_y = self.snake_pos[0]

        if self.direction == 'Left' :
            new_head_pos = (head_x - movement , head_y)
        
        elif self.direction == 'Right' :
            new_head_pos = (head_x + movement , head_y)
        
        elif self.direction == 'Up' :
            new_head_pos = (head_x , head_y - movement)
        
        elif self.direction == 'Down' :
            new_head_pos = (head_x , head_y + movement)
        
        self.snake_pos = [new_head_pos] + self.snake_pos[:-1]

        for segment, position in zip(self.find_withtag('snake'), self.snake_pos):
            self.coords(segment, position)
    
    def boundary(self):
        head_x , head_y = self.snake_pos[0]
        return (head_x in (0 , 700) or head_y in (20 , 700) or (head_x , head_y) in self.snake_pos[1:])
        

    def on_key_press(self , e):
        new_direction = e.keysym 

        all_directions = (
            'Up', 
            'Down', 
            'Left', 
            'Right'
            )
        opposites = (
            {'Up', 'Down'}, 
            {'Left', 'Right'}
            )

        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction 
        

    def perform_actions(self):
        if self.boundary():
            self.finish_game()

        self.consume_food()
        self.snake_movement()

        self.after(speed, self.perform_actions)      

    
    def set_new_food_pos(self):
        run = True 
        while run :
            food_pos = (random.randint(1 , 29) * movement , random.randint(3 , 30) * movement)
            
            if food_pos not in self.snake_pos :
                return food_pos
        
# initializing the root of the Tkinter interface
root = Tk()
root.title('Snake game ')
root.resizable(False , False)

board = Snake()
root.mainloop()
