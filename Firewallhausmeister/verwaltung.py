import tkinter as tk
from tkinter import ttk
from functions import _load_database, _write_database, delete_rule
from PIL import ImageTk, Image
class VerwaltungsFenster:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.title("Verwaltung")
        self.root.geometry("600x200")
        self.root.minsize(width=600, height=300)

        # load list of rules and check:
        self.database = _load_database(check=True)

        # crate the table:
        self.root.title('Treeview demo')

        # define columns

        columns = ('exe_name', 'action', 'dir', 'existing','path')

        tree = tk.ttk.Treeview(self.root, columns=columns, show='headings')

        # define headings
        tree.heading('exe_name', text='Name')
        tree.heading('path', text='Path')
        tree.heading('action', text='Action')
        tree.heading('dir', text='Direction')
        tree.heading('existing', text='Existing')

        # adjust size of columns:
        tree.column('exe_name',width=150)
        tree.column('path',width=200)
        tree.column('action',width=60)
        tree.column('dir',width=60)
        tree.column('existing',width=60)

        tree.grid(row=0, column=0, sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        delete_rule(self.database[1])
        # fill table
        for database_entry in self.database:
            print(database_entry[:-1])
            tree.insert('', tk.END, values=database_entry[:-1])


        # create 4 buttons
        # create allow button
        button_verwaltung = tk.Button(self.root, text='Verwaltung', fg='black',
                                      command=lambda: VerwaltungsFenster(lambda:1))
        button_verwaltung.configure(width=20)
        button_verwaltung.place(x=0, y=875)

        # create allow button
        buttonAllow = tk.Button(self.root, text='Zuslassen', bg='green', fg='black', command=lambda:1)
        buttonAllow.configure(width=20)
        buttonAllow.place(x=150, y=875)

        # create block button
        buttonBlock = tk.Button(self.root, text='Blockieren', bg='red', fg='black', command=lambda:1)
        buttonBlock.configure(width=20)
        buttonBlock.place(x=300, y=875)

        # settings Button
        buttonSettings = tk.Button(self.root, text='Einstellungen', fg='black',
                                   command=lambda:1)
        buttonSettings.configure(width=20)
        buttonSettings.place(x=450, y=875)


