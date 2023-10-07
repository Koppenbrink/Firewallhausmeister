import tkinter as tk
import tkinter.filedialog
from PIL import ImageTk, Image
from functions import *
from helper import config, version
from setting_window import *
from verwaltung import *
from config import change_config, load_config
import os,sys,json


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#
Logo = resource_path("Krause.png")
icon = resource_path("icon.ico")
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
        self.root.geometry('600x800')
        #self.root.minsize(width=600, height=850)
        self.width = 600
        self.height = 800

        self.root.iconbitmap(resource_path(icon))



        # create background img:
        load = Image.open(resource_path(Logo))
        picture_krause = ImageTk.PhotoImage(load)


        '''label_picture_krause = tk.Label(self.root,image=picture_krause)
        label_picture_krause.image = picture_krause
        label_picture_krause.place(x=0,y=0,relwidth=1,relheight=1)
        '''
        # create canvas
        main_window_canvas = tk.Canvas(self.root,width=600,height=800)
        main_window_canvas.pack(fill="both",expand=True)

        # set img in canvas
        main_window_canvas.create_image(0,0,image = picture_krause,anchor="nw")
            # important because of garbage collection
        main_window_canvas.idk = picture_krause

        # add a label
        main_window_canvas.create_text(400,250,text="Welcome",font=("Helvetica",50),fill="white")

        # add buttons
        button_verwaltung = tk.Button(self.root, text='Verwaltung', fg='black', command=lambda:VerwaltungsFenster(self.root))
        buttonAllow = tk.Button(self.root, text='Zuslassen', bg='green', fg='black', command=self.allow)
        buttonBlock = tk.Button(self.root, text='Blockieren', bg='red', fg='black', command=self.block)
        buttonSettings = tk.Button(self.root, text='Einstellungen', fg='black', command=lambda: SettingsWindow(self.root))

        # button window
        button_verwaltung_window = main_window_canvas.create_window(0,775,anchor="nw",window=button_verwaltung)
        buttonAllow_window = main_window_canvas.create_window(100,775,anchor="nw",window=buttonAllow)
        buttonBlock_window = main_window_canvas.create_window(200,775,anchor="nw",window=buttonBlock)
        buttonSettings = main_window_canvas.create_window(300,775,anchor="nw",window=buttonSettings)


        def resizer(e):
            global button_verwaltung, buttonAllow, buttonBlock, buttonSettings
            # open image
            picture_krause_1 = Image.open(resource_path(Logo))
            # resize image
            picture_krause_resized = picture_krause_1.resize(((e.width), (e.height)), Image.ANTIALIAS)
            # def img again
            new_back_ground = ImageTk.PhotoImage(picture_krause_resized)
            # add back to canvas
            main_window_canvas.create_image(0, 0, image=new_back_ground, anchor="nw")
            # important because of garbage collection
            main_window_canvas.idk = new_back_ground


        self.root.bind('<Configure>', resizer)


    def start(self):
        self.root.mainloop()  # start monitoring and updating the GUI


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))


    main_window = MainWindow()
    main_window.start()