# Selection Panel Generator By Tamas Nagy
# Date: 2016.11.22  Version: V.03
# Made in Hungary 6000 Kecskemet
# Kecskemetfilm Ltd.


import maya.cmds as cmds # Import maya commands
import Tkinter as tk
from Tkinter import *
import tkFileDialog
import pickle # Import save load commands
from tkColorChooser import askcolor # Import color picker

class ExampleApp:
    def __init__(self, parent):
        global main_dict  # Stores the rectangle`s data like : color, selected item, cordinates
        global appASD # Here goes te loaded file
        self.appASD = {}
        main_dict = {}
        self.Rid = 1 # Gives the object ID
        self.parent = parent
        self.ColorBase = "red" # Basic rectangle color
        self.i = 1
        self.x = self.y = 0
# ------------------------------------------------------------------------------------------------------------------------------------
        self.canvas = tk.Canvas(self.parent, width=600, height=800, cursor="cross", bg = "Black")  # Canvas options
        self.canvas.pack()
        self.canvas.bind("<ButtonPress-2>", self.on_button_press)
        self.canvas.bind("<ButtonRelease-2>", self.on_button_release)  # With middle button you create a rectangle and save its attributs
        self.canvas.bind("<ButtonPress-1>", self.click)  # Check the id and select the connected object, with left click
        Widget.bind(self.canvas, "<3>", self.mouseDown)
        Widget.bind(self.canvas, "<B3-Motion>", self.mouseMove)  # With right click move the rectangle and update the dict with te new position
        self.canvas.bind("<Shift-ButtonPress-1>", self.click_plus)  # With shift add the selected object to a list
# ------------------------------------------------------------------------------------------------------------------------------------
        self.button= tk.Button(self.parent,text="SAVE", width=10, bg='white', command=self.Save_Dict)  # Save the dict
        self.button.place(x=100 / 7, y=30 + 20)
        self.button = tk.Button(self.parent, text="LOAD", width=10, bg='white', command=self.Load_Dict)  # Load the dict
        self.button.place(x=100 / 7, y=60 + 20)
        self.button = tk.Button(self.parent, text='Select Color', width=10, bg='white', command=self.getColor)  # Select color from palette
        self.button.place(x=100 / 7, y=90 + 20)
        self.button = tk.Button(self.parent, text='Reset Selected', width=10, bg='white', command=self.RESET_SELECTED)  # Reset base pose the selected objects
        self.button.place(x=100 / 7, y=120 + 20)
# -----------------------------------------------------------------------------------------------------------------------------------
        self.aMenu = tk.Menu(self.parent, tearoff = 0)  # Right Click menu options
        self.aMenu.add_command(label="Delete", command =self.del_object)
        self.aMenu.add_command(label="Move Up", command =self.widget_up)
        self.aMenu.add_command(label="Move Down", command=self.widget_down)
        self.canvas.bind("<Shift-Button-3>", self.popup)
# -----------------------------------------------------------------------------------------------------------------------------
        self.rubberbandBox = None
        self.canvas.bind("<Shift-ButtonPress-2>", self.mouseDown)
        self.canvas.bind("<Shift-B2-Motion>", self.ruber_band_selection)
        self.canvas.bind("<Shift-ButtonRelease-2>", self.mouseUp_er)

    def ruber_band_selection(self, event):
        self.x2 = self.canvas.canvasx(event.x)
        self.y2 = self.canvas.canvasy(event.y)

        if (self.lastx != event.x) and (self.lasty != event.y):
            self.canvas.delete(self.rubberbandBox)
            self.rubberbandBox = self.canvas.create_rectangle(
                self.lastx, self.lasty, self.x2, self.y2)
            self.canvas.update_idletasks()

    def mouseUp_er(self, event):
        under = self.canvas.find_overlapping(self.lastx, self.lasty, self.x2, self.y2)
        print under
        self.canvas.delete(self.rubberbandBox)

    def del_object(self):
        print "meh"

    def widget_up(self):
        self.canvas.tag_raise(CURRENT)

    def widget_down(self):
        self.canvas.tag_lower(CURRENT)

    def popup(self, event):
        self.aMenu.post(event.x_root, event.y_root)

    def Get_Selected(self):
        # Get the name of the selected maya object
        sel = cmds.ls(sl = 1)
        print sel
        return sel

    def Save_Dict(self):
        # Save the dict in a file
        root.filename = tkFileDialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("P files", "*.p"),("all files", "*.*")))
        f = open(root.filename, 'w')
        pickle.dump(main_dict, f)
        f.close()

    def getColor(self):
        color = askcolor()
        self.ColorBase = color[1]

    def click_plus(self, event):
        self.tg = self.canvas.gettags(CURRENT)[0]
        print self.tg
        if str(self.tg) in main_dict:
            cmds.select(main_dict[str(self.tg)][0], add = True)

    def RESET_SELECTED(self):
        attrVsDefaultValue = {'sx': 1, 'sy': 1, 'sz': 1, 'rx': 0, 'ry': 0, 'rz': 0, 'tx': 0, 'ty': 0, 'tz': 0}

        sel = cmds.ls(sl=1)
        for obj in sel:
            for attr in attrVsDefaultValue:
                try:
                    cmds.setAttr('%s.%s' % (obj, attr), attrVsDefaultValue[attr])
                except:
                    pass

    def click(self, event):
        self.tg = self.canvas.gettags(CURRENT)[0]
        print self.tg
        if str(self.tg) in main_dict:
            cmds.select(main_dict[str(self.tg)][0])


    def mouseDown(self, event):
        # Get the Mouse position
        self.lastx = event.x
        self.lasty = event.y

    def mouseMove(self, event):
        # whatever the mouse is over gets tagged as CURRENT for free by tk.
        self.canvas.move(CURRENT, event.x - self.lastx, event.y - self.lasty)
        self.lastx = event.x
        self.lasty = event.y
        self.tg = self.canvas.gettags(CURRENT)[0]
        POZI = self.canvas.coords(CURRENT) # After move the new cordinates to the object
        self.new = {} # New attributes of the moved rectangle
        for i, v in enumerate(main_dict):
            if str(self.tg) == v:
                self.new = {v : (main_dict[v][0], POZI[0], POZI[1], POZI[2], POZI[3], main_dict[v][5])}
                main_dict.update(self.new)

    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_button_release(self, event):
        # Create the rectangle and saves the attributes in a dict
        x0, y0 = (self.x, self.y)
        x1, y1 = (event.x, event.y) # Mouse positions
        while str(self.Rid) in main_dict:
            self.Rid = self.Rid + 1
        event.widget.create_rectangle(x0, y0, x1, y1, fill=self.ColorBase, outline ='', tag = str(self.Rid) ) # Rectangle creation
        self.appASD = {str(self.Rid) : (self.Get_Selected(), x0, y0, x1, y1, self.ColorBase)} # Current rectangle attributes
        main_dict.update(self.appASD) # Add the Current rectangle to the main dict
        self.Rid = self.Rid + 1
        print main_dict

    def Load_Dict(self):
        # Load a saved file
        root.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("P files", "*.p"),("all files", "*.*")))
        new_dict = pickle.load(open (root.filename, "rb"))
        main_dict.clear()
        main_dict.update(new_dict)
        for a in main_dict:
            self.canvas.create_rectangle(main_dict[a][1], main_dict[a][2], main_dict[a][3], main_dict[a][4],  outline='', fill=main_dict[a][5], tag =a)

if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (400, 400, 10, 10))
    root.config(bg='white')
    ExampleApp(root)
    root.mainloop()