import os
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Button as tb
from PIL import Image, ImageTk
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, asksaveasfilename,askopenfilename
import requests
#creating window
win=Tk()
win.geometry("700x550")
win.title("Text Editor ")
win.iconbitmap("pad.ico")
current_file="Untitled"
current_font="Calibri"

def open_file():
    global current_file,l
    openfile=askopenfilename(initialdir="E:", title="Select the file",filetypes=(("Text files","*.txt"),("All files","*.*")))
    current_file=openfile
    l.config(text=current_file)
    l.pack(side=TOP)
    try:
        if(openfile is not None) or (openfile != ""):
         
            open_fil=open(openfile, "r+")
            text=open_fil.read()
            tab.delete("1.0",END)
            tab.insert("1.0",text)
            open_fil.close()
        elif (openfile is None) or (openfile=="") or (openfile==()):
            return
    except TypeError:
        return
    except FileNotFoundError:
        return

def open_file_event(event):
    global current_file,l
    openfile=askopenfilename(initialdir="E:", title="Select the file",filetypes=(("Text files","*.txt"),("All files","*.*")))
    current_file=openfile
    l.config(text=current_file)
    l.pack(side=TOP)
    try:
        if(openfile is not None) or (openfile != ""):
         
            open_fil=open(openfile, "r+")
            text=open_fil.read()
            tab.delete("1.0",END)
            tab.insert("1.0",text)
            open_fil.close()
        elif (openfile is None) or (openfile=="") or (openfile==()):
            return
    except TypeError:
        return
    except FileNotFoundError:
        return

def new():
    global current_file
    result=messagebox.askokcancel("Important","The Unsaved file changes will be deleted")
    if result:
        tab.delete('1.0',END)
        current_file="Untitled"
        l.config(text=current_file)
    else:
        return

def new_event(event):
    global current_file
    result=messagebox.askokcancel("Important","The Unsaved file changes will be deleted")
    if result:
        tab.delete('1.0',END)
        current_file="Untitled"
        l.config(text=current_file)
    else:
        return
        
def save():
    global current_file,l
    try:
        if current_file=="Untitled":
            save_as()
        else:
            save_file=open(current_file,"w+")
            save_file.write(tab.get("1.0","end-1c"))
            save_file.close()
    except:
        pass

def save_event(event):
    global current_file,l
    try:
        if current_file=="Untitled":
            save_as()
        else:
            save_file=open(current_file,"w+")
            save_file.write(tab.get("1.0","end-1c"))
            save_file.close()
    except:
        pass

