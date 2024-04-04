import tkinter as tk
import math
from tkinter import *
import random
class minmax_game: 
    def __init__(self, master, n,first_turn):
        self.player_sods = 0
        self.computer_sods=0
        self.master = master
        self.n = n
        self.current_turn=first_turn
        self.buttons = []
        self.selected_buttons = []
        self.locked_buttons=[]
        self.lines=[]
        self.drawn_lines=[]
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.generate_buttons()
        self.canvas.bind("<Button-1>", self.player_click)
        self.player_info = Label(self.canvas, text="player penalty: 0", fg="red",font=("Arial", 10),anchor="nw")
        self.player_info.pack()
        self.canvas.create_window(410, 50, window=self.player_info)
        self.computer_info = Label(self.canvas, text="computer penalty: 0", fg="blue",font=("Arial", 10),anchor="ne")
        self.computer_info.pack()
        self.canvas.create_window(90, 50, window=self.computer_info)
        if first_turn=="computer":
            self.computer_turn()



    def generate_buttons(self):
        for i in range(self.n):
            angle = i * (360 / self.n)
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150* math.sin(math.radians(angle))
            button = self.canvas.create_oval(x-10,y-10,x+10,y+10, fill="white")
            self.buttons.append(button)

    def update_score(self):
        txt1="player penalty: "+str(self.player_sods)
        txt2="computer penalty: "+str(self.computer_sods)
        self.player_info.config(text=txt1)
        self.computer_info.config(text=txt2)       
    def who_won(self):
        end_logs=Toplevel()
        end_logs.title("game over")
        end_logs.geometry("300x200")
        l2=Label(end_logs,text="",font=("Arial", 12))
        l2.pack(pady=20)
        restart_btn=Button(end_logs,text="Restart",command=lambda:[self.restart_game(),end_logs.destroy()])
        restart_btn.pack(pady=20)
        exit_btn=Button(end_logs,text="Exit",command=self.master.quit)
        exit_btn.pack(pady=20)
        if self.player_sods>self.computer_sods:
            l2.config(text="Computer wins")
            
        elif self.player_sods<self.computer_sods:
            l2.config(text="Player wins")
            
        elif self.player_sods==self.computer_sods:
            l2.config(text="Draw")

    def restart_game(self):
        for line in self.drawn_lines:
            self.canvas.delete(line)
        self.lines.clear()
        self.drawn_lines.clear()
        for button in self.buttons:
            self.canvas.itemconfig(button, fill="white")
        self.player_sods=0
        self.computer_sods=0
        self.locked_buttons.clear()
        self.selected_buttons.clear()
        self.player_info.config(text="player penalty: 0")
        self.computer_info.config(text="computer penalty: 0")
        self.current_turn=first_turn
        if first_turn=="computer":
            self.computer_turn()
      
    def player_click(self, event):
        if self.current_turn=="player":
            button= self.canvas.find_closest(event.x, event.y)[0]
            non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
            if button in non_locked_buttons:
                if len(self.selected_buttons) < 2:
                    self.selected_buttons.append(button)
                    self.locked_buttons.append(button)            
                    self.canvas.itemconfig(button, fill="red")
                if len(self.selected_buttons)==1 and self.n-len(self.locked_buttons)==0:
                    self.selected_buttons.clear()
                    self.locked_buttons.clear()
                    self.who_won()    
                if len(self.selected_buttons)==2:
                    button1, button2 = self.selected_buttons
                    self.save_line(button1, button2)
                    self.check_player()
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.update_score()   
                    if self.n-len(self.locked_buttons)<2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()           
                    else:
                        self.current_turn="computer"
                        self.master.after(300, self.computer_turn)
   
    def all_possible_moves(self):
        moves=[]
        non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
        for i in range(len(non_locked_buttons)):
            for j in range(i+1, len(non_locked_buttons)):
                    moves.append((non_locked_buttons[i], non_locked_buttons[j]))   
        return moves
   

    def minimax(self, state, depth, isMaximizing):

        if depth == 0 or self.n - len(self.locked_buttons) <= 1:
            return self.player_sods - self.computer_sods
        
        if isMaximizing:                  #Computer maksimize heiristiskas funkcijas vertibu (computer == maximizer)
            bestScore = -math.inf
            compSodsCopy = self.computer_sods
            lockedButtonsCopy = self.locked_buttons.copy()
            for buttonComb in state:
                self.save_line(buttonComb[0], buttonComb[1])
                self.locked_buttons.append(buttonComb[0])
                self.locked_buttons.append(buttonComb[1])
                self.check_computer()
                score = self.minimax(state, depth-1, False) # Šis ir nākamais gājiens pēc computer, tātad Minimizer
                self.locked_buttons = lockedButtonsCopy.copy()
                self.lines.pop()
                self.computer_sods = compSodsCopy
                bestScore = max(bestScore, score)
            return bestScore

        else:                           # Player minimizee heiristiskas funkcijas vertibu (player == minimizer)
            bestScore = math.inf
            playerSodsCopy = self.player_sods
            lockedButtonsCopy = self.locked_buttons.copy()
            for buttonComb in state:
                self.save_line(buttonComb[0], buttonComb[1])
                self.locked_buttons.append(buttonComb[0])
                self.locked_buttons.append(buttonComb[1])
                self.check_player()
                score = self.minimax(state, depth-1, True) # Šis ir nākamais gājiens pēc player, tātad Maximizer
                self.locked_buttons = lockedButtonsCopy.copy()
                self.lines.pop()
                self.player_sods = playerSodsCopy
                bestScore = min(bestScore, score)
            return bestScore


    def bestMove(self):
        all_moves = self.all_possible_moves()
        bestMove = None
        bestScore = -math.inf 
        compSodsCopy = self.computer_sods
        lockedButtonsCopy = self.locked_buttons.copy()
        for buttonComb in all_moves:
            self.save_line(buttonComb[0], buttonComb[1])
            self.locked_buttons.append(buttonComb[0])
            self.locked_buttons.append(buttonComb[1])
            self.check_computer()
            print(self.locked_buttons)
            score = self.minimax(all_moves, 2, False) # Šis ir nākamais gājiens pēc computer, tātad Minimizer
            self.locked_buttons = lockedButtonsCopy.copy()
            self.lines.pop()
            self.computer_sods = compSodsCopy
            if(score > bestScore):
                bestScore = score
                a, b = buttonComb
                bestMove = a, b
        print(bestScore)
        print(bestMove)
        return bestMove

    def computer_turn(self):
            if self.current_turn=="computer":
                selected_buttons = self.bestMove()
                for button in selected_buttons:
                    if len(self.selected_buttons) < 2:
                        self.selected_buttons.append(button)
                        self.locked_buttons.append(button)
                        self.canvas.itemconfig(button, fill="blue")
                    if len(self.selected_buttons)==1 and self.n-len(self.locked_buttons)==0:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    if len(self.selected_buttons) == 2:
                        button1, button2 = self.selected_buttons
                        self.selected_buttons.clear()
                        self.save_line(button1,button2)
                        self.check_computer()
                        self.draw_line(button1, button2)
                        self.update_score()
                        if self.n-len(self.locked_buttons)<2:                           
                            self.selected_buttons.clear()
                            self.locked_buttons.clear()
                            self.who_won()
                        else:
            
                            self.current_turn="player"

            
    def draw_line(self,button1,button2):
        x1,y1=self.canvas.coords(button1)[0:2]
        x2,y2=self.canvas.coords(button2)[0:2]
        line=self.canvas.create_line(x1+10,y1+10,x2+10,y2+10,fill="black")
        self.drawn_lines.append(line)

    def save_line(self, button1, button2):
        x1,y1=self.canvas.coords(button1)[0:2]
        x2,y2=self.canvas.coords(button2)[0:2]
        line=(x1+10,y1+10,x2+10,y2+10)
        self.lines.append(line)
        
    def check_intersections(self,line1,line2):
        x1,y1,x2,y2=line1
        x3,y3,x4,y4=line2
        def ccw(a, b, c):
            if(c[1]-a[1])*(b[0]-a[0])>(b[1]-a[1])*(c[0]-a[0]):
                return True
        if ccw((x1,y1),(x3,y3),(x4,y4))!=ccw((x2,y2),(x3,y3),(x4,y4))and ccw((x1,y1),(x2,y2),(x3,y3))!=ccw((x1,y1),(x2,y2),(x4,y4)):
            return True 
        
    def check_player(self):
        line1=self.lines[-1]
        for i in self.lines[0:-1]:
            line2=i
            if self.check_intersections(line1,line2)==True:
                self.player_sods=self.player_sods+1

    def check_computer(self):
        line1=self.lines[-1]
        for i in self.lines[0:-1]:
            line2=i
            if self.check_intersections(line1,line2)==True:
                self.computer_sods=self.computer_sods+1    


    

