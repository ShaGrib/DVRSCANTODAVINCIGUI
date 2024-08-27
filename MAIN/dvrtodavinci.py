import re
import os
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

#app class
class App(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

#VARIABLES
#different fps variables
#fps23 = 24000/1001
#fps24 = 24.000
#fps29 = 30000/1001
#fps30 = 30.000
#fps59 = 60000/1001
#fps60 = 60.000

#fps options for dropdown
fps_choices = [
    24000/1001,
    24.000,
    30000/1001,
    30.000,
    60000/1001,
    60.000
]

#audio video options for dropdown
av_choices = [
    "A   ",
    "B   ",
    "V   ",
    "A2  ",
    "A2/V",
    "AA  ",
    "AA/V",
]

#audio video options for dropdown
fcm_choices = [
    "NON-DROP FRAME",
    "DROP FRAME    "
]

#edit codes
edit_choices = [
    "C   ",
    "D   "
]

#reel codes
reel_choices = [
    "AX  ",
    "BL  "
]

#create the app
myapp = App()

#icon converter
icon = PhotoImage (file='dvrscanbridge.png')
myapp.master.iconphoto(True, icon)

#display and graphics
style = ttk.Style(myapp)
style.theme_use("clam")
myapp.master.title("DVR Scan to Davinci Bridge")
myapp.master.minsize(640, 640)
myapp.master.maxsize(3840, 2160)
frm1 = Frame(myapp).pack()
frm2 = Frame(myapp).pack()
frm3 = Frame(myapp).pack()
frm4 = Frame(myapp).pack()
frm5 = Frame(myapp).pack()
frm6 = Frame(myapp).pack()
frm7 = Frame(myapp).pack()

#source and target fps
source = StringVar()
source.set(str(fps_choices[0]))
#sourcefps = float(source.get())
target = StringVar()
target.set(str(fps_choices[0]))
#targetfps = float(target.get())

#title setter/getter
titletext = StringVar()
titletext.set("Timeline")
title = titletext.get()

#fcm setter/getter
fcmtext = StringVar()
fcmtext.set(fcm_choices[0])
fcm = fcmtext.get()

#reel setter/getter
reeltext = StringVar()
reeltext.set("AX  ")
reel = reeltext.get()

#audio/video setter/getter
avtext = StringVar()
avtext.set(av_choices[2])
av = avtext.get()

#edit statement setter/getter (4 char)
edittext = StringVar()
edittext.set(edit_choices[0])
edit = edittext.get()

#created file name variable
#edl = "eventguitest.edl"

#time to add to recorded time
addtime = "01:00:00:00"

#get the location of python script location
scriptloc = os.path.dirname(os.path.realpath(__file__))

#get file save location
saveloc = scriptloc

#get current working directory
currentloc = os.getcwd()

#FUNCTIONS
#open log file
def openlogfile():
    return askopenfilename(filetypes=[("text files", "*.txt")] , initialdir= scriptloc, title= "DVR Scan log selection")

#take the time and convert it to frames so it can have math operations performed on it
def timecodetoframes(value, fps):
    value = value.replace(".",":")
    return round(sum((frames * float(time) for frames, time in zip((3600 * fps, 60 * fps, fps, 1), value.split(":")))))

#take frames and convert to time of source or selected fps
def frameconverter(value, fps):
    return '{h:02d}:{m:02d}:{s:02d}:{f:02d}' \
            .format(h = int(value / (3600 * fps)),
                    m = int(value / (60 * fps) % 60),
                    s =int(value / fps % 60),
                    f =int(value % fps))

#convert time of source
def sconv(value, fps):
    tmcd = timecodetoframes(value, fps)
    return (frameconverter(tmcd, fps))

#convert time of source with added value of timeline/recording value
def conv(value, addvalue, fps):
    tmcd = timecodetoframes(value, fps)
    rectime = timecodetoframes(addvalue, fps)
    ntime = rectime + tmcd
    return (frameconverter(ntime, fps))

#check contents of log file
def readlines():
    with open(openlogfile()) as logfile:
        for line in logfile:
            print(line)

#show reel entry
def showreel():
    Label(frm7, text = "Reel code is: " + reeltext.get()).pack()

#show reel entry
def showedit():
    Label(frm7, text = "Edit entry is: " + edittext.get()).pack()

#selects the source fps
def showsourcefps():
    Label(frm7, text = "Source FPS is: " + source.get()).pack()

#selects the target fps
def showtargetfps():
    Label(frm7, text = "Target FPS is: " + target.get()).pack()

#selects the audio video setting
def showav():
    Label(frm7, text = "A/V setting is: " + avtext.get()).pack()

#selects the title setting
def showtitle():
    Label(frm7, text = "Title is: " + titletext.get()).pack()

#selects the title setting
def showfcm():
    Label(frm7, text = "FCM setting is: " + fcmtext.get()).pack()

#create the edl file and write the starting bit to it then call the conversion function and return the new saveloc variable
def savefile():
    #opens the file, then creates variables for the line numbers and clipname
    def createlines():
        with open(openlogfile()) as logfile:
            numi = 1
            clipname = ""
            #loop over each line of the dvrscan file and search for the video name and add it to the clipname variable
            for line in logfile:
                if re.findall("Opened video", line):
                    line = re.sub(r"\[DVR-Scan] Opened video ", "", line)
                    line = line.replace(" (3840 x 2160 at 23.976 FPS).", "")
                    clipname = line
                #loop over each line and search for the source in and out times and then remove unnecessary parts of the output
                if re.findall("[0-9][0-9]:[0-9][0-9]:[0-9][0-9].[0-9]", line):
                    line = re.sub(r"Event    [0-9]", "", line)
                    line = re.sub(r"Event   [0-9][0-9]", "", line)
                    line = re.sub(r"Event  [0-9][0-9][0-9]", "", line)
                    line = line.replace("|", "")
                    line = line.replace(".",":")
                    #split up the lines based on spaces for easier access of functions
                    line = line.split(" ")
                    #convert the source time from string to int so math can be performed then back to string
                    sourcein = sconv((line[6]), float(source.get()))
                    #durat = sconv(line[10]), sourcefps)
                    sourceout = sconv((line[14]), float(source.get()))
                    #convert the source time to selected fps and add the base time for the timeline
                    recin = conv((line[6]), addtime, float(target.get()))
                    recout = conv((line[14]), addtime, float(target.get()))
                    #place the numbers for each line in correct format and then step forward to next number(has to be done prior to first time to pop count up to 001 for for edl entry)
                    num = '{0:0>3}'.format(numi)
                    numi += 1
                    #printing the values of each to the terminal for diagnostic
                    print(f'{sourcein} {sourceout} {recin} {recout}')
                    #fill out line in event.edl file and make an empty line
                    add(f'{num} {reeltext.get()}  {avtext.get()}  {edittext.get()}  {sourcein} {sourceout} {recin} {recout} \n')
                    add(f'* FROM CLIP NAME: {clipname}\n')
    #opens the file, adds the value to file then closes the file
    def add(value):
        f = open(saveloc, 'a')
        f.write(value)
        f.close()
    saveloc = asksaveasfilename(confirmoverwrite= True, filetypes=[("EDL files", "*.edl")] , initialdir= scriptloc, title= "EDL file creation")
    f = open(saveloc, 'w')
    f.write("TITLE: " + titletext.get() + "\n")
    f.write("FCM: " + fcmtext.get() + "\n\n")
    f.close()
    createlines()
    #print value of frames of the time to add to the record time to terminal for diagnostic
    print(timecodetoframes(addtime, float(target.get())))
    #print paths for diagnostics
    print(scriptloc)
    print(currentloc)
    #print completion
    print(f'Completed, file saved at {saveloc}')

#call the conversion function  
#savefile()

#functions
#set character limit to 4
def setcharlimit4(strvar):
    if len(strvar) == 0:
        return False
    elif len(strvar) < 5:
        return True

#set character limit to 70
def setcharlimit70(strvar):
    if len(strvar) == 0:
        return False
    elif len(strvar) < 70:
        return True

#GUI
#title label
maintitlelabel = Label(frm1, text= "DVR Scan to Davinci Bridge", font=("Comic Sans", 24)).pack()

#reel entry and buttons
reellabel = Label(frm2, text="Enter Reel code (4 chars)", font=("Comic Sans", 18)).pack()
reeltextsetting = OptionMenu(frm2, reeltext, *reel_choices)
reeltextsetting.pack()
#setcharlimit4(reeltext)
showreelsetting = Button(frm2, text= "show selected reel setting", command= showreel).pack()

#edit entry and buttons
editlabel = Label(frm2, text="Enter Edit code", font=("Comic Sans", 18)).pack()
edittextsetting = OptionMenu(frm2, edittext, *edit_choices)
edittextsetting.pack()
#setcharlimit4(edittext)
showeditsetting = Button(frm2, text= "show selected edit setting", command= showedit).pack()

#source fps frame and buttons
sourcelabel = Label(frm3, text="Choose the source FPS", font=("Comic Sans", 18)).pack()
sourcefpsmenu = OptionMenu(frm3, source, *fps_choices)
sourcefpsmenu.pack()
showsourcefpssetting = Button(frm3, text= "show selected source fps", command= showsourcefps).pack()

#target fps frame and buttons
targetlabel = Label(frm3, text="Choose the target FPS", font=("Comic Sans", 18)).pack()
targetfpsmenu = OptionMenu(frm3, target, *fps_choices)
targetfpsmenu.pack()
showtargetfpssetting = Button(frm3, text= "show selected target fps", command= showtargetfps).pack()

#audio video frame and buttons
avlabel = Label(frm4, text="Choose the A/V type", font=("Comic Sans", 18)).pack()
avmenu = OptionMenu(frm4, avtext, *av_choices)
avmenu.pack()
showavsetting = Button(frm4, text= "show selected a/v setting", command= showav).pack()

#title buttons
titlelabel = Label(frm4, text="Enter title name (70 chars)", font=("Comic Sans", 18)).pack()
titletextsetting = Entry(frm4, textvariable= titletext)
titletextsetting.pack()
#setcharlimit70(titletextsetting)
showtitlesetting = Button(frm4, text= "show selected title setting", command= showtitle).pack()

#fcm buttons
fcmlabel = Label(frm5, text="Enter FCM choice", font=("Comic Sans", 18)).pack()
fcmtextmenu = OptionMenu(frm5, fcmtext, *fcm_choices)
fcmtextmenu.pack()
showfcmsetting = Button(frm5, text= "show selected fcm setting", command= showfcm).pack()

#save converted file to EDL
fclabel = Label(frm6, text= "Create EDL file and choose DVR log file", font=("Comic Sans", 18)).pack()
savefiledialog = Button(frm6, text= "Start coversion", command= savefile)
savefiledialog.pack()

#etc Buttons
quit = Button(frm6, text="Quit", background= "orangered", command= myapp.master.destroy).pack()

#start the app
myapp.mainloop()