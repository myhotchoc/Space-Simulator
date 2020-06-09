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
base.title("Select a planet to view it's information")
base["bg"] = "black"
star4= tk.Label(base, height = 1, width = 1, bg = "black")
star4.grid(row=0, column = 1)
# title = tk.Label(base, text = "Select a planet to view it's information", bg = 'white')
# title2 = tk.Label(base, text = "information about it.", bg = 'white')
# title.grid(row = 0, column = 0)
# title2.grid(row=0, column = 1)

#opens the file and adds al the data to an array
file = open("planet_data.txt", "r")
for line in file:
    y = line.split()
    data_array.append(y)
file.close()

#prints the data for the selected planet
def PrintInfo(p,q, planet):
    baseFrame = tk.Toplevel(base)
    baseFrame.title(planet)
    quote1 = "The distance from " + planet + " to the Sun is: " + data_array[p][2] + " in metres." 
    quote2 = "The mass of " + planet + " is: " + data_array[p+1][2] + " in kg."
    quote3 = "The radius of " + planet + " is:" + data_array[q][2] + " in metres."
    quote = quote1 + "\n" + quote2 + "\n" + quote3
    data = tk.Text(baseFrame)
    data.insert(tk.END, quote)
    data.pack()

#creates the layout on the interface
merc = tk.Button(base, text = "Mercury", command = lambda: PrintInfo(1, 4, "Mercury"),bg = "grey1", fg = 'grey69' )
merc.grid(row = 1, column = 1,)
star3 = tk.Label(base, height = 1, width = 6, bg = 'black')
star3.grid(row=2, column = 0)
space = tk.Label(base, height = 1, width = 6, bg = "black")
space.grid(row=1, column = 2)
ven = tk.Button(base, text = "Venus", command = lambda: PrintInfo(4, 7, "Venus"), fg = 'orange red')
ven.grid(row=1, column = 3)
star = tk.Label(base, height = 1, width = 1, bg = 'black')
star.grid(row=2, column = 0)
space1 = tk.Label(base, height = 1, width = 6, bg = "black")
space1.grid(row=3, column = 2)
ear = tk.Button(base, text = "Earth", command = lambda: PrintInfo(7, 10, "Earth"), fg = 'seagreen3')
ear.grid(row=3, column = 1)
star5 = tk.Label(base, height = 1, width = 6, bg = 'black')
star5.grid(row=3, column = 0)
mar = tk.Button(base, text = "Mars", command = lambda: PrintInfo(10, 13, "Mars"), fg = 'light salmon')
mar.grid(row=3, column = 3)
star1 = tk.Label(base, height = 1, width = 1, bg = 'black')
star1.grid(row=4, column = 0)
jup = tk.Button(base, text = "Jupiter", command = lambda: PrintInfo(13, 16, "Jupiter"), fg = 'red3')
jup.grid(row=5, column = 1)
star6 = tk.Label(base, height = 1, width = 6, bg = 'black')
star6.grid(row=5, column = 0)
space3 = tk.Label(base, height = 1, width = 6, bg = "black")
space3.grid(row=5, column = 2)
sat = tk.Button(base, text = "Saturn", command = lambda: PrintInfo(16, 19, "Saturn"), fg = 'pale goldenrod')
sat.grid(row=5, column = 3)
star2 = tk.Label(base, height = 1, width = 1, bg = 'black')
star2.grid(row=6, column = 0)
ura = tk.Button(base, text = "Uranus", command = lambda: PrintInfo(19, 22, "Uranus"), fg = 'turquoise2')
ura.grid(row=7, column = 1)
star7 = tk.Label(base, height = 1, width = 6, bg = 'black')
star7.grid(row=7, column = 0)
space4 = tk.Label(base, height = 1, width = 6, bg = "black")
space4.grid(row=7, column = 2)
nep = tk.Button(base, text = "Neptune", command = lambda: PrintInfo(22, 24, "Neptune"), fg = 'blue')
nep.grid(row=7, column = 3)
space5 = tk.Label(base, height = 1, width = 6, bg = "black")
space5.grid(row=8, column = 2)
endspace = tk.Label(base, height = 1, width = 6, bg = "black")
endspace.grid(row=1, column = 4)

base.mainloop()
root.mainloop()
