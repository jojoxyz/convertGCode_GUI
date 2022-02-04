from tkinter import *
from tkinter import filedialog

import math
import sys


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
  # scale to the laser range
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
        filetypes=(("Text Files", "*.txt"),)
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

ws = Tk()
ws.title("PythonGuides")
ws.geometry("400x500")
ws['bg']='#2a636e'

# adding frame
frame = Frame(ws)
frame.pack(pady=20)

# adding scrollbars 
ver_sb = Scrollbar(frame, orient=VERTICAL )
ver_sb.pack(side=RIGHT, fill=BOTH)

hor_sb = Scrollbar(frame, orient=HORIZONTAL)
hor_sb.pack(side=BOTTOM, fill=BOTH)

# adding writing space
txtarea = Text(frame, width=40, height=20)
txtarea.pack(side=LEFT)

# binding scrollbar with text area
txtarea.config(yscrollcommand=ver_sb.set)
ver_sb.config(command=txtarea.yview)

txtarea.config(xscrollcommand=hor_sb.set)
hor_sb.config(command=txtarea.xview)

# adding path showing box
pathh = Entry(ws)
pathh.pack(expand=True, fill=X, padx=10)

# adding buttons 
Button(
    ws, 
    text="Open File", 
    command=openFile
    ).pack(side=LEFT, expand=True, fill=X, padx=20)

Button(
    ws, 
    text="Save File", 
    command=saveFile
    ).pack(side=LEFT, expand=True, fill=X, padx=20)

Button(
    ws, 
    text="Exit", 
    command=lambda:ws.destroy()
    ).pack(side=LEFT, expand=True, fill=X, padx=20, pady=20)

ws.mainloop()