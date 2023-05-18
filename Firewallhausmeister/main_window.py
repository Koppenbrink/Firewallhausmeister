import tkinter as tk
import tkinter.filedialog
from PIL import ImageTk, Image
from functions import *
from helper import config, version
from setting_window import *
from verwaltung import *
from config import load_config
import os

# set direct
class MainWindow:
    def allow(self):
        file_path = tkinter.filedialog.askopenfilename()
        file_path = file_path.replace('/', '\\')
        if file_path:
            config = load_config()
            set_rule(file_path, action='allow', direction=(config['direction']))

    def block(self):
        file_path = tkinter.filedialog.askopenfilename()
        file_path = file_path.replace('/', '\\')
        if file_path:
            config = load_config()
            set_rule(file_path, action='block', direction=(config['direction']))
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f'Firewallhausmeister {version}')
        self.root.geometry('400x800')
        self.root.minsize(width=600, height=850)


        # create background img:
        picture_krause = Image.open("resources/Krause.png")
        picture_krause = ImageTk.PhotoImage(picture_krause)

        label_picture_krause = tk.Label(self.root,image=picture_krause)
        label_picture_krause.image = picture_krause
        label_picture_krause.pack()

        # create allow button
        button_verwaltung = tk.Button(self.root, text='Verwaltung', fg='black', command=lambda:VerwaltungsFenster(self.root))
        button_verwaltung.configure(width=20)
        button_verwaltung.place(x=0, y=810)

        # create allow button
        buttonAllow = tk.Button(self.root, text='Zuslassen', bg='green', fg='black', command=self.allow)
        buttonAllow.configure(width=20)
        buttonAllow.place(x=150, y=810)

        # create block button
        buttonBlock = tk.Button(self.root, text='Blockieren', bg='red', fg='black', command=self.block)
        buttonBlock.configure(width=20)
        buttonBlock.place(x=300, y=810)


        # settings Button
        buttonSettings = tk.Button(self.root, text='Einstellungen', fg='black', command=lambda: SettingsWindow(self.root))
        buttonSettings.configure(width=20)
        buttonSettings.place(x=450, y=810)

    def start(self):
        self.root.mainloop()  # start monitoring and updating the GUI