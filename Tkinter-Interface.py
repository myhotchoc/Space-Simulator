# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:29:45 2020

@author: Danny and Jenni (but he smells)

NEVERMIND ILL FIND SOEMONE LIKE YOUUUUUUUUUU
"""

import tkinter as tk
from tkinter import ttk

root = tk.Tk()

v = tk.StringVar()

#planet = tk.Label(root, message = 'Choose which planets you want:')
planets_array = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]


# merc = tk. Radiobutton(root, text= planets_array[0], variable=v).pack()
# print(merc)
planets_selection = tk.Listbox(root, selectmode = 'multiple', height = 8 )
for item in planets_array:
    planets_selection.insert(tk.END, item)
planets_selection.pack()

array = planets_selection.get(tk.ACTIVE)
print(array)
root.mainloop()
