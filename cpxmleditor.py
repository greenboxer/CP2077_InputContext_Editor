import tkinter as tk
import xml.etree.ElementTree as ET
import os.path as PATH
import time
# import lxml.etree as ET


class InputContextEditor:
    def __init__(self, win):
        # Initialize the Disassemble time label and entry 
        self.lbl1 = tk.Label(win, text='Disassemble Time')
        self.lbl1.place(x=96, y=50)
        self.t1 = tk.Entry(justify='center')
        self.t1.place(x=200, y=50, width=30)

        # Initialize the Craft time label and entry
        self.lbl2 = tk.Label(win, text='Craft Time')
        self.lbl2.place(x=135, y=70)
        self.t2 = tk.Entry(justify='center')
        self.t2.place(x=200, y=70, width=30)

        # Initialize the Status Message
        self.statustext = tk.StringVar()
        self.statustext.set('Status: Initialized')
        self.lbl3 = tk.Label(win, textvariable=self.statustext)
        self.lbl3.place(x=100, y=170)

        # Initialize inputcontext file - should probably update to check in different directories steam/gog
        contextfilename = 'inputContexts.xml'
        steampath = 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Cyberpunk 2077\\r6\\config\\'
        gogpath = 'C:\\Program Files (x86)\\GOG Galaxy\\Games\\Cyberpunk 2077\\r6\\config\\'
        if PATH.isfile(steampath + contextfilename):
            self.inputcontextfile = steampath + contextfilename
        elif PATH.isfile(gogpath + contextfilename):
            self.inputcontextfile = gogpath + contextfilename
        else:
            self.updatestatus('Can\'t Find inputContexts.xml')
            return
        
        # Initialize the Status Message
        self.b1 = tk.Button(win, text='Update', command=self.update)
        self.b1.place(x=100, y=100, width=130)
        self.b2 = tk.Button(win, text='Write Data', command=self.writedata)
        self.b2.place(x=100, y=125, width=130)
        self.parseXML(self.inputcontextfile)

    # Just needed a method to refresh values
    def update(self):
        self.parseXML(self.inputcontextfile)

    # Pulls the current input values for entries t1 and t2, then calls parseXML to write
    def writedata(self):
        disassemble_time = self.t1.get()
        craft_time = self.t2.get()
        self.parseXML(self.inputcontextfile,disassemble_time,craft_time)

    # Just in case we want to update the status text from anywhere and do other stuff
    def updatestatus(self,statustext):
        self.statustext.set(statustext)

    # Parses the xml, without dtime and ctime input arguments, will simply read the xml file
    def parseXML(self, file, dtime=None,ctime=None):
        # Sets custom parser to preserve xml file comments
        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        
        # Reads XML file, should probably set to try and except reading and break and have status message if error
        self.updatestatus('Reading XML File')
        tree = ET.parse(file,parser)
        statustext = 'Finished reading XML File'

        # Reads the parsed XML to look for disassemble and craft item times.
        for node in tree.findall('hold'):
            if node.attrib['action'] == 'disassemble_item':
                disassemble_time = node.attrib['timeout']
                if dtime:
                    node.attrib['timeout'] = dtime
            if node.attrib['action'] == 'craft_item':
                craft_time = node.attrib['timeout']
                if ctime:
                    node.attrib['timeout'] = ctime

        # If we have a set dtime/ctime - write the values - should update to self.inputcontextfile
        if dtime or ctime:
            tree.write(self.inputcontextfile)
            statustext = 'Finished writing XML File'
        
        self.t1.delete(0, 'end')
        self.t2.delete(0, 'end')
        self.t1.insert(0,str(disassemble_time))
        self.t2.insert(0,str(craft_time))
        self.updatestatus(statustext)

        return

window = tk.Tk()
EditorWindow = InputContextEditor(window)
window.title('Cyberpunk 2077 Input Context Editor')
window.geometry("340x300+10+10")
window.mainloop()