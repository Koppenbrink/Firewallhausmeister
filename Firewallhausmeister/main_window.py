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
        #self.root.minsize(width=600, height=850)
        self.width = 625
        self.height = 825
        self.root.geometry(f'{self.width}x{self.height}')

        self.root.iconbitmap(resource_path(icon))

        # get firewall status
        command = f'netsh advfirewall show allprofiles state'
        output = subprocess.check_output(command,text=True)


        firewall_states = [row.split()[1] for row in output.split("\n") if "State" in row]




        # create background img:
        load = Image.open(resource_path(Logo))
        picture_krause = ImageTk.PhotoImage(load)


        '''label_picture_krause = tk.Label(self.root,image=picture_krause)
        label_picture_krause.image = picture_krause
        label_picture_krause.place(x=0,y=0,relwidth=1,relheight=1)
        '''
        # create canvas
        main_window_canvas = tk.Canvas(self.root,width=600,height=800,scrollregion=(0, 0, 600, 800))
        main_window_canvas.pack(fill="both",expand=True)


        # set img in canvas
        main_window_canvas.create_image(0,0,image = picture_krause,anchor="nw")
            # important because of garbage collection
        main_window_canvas.idk = picture_krause

        #scrollbar
        vbar = tk.Scrollbar(self.root, orient="vertical")
        vbar.pack(side="right", fill="y")
        vbar.config(command=main_window_canvas.yview)
        main_window_canvas.config(yscrollcommand=vbar.set)
        main_window_canvas.pack(side="left", expand=True, fill="both")

        # add buttons
        button_verwaltung = tk.Button(self.root, text='Verwaltung', fg='black', command=lambda:VerwaltungsFenster(self.root))
        buttonAllow = tk.Button(self.root, text='Zuslassen', bg='green', fg='black', command=self.allow)
        buttonBlock = tk.Button(self.root, text='Blockieren', bg='red', fg='black', command=self.block)
        buttonSettings = tk.Button(self.root, text='Einstellungen', fg='black', command=lambda: SettingsWindow(self.root))

        # button window
        button_verwaltung_window = main_window_canvas.create_window(0,775,anchor="nw",window=button_verwaltung)
        buttonAllow_window = main_window_canvas.create_window(100,775,anchor="nw",window=buttonAllow)
        buttonBlock_window = main_window_canvas.create_window(200,775,anchor="nw",window=buttonBlock)
        buttonSettings_window = main_window_canvas.create_window(300,775,anchor="nw",window=buttonSettings)

        # add firewalls status buttons
        main_window_canvas.create_text(300, 400, text='domain:', anchor='nw', font=('Helvetica',10), fill='white')
        main_window_canvas.create_text(300, 450, text='private:', anchor='nw', font=('Helvetica', 10), fill='white')
        main_window_canvas.create_text(300, 500, text='public:', anchor='nw', font=('Helvetica', 10), fill='white')

        def swap_on_off(x):
            if x == "ON":
                return "OFF"
            if x == "OFF":
                return "ON"
            return False

        def domain_updater(state):
            action = swap_on_off(state)
            profile_switch("domain",action)
            domain_button.configure(text=action)
            firewall_states[0] = action

        def private_updater(state):
            action = swap_on_off(state)
            profile_switch("private", action)
            private_button.configure(text=action)
            firewall_states[1] = action

        def public_updater(state):
            action = swap_on_off(state)
            profile_switch("public",action)
            public_button.configure(text=action)
            firewall_states[2] = action

        def all_on():
            profile_switch("all","ON")
            domain_button.configure(text="ON")
            private_button.configure(text="ON")
            public_button.configure(text="ON")
            for i in range(len(firewall_states)):
                firewall_states[i] = "ON"

        def all_off():
            profile_switch("all","OFF")
            domain_button.configure(text="OFF")
            private_button.configure(text="OFF")
            public_button.configure(text="OFF")
            for i in range(len(firewall_states)):
                firewall_states[i] = "OFF"



        domain_button = tk.Button(self.root, text=firewall_states[0], fg='black',command=lambda:domain_updater(firewall_states[0]))
        private_button = tk.Button(self.root, text=firewall_states[1], fg='black',command=lambda:private_updater(firewall_states[1]))
        public_button = tk.Button(self.root, text=firewall_states[2], fg='black',command=lambda:public_updater(firewall_states[2]))
        all_on_button = tk.Button(self.root, text="All ON", fg='black',command=lambda:all_on())
        all_off_button = tk.Button(self.root, text="All OF", fg='black',command=lambda:all_off())



        domain_button_window = main_window_canvas.create_window(350, 400, anchor="nw", window=domain_button)
        private_button_window = main_window_canvas.create_window(350, 450, anchor="nw", window=private_button)
        public_button_window = main_window_canvas.create_window(350, 500, anchor="nw", window=public_button)
        all_on_button_window = main_window_canvas.create_window(350, 550, anchor="nw", window=all_on_button)
        all_off_button_window = main_window_canvas.create_window(400, 550, anchor="nw", window=all_off_button)

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

            main_window_canvas.create_text(300, 400, text='domain:', anchor='nw', font=('Helvetica', 10), fill='white')
            main_window_canvas.create_text(300, 450, text='private:', anchor='nw', font=('Helvetica', 10), fill='white')
            main_window_canvas.create_text(300, 500, text='public:', anchor='nw', font=('Helvetica', 10), fill='white')

            wscale = float(e.width) / self.width
            hscale = float(e.height) / self.height
            self.width = e.width
            self.height = e.height

            # rescale all the objects tagged with the "all" tag
            #main_window_canvas.scale("all", 0, 0, wscale, hscale)

        main_window_canvas.addtag_all("all")
        self.root.bind('<Configure>', resizer)





    def start(self):
        self.root.mainloop()  # start monitoring and updating the GUI


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))


    main_window = MainWindow()
    main_window.start()