###########################################################################################################
class alphabeta_game: 
    def __init__(self, master, n,first_turn):
        self.player_sods = 0
        self.computer_sods=0
        self.master = master
        self.n = n
        self.current_turn=first_turn
        self.buttons = []
        self.selected_buttons = []
        self.locked_buttons=[]
        self.lines=[]
        self.drawn_lines=[]
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.generate_buttons()
        self.canvas.bind("<Button-1>", self.player_click)
        self.player_info = Label(self.canvas, text="player penalty: 0", fg="red",font=("Arial", 10),anchor="nw")
        self.player_info.pack()
        self.canvas.create_window(410, 50, window=self.player_info)
        self.computer_info = Label(self.canvas, text="computer penalty: 0", fg="blue",font=("Arial", 10),anchor="ne")
        self.computer_info.pack()
        self.canvas.create_window(90, 50, window=self.computer_info)
        if first_turn=="computer":
            self.computer_turn()



    def generate_buttons(self):
        for i in range(self.n):
            angle = i * (360 / self.n)
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150* math.sin(math.radians(angle))
            button = self.canvas.create_oval(x-10,y-10,x+10,y+10, fill="white")
            self.buttons.append(button)

    def update_score(self):
        txt1="player penalty: "+str(self.player_sods)
        txt2="computer penalty: "+str(self.computer_sods)
        self.player_info.config(text=txt1)
        self.computer_info.config(text=txt2)       
    def who_won(self):
        end_logs=Toplevel()
        end_logs.title("game over")
        end_logs.geometry("300x200")
        l2=Label(end_logs,text="",font=("Arial", 12))
        l2.pack(pady=20)
        restart_btn=Button(end_logs,text="Restart",command=lambda:[self.restart_game(),end_logs.destroy()])
        restart_btn.pack(pady=20)
        exit_btn=Button(end_logs,text="Exit",command=self.master.quit)
        exit_btn.pack(pady=20)
        if self.player_sods>self.computer_sods:
            l2.config(text="Computer wins")
            
        elif self.player_sods<self.computer_sods:
            l2.config(text="Player wins")
            
        elif self.player_sods==self.computer_sods:
            l2.config(text="Draw")

    def restart_game(self):
        for line in self.drawn_lines:
            self.canvas.delete(line)
        self.lines.clear()
        self.drawn_lines.clear()
        for button in self.buttons:
            self.canvas.itemconfig(button, fill="white")
        self.player_sods=0
        self.computer_sods=0
        self.locked_buttons.clear()
        self.selected_buttons.clear()
        self.player_info.config(text="player penalty: 0")
        self.computer_info.config(text="computer penalty: 0")
        self.current_turn=first_turn
        if first_turn=="computer":
            self.computer_turn()
      
    def player_click(self, event):
        if self.current_turn=="player":
            button= self.canvas.find_closest(event.x, event.y)[0]
            non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
            if button in non_locked_buttons:
                if len(self.selected_buttons) < 2:
                    self.selected_buttons.append(button)
                    self.locked_buttons.append(button)            
                    self.canvas.itemconfig(button, fill="red")
                if len(self.selected_buttons)==1 and self.n-len(self.locked_buttons)==0:
                    self.selected_buttons.clear()
                    self.locked_buttons.clear()
                    self.who_won()    
                if len(self.selected_buttons)==2:
                    button1, button2 = self.selected_buttons
                    self.save_line(button1, button2)
                    self.check_player()
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.update_score()   
                    if self.n-len(self.locked_buttons)<2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()           
                    else:
                        self.current_turn="computer"
                        self.master.after(300, self.computer_turn)
   
    def all_possible_moves(self):
        moves=[]
        non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
        for i in range(len(non_locked_buttons)):
            for j in range(i+1, len(non_locked_buttons)):
                    moves.append((non_locked_buttons[i], non_locked_buttons[j]))   
        return moves

    def computer_turn(self):
            if self.current_turn=="computer":
                non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
                selected_buttons = random.sample(non_locked_buttons, 2)
                selected_buttons = self.bestMove()
                for button in selected_buttons:
                    if len(self.selected_buttons) < 2:
                        self.selected_buttons.append(button)
                        self.locked_buttons.append(button)
                        self.canvas.itemconfig(button, fill="blue")
                    if len(self.selected_buttons)==1 and self.n-len(self.locked_buttons)==0:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    if len(self.selected_buttons) == 2:
                        button1, button2 = self.selected_buttons
                        self.selected_buttons.clear()
                        self.save_line(button1,button2)
                        self.check_computer()
                        self.draw_line(button1, button2)
                        self.update_score()
                        if self.n-len(self.locked_buttons)<2:                           
                            self.selected_buttons.clear()
                            self.locked_buttons.clear()
                            self.who_won()
                        else:
            
                            self.current_turn="player"

            
    def draw_line(self,button1,button2):
        x1,y1=self.canvas.coords(button1)[0:2]
        x2,y2=self.canvas.coords(button2)[0:2]
        line=self.canvas.create_line(x1+10,y1+10,x2+10,y2+10,fill="black")
        self.drawn_lines.append(line)

    def save_line(self, button1, button2):
        x1,y1=self.canvas.coords(button1)[0:2]
        x2,y2=self.canvas.coords(button2)[0:2]
        line=(x1+10,y1+10,x2+10,y2+10)
        self.lines.append(line)
        
    def check_intersections(self,line1,line2):
        x1,y1,x2,y2=line1
        x3,y3,x4,y4=line2
        def ccw(a, b, c):
            if(c[1]-a[1])*(b[0]-a[0])>(b[1]-a[1])*(c[0]-a[0]):
                return True
        if ccw((x1,y1),(x3,y3),(x4,y4))!=ccw((x2,y2),(x3,y3),(x4,y4))and ccw((x1,y1),(x2,y2),(x3,y3))!=ccw((x1,y1),(x2,y2),(x4,y4)):
            return True 
        
    def check_player(self):
        line1=self.lines[-1]
        for i in self.lines[0:-1]:
            line2=i
            if self.check_intersections(line1,line2)==True:
                self.player_sods=self.player_sods+1

    def check_computer(self):
        line1=self.lines[-1]
        for i in self.lines[0:-1]:
            line2=i
            if self.check_intersections(line1,line2)==True:
                self.computer_sods=self.computer_sods+1    


    


