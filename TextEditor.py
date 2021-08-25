from tkinter import Tk
import tkinter as tk
from tkinter import filedialog 
from tkinter import font

root=Tk()
root.title("Simple Text Editor")

#Functions for File Menu begin here
def saveAs():
    f=filedialog.asksaveasfile(mode='w',defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    text2save=str(text.get(1.0, tk.END))
    f.write(text2save)
    f.close() 

def Open():
    name=filedialog.askopenfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                           title = "Choose a file.")
    print(name) #Use this as the status bar
    #Using try in case user types in unknown file or closes without choosing a file.
    try:
        with open(name,'r') as file:
            print(file.read())
    except:
        print("No file exists")

#Functions for File Menu end here
                
#MenuBar design begins. Placed at the top of the screen by DEFAULT.
myMenu=tk.Menu(root,bg="#CDB79E")  #myMenu is the blank menubar
root.config(menu=myMenu)

fileMenu=tk.Menu(myMenu)
myMenu.add_cascade(label="File",menu=fileMenu)
fileMenu.add_command(label="New")  #try implementing keyboard shortcuts for all of these later
fileMenu.add_command(label="Open",command=Open) 
fileMenu.add_separator()
fileMenu.add_command(label="Save")
fileMenu.add_command(label="Save As",command=saveAs)
fileMenu.add_separator()
fileMenu.add_command(label="Close")

#Functions for Edit Menu begin here
def Cut():
    content=text.get(tk.SEL_FIRST,tk.SEL_LAST)
    root.clipboard_append(content)
    text.delete(tk.SEL_FIRST,tk.SEL_LAST)
    #Try using the content variable for Undo and Redo later on

def Copy():
    root.clipboard_clear()
    textToAppend=text.get(tk.SEL_FIRST,tk.SEL_LAST)
    root.clipboard_append(textToAppend)
    
def Paste():
    textToPaste=root.clipboard_get()
    text.insert(tk.INSERT,textToPaste)

def Delete():
    text.delete(tk.SEL_FIRST,tk.SEL_LAST)

def SelectAll():
    text.tag_add('sel',1.0,tk.END)

def Undo():
    text.edit_undo()

def Redo():
    text.edit_redo()    

def FindAndReplace():
    
    def Find():
        content=e1.get()
        i=len(content)
        idx="1.0" 
        while(True):
            if(var_1.get()==0 and var_2.get()==0):
                idx=text.search(content,idx,nocase=1,stopindex='end')
            elif(var_1.get()==1 and var_2.get()==0):
                idx=text.search(content,idx,nocase=0,stopindex='end')
            '''   
            Match for whole word not working. Fix Later 
            
            
            elif(var_1.get()==0 and var_2.get()==1):
                idx=text.search(r'\y%s\y'%content,tk.INSERT,backwards=True,regexp=True,nocase=1)
            #lse:
                idx=text.search('\y%s\y'%content,tk.INSERT,backwards=True,regexp=True,nocase=0)
            '''
            if(idx):
                idx2=text.index("%s+%dc"%(idx,i)) #What does this mean?
                text.tag_add("highlight",idx,idx2)
                text.tag_config("highlight",background="lime")
                idx=idx2
    
    def ReplaceAll():
        content=e1.get()
        newText=e2.get()
        i=len(content)
        idx="1.0"
        while(True):
            if(var_1.get()==0):
                idx=text.search(content,idx,nocase=1,stopindex='end')
            else:
                idx=text.search(content,idx,nocase=0,stopindex='end')
            if(idx):
                idx2=text.index("%s+%dc"%(idx,i)) 
                text.delete(idx,idx2)
                text.insert(idx,newText)
                idx=idx2
    
    def Cancel():
        findReplace.destroy()         
          
    findReplace=tk.Toplevel()
    findReplace.title("Find and Replace")
    findReplace.resizable(0,0)
    findReplace.geometry('560x170')
    label_1=tk.Label(findReplace,text="Find What")
    label_1.grid(row=0,sticky='W')
    label_2=tk.Label(findReplace,text="Replace With")
    label_2.grid(row=1,sticky='W')
    e1=tk.Entry(findReplace)
    e1.grid(row=0,column=1)
    e2=tk.Entry(findReplace)
    e2.grid(row=1,column=1)
    button_1=tk.Button(findReplace,text="Find",width=20,command=Find)
    button_1.grid(row=0,column=4,padx=40)
    button_2=tk.Button(findReplace,text="Replace All",width=20,command=ReplaceAll)
    button_2.grid(row=1,column=4,padx=40)
    button_3=tk.Button(findReplace,text="Cancel",width=20,command=Cancel)
    button_3.grid(row=2,column=4,padx=40)
    var_1=tk.IntVar()
    c1=tk.Checkbutton(findReplace,text="Match Case",variable=var_1)
    c1.grid(row=3,column=0,sticky='W')
    var_2=tk.IntVar()
    c2=tk.Checkbutton(findReplace,text="Match whole word only",variable=var_2)
    c2.grid(row=4,column=0,sticky='W')
    
