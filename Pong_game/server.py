import socket
from _thread import *
from Player import Player
from game import Game
from ball import Ball 
import pickle

server = "192.168.1.2"
port = 5555

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

try :
    s.bind((server , port))
except socket.error as e :
    str(e)

s.listen(2)
print("WAITING FOR CONNECTIONS , SERVER STARTED !")

# player variables
WIDTH , HEIGHT = 1000 , 600
paddle_height = 200
paddle_width = 50
color = (0,0,0)


    #initializing ball variables
ball_x , ball_y = WIDTH //2 - 10 , HEIGHT//2 - 10
dx , dy = 5,5
RADIUS = 20

players = [Player(100 , HEIGHT//2 - paddle_height//2 , paddle_width , paddle_height , color) , Player(850 , HEIGHT//2 - paddle_height//2 , paddle_width , paddle_height , color)]
ball = Ball(ball_x , ball_y , RADIUS , (0 , 0 , 255))

# game variables
games = {}
idCount = 0

def threaded_client(conn , player , gameId):
    global idCount , players , ball
    conn.send(pickle.dumps((players[player] , ball)))
    reply = ""

    while True :
        try :
            data = pickle.loads(conn.recv(8192))

            if data != "get" :
                players[player] , ball = data

            if gameId in games :
                if not data :
                    print("Disconnected ....")
                    break
                else :
                    if data == "get":
                        conn.send(pickle.dumps(games[gameId]))
                    else :    
                        if player == 1:
                            reply = players[0]
                        else :
                            reply = players[1]

                        conn.sendall(pickle.dumps((reply , ball)) )
            
            else :
                break

        except :
            break
    
    print("Lost connection ....")

    try :
        games[gameId]
        del games[gameId]
        print("Closing game : " , gameId)
    except :
        pass
    
    players = [Player(100 , HEIGHT//2 - paddle_height//2 , paddle_width , paddle_height , color) , Player(850 , HEIGHT//2 - paddle_height//2 , paddle_width , paddle_height , color)]

    idCount -= 1
    conn.close()

# so that when called by client.py it may not run simultaneously


while True :
    conn , addr = s.accept()
    print("Connected to : " , addr)
    idCount += 1
    p = 0 
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        print("CREATING  A NEW GAME ......")
        games[gameId] = Game(gameId)
    else :
        games[gameId].ready = True 
        p = 1
        
    start_new_thread(threaded_client , (conn , p  , gameId))
