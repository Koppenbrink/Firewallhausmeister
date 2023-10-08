import tkinter as tk
from tkinter import ttk
from functions import _load_database, _write_database, delete_rules, resource_path
from helper import icon_location
from PIL import ImageTk, Image

class VerwaltungsFenster:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.title("Verwaltung")
        self.root.geometry("600x200")
        self.root.minsize(width=600, height=300)
        self.selected_items = []
        self.root.iconbitmap(resource_path(icon_location))

        # load list of rules and check:
        self.database = _load_database(check=True)

        # crate the table:
        self.root.title('Regeln')

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

        # fill table
        def update_tabel():
            tree.delete(*tree.get_children())
            self.database = _load_database(check=True)
            for database_entry in self.database:
                tree.insert('', tk.END, values=database_entry[:-1])

        update_tabel()

        def item_selected(event):
            self.selected_items = []
            for selected_item in tree.selection():
                selected = tree.index(selected_item)
                self.selected_items.append(selected)

        tree.bind('<<TreeviewSelect>>', item_selected)


        # create 4 buttons
        # create allow button
        button_verwaltung = tk.Button(self.root, text='rescan', fg='black',
                                      command=lambda:update_tabel())
        button_verwaltung.configure(width=20)
        button_verwaltung.place(x=0, y=270)

        # create allow button
        buttonAllow = tk.Button(self.root, text='HIER KÖNNTE IHRE WERBUNG STEHEN', bg='green', fg='black', command=lambda:print(self.selected_items))
        buttonAllow.configure(width=20)
        buttonAllow.place(x=150, y=270)

        # create delete entries button
        def delete_entries_button():
            self.delete_selected_entries()
            update_tabel()

        buttonBlock = tk.Button(self.root, text='Einträge Löschen', bg='red', fg='black', command=lambda:delete_entries_button())
        buttonBlock.configure(width=20)
        buttonBlock.place(x=300, y=270)

        # settings Button
        def settings_button():
            self.clean_up()
            update_tabel()

        button_clean_up = tk.Button(self.root, text='Aufräumen', fg='black',
                                   command=lambda:settings_button())
        button_clean_up.configure(width=20)
        button_clean_up.place(x=450, y=270)

    def delete_selected_entries(self):
        delete_rules(self.selected_items)
    def clean_up(self):
        to_clean = [x for x in range(len(self.database)) if self.database[x][3] == False]
        delete_rules(to_clean)