def save_as():
    global current_file,l
    try:
        text2=tab.get("1.0","end-1c")
        save_as=asksaveasfilename(initialdir="E:",title="Save As", filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        if save_as is None:
            return
        saveas_file=open(save_as,"w+")
        saveas_file.write(text2)
        saveas_file.close()
        current_file=save_as
        l.config(text=current_file)
        l.pack(side=TOP)
    except:
        pass

def save_as_event(event):
    global current_file,l
    try:
        text2=tab.get("1.0","end-1c")
        save_as=asksaveasfilename(initialdir="E:",title="Save As", filetypes=(("Text Files","*.txt"),("All Files","*.*")))
        if save_as is None:
            return
        saveas_file=open(save_as,"w+")
        saveas_file.write(text2)
        saveas_file.close()
        current_file=save_as
        l.config(text=current_file)
        l.pack(side=TOP)
    except:
        pass

def quit(event):
    result2=messagebox.askyesnocancel("Quit","Do you really want to quit")
    if result2:
        win.destroy()
    else:
        return
#--------------edit----------------------------#

def text_copy():
    try:
        tab.clipboard_clear()
        tab.clipboard_append(tab.selection_get())
    except:
        pass

def text_cut():
    try:
        text_copy()
        tab.delete("sel.first","sel.last")
    except:
        pass

def text_paste():
    try:
        tab.insert(INSERT, tab.clipboard_get())
    except:
        pass

def text_delete():
    try:
        tab.delete("sel.first","sel.last")
        return
    except:
        pass

def text_selectall():
    try:
        tab.tag_add('sel','1.0','end')
        return "break"
    except:
        pass
def selectall_event(event):
    try:
        win.tag_add('sel','1.0','end')
        return "break"
    except:
        pass

#-------------options---------------------------#
def themeblueonblack():
    menubar.config(bg="black",fg="#00bfff",activeforeground="azure",activebackground="black")
    tab.config(bg="gray13",fg="white",highlightcolor="grey",insertbackground="white")
    file_1.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
    edit_2.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
    option_3.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
    option_3_font.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
    option_3_fontsize.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
    preference_4.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
    preference_4_trans.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
    preference_4_theme.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
    help_5.config(bg="gray13", fg="#00bfff", activeforeground="white", activebackground="gray13")
def themedark():
    menubar.config(bg="black",fg="white",activeforeground="azure",activebackground="black")
    tab.config(bg="gray15",fg="white",highlightcolor="lightblue",insertbackground="white" )
    file_1.config(bg="gray15", fg="white",activeforeground="black",activebackground="white")
    edit_2.config(bg="gray15", fg="white",activeforeground="black",activebackground="white")
    option_3.config(bg="gray15", fg="white",activeforeground="black",activebackground="white")
    option_3_font.config(bg="gray15", fg="white",activeforeground="black",activebackground="white")
    option_3_fontsize.config(bg="gray15", fg="white",activeforeground="black",activebackground="white")
    preference_4.config(bg="gray15", fg="white",activeforeground="black",activebackground="white")
    preference_4_trans.config(bg="gray15", fg="white",activeforeground="black",activebackground="white")
    preference_4_theme.config(bg="gray15", fg="white",activeforeground="black",activebackground="white")
    help_5.config(bg="gray14", fg="white",activeforeground="black",activebackground="white")
def themegreenonblack():
    menubar.config(bg="black",fg="lawngreen",activeforeground="white",activebackground="black")
    tab.config(bg="gray14",fg="white",insertbackground="white",highlightcolor="grey", )
    file_1.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
    edit_2.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
    option_3.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
    option_3_font.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
    option_3_fontsize.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
    preference_4.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
    preference_4_trans.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
    preference_4_theme.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
    help_5.config(bg="gray14", fg="lawngreen",activeforeground="white",activebackground="gray14")
def themeredonblack():
    menubar.config(bg="black",fg="red",activeforeground="azure",activebackground="black")
    tab.config(bg="gray14",fg="white",insertbackground="white",highlightcolor="grey", )
    file_1.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
    edit_2.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
    option_3.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
    option_3_font.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
    option_3_fontsize.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
    preference_4.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
    preference_4_trans.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
    preference_4_theme.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
    help_5.config(bg="gray14", fg="red",activeforeground="white",activebackground="gray14")
def default():
    win.wm_attributes("-alpha",1) 
    original_bg=win.cget("background")
    file_1.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    edit_2.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    option_3.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    option_3_font.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    option_3_fontsize.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    preference_4.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    preference_4_trans.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    preference_4_theme.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    help_5.config(bg=original_bg,fg="black", activeforeground="black",activebackground="lightskyblue")
    menubar.config(bg="SystemButtonFace")
    tab.config(bg="SystemButtonFace",fg="black",insertbackground="#000000", highlightcolor="gray",) 
    file_1.config(bg="SystemButtonFace",fg="black",activebackground="lightskyblue",activeforeground="black")

#------------------------------------+--------+---------+
def fontbritannic():
    global current_font
    current_font="Britannic"
    tab.config(font=current_font)
def fontbroadway():
    global current_font
    current_font="Broadway"
    tab.config(font=current_font)
def fontarial():
    global current_font
    current_font="arial"
    tab.config(font=current_font)
def fontcalibri():
    global current_font
    current_font="Calibri"
    tab.config(font=current_font)
def fontcambria():
    global current_font
    current_font="Cambria"
    tab.config(font=current_font)
def fontcentury():
    global current_font
    current_font="Century"
    tab.config(font=current_font)
def fontelephant():
    global current_font
    current_font="Elephant"
    tab.config(font=current_font)
def fontforte():
    global current_font
    current_font="Forte"
    tab.config(font=current_font)
def fontgeorgia():
    global current_font
    current_font="Georgia"
    tab.config(font=current_font)
def fontkunstler():
    global current_font
    current_font="kunstlerscript"
    tab.config(font=current_font)
def fontnina():
    global current_font
    current_font="nina"
    tab.config(font=current_font)
def fontravie():
    global current_font
    current_font="ravie"
    tab.config(font=current_font)
def fonttimesnewroman():
    global current_font
    current_font="timesnewroman"
    tab.config(font=current_font)
def fontswitalt():
    global current_font
    current_font="switalt"
    tab.config(font=current_font)
def fontverdana():
    global current_font
    current_font="verdana"
    tab.config(font=current_font)
#--------------font------------------#
def fontsmall():
    tab.config(font=("",14))
def fontmedium():
    tab.config(font=("",18))
def fontlarge():
    tab.config(font=("",24))

#-------------transparence------------------------#
def transhigh():
    win.wm_attributes("-alpha",1)
def transmedium():
    win.wm_attributes("-alpha",0.9)
def translow():
    win.wm_attributes("-alpha",0.7)
#---------------about-------------------------------#
def about():
    messagebox.showinfo("About","The Simple Text Editor powdered by Python Tkinter")

ip=""
if True:
    try:
        response=requests.get("https://checkip.amazonaws.com")
        ip=str(response.text)
    except:
        pass

def feedback():
    global ip
    if ip !="":
        messagebox.showerror("Error","Your Ip :"+ip+"\nCan't locate the webpage!!")
    else:
        messagebox.showerror("Error","Can't locate the webpage,please try again later with proper internet Connection.")


l=Label(win,text=current_file)
l.pack(side=TOP)
#btn1=tb(l,text="").pack(side=RIGHT)
scroll_bar_y=Scrollbar(win,cursor="arrow")
scroll_bar_y.pack(side="right", fill="y")
tab=Text(win,font="courier", undo=True,borderwidth=1,yscrollcommand=scroll_bar_y.set)
tab.pack(side=LEFT,fill=BOTH, expand=1)

#scroll_bar_y.config(command=tab.yview)

#---------->> create the main menu
menubar=Menu(win)
#---------->>  file-1st-menu
file_1=Menu(menubar, tearoff = 0)
menubar.add_cascade(label="File", menu=file_1)
file_1.add_command(label="New",accelerator="Ctrl+n", command=new)
file_1.add_command(label="Open",accelerator="Ctrl+o", command=open_file)
file_1.add_command(label="Save",accelerator="Ctrl+s", command=save)
file_1.add_command(label="Save As",accelerator="Ctrl+Shift+s",command=save_as )
file_1.add_separator()
file_1.add_command(label="Print Preview")
file_1.add_command(label="Print",accelerator="Ctrl+p")
file_1.add_separator()
file_1.add_command(label="Exit",accelerator="Ctrl+q", command=win.destroy )
#win.config(menu = menubar)

#---------->>  edit-2nd-menu
edit_2=Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_2)
edit_2.add_command(label="Undo",accelerator="Ctrl+Z", command=tab.edit_undo)
edit_2.add_command(label="Redo",accelerator="Ctrl+Y", command=tab.edit_redo)
edit_2.add_separator()
edit_2.add_command(label="Cut",accelerator="Ctrl+X", command=text_cut)
edit_2.add_command(label="Copy",accelerator="Ctrl+C", command=text_copy)
edit_2.add_command(label="Paste",accelerator="Ctrl+V", command=text_paste)
edit_2.add_command(label="Delete",accelerator="Del",command=text_delete)
edit_2.add_separator()
edit_2.add_command(label="Select All", accelerator="Ctrl+A",command=text_selectall)
#win.config(menu=x)

