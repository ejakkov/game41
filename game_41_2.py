
import tkinter as tk
import math
from tkinter import *
import random

class player_minmax_game: 
    def __init__(self, master, n):
        self.player_sods = 0
        self.computer_sods=0
        self.master = master
        self.n = n
        self.buttons = []
        self.selected_buttons = []
        self.locked_buttons=[]
        self.lines=[]
        self.player_turn=True
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        self.generate_buttons()
        self.canvas.bind("<Button-1>", self.player_click)

    def generate_buttons(self):
        for i in range(self.n):
            angle = i * (360 / self.n)
            x = 200 + 150 * math.cos(math.radians(angle))
            y = 200 + 150* math.sin(math.radians(angle))
            button = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white")
            self.buttons.append(button)

    def player_click(self, event):
        if self.player_turn:
            button= self.canvas.find_closest(event.x, event.y)[0]
            non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
            if button in non_locked_buttons:
                if len(self.selected_buttons) < 2:
                    self.selected_buttons.append(button)
                    self.locked_buttons.append(button)
                    self.canvas.itemconfig(button, fill="red")
                if len(self.selected_buttons) == 2:
                    button1, button2 = self.selected_buttons
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.player_turn=False
                    self.master.after(1000, self.computer_turn)

    def computer_turn(self):
        non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
        selected_buttons = random.sample(non_locked_buttons, 2)
        for button in selected_buttons:
            if len(self.selected_buttons) < 2:
                self.selected_buttons.append(button)
                self.locked_buttons.append(button)
                self.canvas.itemconfig(button, fill="blue")
            if len(self.selected_buttons) == 2:
                button1, button2 = self.selected_buttons
                self.draw_line(button1, button2)
                self.selected_buttons.clear()
                self.player_turn = True    

             
    def draw_line(self, button1, button2):
        x1, y1 = self.canvas.coords(button1)[0:2]
        x2, y2 = self.canvas.coords(button2)[0:2]
        line = self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10, fill="black")
        self.lines.append(line)

def player_minmax_start():
    l.destroy()
    player_minmax_game(logs,n)

def c_m_start():
    l.config(text="work in progress")


def p_a_start():
    l.config(text="work in progress")
 

def c_a_start():
    l.config(text="work in progress")
  

def click_ok():
    sk=slide.get()
    global n
    n=sk
    slide.destroy()
    btn_ok.destroy()
    l.config(text="Choose who will start")
    def click_c():
        l.config(text="Choose algorithm")
        button_c.config(text="ALPHA-BETA",command=lambda:[button_c.destroy(),button_p.destroy(),c_a_start()])
        button_p.config(text="MIN-MAX",command=lambda:[button_c.destroy(),button_p.destroy(),c_m_start()])
    button_c=Button(logs,text="COMPUTER",command=click_c)
    button_c.pack(side='left', expand=True)
    def click_p():
        l.config(text="Choose algorithm")
        button_c.config(text="ALPHA-BETA",command=lambda:[button_c.destroy(),button_p.destroy(),p_a_start()])
        button_p.config(text="MIN-MAX",command=lambda:[button_c.destroy(),button_p.destroy(),player_minmax_start()])
    button_p=Button(logs,text="PLAYER",command=click_p)
    button_p.pack(side='right', expand=True)

    
    
logs = tk.Tk()
logs.title("Game 41")
logs.geometry("400x400")
l=Label(logs,text="Choose number of fields",font=("Arial", 12))
l.pack()
slide = Scale(logs, from_=15, to=25,orient=HORIZONTAL)
slide.pack(pady=40)
btn_ok=Button(logs,text="OK",command=click_ok)    
btn_ok.pack()

logs.mainloop()