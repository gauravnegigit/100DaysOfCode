from tkinter import *
from tkinter import messagebox , filedialog

from pytube import YouTube

def Widgets() :
    label = Label(root , text = "YOUTUBE VIDEO DOWNLOADER USING TKINTER " , width = -20 , padx = 15 , pady = 15 , font = ("Arial Black" , 15) , bg = "light blue" , fg = "red")
    label.grid(row = 1 , column = 1 , pady = 10 , padx = 5 , columnspan = 3)
    link_label = Label(root , text = "Youtube link : " , bg = "salmon" , pady = 5 , padx = 5)
    link_label.grid(row = 3 , column = 0 , pady = 5 , padx = 5)

    root.linkTest = Entry(root , width = 35 , textvariable=video_link , font = "Arial 14")
    root.linkTest.grid(row = 3 , column = 2 , pady = 5, padx = 5, columnspan = 2)
    destination_label = Label(root , text = "Destination : "  , bg = "salmon" , padx = 5 , pady = 5)

    root.destinationText = Entry(root,
                                 width=27,
                                 textvariable=download_path,
                                 font="Arial 14")
    root.destinationText.grid(row=5,
                              column=2,
                              pady=5,
                              padx=5)

    browse_B = Button(root,
                      text="Browse",
                      command=browse,
                      width=10,
                      bg="bisque",
                      relief=GROOVE)
    browse_B.grid(row=5,
                  column=3,
                  pady=1,
                  padx=1)
 
    Download_B = Button(root,
                        text="Download Video",
                        command=download,
                        width=20,
                        bg="thistle1",
                        pady=10,
                        padx=15,
                        relief=GROOVE,
                        font="Georgia, 13")
    Download_B.grid(row=6,
                    column=1,
                    pady=20,
                    padx=20)

def browse() :
    download_directory = filedialog.askdirectory(initialdir = "YOUR DIRECTORY PATH " , title = "Save Video")

    download_path.set(download_directory)

def download() :
    youtube_link = video_link.get()

    download_folder = download_path.get()
    getVideo = YouTube(youtube_link)

    '''getting all the available streams of the youtube video and slecting the first from the'''
    videoStream = getVideo.streams.first()
    videoStream.download(download_folder)

    # displaying the message
    messagebox.showinfo("SUCCESSFULLY DOWNLOADED AND SAVED IN " + download_folder)

root = Tk()
root.geometry("500x300")
root.title("Youtube Video Downloader ")

root.config(background= "Light green")

# main tkinter GUI logic 
# creating the tkinter Variables
video_link = StringVar()
download_path = StringVar()

# calling the widgets function
Widgets()

root.mainloop()