from tkinter import *
from tkinter import font
from tkinter import ttk

import serial
import serial.tools.list_ports
import time

# version 1.1   2017-09-21      AA
# version 1.2   2019-08-15      AA
#   added a few comments for publication and update to retraction length mapping (15->30mm)

arduinoPort = "/dev/cu.usbmodem1411"

# the port should be detected automatically.  what you should use as default when it is not
# auto-detected will vary by OS.

all_ports = list(serial.tools.list_ports.comports()) # list of a 3-tuple for each port
ports = [(port, desc) for port, desc, hwid in all_ports if "Arduino" in desc]
if len(ports) > 0:
    arduinoPort, arduinoDesc = ports[0]
    print("Detected port: %s (%s)" % (arduinoPort, arduinoDesc))
else:
    print("Could not auto-detect port. Using %s as default." % arduinoPort)
    print("Ports:")
    print(all_ports)

ser = serial.Serial(arduinoPort, 9600)

def go(*args):
    try:
        speeds = ['null','a','b','c','d','e','f']
        spdi = int(speed.get())
        spd = speeds[spdi]
        pos = coord.get()
     
        cmd = format("%d%s" % (pos,spd))

        command.set(cmd)
        iibyte=bytearray(cmd,'ascii')
        ser.write(iibyte)
        #        print(ii)
        print(iibyte)
    except ValueError:
        pass

def zero(*args):
    try:
        speeds = ['null','a','b','c','d','e','f']
        spdi = int(speed.get())
        spd = speeds[spdi]
        pos = 0
        
        cmd = format("%d%s" % (pos,spd))
        
        command.set(cmd)
        iibyte=bytearray(cmd,'ascii')
        ser.write(iibyte)
    except ValueError:
        pass

def repeat(*args):
    try:
        repeati=int(repeats.get());
        zero()
        time.sleep(3)
        
        for i in range(0,repeati):
            print(i)
            go()
            time.sleep(3)
            zero()
            time.sleep(3)
    except ValueError:
        pass

root = Tk()
root.title("Crayfish MRO puller interface")

command = StringVar()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

headFont = font.Font(family='Helvetica', size=16, weight='bold')
smallFont = font.Font(family='Helvetica', size=8)

porty = StringVar()
porty = "Arduino on port: %s" % arduinoPort
ttk.Label(mainframe, text=porty).grid(column=1, row=8, columnspan=4)

ttk.Label(mainframe, textvariable=command).grid(column=1, row=6, sticky=S, columnspan=4)

speed = DoubleVar()
speedframe = ttk.Labelframe(mainframe, text='Speed')
slider = Scale(speedframe, orient=HORIZONTAL, variable=speed, length=100, from_=1, to=6, resolution=1).grid(column=1, row=2)
ttk.Label(speedframe, text="(6 being fastest)").grid(column=1, row=4, sticky=N)
speed.set(3)
speedframe.grid(column=1,row=1,columnspan=4)

# the Arduino will translate this coordinate to a position on a 90 degree arc of the servo's range.
# The actual retraction length this corresponds to will depend on the length of the arm mounted to the servo.

coord = DoubleVar()
coordframe = ttk.Labelframe(mainframe, text='Retraction')
slider = Scale(coordframe, orient=HORIZONTAL, variable=coord, length=250, from_=0, to=30, resolution=1).grid(column=1, row=2)
ttk.Label(coordframe, text="from 0 to ~30 mm").grid(column=1, row=4, sticky=N)
coord.set(0)
coordframe.grid(column=1,row=2,columnspan=4)

ttk.Button(mainframe, text="go", command=go).grid(column=1, row=9, sticky=W)
ttk.Button(mainframe, text="repeat", command=repeat).grid(column=2, row=9, sticky=E)

repeats = DoubleVar()
repeatentry = ttk.Entry(mainframe, textvariable=repeats, width=2).grid(column=3, row=9, sticky=E)
repeats.set(3)
ttk.Label(mainframe, text="repeats").grid(column=4, row=9, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.bind('<Return>', go)

root.mainloop()