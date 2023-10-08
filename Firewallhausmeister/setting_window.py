import tkinter as tk
from config import change_config, load_config
from PIL import Image, ImageTk
from helper import icon_location
import sys,os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
la_creatura = resource_path("timos_mutter.png")
icon = resource_path(icon_location)
class SettingsWindow:
    def __init__(self, master):
        self.settings_labels_dict = {}
        config = load_config()
        settings = tk.Toplevel(master)
        settings.title("Einstellungen")
        settings.iconbitmap(resource_path(icon))

        settings.geometry("200x300")

        tk.Label(settings,
                 text="Einstellungen").pack()

        current_direction_field_to_show_in_setting = tk.StringVar()
        current_direction_field_to_show_in_setting.set(f'Richtung: ' + config['direction'])

        label_current_direction = tk.Label(settings, textvariable=current_direction_field_to_show_in_setting)
        label_current_direction.pack()

        # settings for directions
        self.settings_labels_dict['direction'] = current_direction_field_to_show_in_setting

        button_in = tk.Button(settings, text='In', fg='black',
                              command=lambda: self.change_config_entry_and_update_labels('direction', 'in'))
        button_in.configure(width=20)
        button_in.pack()

        button_out = tk.Button(settings, text='Out', fg='black',
                               command=lambda: self.change_config_entry_and_update_labels('direction', 'out'))
        button_out.configure(width=20)
        button_out.pack()

        button_both = tk.Button(settings, text='Both', fg='black',
                                command=lambda: self.change_config_entry_and_update_labels('direction', 'both'))
        button_both.configure(width=20)
        button_both.pack()

        # präfix menu
        current_prefix_field_to_show_in_setting = tk.StringVar()
        current_prefix_field_to_show_in_setting.set(f'Präfix: ' + config['prefix'])

        self.settings_labels_dict['prefix'] = current_prefix_field_to_show_in_setting
        tk.Label(settings, textvariable=current_prefix_field_to_show_in_setting).pack()

        # field:
        label = tk.Label(settings, text="Neues Präfix setzen:")
        label.pack()

        # Create an Entry widget to accept User Input
        entry = tk.Entry(settings, width=20)
        # entry.focus_set()
        entry.pack()
        tk.Button(settings, text="Okay", width=20,
                  command=lambda: self.change_config_entry_and_update_labels('prefix', entry.get())).pack()

        tk.Label(settings,
                 text="Extras:").pack()

        # Knopf TImos mom
        buttonMoM = tk.Button(settings, text='Bild von deiner Mutter!', fg='black',
                              command=lambda: open_image_mom(settings))
        buttonMoM.configure(width=20)
        buttonMoM.pack()

    def update_label_in_menu(self, key, value):
            current_name_of_button = self.settings_labels_dict[key].get()
            prefix_of_button = current_name_of_button.split(':')[0]
            self.settings_labels_dict[key].set(prefix_of_button+': ' + value)

    def change_config_entry_and_update_labels(self,key,value):
            change_config(key, value)
            self.update_label_in_menu(key, value)


def open_image_mom(root):
    MutterBild = tk.Toplevel(root)
    MutterBild.iconbitmap(resource_path(icon))
    MutterBild.geometry("1080x1184")
    MutterBild.title("La creatura")


    image_mutter = Image.open(resource_path(la_creatura))
    image_mutter = ImageTk.PhotoImage(image_mutter)

    label = tk.Label(MutterBild,image=image_mutter)
    label.image = image_mutter
    label.pack()
