import tkinter as tk
from PIL import ImageTk, Image
from functions import *
from helper import config, version
from setting_window import *
from config import load_config
import os

# set direct
class MainWindow:
    def allow(self):
        file_path = tk.filedialog.askopenfilename()
        file_path = file_path.replace('/', '\\')
        if file_path:
            config = load_config()
            set_rule(file_path, action='allow', direction=(config['direction']))

    def block(self):
        file_path = tk.filedialog.askopenfilename()
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

        label_picture_krause = tk.Label(image=picture_krause)
        label_picture_krause.image = picture_krause
        label_picture_krause.pack()

        # create allow button
        buttonAllow = tk.Button(self.root, text='Zuslassen', bg='green', fg='black', command=self.allow)
        buttonAllow.configure(width=20)
        buttonAllow.place(x=50, y=810)

        # create block button
        buttonBlock = tk.Button(self.root, text='Blockieren', bg='red', fg='black', command=self.block)
        buttonBlock.configure(width=20)
        buttonBlock.place(x=200, y=810)


        #
        # settings Button
        buttonSettings = tk.Button(self.root, text='Einstellungen', fg='black', command=lambda: SettingsWindow(self.root))
        buttonSettings.configure(width=20)
        buttonSettings.place(x=400, y=810)

    def start(self):
        self.root.mainloop()  # start monitoring and updating the GUI