#----------->>  option-3th-menu
option_3=Menu(menubar, tearoff=0)     #menu
menubar.add_cascade(menu=option_3,label="Options")
#option_3.add_command(label="Wrap")
option_3.add_command(label="Word Wrap")
#--------------------------------------------------------------#
#############  submenu-within-option --- [fonts]  ###############

option_3_font=Menu(option_3,tearoff=0)
option_3.add_cascade(label="Fonts", menu=option_3_font)
option_3_font.add_command(label="Arial", command=fontarial)
option_3_font.add_command(label="Britannic", command=fontbritannic)
option_3_font.add_command(label="Broadway", command=fontbroadway)
option_3_font.add_command(label="Calibri", command=fontcalibri)
option_3_font.add_command(label="Cambria", command=fontcambria)
option_3_font.add_command(label="Century", command=fontcentury)
option_3_font.add_command(label="Elephant", command=fontelephant)
option_3_font.add_command(label="Forte",command=fontforte)
option_3_font.add_command(label="Georgia", command=fontgeorgia)
option_3_font.add_command(label="kunstler script", command=fontkunstler)
option_3_font.add_command(label="Nina", command=fontnina)
option_3_font.add_command(label="Ravie",command=fontravie)
option_3_font.add_command(label="SWItalc", command=fontswitalt)
option_3_font.add_command(label="Times New Roman", command=fonttimesnewroman)
option_3_font.add_command(label="Verdana",command=fontverdana)

