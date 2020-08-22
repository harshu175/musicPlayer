import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer
from PIL import ImageTk, Image

root = tk.ThemedTk()
root.attributes('-fullscreen',True)
root.title("windows application")

load=Image.open('mpbg.jpg')
render=ImageTk.PhotoImage(load)
img=Label(root,image=render)
root.attributes('-alpha',1.0)

img.place(x=0,y=0)

topframe=Frame(root,width=1500,height=200,bg="blue",relief="raise",bd=10)
topframe.pack(side=TOP)

lb=Label(topframe,text="dJ BeAt BoX",font=('algerian',40,'bold'),width=42,fg='white',bg='black',bd=4,relief='raised')
lb.grid(row=0,column=0)

root.get_themes()                 
root.set_theme("radiance")  

statusbar =Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W,font=('algerian',10,'italic'),fg='white',bg='black')
statusbar.pack(side=TOP, fill=X)

statusbar1 =Label(root, text="MADE BY HARSHIT PANDEY AND SURBHI SOLANI", relief=SUNKEN, anchor=W, font=('algerian',10,'italic'),fg='white',bg='black')
statusbar1.pack(side=BOTTOM, fill=X)

menubar = Menu(root)
root.config(menu=menubar)

subMenu = Menu(menubar, tearoff=0)

playlist = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Melody', ' A project by college student named *Surbhi Solani* and *Harshit Pandey* ')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()  
root.title("Melody")

leftframe = Frame(root,bg='black',bd=20,relief='raised')
leftframe.pack(side=LEFT, padx=30, pady=30)

playlistbox = Listbox(leftframe,bg='pink',bd=5)
playlistbox.pack()

addBtn =Button(leftframe,text='      +Add       ',font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE,command=browse_file)
addBtn.pack(side=LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delBtn =Button(leftframe, text="      - Del      ",font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE,command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root,bg='black',bd=20,relief='raised')
rightframe.pack(pady=30)

topframe = Frame(rightframe,bd=10,bg='black',relief='raised')
topframe.pack()

lengthlabel =Label(topframe, text='Total Length : --:--',font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE)
lengthlabel.pack(pady=5)

currenttimelabel =Label(topframe, text='Current Time : --:--', font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE)
currenttimelabel.pack()

def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'Melody could not find the file. Please check again.')

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    
muted = FALSE


def mute_music():
    global muted
    if muted:  
        mixer.music.set_volume(1.0)
        volumeBtn.configure(text='     mute      ')
        scale.set(100)
        muted = FALSE
    else:  
        mixer.music.set_volume(0)
        volumeBtn.configure(text='    unmute     ')
        scale.set(0)
        muted = TRUE


middleframe = Frame(rightframe,bg='black',bd=10,relief='raised')
middleframe.pack(pady=30, padx=30)

playBtn =Button(middleframe,text='      play     ',font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE, command=play_music)
playBtn.grid(row=0, column=0, padx=10)

stopBtn =Button(middleframe,text='      stop     ', font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE,command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)

pauseBtn =Button(middleframe,text='      pause    ', font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE,command=pause_music)
pauseBtn.grid(row=1, column=1, padx=10)


bottomframe = Frame(rightframe,bg='black',bd=10,relief='raised')
bottomframe.pack()

rewindBtn =Button(bottomframe,text='      rewind     ', font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE,command=rewind_music)
rewindBtn.grid(row=2, column=1)

volumeBtn =Button(bottomframe,text='      mute     ', font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE,command=mute_music)
volumeBtn.grid(row=2, column=2)

scale =Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, font=('times',15,'bold'),bg='black',fg='white',relief=GROOVE,command=set_vol)
scale.set(69)
mixer.music.set_volume(1.0)
scale.grid(row=1, column=1, pady=15, padx=30)


def on_closing():
    stop_music()
    root.destroy()


leftframe3 = Frame(root,bg='black',bd=15,relief='raised')
leftframe3.pack(side=BOTTOM)


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
