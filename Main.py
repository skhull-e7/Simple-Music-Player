from tkinter import Tk, Label, Frame, Button, LEFT, Scrollbar, END, TOP, NONE, BOTH, CENTER, FLAT, YES, Y, W, NO, Listbox
from tkinter.font import BOLD
import os, pygame, random
from tkinter.filedialog import askdirectory

def playSong(event=None, songToPlay=None):
    try:
        if event != None:
            songToPlay = songList_[event.widget.curselection()[0]]
        pygame.mixer.music.unload()
        pygame.mixer.music.load(os.path.join(file_, songToPlay))
        pygame.mixer.music.play()
        songNamePlaying.config(text=songToPlay[:-4])
        root.title(songToPlay[:-4]+'  - Sky Dive Music Player')
        playButton.button.config(text='\u23f8', command=pauseSong)
        addKeyboardCommands()
    except:
        pass

def playPrevSong(evnt=None):
    try:
        if songNamePlaying['text'] == 'None Playing':
            playSong(songToPlay=songList_[-1])
            return
        songPlaying = songNamePlaying['text']+'.mp3'
        songPlayingIndex = songList_.index(songPlaying)
        if pygame.mixer.music.get_pos()/1000 > 10.0:
            playSong(songToPlay=songPlaying)
            return
        if shuffleButton['fg'] == 'white' and repeatButton.button['text'] == '🔁':
            songToPlay = random.choice(songList_)
            playSong(songToPlay=songToPlay)
        elif repeatButton.button['text'] == '🔂':
            playSong(songToPlay=songPlaying)
        else:
            if shuffleButton['fg'] == 'white':
                songToPlay = random.choice(songList_)
                playSong(songToPlay=songToPlay)
            else:
                playSong(songToPlay=songList_[songPlayingIndex-1])
    except:
        pass

def playNextSong(evnt=None):
    try:
        if songNamePlaying['text'] == 'None Playing':
            playSong(songToPlay=songList_[0])
            return
        songPlaying = songNamePlaying['text']+'.mp3'
        songPlayingIndex = songList_.index(songPlaying)
        if shuffleButton['fg'] == 'white' and repeatButton.button['text'] == '🔁':
            songToPlay = random.choice(songList_)
            playSong(songToPlay=songToPlay)
        elif repeatButton.button['text'] == '🔂':
            playSong(songToPlay=songPlaying)
        else:
            try:
                playSong(songToPlay=songList_[songPlayingIndex+1])
            except:
                playSong(songToPlay=songList_[0])
    except:
        pass

def pauseSong(evnt=None):
    if playButton.button['text'] == '\u23f8':
        pygame.mixer.music.pause()
        playButton.button.config(text='\u25b6')
    else:
        pygame.mixer.music.unpause()
        playButton.button.config(text='\u23f8')

def checkSong():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            playNextSong()
    root.after(100, checkSong)

def changeShuffle(evnt=None):
    if shuffleButton['fg'] == '#53acb0':
        shuffleButton.config(fg='white')
    else:
        shuffleButton.config(fg='#53acb0')

def changeRepeat(evnt=None):
    if repeatButton.button['text'] == "🔁":
        repeatButton.button.config(text="🔂")
    else:
        repeatButton.button.config(text="🔁")

def changeDir():
    global file_, songList_
    newDir = askdirectory()
    if newDir == '':
        return
    else:
        file_ = newDir
        songList_ = os.listdir(file_)
        songList_ = [song for song in songList_ if song[-4:] == '.mp3']
        songList.delete(0, END)
        for song in songList_:
            songList.insert(END, song[:-4])
        songNumbers.config(text=f'{len(songList_)} Songs', font=('Segoe Script', 19, BOLD))

def addKeyboardCommands():
    songList.bind('<Up>', NONE)
    songList.bind('<Down>', NONE)
    songList.bind('<space>', NONE)
    root.bind('<Tab>', NONE)
    root.bind('<Left>', playPrevSong)
    root.bind('<Right>', playNextSong)
    for frame in root.winfo_children():
        frame.bind('<Left>', playPrevSong)
        frame.bind('<Right>', playNextSong)
        for wid in frame.winfo_children():
            wid.bind('<Left>', playPrevSong)
            wid.bind('<Right>', playNextSong)
    root.bind('<s>', changeShuffle)
    root.bind('<a>', changeRepeat)

