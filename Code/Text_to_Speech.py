from tkinter import *
from tkinter import filedialog, ttk, messagebox
from tkinter import Tk, Canvas
from tkinter.ttk import Style

import pyttsx3
from tkinter.scrolledtext import *
from queue import Queue
import pygame
import os
from shutil import copyfile

root = Tk()
engine = pyttsx3.init()
root.geometry("1000x1000")
root.title("TTS")
canvas = Canvas(root, width=500, height=500)
canvas.pack(fill=BOTH,expand=True)
checks=False
q=Queue()
content=""
pygame.mixer.init()
temp_file='test1.mp3'

def save_dummy(checks,file_name):
    voices = engine.getProperty('voices')
    engine.setProperty('rate',150)
    if checks:
        engine.setProperty('voice', voices[0].id)
        engine.save_to_file(content.rstrip(), file_name)
    else:
        engine.setProperty('voice', voices[1].id)
        engine.save_to_file(content.rstrip(), file_name)
    engine.runAndWait()
def savefile():
    global content
    if text.get("1.0", END) == "\n":
        messagebox.showerror("ERROR","YOU ARE NOT SELECTED ANY RELATED FILE\nTEXT FIELD IS EMPTY")
        return
    content=text.get('1.0',END)
    files = [("Text", '*.txt'), ('All Files', '*.*')]
    file = filedialog.asksaveasfile(filetypes=files, defaultextension="txt")
    save_text=open("text1.txt",'w')
    save_text.write(content)
    save_text.close()
    copyfile("text1.txt",file.name)
    os.remove("text1.txt")
    save_dummy(checks,temp_file)
    messagebox.showinfo("Information","CONTENT FROM TEXT FIELD TO TEXT FILE IS SAVED")

def save_text():
    global content,playing_state
    if playing_state:
        stop()
    if text.get("1.0", END) == "\n":
        messagebox.showerror("ERROR","YOU ARE NOT SELECTED ANY RELATED FILE\nTEXT FIELD IS EMPTY")
        val.set(0)
        return
    content = text.get('1.0', 'end-1c')
    save_text = open("text1.txt", 'w')
    save_text.write(content)
    save_text.close()
    os.remove("text1.txt")
    save_dummy(checks, temp_file)
    messagebox.showinfo("Information","TEXT FIELD CONTENT IS SAVED")
    val.set(0)

def open_text():
    global content
    if text.get("1.0", END) != "\n":
        p = messagebox.askquestion("CONFIRMATION", "DO YOU WANT TO REMOVE CONTENT FROM TEXT FIELD?")
        if p=="yes":
            text.delete('1.0',END)
        val.set(0)
    filename = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                          filetypes=(("Text file", "*.txt"), ("all files", "*.*")))
    try:
        filename = open(filename, 'r')
        content = filename.read()
        text.insert(END, content)
        filename.close()
        save_dummy(checks, temp_file)
    except:
        messagebox.showwarning("Warning", "YOU ARE NOT SELECTED ANY RELATED FILE\nTEXT FIELD IS EMPTY")
        return

def change_voice():
    if text.get("1.0", END) == "\n":
        messagebox.showerror("ERROR","YOU ARE NOT SELECTED ANY RELATED FILE\nTEXT FIELD IS EMPTY")
        return
    p=messagebox.askquestion("Confirm","Are You sure?")
    if p!="yes":
        val.set(0)
        return
    os.remove(temp_file)
    global checks
    voices = engine.getProperty('voices')
    if checks:
        engine.setProperty('voice',voices[0].id)
        checks=False
    else:
        engine.setProperty('voice',voices[1].id)
        checks=True
    save_dummy(checks,temp_file)
    if checks==False:
        messagebox.showinfo("Gender","Female")
    else:
        messagebox.showinfo("Gender","Male")
    val.set(0)


global audio
check_play=True
def play():
    global audio,check,check_play,playing_state
    if text.get("1.0", END) == "\n":
        messagebox.showwarning("Warning","Text Field is Empty\nSelect Any Related File")
        return
    if not playing_state:
        audio=pygame.mixer.Sound(temp_file)
        audio.play()

def stop():
    global checks
    global audio
    if text.get("1.0", END) == "\n":
        messagebox.showwarning("Warning","Text Field is Empty\nSelect Any Related File")
        return
    audio.stop()

playing_state=False
def pausesong():
    global playing_state
    if text.get("1.0", END) == "\n":
        messagebox.showwarning("Warning","Text Field is Empty\nSelect Any Related File")
        return
    if not playing_state:
        pygame.mixer.pause()
        playing_state = True

def unpausesong():
    if text.get("1.0", END) == "\n":
        messagebox.showwarning("Warning","Text Field is Empty\nSelect Any Related File")
        return
    global playing_state
    if playing_state:
        pygame.mixer.unpause()
        playing_state = False


def save_audio():
    global content
    if text.get("1.0", END) == "\n":
        messagebox.showerror("ERROR", "YOU ARE NOT SELECTED ANY RELATED FILE\nTEXT FIELD IS EMPTY")
        return
    os.remove(temp_file)
    engine.setProperty('rate',150)
    voices = engine.getProperty('voices')
    if checks:
        engine.setProperty('voice', voices[0].id)
        engine.save_to_file(content.rstrip(), temp_file)
    else:
        engine.setProperty('voice', voices[1].id)
        engine.save_to_file(content.rstrip(), temp_file)
    engine.runAndWait()
    files = [("MP3 File",'*.mp3'),('All Files','*.*')]
    file = filedialog.asksaveasfile(filetypes=files, defaultextension="mp3")
    copyfile(temp_file,file.name)
    messagebox.showinfo("Information","AUDIO FILE IS SAVED")

