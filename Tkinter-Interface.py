# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 17:29:45 2020

@author: Danny and Jenni (but he smells)
"""
import tkinter as tk

planets_array = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
data_array =  []

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

#opens the file and adds al the data to an array
file = open("planet_data.txt", "r")
for line in file:
    y = line.split()
    data_array.append(y)
file.close()

#prints the data for the selected planet
def PrintInfo(p,q):
    for x in range(p, q):
        print(data_array[x])
    print("")

#creates individual buttons for each planet
merc = tk.Button(base, text = "Mercury", command = lambda: PrintInfo(1,4))
merc.grid(row = 1, column = 0)
ven = tk.Button(base, text = "Venus", command = lambda: PrintInfo(4,7))
ven.grid(row=1, column = 1)
ear = tk.Button(base, text = "Earth", command = lambda: PrintInfo(7, 10))
ear.grid(row=2, column = 0)
mar = tk.Button(base, text = "Mars", command = lambda: PrintInfo(10, 13))
mar.grid(row=2, column = 1)
jup = tk.Button(base, text = "Jupiter", command = lambda: PrintInfo(13, 16))
jup.grid(row=3, column = 0)
sat = tk.Button(base, text = "Saturn", command = lambda: PrintInfo(16, 19))
sat.grid(row=3, column = 1)
ura = tk.Button(base, text = "Uranus", command = lambda: PrintInfo(19, 22))
ura.grid(row=4, column = 0)
nep = tk.Button(base, text = "Neptune", command = lambda: PrintInfo(22, 25))
nep.grid(row=4, column = 1)

base.mainloop()
root.mainloop()