#Functions for Edit Meu end here

editMenu=tk.Menu(myMenu)
myMenu.add_cascade(label="Edit",menu=editMenu)
editMenu.add_command(label="Cut",command=Cut)
editMenu.add_command(label="Copy",command=Copy)
editMenu.add_command(label="Paste",command=Paste)
editMenu.add_command(label="Delete",command=Delete)
editMenu.add_separator()
editMenu.add_command(label="Select All",command=SelectAll)
editMenu.add_separator()
editMenu.add_command(label="Find and Replace",command=FindAndReplace)
editMenu.add_separator()
editMenu.add_command(label="Undo",command=Undo)
editMenu.add_command(label="Redo",command=Redo)

#Functions for View Menu begin here

def LowerCase():
    c=text.get(1.0,tk.END)
    text.delete(1.0,tk.END)
    text.insert(1.0,c.lower())
    
def UpperCase():
     t=text.get(1.0,tk.END)
     text.delete(1.0,tk.END)
     text.insert(1.0,t.upper())     

#Functions for View Menu end here
viewMenu=tk.Menu(myMenu)
myMenu.add_cascade(label="View",menu=viewMenu)
viewMenu.add_separator()
viewMenu.add_command(label="Convert to Lowercase",command=LowerCase)
viewMenu.add_command(label="Convert to Uppercase",command=UpperCase)
#MenuBar design done

#Functions for Toolbar#1 begin here
def Cut_1():
    content=text.get(tk.SEL_FIRST,tk.SEL_LAST)
    root.clipboard_append(content)
    text.delete(tk.SEL_FIRST,tk.SEL_LAST)

def Copy_1():
    root.clipboard_clear()
    textToAppend=text.get(tk.SEL_FIRST,tk.SEL_LAST)
    root.clipboard_append(textToAppend)

def Paste_1():
    textToPaste=root.clipboard_get()
    text.insert(tk.INSERT,textToPaste)

def Undo_1():
    text.edit_undo()

def Redo_1():
    text.edit_redo()    
#Functions for Toolbar#1 end here
#Toolbar #1 design begins
toolbar_1=tk.Frame(root,bg="gray",bd=1)

newImage=tk.PhotoImage(file="new.png")
newButton=tk.Button(toolbar_1,image=newImage)
newButton.pack(side=tk.LEFT,padx=2,pady=2)

openImage=tk.PhotoImage(file="open.png")
openButton=tk.Button(toolbar_1,image=openImage)
openButton.pack(side=tk.LEFT,padx=2,pady=2)

saveImage=tk.PhotoImage(file="save.png")
saveButton=tk.Button(toolbar_1,image=saveImage)
saveButton.pack(side=tk.LEFT,padx=2,pady=2)