class musicPlayerButton():
    """Styled Button for this Music Player
    -> the button will change colour if mouse pointer
    -> is above the button."""

    def __init__(self, master=NONE, text='0', command=None, bg='#10111b', fg='white', relief=FLAT, font='consolas 23 bold', bd=0, side=LEFT, expand=YES, fill=BOTH, anchor=CENTER, padx=0, pady=0, ab='white', af='black', entercolbg='grey', entercolfg='yellow'):
        self.entercolbg, self.entercolfg = entercolbg, entercolfg
        self.bg = bg
        self.fg = fg
        self.button = Button(master, text=text, font=font,
                             relief=relief, bg=bg, fg=fg, command=command, bd=bd, activebackground=ab, activeforeground=af)
        self.button.pack(side=side, anchor=anchor, expand=expand, fill=fill, padx=padx, pady=pady)
        self.button.bind('<Enter>', self.focusButton)
        self.button.bind('<Leave>', self.focusButton)

    def focusButton(self, event=None):
        """Changes Colour if mouse pointers hover above the button"""
        event = str(event)[1:6]
        if event == 'Enter':
            self.button.config(bg=self.entercolbg, fg=self.entercolfg)
        else:
            self.button.config(bg=self.bg, fg=self.fg)

root = Tk()
pygame.init()
root.geometry('550x450+250+220')
root.minsize(550, 450)
# root.resizable(False, False)
root.title('Sky Dive Music Player')
#root.wm_iconbitmap(r'./icon.ico')
root.config(bg='#10111b')

titleBar = Frame(root, bg='#10111b')
songListBar = Frame(root, bg='#10111b')
songPlayBar = Frame(root, bg='#10111b')
titleBar.pack(fill=BOTH)
songListBar.pack(fill=BOTH, expand=YES)
songPlayBar.pack(fill=BOTH, pady=5)

# Title Bar :
songNumbers = Label(titleBar, text='Choose Directory ->', font=('Consolas', 19), fg='White', bg='#10111b')
songNumbers.pack(side=LEFT, expand=YES, anchor=CENTER)
fileButton = musicPlayerButton(titleBar, fg='yellow', entercolfg='yellow', entercolbg='red', text='📁', expand=NO, fill=NONE, anchor=CENTER, command=changeDir)

# Song List Bar : 
songList = Listbox(songListBar, font=('Consolas', 16), activestyle=NONE, bg='#10111b', fg='white', bd=0, selectborderwidth=0, selectforeground='white', selectbackground='#10111b', highlightthickness=0)
songListScroll = Scrollbar(songListBar, bd=0, command=songList.yview)
songList.config(yscrollcommand=songListScroll.set)
songList.pack(side=LEFT, fill=BOTH, expand=YES, anchor=CENTER, padx=10, pady=10)
songListScroll.pack(side=LEFT, fill=Y, pady=10)


# Song Play Bar :
songNamePlaying = Label(songPlayBar, text='None Playing', bg='#10111b', fg='grey', font=('Courier New', 19, BOLD), anchor=W)
songNamePlaying.pack(side=TOP, anchor=CENTER, fill=Y, padx=10, expand=YES)
shuffleButton = Button(songPlayBar, text='🔀', bg='#10111b', fg='#53acb0', relief=FLAT, activeforeground='#53acb0', activebackground='white', command=changeShuffle, bd=0, font=('consolas', 35))
shuffleButton.pack(expand=YES, fill=NONE, anchor=CENTER, side=LEFT)
playPrevButton = musicPlayerButton(songPlayBar, text='\u23ee', entercolfg='black', expand=YES, fill=NONE, fg='#53acb0', font=('consolas', 31, BOLD), af='#53acb0', command=playPrevSong)
playButton = musicPlayerButton(songPlayBar, text='\u25b6', entercolfg='black', expand=YES, fill=NONE, fg='#53acb0', font=('consolas', 31, BOLD), af='#53acb0', command=playNextSong)
playNextButton = musicPlayerButton(songPlayBar, text='\u23ed', entercolfg='black', expand=YES, fill=NONE, fg='#53acb0', font=('consolas', 31, BOLD), af='#53acb0', command=playNextSong)
repeatButton = musicPlayerButton(songPlayBar, text='🔁', entercolfg='black', expand=YES, fill=NONE, fg='#53acb0', font=('consolas', 35), af='#53acb0', command=changeRepeat)


MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

root.bind('<<ListboxSelect>>', playSong)
shuffleButton.bind('<Enter>', lambda x: shuffleButton.config(bg='grey'))
shuffleButton.bind('<Leave>', lambda x: shuffleButton.config(bg='#10111b'))
songList.bind('<Left>', NONE)
songList.bind('<Right>', NONE)

checkSong()

root.mainloop(), NONE
