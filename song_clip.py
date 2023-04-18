notes = '''
100 or nun by kenny mason

1:54 to 2:30 needs to be skipped
'''

from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk
import pygame
import os
from pydub import AudioSegment

root = Tk()
root.title("chandlys music player")
root.geometry("1000x600")


pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
current_song = ""
paused = False
length = -1

songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

cwd = os.getcwd()
root.directory = cwd + '/songs/'
for song in os.listdir(root.directory):
  name, ext = os.path.splitext(song)
  if ext == '.mp3':
      songs.append(song)
for song in songs:
  songlist.insert("end", song)
  songlist.selection_set(0)
  current_song = songs[songlist.curselection()[0]]


# FUNCTIONS
def load_music():
  global current_song
  root.directory = filedialog.askdirectory()

  for song in os.listdir(root.directory):
    name, ext = os.path.splitext(song)
    if ext == '.mp3' and not song in songs:
      songs.append(song)
  for song in songs:
    print(song)
    songlist.insert("end", song)
  songlist.selection_set(0)
  current_song = songs[songlist.curselection()[0]]

def play_music():
  global current_song, paused, length

  if not paused:
    print(os.path.join(root.directory, current_song))
    pygame.mixer.music.load(os.path.join(root.directory, current_song))
    pygame.mixer.music.play()
    sound_len = pygame.mixer.Sound(os.path.join(root.directory, current_song))

    print(sound_len.get_length())
    length = sound_len.get_length()
  else:
    pygame.mixer.music.unpause()
    paused = False

def pause_music():
  global pause
  pygame.mixer.music.pause()
  paused = True

def next_music():
  global current_song, paused

  try:
    songlist.selection_clear(0, END)
    songlist.selection_set(songs.index(current_song) + 1)
    current_song = songs[songlist.curselection()[0]]
    play_music()
  except:
    pass

def prev_music():
  global current_song, paused

  try:
    songlist.select_clear(0, END)
    songlist.selection_set(songs.index(current_song) - 1)
    current_song = songs[songlist.curselection()[0]]
    play_music()
  except:
    pass
  songlist.selection_set(0)
  current_song = songs[songlist.curselection()[0]]

#cutting a song example


def cut_song():
  global current_song

  frame = Frame(root)
  frame.pack()
  label_one = Label(frame, text="start time")
  entry_one = Entry(frame)

  label_two = Label(frame, text="end time")
  entry_two = Entry(frame)

  label_one.grid(row=0, column=0)
  entry_one.grid(row=1, column=0)
  label_two.grid(row=2, column=0)
  entry_two.grid(row=3, column=0)


  def get_times():
    start = entry_one.get()
    print(start)
    end = entry_two.get()
    print(end)

    if start and end:
      split = start.split(':')
      start_min = split[0]
      start_sec = split[1]
      print(start_sec)
      print(start_min)

      split = end.split(':')
      end_min = split[0]
      end_sec = split[1]
      print(end_min)
      print(end_sec)

      print(os.path.join(root.directory, current_song))
      song = AudioSegment.from_file(os.path.join(root.directory, current_song))

      start_mill = ((int(start_min) * 60) * 1000 + int(start_sec) * 1000)
      print(start_mill)
      end_mill = ((int(end_min) * 60) * 1000 + int(end_sec) * 1000 )
      print(end_mill)

      new_song = song[:start_mill] + song[end_mill:]
      new_song.export('test.mp3',format= 'mp3')
    elif start:
      split = start.split(':')
      start_min = split[0]
      start_sec = split[1]
      song = AudioSegment.from_file(os.path.join(root.directory, current_song))
      start_mill = ((int(start_min) * 60) * 1000 + int(start_sec) * 1000)
      new_song = song[start_mill:]
      new_song.export('test.mp3',format= 'mp3')
    else:
      split = end.split(':')
      end_min = split[0]
      end_sec = split[1]
      song = AudioSegment.from_file(os.path.join(root.directory, current_song))
      end_mill = ((int(start_min) * 60) * 1000 + int(start_sec) * 1000)
      new_song = song[:end_mill]
      new_song.export('test.mp3',format= 'mp3')
  button = Button(frame, text="submit", command=get_times)
  button.grid(row=4, column=0)

def create_playlist():
  pass


organize_menu = Menu(menubar)
organize_menu.add_command(label='select folder', command=load_music)
organize_menu.add_command(label='create playlist', command=create_playlist)
menubar.add_cascade(label="organize", menu=organize_menu)



# Setting pngs to photo image objects
play_img = Image.open("icons/play-button-round-icon.png")
play_img = play_img.resize((30, 30))
play_image = ImageTk.PhotoImage(play_img)
pause_img = Image.open("icons/pause-button-round-icon.png")
pause_img = pause_img.resize((30, 30))
pause_image = ImageTk.PhotoImage(pause_img)
next_img = Image.open("icons/next-icon.png")
next_img = next_img.resize((30, 30))
next_image = ImageTk.PhotoImage(next_img)
prev_img = Image.open("icons/previous-icon.png")
prev_img = prev_img.resize((30, 30))
prev_image = ImageTk.PhotoImage(prev_img)
cut_img = Image.open("icons/cut.png")
cut_img = cut_img.resize((30, 30))
cut_image = ImageTk.PhotoImage(cut_img)


control_frame = Frame(root)
control_frame.pack()

# assigning images to buttons and assigning them to control frame div type object
play_btn = Button(control_frame, image=play_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_image, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_image, borderwidth=0, command=prev_music)
cut_btn = Button(control_frame,image=cut_image, borderwidth=0, command=cut_song)

# placing them within the controlframe
play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)
cut_btn.grid(row=0, column=4, padx=7, pady=10)

root.mainloop()