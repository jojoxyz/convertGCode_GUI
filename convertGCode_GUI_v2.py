from tkinter import *
from tkinter import filedialog

import math
import sys

## okno
ws = Tk()
ws.title("PythonGuides")
ws.geometry("410x500")     
ws['bg']='#003d4d'         

############# adding label

Label(
    ws, 
    text=" Laser Show ",
    fg = "light green",
    bg = "dark green",
    font = "Helvetica 16 bold italic"
    ).place(x=34, y=10,)

Label(
    ws, 
    text="G code",
    fg = "light green",
    bg = "#003d4d",
    font = "Verdana 12 bold"
    ).place(x=271, y=10,)
    
Label(
    ws, 
    text="to",
    fg = "light green",
    bg = "#003d4d",
    font = "Verdana 10 bold"
    ).place(x=294, y=30,)    

Label(
    ws, 
    text="hex Convertor",
    fg = "light green",
    bg = "#003d4d",
    font = "Verdana 12 bold"
    ).place(x=238, y=47,)


############# how to
Label(
    ws, 
    text="Correct form :  Input",
    fg = "#0ac200",
    bg = "#003d4d",
    font = "Verdana 8 bold"
    ).place(x=210, y=80,)


Label(
    ws, 
    text="G00        (Laser off)",
    fg = "#0ac200",
    bg = "#003d4d",
    font = "Verdana 8"
    ).place(x=210, y=95,)

Label(
    ws, 
    text="X10 Y20  (diagonal move)",
    fg = "#0ac200",
    bg = "#003d4d",
    font = "Verdana 8"
    ).place(x=210, y=110,)

Label(
    ws, 
    text="G01        (Laser ON)",
    fg = "#0ac200",
    bg = "#003d4d",
    font = "Verdana 8"
    ).place(x=210, y=125,)

Label(
    ws, 
    text="X50 Y20  (horisontal line 40 mm)",
    fg = "#0ac200",
    bg = "#003d4d",
    font = "Verdana 8"
    ).place(x=210, y=140,)

Label(
    ws, 
    text="Incorrect form :  Input",
    fg = "#eb0000",
    bg = "#003d4d",
    font = "Verdana 8 bold"
    ).place(x=210, y=165,)

Label(
    ws, 
    text="G00 X10 Y20",
    fg = "#eb0000",
    bg = "#003d4d",
    font = "Verdana 8"
    ).place(x=210, y=180,)

Label(
    ws, 
    text="G01 X50 Y20",
    fg = "#eb0000",
    bg = "#003d4d",
    font = "Verdana 8"
    ).place(x=210, y=195,)


Label(
    ws, 
    text="1. Open File",
    fg = "#e6de00",
    bg = "#003d4d",
    font = "Verdana 7"
    ).place(x=215, y=220,)

Label(
    ws, 
    text="automatic conversion",
    fg = "#e6de00",
    bg = "#003d4d",
    font = "Verdana 7"
    ).place(x=230, y=235,)

Label(
    ws, 
    text="3. Save File to",
    fg = "#e6de00",
    bg = "#003d4d",
    font = "Verdana 7"
    ).place(x=215, y=260,)

################### converter ####################

def createObject(name, cmds):
  minx = miny = 10000000
  maxx = maxy = 0
  string = ""
  for cmd in cmds:
    if cmd[0] == 2:
      minx = min(minx,cmd[1])
      miny = min(miny,cmd[2])
      maxx = max(maxx,cmd[1])
      maxy = max(maxy,cmd[2])

  string += "const unsigned short draw_" + name + "[] PROGMEM = {\n";
  laserState = False
  
  biggestSide = max(maxx-minx, maxy-miny)

################### scale to the laser range max 4095

  scale = 1500. / biggestSide;

  print ("bounding box x: ", minx, maxx)
  print ("bounding box y: ", miny, maxy)
  print ("scale: ", scale)
  for cmd in cmds:
    if cmd[0] == 0:laserState = False
    if cmd[0] == 1:laserState = True
    if cmd[0] == 2:
      x = int(math.floor((cmd[1]-minx) * scale))
      y = int(math.floor((cmd[2]-miny) * scale))
      if laserState:
        x += 0x8000
      string += hex(x) + "," + hex(y) + ",\n"
  string += "};\n"
  return string
  
##################################################


#################### open file ###################
 
def openFile():
    tf = filedialog.askopenfilename(
        initialdir="C:/Users/MainFrame/Desktop/", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.*"),)
        )
    pathh.insert(END, tf)
    tf = open(tf)

    lines = tf.readlines()
    drawing = False 
    posx = posy = 0.

    cmds = [] 
    for l in lines:
      if l.startswith("G00"):
        if drawing: 
          cmds.append((0,))
        drawing = False 
      elif l.startswith("G01"):
        drawing = True 
        cmds.append((1,))
      elif l.startswith("X"):
        parts = l.split("Y")
        newposx = float(parts[0][1:])
        newposy = float(parts[1])
        cmds.append((2,newposx,newposy))
        posx = newposx
        posy = newposy

    result = createObject("object", cmds)

    file_cont = tf.read()                   # read converted result 
    txtarea.insert(END, result)             # write converted result to text space


    tf.close()

################################################


################ save file ####################

def saveFile():
    tf = filedialog.asksaveasfile(
        mode='w',

        title ="Save file",
        defaultextension=".cpp"
        )
   # tf.config(mode='w')

    pathh.insert(END, tf)
    result = str(txtarea.get(1.0, END))
    tf.write(result) 
   
    tf.close()


###############################################


############# adding frame
frame = Frame(ws)
frame.place(x=10, y=50)                         

############# adding scrollbars 
ver_sb = Scrollbar(frame, orient=VERTICAL )
ver_sb.pack(side=RIGHT, fill=BOTH)

hor_sb = Scrollbar(frame, orient=HORIZONTAL)
hor_sb.pack(side=BOTTOM, fill=BOTH)

############# adding writing space
txtarea = Text(frame, width=21, height=23)      
txtarea.pack(side=LEFT)

############# binding scrollbar with text area
txtarea.config(yscrollcommand=ver_sb.set)
ver_sb.config(command=txtarea.yview)

txtarea.config(xscrollcommand=hor_sb.set)
hor_sb.config(command=txtarea.xview)

############# adding path showing box
pathh = Entry(ws)
pathh.place(x=10, y=460, width=390)

############# adding scalng box
#pathh = Entry(ws)
#pathh.place(x=10, y=460, width=380)


############# add buttons
#Button(
#    ws, 
#    text="Scale Size",
#    width = 20,
#    height = 1, 
#    background = "#a8a305",            
#    foreground = "#47e7ff",               
   # command=openFile
#    ).place(  x=224,  y=230)

Button(
    ws, 
    text="Open File",
    width = 20,
    height = 1, 
    background = "#6e3dff",                
    foreground = "#47e7ff",                
    command=openFile
    ).place(  x=230,  y=300)

############# file types
Label(
    ws, 
    text=".txt   .gcode   .nc",
    fg = "light green",
    bg = "#003d4d",
    font = "Verdana 7"
    ).place(x=256, y=326,)


Button(
    ws, 
    text="Save File",
    width = 20,
    height = 1, 
    background = "#237713",                   
    foreground = "#47e7ff",                  
    command=saveFile
    ).place(  x=230,  y=360)

Button(
    ws, 
    text="Exit",
    width = 20,
    height = 1, 
    background = "#ff1f1f",                 
    foreground = "#f4ff1f",                 
    command=lambda:ws.destroy()
    ).place(  x=230,  y=414)



ws.mainloop()