closeImage=tk.PhotoImage(file="close.png")
closeButton=tk.Button(toolbar_1,image=closeImage)
closeButton.pack(side=tk.LEFT,padx=2,pady=2)

cutImage=tk.PhotoImage(file="cut.png")
cutButton=tk.Button(toolbar_1,image=cutImage,command=Cut_1)
cutButton.pack(side=tk.LEFT,padx=2,pady=2)

copyImage=tk.PhotoImage(file="copy.png")
copyButton=tk.Button(toolbar_1,image=copyImage,command=Copy_1)
copyButton.pack(side=tk.LEFT,padx=2,pady=2)

pasteImage=tk.PhotoImage(file="paste.png")
pasteButton=tk.Button(toolbar_1,image=pasteImage,command=Paste_1)
pasteButton.pack(side=tk.LEFT,padx=2,pady=2)

undoImage=tk.PhotoImage(file="undo.png")
undoButton=tk.Button(toolbar_1,image=undoImage,command=Undo_1)
undoButton.pack(side=tk.LEFT,padx=2,pady=2)

redoImage=tk.PhotoImage(file="redo.png")
redoButton=tk.Button(toolbar_1,image=redoImage,command=Redo_1)
redoButton.pack(side=tk.LEFT,padx=2,pady=2)

toolbar_1.pack(side=tk.TOP,fill=tk.X)
#Toolbar #1 design done

#Functions for Toolbar #2 begin here
def make_Bold():
        current_tags=text.tag_names(tk.SEL_FIRST)
        if "bt" in current_tags:
            text.tag_remove("bt",tk.SEL_FIRST,tk.SEL_LAST)
        else:
            text.tag_add("bt",tk.SEL_FIRST,tk.SEL_LAST)
            
        bold_font=font.Font(text,text.cget("font"))
        bold_font.configure(weight="bold",size=12)
        text.tag_configure("bt",font=bold_font)

def make_Italics():
    current_tags=text.tag_names(tk.SEL_FIRST)
    if "it" in current_tags:
        text.tag_remove("it",tk.SEL_FIRST,tk.SEL_LAST)
    else:
        text.tag_add("it",tk.SEL_FIRST,tk.SEL_LAST)
    
    italics_font=font.Font(text,text.cget("font"))
    italics_font.configure(slant=font.ITALIC,size=12)
    text.tag_configure("it",font=italics_font)
    
def make_Underline():
    current_tags=text.tag_names(tk.SEL_FIRST)
    if "ud" in current_tags:
        text.tag_remove("ud",tk.SEL_FIRST,tk.SEL_LAST)
    else:
        text.tag_add("ud",tk.SEL_FIRST,tk.SEL_LAST)
    underline_text=font.Font(text,text.cget("font"))
    underline_text.configure(underline=True)
    text.tag_configure("ud",font=underline_text,size=12)

def strike():
    current_tags=text.tag_names(tk.SEL_FIRST)
    if "st" in current_tags:
        text.tag_remove("st",tk.SEL_FIRST,tk.SEL_LAST)
    else:
        text.tag_add("st",tk.SEL_FIRST,tk.SEL_LAST)
    text.tag_configure("st",overstrike=True,size=12)  

