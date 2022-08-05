import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from functions import set_rule
from helper import version


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

def zulassen():
    file_path = filedialog.askopenfilename()
    file_path = file_path.replace('/', '\\')
    if file_path:
        set_rule(file_path, action='allow', dir='both')

buttonAllow = tk.Button(root, text='Zuslassen',bg='green', fg='black', command=zulassen)
buttonAllow.configure(width=20)
buttonAllow.place(x=50, y=810)

def block():
    file_path = filedialog.askopenfilename()
    file_path = file_path.replace('/', '\\')
    if file_path:
        set_rule(file_path, action='block', dir='both')

buttonBlock = tk.Button(root, text='Blockieren', bg='red', fg='black', command=block)
buttonBlock.configure(width=20)
buttonBlock.place(x=400, y=810)


#for item in labelKrause.keys():
#    print(item, ': ', labelKrause[item])

root.mainloop()
#root.withdraw()