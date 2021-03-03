from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import speech_recognition as sr
import webbrowser as wb
import pyttsx3

#pygame.mixer.init()
engine=pyttsx3.init()
root = Tk()
root.geometry("1000x1000")
root.title("SPEECH To TEXT")
canvas = Canvas(root, width=800, height=800)
canvas.pack(fill=BOTH,expand=True)
bgImg = PhotoImage(file="image1.png")
canvas.create_image(300,300,image=bgImg)
bgImg1= PhotoImage(file="image1.png")
canvas.create_image(1000,300,image=bgImg)

FirstTimeFile=False

menubar = Menu(root)
root.config(menu=menubar)
filemenu = Menu(menubar)
filemenu1 = Menu(menubar)
filemenu2 = Menu(menubar)
filemenu3 = Menu(menubar)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit",menu=filemenu1)
menubar.add_cascade(label="Info", menu=filemenu2)
menubar.add_cascade(label="About us",menu=filemenu3)



def convertToText():
    r=sr.Recognizer()
    engine.say("Speak now!!")
    engine.runAndWait()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio=r.listen(source)
        try:
            text=r.recognize_google(audio)
            #text=r.recognize_sphinx(audio)
            ResultWidget.insert(END,str(text)+"\n")
        except sr.RequestError as e:
            messagebox.showwarning("No Internet","Check your Internet Connection and Try Again")
        except sr.UnknownValueError:
            messagebox.showinfo("Didn't get that","Try again")

def searchWeb():
    content=ResultWidget.get('1.0',END)
    if content:
        URL='https://www.google.com/search?q='
        wb.open_new_tab(URL+content)
    else:
        messagebox.showwarning("Empty Box","No content to Search")

def clearText():
    ResultWidget.delete(1.0,END)

def saveAsFile():
    global FirstTimeFile
    FirstTimeFile = filedialog.asksaveasfilename(defaultextension="*.txt",initialdir="C:",title="Save File",filetypes=(("Text File","*.txt"),("HTML File","*.html"), ("Python File","*.py")))
    if FirstTimeFile:
        text_file=open(FirstTimeFile,'w')
        text_file.write(ResultWidget.get("1.0",END))
        text_file.close()

def saveFile():
    global FirstTimeFile
    if FirstTimeFile:
        text_file=open(FirstTimeFile,'w')
        text_file.write(ResultWidget.get("1.0",END))
        text_file.close()
    else:
        saveAsFile()

def provideInfo():
    info="Press Mic Button to Speak\nPress Google Button to Web search content in Box"
    messagebox.showinfo("Info",info)

def provideAboutUs():
    AbtUs="This Speech To Text Module is part of IT204 Project\nDevelopers:\n         Anshul Patel\n         Kiran Acharya\n         Mohit Awachar\n         Rakshit KulKarni\nUnder Guidance of:\n         Priyadarshini Mam"
    messagebox.showinfo("About Us",AbtUs)

FileFrame=Frame(canvas)
FileFrame.grid(row=0,column=0,padx=100)

filemenu.add_command(label="Save", command=saveFile)
filemenu.add_command(label="Save As", command=saveAsFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

filemenu1.add_command(label="Clear", command=clearText)
filemenu2.add_command(label="Info", command=provideInfo)
filemenu3.add_command(label="About Us", command=provideAboutUs)




RemainingFrame=Frame(canvas,bg="#03FADE")
RemainingFrame.grid(row=0,column=1,padx=30,pady=15)

WelcomeMessage =Label(RemainingFrame,text="Welcome to Speech to Text",fg="#8000ff",font="Times 32 bold",bg="#03FADE")
WelcomeMessage.pack()

ResultWidget=ScrolledText(RemainingFrame,height=20,font=('Times',15),bg="black",fg="white",insertbackground='white')
ResultWidget.pack()


SubFrameInRemaingFrame=Frame(RemainingFrame,bg="#03FADE")
SubFrameInRemaingFrame.pack()

#Mic Button
imgMic=PhotoImage(file="mic3.png")
MicButton=Button(SubFrameInRemaingFrame,image=imgMic,bd=0,command= convertToText,bg="#03FADE")
MicButton.grid(row=1,column=0,pady=5,padx=50)

#Google stuff
imgGoogle=PhotoImage(file="google1.png")
GoogleButton=Button(SubFrameInRemaingFrame,image=imgGoogle,bd=0,command= searchWeb,bg="#03FADE")
GoogleButton.grid(row=1,column=1,pady=5,padx=50)

root.mainloop()