import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
import customtkinter as ctk
import re

vlc="c:\\Program Files\\VideoLAN\VLC\\vlc.exe" #default vlc path
input_f="" #path to file
options={} #dictionary with input options

vcoptions=['None','h264','mp2v','mp4v','MJPG']

acoptions=['None','mp3','mp4a','mpga','flac']






def showCurrentOptions():
    if options:     
        tr_info=[f"{k}={v}" for k,v in options.items()]
        tr_info=','.join(tr_info)
    else:
        tr_info="None"
    infoLabel2.configure( text=tr_info)

def changeVlcPath():
    path=filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Executables",
                                                        "*.exe*"),
    
                                                 ))
    if path!="": 
        global vlc
        vlc=path
        vlcLabel.configure( text="Vlc path: "+vlc)

def SelectInputPath():
    path=filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Video files",
                                                        ("*.mp4*","*.mov",
                                                         "*.wmv","*.flv",
                                                         "*.avi","*.mkv")),
                                                 ))
    if path!="": 
        global input_f
        input_f=path
        inputLabel.configure( text="Input file path: "+input_f)


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("vlc transcoder")
app.geometry("1000x415")
app.grid_columnconfigure(0, weight=1)
app.rowconfigure(0,pad=20)



# first row with VLC path 
frame=ctk.CTkFrame(app, width=1000, height=100, bg_color="transparent", corner_radius=0)
frame.grid(sticky="nwes")
frame.grid_rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

vlcLabel=ctk.CTkLabel(
    master=frame,
    text="Vlc path: "+vlc,
    pady=10)

vlcLabel.configure(font=("CtkFont",14))

vlcLabel.grid(row=0, column=0, columnspan=1)

vlcPathButton = ctk.CTkButton(master=frame, text="Change VLC path",
                              command=changeVlcPath)
vlcPathButton.grid(row=1, column=0, pady=(0,20))

#second row with input path
frame2=ctk.CTkFrame(app, width=1000, height=100, bg_color="transparent", corner_radius=0)
frame2.grid(sticky="nwes")
frame2.grid_rowconfigure(1, weight=1, pad=10)
frame2.grid_columnconfigure(0, weight=1)

inputLabel = ctk.CTkLabel(
    master=frame2,
    text="Input file path: "+input_f,
    )

inputLabel.configure(font=("CtkFont",14), pady=10)

inputLabel.grid(row=0, column=0, columnspan=1)

inputPathButton = ctk.CTkButton(master=frame2, text="Select Input file",
                              command=SelectInputPath)
inputPathButton.grid(row=1, column=0, pady=(0,20))

#second row with transcoder options
frame3=ctk.CTkFrame(app, width=1000, height=100, bg_color="transparent", corner_radius=0)
frame3.grid(sticky="nwse")
frame3.grid_rowconfigure(2, weight=1, pad=20)
frame3.grid_columnconfigure((0,1,2,3,4,5),weight=1, pad=10)

def only_numbers(char):
    return char.isdigit()
validation = frame3.register(only_numbers)

def only_floats(char):
    result = re.match(r"^\d*\.?\d*$", char)
    return result is not None
float_validation=frame3.register(only_floats)

vcLabel = ctk.CTkLabel(
    master=frame3,
    text="Video codec"
    )
vcLabel.grid(row=0,column=0)

def choose_v(selected):
    options['vcodec']=selected
    if selected=='None':
        options.pop('vcodec')
    showCurrentOptions()

vcMenu=ctk.CTkOptionMenu(master=frame3, values=vcoptions, command=choose_v)
vcMenu.grid(row=1,column=0, sticky="")


acLabel = ctk.CTkLabel(
    master=frame3,
    text="Audio codec"
    )
acLabel.grid(row=0,column=1)

def choose_a(selected):
    options['acodec']=selected
    if selected=='None':
        options.pop('acodec')
    showCurrentOptions()

acMenu=ctk.CTkOptionMenu(master=frame3, values=acoptions, command=choose_a)
acMenu.grid(row=1,column=1,  sticky="")

vbLabel = ctk.CTkLabel(
    master=frame3,
    text="Video Bitrate"
    )
vbLabel.grid(row=0,column=2)

def choose_vb(vbInput):
    vb=vbInput.get()
    if vb=="":
        options.pop('vb')
    else:
        options['vb']=vb
    showCurrentOptions()

vbInput=tk.StringVar()
vbInput.trace("w", lambda name, index,mode, vbInput=vbInput:choose_vb(vbInput))

vbitrate = ctk.CTkEntry(master=frame3, validate="key", validatecommand=(validation, '%S'), textvariable=vbInput)
vbitrate.grid(row=1,column=2,  sticky="")