############  end-of-submenu --- [font]  ####################

#----------->> Preference-4th-menu
preference_4=Menu(menubar, tearoff=0)
preference_4.add_command(label="Default", command=default)
preference_4_trans=Menu(preference_4, tearoff=0)
menubar.add_cascade(label="Preference", menu=preference_4) 
preference_4.add_cascade(label="Transparence", menu=preference_4_trans)
preference_4_trans.add_command(label="High",command=transhigh)
preference_4_trans.add_command(label="Medium",command=transmedium)
preference_4_trans.add_command(label="Low",command=translow)

#############  submenu-within-option --- [theme]  #############
preference_4_theme=Menu(preference_4, tearoff=0)    #submenu--->1
preference_4.add_cascade(label="Theme", menu=preference_4_theme)    #specifing-submenu
preference_4_theme.add_command(label="Dark Theme", command=themedark)   #adding-submenu
preference_4_theme.add_command(label="BlueOnBlack", command=themeblueonblack)   #adding-submenu
preference_4_theme.add_command(label="RedOnBlack", command=themeredonblack)
preference_4_theme.add_command(label="GreenOnBlack", command=themegreenonblack)
#preference_4_theme.add_command(label="BlueWithBlack", command=themeblueonblack)
#############  end-of-submenu --- [theme]  ################
#----------->>  help-5th-menu
help_5=Menu(menubar,tearoff=0)
help_5.add_command(label="About", command=about)
help_5.add_command(label="Feedback", command=feedback)
menubar.add_cascade(label="Help", menu=help_5)

#------------>> leftclick-menu-popup
def click(event):
    try:
        edit_2.tk_popup(event.x_root,event.y_root)
    finally:
        edit_2.grab_release()

win.bind('<Control-n>', new_event)
win.bind('<Control-s>', save_event)
win.bind('<Control-S>', save_as_event)
win.bind('<Control-o>', open_file_event)
#tab.bind('<Control-p>', print_file)
win.bind('<Control-q>', quit)
win.bind('<Control-a>', selectall_event)
tab.bind('<Button-3>',click)
tab.bind('<Button-1')

win.config(menu=menubar)
win.config()
tab.config()
win.mainloop()
#------------xxxxxxxxxxxxxxxxxxxxxxxxxx-----------------#

