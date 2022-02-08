import socket
from _thread import *
from game import *
import pickle

server = "Your IPv4 address"
port = 5555

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

try :
    s.bind((server , port))
except socket.error as e :
    str(e)

s.listen(2)
print("WAITING FOR CONNECTIONS , SERVER STARTED !")


    #initializing ball variables


ball = Ball(ball_x , ball_y , RADIUS , (0 , 0 , 255))

# game variables
games = {}
idCount = 0

# using threading
def threaded_client(conn , player , gameId):
    
    global idCount 

    if gameId in games :

        # it may seem to be complicated
        conn.send(pickle.dumps((games[gameId].players[player] , games[gameId].ball)))
    
    reply = ""

    while True :
        try :
            data = pickle.loads(conn.recv(8192))

            if data != "get" :
                games[gameId].players[player] , games[gameId].ball = data

            if gameId in games :
                game = games[gameId]
                if not data :
                    print("Disconnected ....")
                    break
                else :
                    if data == "get":
                        conn.send(pickle.dumps(games[gameId]))
                    else :    
                        if player == 1:
                            reply = game.players[0]
                        else :
                            reply = game.players[1]

                        conn.sendall(pickle.dumps((reply , game.ball)) )
            
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
