import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog

import PIL.Image
from PIL import Image, ImageTk
from functions import *
from helper import config, version
from config import change_config, load_config
import os

# set direct
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))

# root
root = tk.Tk()
root.title(f'Firewallhausmeister {version}')
root.geometry('400x800')
root.minsize(width=600, height=850)


image = Image.open('recources/Krause.png')
photo = ImageTk.PhotoImage(image)


labelKrause = ttk.Label(root, image=photo)
labelKrause.configure(font=('Arial', 10))
labelKrause.pack()

#deny button

def zulassen():
    file_path = filedialog.askopenfilename()
    file_path = file_path.replace('/', '\\')
    if file_path:
        config = load_config()
        set_rule(file_path, action='allow', direction=(config['direction']))

buttonAllow = tk.Button(root, text='Zuslassen',bg='green', fg='black', command=zulassen)
buttonAllow.configure(width=20)
buttonAllow.place(x=50, y=810)

# allow button
def block():
    file_path = filedialog.askopenfilename()
    file_path = file_path.replace('/', '\\')
    if file_path:
        config = load_config()
        set_rule(file_path, action='block', direction=(config['direction']))

buttonBlock = tk.Button(root, text='Blockieren', bg='red', fg='black', command=block)
buttonBlock.configure(width=20)
buttonBlock.place(x=200, y=810)


#for item in labelKrause.keys():
#    print(item, ': ', labelKrause[item])

# settings menu
def openSettingsWindow():
    config = load_config()
    Settings = tk.Toplevel(root)

    # Toplevel widget
    Settings.title("Einstellungen")

    Settings.geometry("200x200")

    tk.Label(Settings,
          text="Einstellungen").pack()


    settings_button_dict={}



    current_direction = tk.StringVar()
    current_direction.set(f'Richtung: ' + config['direction'])


    # change settings and update
    def update(key, value):
        for key in settings_button_dict:
            settings_button_dict[key].set(f'Richtung: ' + value)

    label_current_direction = tk.Label(Settings, textvariable=current_direction)
    label_current_direction.pack()

    def change_config_button(key,value):
        change_config(key, value)
        update(key, value)


    # settings for directions

    settings_button_dict['direction'] = current_direction


    buttonIn = tk.Button(Settings, text='In', fg='black', command=lambda: change_config_button('direction','in'))
    buttonIn.configure(width=20)
    buttonIn.pack()

    buttonOut = tk.Button(Settings, text='Out', fg='black', command=lambda: change_config_button('direction','out'))
    buttonOut.configure(width=20)
    buttonOut.pack()

    buttonBoth = tk.Button(Settings, text='Both', fg='black', command=lambda: change_config_button('direction','both'))
    buttonBoth.configure(width=20)
    buttonBoth.pack()



    tk.Label(Settings,
             text="Extras:").pack()

    # Knopf TImos mom
    def open_image_mom():
        '''
        MutterBild = tk.Toplevel(Settings)
        MutterBild.geometry("1080x1184")

        MutterBild.title("La creatura")

        image_mutter = Image.open('recources/timos_mutter.png')
        photo_mutter = ImageTk.PhotoImage(image_mutter)

        label = ttk.Label(MutterBild,image=photo_mutter)
        label.pack()
        '''
        im = PIL.Image.open('recources/timos_mutter.png')
        im.show()

    buttonMoM = tk.Button(Settings, text='Bild von deiner Mutter!', fg='black', command=open_image_mom)
    buttonMoM.configure(width=20)
    buttonMoM.pack()


# settigns Button

buttonSettings = tk.Button(root, text='Einstellungen', fg='black', command=openSettingsWindow)
buttonSettings.configure(width=20)
buttonSettings.place(x=400, y=810)



root.mainloop()
#root.withdraw()