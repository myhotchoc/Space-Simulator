# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:29:45 2020

@author: Danny and Jenni (but he smells)
"""
import tkinter as tk

planets_array = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

root = tk.Tk()
root.title("Planets")
title = tk.Label(root, text = 'Choose which planets you want:')
title.grid(row= 0, column = 0)

#creates a list of the avaliable planets to be shown on the pygame interface
planets_selection = tk.Listbox(root, selectmode = 'multiple', height = 8 )
for item in planets_array:
    planets_selection.insert(tk.END, item)
planets_selection.grid(row = 1, column = 0)

#produces a list of the indices of the planets selected - starting from zero
btn = tk.Button(root, text='Done', command=lambda: print(planets_selection.curselection()))
btn.grid(row = 2, column = 0)


base = tk.Tk()
base.title("Planet Information")
title = tk.Label(base, text = "Select a planet to view")
title2 = tk.Label(base, text = "information about it.")
title.grid(row = 0, column = 0)
title2.grid(row=0, column = 1)

def PrintInfo():
    print("WORKING")

merc = tk.Button(base, text = "Mercury", command = lambda: PrintInfo())
merc.grid(row = 1, column = 0)
ven = tk.Button(base, text = "Venus", command = lambda: PrintInfo())
ven.grid(row=1, column = 1)
ear = tk.Button(base, text = "Earth", command = lambda: PrintInfo())
ear.grid(row=2, column = 0)
mar = tk.Button(base, text = "Mars", command = lambda: PrintInfo())
mar.grid(row=2, column = 1)
jup = tk.Button(base, text = "Jupiter", command = lambda: PrintInfo())
jup.grid(row=3, column = 0)
sat = tk.Button(base, text = "Saturn", command = lambda: PrintInfo())
sat.grid(row=3, column = 1)
ura = tk.Button(base, text = "Uranus", command = lambda: PrintInfo())
ura.grid(row=4, column = 0)
nep = tk.Button(base, text = "Neptune", command = lambda: PrintInfo())
nep.grid(row=4, column = 1)


base.mainloop()
root.mainloop()
