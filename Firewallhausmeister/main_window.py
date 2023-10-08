import tkinter as tk
import tkinter.filedialog
from PIL import ImageTk, Image
from functions import *
from helper import config, version, icon_location
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
icon = resource_path(icon_location)

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
        self.width = 350
        self.height = 350
        self.root.geometry(f'{self.width}x{self.height}')

        self.root.iconbitmap(resource_path(icon))

        # get firewall status
        command = f'netsh advfirewall show allprofiles state'
        output = subprocess.check_output(command,text=True)


        firewall_states = [row.split()[1] for row in output.split("\n") if "State" in row]


        # create items for firewall status

        # create frame
        status_button_frame = tk.Frame(master=self.root, width=300, height=250,pady=10,)
        status_button_frame.pack()

        # firewall status label
        label = tk.Label(status_button_frame, text="Firewall status")
        label.grid(column=0,row=0,columnspan=2,pady=7)

        # add firewalls status buttons
        domain_label = tk.Label(status_button_frame, text="domain:")
        domain_label.grid(column=0,row=1,pady=5)

        private_label = tk.Label(status_button_frame, text="private:")
        private_label.grid(column=0, row=2,pady=5)

        public_label = tk.Label(status_button_frame, text="public:")
        public_label.grid(column=0, row=3,pady=5)

        # functions for status buttons:

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



        # define buttons
        domain_button = tk.Button(status_button_frame, text=firewall_states[0], fg='black',command=lambda:domain_updater(firewall_states[0]))
        private_button = tk.Button(status_button_frame, text=firewall_states[1], fg='black',command=lambda:private_updater(firewall_states[1]))
        public_button = tk.Button(status_button_frame, text=firewall_states[2], fg='black',command=lambda:public_updater(firewall_states[2]))
        all_on_button = tk.Button(status_button_frame, text="All ON", fg='black',command=lambda:all_on())
        all_off_button = tk.Button(status_button_frame, text="All OFF", fg='black',command=lambda:all_off())

        # add buttons
        domain_button.grid( column=1,row=1)
        private_button.grid(column=1, row=2)
        public_button.grid(column=1, row=3)
        all_on_button.grid(column=0, row=4,pady=5,padx=5)
        all_off_button.grid(column=1, row=4,pady=5,padx=5)

        # buttons for creating rules

        # create frame
        rule_button_frame = tk.Frame(master=self.root, width=self.width, height=200, pady=5)
        rule_button_frame.pack()

        # create buttons
        button_verwaltung = tk.Button(rule_button_frame, text='Verwaltung', fg='black', command=lambda:VerwaltungsFenster(self.root))
        buttonAllow = tk.Button(rule_button_frame, text='Zulassen', bg='green', fg='black', command=self.allow)
        buttonBlock = tk.Button(rule_button_frame, text='Blockieren', bg='red', fg='black', command=self.block)
        buttonSettings = tk.Button(rule_button_frame, text='Einstellungen', fg='black', command=lambda: SettingsWindow(self.root))
        buttonKrause = tk.Button(rule_button_frame, text='Krause!', fg='black',font=10, command=lambda : open_image_krause(self.root))

        # place buttons

        buttonAllow.grid(column=0,row=0, pady=5)
        buttonBlock.grid(column=1,row=0,pady=5)
        buttonSettings.grid(column=1,row=1,pady=5)
        button_verwaltung.grid(column=0, row=1,pady=5)
        buttonKrause.grid(column=0,row=2,columnspan=2,pady=10)

        def open_image_krause(root):
            KrauseBild = tk.Toplevel(root)
            KrauseBild.geometry("600x800")
            KrauseBild.title("Krause")
            KrauseBild.iconbitmap(resource_path(icon))

            image_krause = Image.open(resource_path(Logo))
            image_krause = ImageTk.PhotoImage(image_krause)

            krause_label = tk.Label(KrauseBild, image=image_krause)
            krause_label.image = image_krause
            krause_label.pack()


    def start(self):
        self.root.mainloop()  # start monitoring and updating the GUI


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))


    main_window = MainWindow()
    main_window.start()