abLabel = ctk.CTkLabel(
    master=frame3,
    text="Audio Bitrate"
    )
abLabel.grid(row=0,column=3)

def choose_ab(abInput):
    ab=abInput.get()
    if ab=="":
        options.pop('ab')
    else:
        options['ab']=ab
    showCurrentOptions()

abInput=tk.StringVar()
abInput.trace("w", lambda name, index,mode, abInput=abInput:choose_ab(abInput))

abitrate = ctk.CTkEntry(master=frame3, validate="key", validatecommand=(validation, '%S'),textvariable=abInput)
abitrate.grid(row=1,column=3,  sticky="")

fpsLabel= ctk.CTkLabel(
    master=frame3,
    text="Frames per second"
    )
fpsLabel.grid(row=0,column=4)

def choose_fps(fpsInput):
    fps=fpsInput.get()
    if fps=="":
        options.pop('fps')
    else:
        options['fps']=fps
    showCurrentOptions()

fpsInput=tk.StringVar()
fpsInput.trace("w", lambda name, index,mode, fpsInput=fpsInput:choose_fps(fpsInput))

fps = ctk.CTkEntry(master=frame3, validate="key", validatecommand=(validation, '%S'), textvariable=fpsInput)
fps.grid(row=1,column=4,  sticky="")

scaleLabel= ctk.CTkLabel(
    master=frame3,
    text="Scale"
    )
scaleLabel.grid(row=0,column=5)

def choose_scale(scaleInput):
    scale=scaleInput.get()
    if not re.match(r"^\d*\.?\d*$", scale):
        return
    if scale=="":
        options.pop('scale')
    else:
            options['scale']=scale
    showCurrentOptions()


scaleInput=tk.StringVar()
scaleInput.trace("w", lambda name, index,mode, scaleInput=scaleInput:choose_scale(scaleInput))

scale = ctk.CTkEntry(master=frame3, validate="key", validatecommand=(float_validation, '%S'), textvariable=scaleInput)
scale.grid(row=1,column=5,  sticky="")


#selected options info
frame4=ctk.CTkFrame(app, width=1000, height=100, bg_color="transparent", corner_radius=0)
frame4.grid(sticky="nwes")
frame4.grid_rowconfigure(0, weight=1, pad=20)
frame4.grid_columnconfigure(0, weight=1)

infoLabel = ctk.CTkLabel(
    master=frame4,
    text="Selected options"
    )
infoLabel.grid(row=0,column=0)
infoLabel.configure(font=("CtkFont",18))

infoLabel2 = ctk.CTkLabel(
    master=frame4,
    text="None"
    )
infoLabel2.grid(row=1,column=0)
infoLabel2.configure(font=("CtkFont",12))

#save button
frame5=ctk.CTkFrame(app, width=1000, height=100, bg_color="transparent", corner_radius=0)
frame5.grid(sticky="nwes")
frame5.grid_rowconfigure(0, weight=1, pad=20)
frame5.grid_columnconfigure(0, weight=1)

def transcode():
    if input_f=="":
        errorLabel.configure(text="No video selected")
        return
    if options:     
        output=asksaveasfile(initialfile = 'transcoded.mp4',
                            defaultextension=".mp4",
                            filetypes = (("MP4 file","*.mp4*"),
                                         ("MOV file","*.mov*"),
                                         ("WMV file","*.wmv*"),
                                         ("FLV file","*.flv*"),
                                         ("AVI file","*.avi*"),
                                         ("MKV file","*.mkv*")
                                                    ))
        output=output.name
        #replace / to \ due to not taking path by cmd
        input_file=input_f.replace("/","\\")
        output=output.replace("/","\\")
        tr_info=[f"{k}={v}" for k,v in options.items()]
        tr_info=','.join(tr_info)
        transcode="--sout=#transcode{"+tr_info+"}:standard{access=file,mux=ts,dst="+'"'+output+'"'+"}"
        subprocess.run([vlc, input_file, transcode, "vlc://quit" ], shell=True)
    else:
        errorLabel.configure(text="No options selected")

saveButton = ctk.CTkButton(master=frame5, text="Transcode",
                              command=transcode)
saveButton.grid(row=1, column=0, pady=(20,10))

#error
frame6=ctk.CTkFrame(app, width=1000, height=100, bg_color="transparent", corner_radius=0)
frame6.grid(sticky="nwes")
frame6.grid_rowconfigure(0, weight=1, pad=20)
frame6.grid_columnconfigure(0, weight=1)
errorLabel = ctk.CTkLabel(
    master=frame6,
    text_color="red",
    text=""
    )
errorLabel.grid(row=1,column=0)
errorLabel.configure(font=("CtkFont",14))

app.mainloop()