###########################################################################################################


def player_minmax_start():
    l.destroy()
    global first_turn
    first_turn="player"
    minmax_game(logs,n,first_turn)

def computer_minmax_start():
    l.destroy()
    global first_turn
    first_turn="computer"
    minmax_game(logs,n,first_turn)


def player_alphabeta_start():
    l.destroy()
    global first_turn
    first_turn="player"
    alphabeta_game(logs,n,first_turn)
    
 

def computer_alphabeta_start():
    l.destroy()
    global first_turn
    first_turn="computer"
    alphabeta_game(logs,n,first_turn)
  

def click_ok():
    sk=slide.get()
    global n
    n=sk
    slide.destroy()
    btn_ok.destroy()
    l.config(text="Choose who will start")
    def click_c():
        l.config(text="Choose algorithm")
        button_c.config(text="ALPHA-BETA",command=lambda:[button_c.destroy(),button_p.destroy(),computer_alphabeta_start()])
        button_p.config(text="MIN-MAX",command=lambda:[button_c.destroy(),button_p.destroy(),computer_minmax_start()])
    button_c=Button(logs,text="COMPUTER",command=click_c)
    button_c.pack(side='left', expand=True)
    def click_p():
        l.config(text="Choose algorithm")
        button_c.config(text="ALPHA-BETA",command=lambda:[button_c.destroy(),button_p.destroy(),player_alphabeta_start()])
        button_p.config(text="MIN-MAX",command=lambda:[button_c.destroy(),button_p.destroy(),player_minmax_start()])
    button_p=Button(logs,text="PLAYER",command=click_p)
    button_p.pack(side='right', expand=True)

   
logs = tk.Tk()
logs.title("Game 41")
logs.geometry("500x500")
l=Label(logs,text="Choose number of fields",font=("Arial", 12))
l.pack()
slide = Scale(logs, from_=15, to=25,orient=HORIZONTAL)
slide.pack(pady=40)
btn_ok=Button(logs,text="OK",command=click_ok)    
btn_ok.pack()

logs.mainloop()