def volumesilder(postion):
    global audio,current_volume,current
    try:
        current = volume_slider.get()
        audio.set_volume(current)
        current_volume=audio.get_volume()
    except Exception as e:
        pass
    finally:
        current_volume=current*100
        if int(current_volume)<1:
            vol_meter.config(image=vol0)
        elif int(current_volume)>=1 and int(current_volume)<30:
            vol_meter.config(image=vol1)
        elif int(current_volume)>=30 and int(current_volume)<60:
            vol_meter.config(image=vol2)
        elif int(current_volume)>=60 and int(current_volume)<90:
            vol_meter.config(image=vol3)
        elif int(current_volume)>=90 and int(current_volume)<=100:
            vol_meter.config(image=vol4)

def confirm_male():
    global checks
    checks=False
    change_voice()

def confirm_female():
    global checks
    checks=True
    change_voice()

menubar = Menu(root)
root.config(menu=menubar)
filemenu = Menu(menubar)
filemenu1 =Menu(menubar)
filemenu2=Menu(menubar)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit",menu=filemenu1)



filemenu.add_command(label="Open", command=open_text)
filemenu.add_separator()
filemenu.add_command(label="Save Text",command=savefile)
filemenu.add_separator()
filemenu.add_command(label="Save Speech",command=save_audio)


sub_menu_filemenu1=Menu(filemenu1)
sub_menu_filemenu1.add_command(label="Male",command=confirm_male)
sub_menu_filemenu1.add_command(label="Female",command=confirm_female)
filemenu1.add_cascade(label="Chage Voice",command=change_voice,menu=sub_menu_filemenu1)




bgImg = PhotoImage(file="Images\\backg1.png")

control_frame=LabelFrame(canvas,text="User Controls",bg="orange")
control_frame.place(x=40,y=150)

play_img=PhotoImage(file="Images\\play1.png")
stop_img=PhotoImage(file="Images\\stop1.png")
pause_img=PhotoImage(file="Images\\pause.png")
unpause_img=PhotoImage(file="Images\\unpause1.png")

play_btn=Button(control_frame,image=play_img,command=play,borderwidth=0,bg="black")
play_btn.pack(pady=10)
pause_btn=Button(control_frame,image=pause_img,command=pausesong,borderwidth=0,bg="black")
pause_btn.pack(pady=10)
unpause_btn=Button(control_frame,image=unpause_img,command=unpausesong,borderwidth=0,bg="black")
unpause_btn.pack(pady=10)
stop_btn=Button(control_frame,image=stop_img,command=stop,borderwidth=0,bg="black")
stop_btn.pack(pady=10)

canvas.create_image(500,500,image=bgImg)



vol0=PhotoImage(file="Images\\vol0.png")
vol1=PhotoImage(file="Images\\vol1.png")
vol2=PhotoImage(file="Images\\vol2.png")
vol3=PhotoImage(file="Images\\vol3.png")
vol4=PhotoImage(file="Images\\vol4.png")


volume_frame=LabelFrame(canvas,text="Volume",bg="#42E3F2")
volume_frame.place(x=950,y=200)

vol_m=LabelFrame(canvas,text="Volume Meter")
vol_m.place(x=950,y=400)
vol_meter=Label(vol_m,image=vol4)

audio_frame=LabelFrame(canvas,text="Audio Speed",bg="#ADEDDE")
audio_frame.place(x=1050,y=200)
speed_frame=Style(audio_frame)
speed_frame.configure("TRadiobutton", font=("Courier New", 14, "bold"))
val=StringVar(audio_frame)
val.set(0)

def speed():
    try:
       pausesong()
       os.remove(temp_file)
       engine.setProperty('rate',int(val.get()))
       voices = engine.getProperty('voices')
       if checks:
           engine.setProperty('voice', voices[0].id)
           engine.save_to_file(content.rstrip(),temp_file)
       else:
           engine.setProperty('voice', voices[1].id)
           engine.save_to_file(content.rstrip(), temp_file)
       engine.runAndWait()
       unpausesong()

    except Exception as e:
        pass

engine.setProperty('rate',350)
values = {"0.5x": 50,
          "0.75x": 75,
          "Normal": 150,
          "1.5x": 250,
          "2x": 350 }

for text, value in values.items():
    Radiobutton(audio_frame, text=text, variable=val,background="#ADEDDE",activebackground="#EE8293",foreground = "#FB3F08",bg="#ADEDDE",value=value,command=speed).pack(side=TOP,ipady=3)


l1 = Label(canvas, text="WELCOME TO TEXT TO SPEECH INTERFACE",bg="pink")
text = ScrolledText(canvas,width=80,height=30,bg="black",fg="white",insertbackground='white',undo=True)
text.configure(font=("Courier", 10, "italic"))
save_text_btn=Button(canvas,text="SAVE TEXT",command=save_text,bg="#96BFF4",activebackground="#15F3D7")

volume_slider=ttk.Scale(volume_frame,from_=0,to=1,orient=VERTICAL,value=1,command=volumesilder,length=150)

l1.place(x=400,y=0)
text.place(x=200,y=40)
save_text_btn.place(x=500,y=580)
volume_slider.pack()
vol_meter.pack()

canvas.grid_rowconfigure(5, weight=1)
canvas.grid_columnconfigure(5, weight=1)

root.mainloop()

try:
    os.remove(temp_file)
except:
    pass