def ChangeFontSize():
    changeFontSize=tk.Toplevel()
    changeFontSize.title("Change Font Size")
    changeFontSize.resizable(0,0)
    changeFontSize.geometry('700x250')
    
    label1=tk.Label(changeFontSize,text="Font:")
    label1.grid(row=0,sticky='W',padx=40)
    label3=tk.Label(changeFontSize,text="Font Size:")
    label3.grid(row=0,column=2,sticky='W',padx=40)
    
    e1=tk.Entry(changeFontSize)
    e1.insert(0,"Select Font..")
    e1.grid(row=1,padx=40,sticky='w')
    e3=tk.Entry(changeFontSize)
    e3.grid(row=1,column=2)
    
    var1=tk.StringVar(e1)
    currentFont=text.cget('font')
    var1.set(currentFont)
    listOfFonts=['Courier','MS Serif','MS Sans Serif','Arial CE','Arial CYR','Arial Greek',
                 'Calibri','Calibri Light','Courier New','Courier New CE',
                 'Times New Roman CE','Times New Roman',
                 'Times New Roman TUR','Lucida Handwriting','Lucida Fax','MS Outlook']
    
    option1=tk.OptionMenu(changeFontSize,var1,*listOfFonts)
    option1.grid(row=2,column=0,padx=40,columnspan=50,sticky='W')
    
    listOfFontSizes=[8,9,10,11,12,14,16,18,24,30,36,48,60,72,96]
    var2=tk.StringVar(e3)
    option2=tk.OptionMenu(changeFontSize,var2,*listOfFontSizes)
    option2.grid(row=2,column=2,padx=40,columnspan=20,sticky='W')
    
    def enableFont():
        e1.delete(0,tk.END)
        e1.insert(0,var1.get())
        text.tag_add("change","1.0",tk.END)
        new_font=(var1.get(),12)
        text.tag_configure("change",font=new_font)
        
    button=tk.Button(changeFontSize,text="Enable Font",command=enableFont)
    button.grid(row=3,column=1)
    
    def FontSize():
        e3.delete(0,tk.END)
        e3.insert(0,var2.get())
        text.tag_add("size","1.0",tk.END)
        current_font=font.Font(text,text.cget("font"))
        new_font=(current_font,var2.get())
        #change=var2.get()
        text.tag_configure("size",font=new_font,)
    
    button_1=tk.Button(changeFontSize,text="Change Font Size",command=FontSize)
    button_1.grid(row=3,column=2)

#Functions for Toolbar #2 end here
#Toolbar #2 design begins
toolbar_2=tk.Frame(root,bg="#CDC0B0",bd=1)

boldImage=tk.PhotoImage(file="bold.png")
boldButton=tk.Button(toolbar_2,image=boldImage,command=make_Bold)
boldButton.pack(side=tk.LEFT,padx=2,pady=2)

italicsImage=tk.PhotoImage(file="italics.png")
italicsButton=tk.Button(toolbar_2,image=italicsImage,command=make_Italics)
italicsButton.pack(side=tk.LEFT,padx=2,pady=2)

underlineImage=tk.PhotoImage(file="underline.png")
underlineButton=tk.Button(toolbar_2,image=underlineImage,command=make_Underline)
underlineButton.pack(side=tk.LEFT,padx=2,pady=2)

strikeImage=tk.PhotoImage(file="strike.png")
strikeButton=tk.Button(toolbar_2,image=strikeImage,command=strike)
strikeButton.pack(side=tk.LEFT,padx=2,pady=2)

changeFontImage=tk.PhotoImage(file="font.png")
changeFontButton=tk.Button(toolbar_2,image=changeFontImage,command=ChangeFontSize)
changeFontButton.pack(side=tk.LEFT,padx=2,pady=2)

toolbar_2.pack(side=tk.TOP,fill=tk.X)
#Toolbar #2 design done

scroll=tk.Scrollbar(root)
text=tk.Text(root,height=200,width=120,yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT,fill=tk.Y)
text.pack()
scroll.config(command=text.yview)
'''
DISPLAY LINE NUMBER AND COLUMN NUMBER AT STATUS BAR CONTINOUSLY
labelText=tk.StringVar()
status=tk.Label(root,bd=1,height=1,anchor='w',textvariable=labelText,bg='red')
status.pack(side="bottom",fill=tk.X)
print(text.index())
#ALSO SEE HOW TO CONTINOUSLY DISPLAY LINE NUNMBER AND COLUMN NUMBER
'''
#print(font.families())

#All of the KeyBoard shortcuts 
root.mainloop()