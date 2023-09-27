import tkinter as tk
import xml.etree.ElementTree as ET
# import lxml.etree as ET


class InputContextEditor:
    def __init__(self, win):
        # Initialize inputcontext file
        self.inputcontextfile = 'inputContexts.xml'
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

        # Initialize the Status Message
        self.b1 = tk.Button(win, text='Update', command=self.update)
        self.b1.place(x=100, y=100, width=130)
        self.b2 = tk.Button(win, text='Write Data', command=self.writedata)
        self.b2.place(x=100, y=125, width=130)
        self.parseXML(self.inputcontextfile)

    def update(self):
        self.parseXML(self.inputcontextfile)

    def writedata(self):
        disassemble_time = self.t1.get()
        craft_time = self.t2.get()
        self.parseXML(self.inputcontextfile,disassemble_time,craft_time)
    
    def updatestatus(self,statustext):
        self.statustext.set(statustext)


    def parseXML(self, file, dtime=None,ctime=None):
        parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
        self.updatestatus('Reading XML File')
        disassemble_time = 0
        craft_time = 0
        tree = ET.parse(file,parser)
        statustext = 'Finished reading XML File'

        for node in tree.findall('hold'):
            if node.attrib['action'] == 'disassemble_item':
                disassemble_time = node.attrib['timeout']
                if dtime:
                    node.attrib['timeout'] = dtime
            if node.attrib['action'] == 'craft_item':
                craft_time = node.attrib['timeout']
                if ctime:
                    node.attrib['timeout'] = ctime

        if dtime or ctime:
            tree.write('inputContexts2.xml')
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
