import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from functions import set_rule
from helper import *
from config import change_config

# root
root = tk.Tk()
root.title(f'Firewallhausmeister {version}')
root.geometry('400x800')
root.minsize(width=600, height=850)


image = Image.open('./Krause.png')
photo = ImageTk.PhotoImage(image)


strVar = tk.StringVar()
strVar.set('Dreck!')


labelKrause = ttk.Label(root, textvariable=strVar, image=photo)
labelKrause.configure(font=('Arial', 10))
labelKrause.pack()

#deny button

def zulassen():
    file_path = filedialog.askopenfilename()
    file_path = file_path.replace('/', '\\')
    if file_path:
        set_rule(file_path, action='allow', direction='both')

buttonAllow = tk.Button(root, text='Zuslassen',bg='green', fg='black', command=zulassen)
buttonAllow.configure(width=20)
buttonAllow.place(x=50, y=810)

# allow button
def block():
    file_path = filedialog.askopenfilename()
    file_path = file_path.replace('/', '\\')
    if file_path:
        set_rule(file_path, action='block', direction='both')

buttonBlock = tk.Button(root, text='Blockieren', bg='red', fg='black', command=block)
buttonBlock.configure(width=20)
buttonBlock.place(x=200, y=810)


#for item in labelKrause.keys():
#    print(item, ': ', labelKrause[item])

# settings menu
def openSettingsWindow():
    Settings = tk.Toplevel(root)

    # sets the title of the
    # Toplevel widget
    Settings.title("Einstellungen")

    # sets the geometry of toplevel
    Settings.geometry("200x200")

    # A Label widget to show in toplevel
    tk.Label(Settings,
          text="Direction").pack()

    current_direction = tk.StringVar()
    current_direction.set(f'Richtung: ' + config['direction'])

    label_current_direction = tk.Label(Settings, textvariable=current_direction)
    label_current_direction.pack()


    buttonIn = tk.Button(Settings, text='In', fg='black', command=lambda: change_config('direction','in'))
    buttonIn.configure(width=20)
    buttonIn.pack()

    buttonOut = tk.Button(Settings, text='Out', fg='black', command=lambda: change_config('direction','out'))
    buttonOut.configure(width=20)
    buttonOut.pack()

    buttonBoth = tk.Button(Settings, text='Both', fg='black', command=lambda: change_config('direction','both'))
    buttonBoth.configure(width=20)
    buttonBoth.pack()




buttonSettings = tk.Button(root, text='Einstellungen', fg='black', command=openSettingsWindow)
buttonSettings.configure(width=20)
buttonSettings.place(x=400, y=810)





root.mainloop()
#root.withdraw()