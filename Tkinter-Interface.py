# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:29:45 2020

@author: Danny and Jenni (but he smells)
"""

import tkinter as tk

root = tk.Tk()
v = tk.StringVar()

title = tk.Label(root, text = 'Choose which planets you want:')
title.grid(row= 0, column = 0)
planets_array = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

#creates a list of the avaliable planets to be shown on the pygame interface
planets_selection = tk.Listbox(root, selectmode = 'multiple', height = 8 )
for item in planets_array:
    planets_selection.insert(tk.END, item)
planets_selection.grid(row = 1, column = 0)

#produces a list of the indices of the planets selected - starting from zero
btn = tk.Button(root, text='Done', command=lambda: print(planets_selection.curselection()))
btn.grid(row = 2, column = 0)

root.mainloop()
