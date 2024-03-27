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
      
 
    def all_possible_moves(self):
        moves=[]
        non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
        for i in range(len(non_locked_buttons)):
            for j in range(i+1, len(non_locked_buttons)):
                    moves.append((non_locked_buttons[i], non_locked_buttons[j]))   
        return moves
   
    

    def player_click(self, event):
        if self.current_turn == "player":
            button = self.canvas.find_closest(event.x, event.y)[0]
            non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
            if button in non_locked_buttons:
                if len(self.selected_buttons) < 2:
                    self.selected_buttons.append(button)
                    self.locked_buttons.append(button)
                    self.canvas.itemconfig(button, fill="red")
                if len(self.selected_buttons) == 1 and self.n - len(self.locked_buttons) == 0:
                    self.selected_buttons.clear()
                    self.locked_buttons.clear()
                    self.who_won()
                if len(self.selected_buttons) == 2:
                    button1, button2 = self.selected_buttons
                    self.save_line(button1, button2)
                    self.check_and_update_penalty("player")
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.update_score()
                    if self.n - len(self.locked_buttons) < 2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    else:
                        self.current_turn = "computer"
                        self.master.after(300, self.computer_turn)

    def computer_turn(self):
        if self.current_turn == "computer":
            non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
            selected_buttons = self.get_best_move()
            for button in selected_buttons:
                if len(self.selected_buttons) < 2:
                    self.selected_buttons.append(button)
                    self.locked_buttons.append(button)
                    self.canvas.itemconfig(button, fill="blue")
                if len(self.selected_buttons) == 1 and self.n - len(self.locked_buttons) == 0:
                    self.selected_buttons.clear()
                    self.locked_buttons.clear()
                    self.who_won()
                if len(self.selected_buttons) == 2:
                    button1, button2 = self.selected_buttons
                    self.selected_buttons.clear()
                    self.save_line(button1, button2)
                    self.check_and_update_penalty("computer")
                    self.draw_line(button1, button2)
                    self.update_score()
                    if self.n - len(self.locked_buttons) < 2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    else:
                        self.current_turn = "player"
            
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

    def check_and_update_penalty(self, current_turn):
        line1 = self.lines[-1]
        for i in self.lines[0:-1]:
            line2 = i
            if self.check_intersections(line1, line2):
                if current_turn == "player":
                    self.player_sods += 1
                else:
                    self.computer_sods += 1
    def evaluate_game_state(game):
        return game.player_sods - game.computer_sods

    def generate_moves(game):
        moves = []
        non_locked_buttons = [button for button in game.buttons if button not in game.locked_buttons]
        for i in range(len(non_locked_buttons)):
            for j in range(i + 1, len(non_locked_buttons)):
                moves.append((non_locked_buttons[i], non_locked_buttons[j]))
        return moves

    def minimax(game, depth, maximizing_player):
        if depth == 0 or game.n - len(game.locked_buttons) < 2:
            return game.evaluate_game_state()

        if maximizing_player:
            max_eval = float('-inf')
            for move in game.generate_moves():
                game.selected_buttons = list(move)
                tempPlayerSods = game.player_sods
                tempCompSods = game.computer_sods
                game.locked_buttons.extend(list(move))
                game.save_line(move[0], move[1])
                game.check_and_update_penalty(game.current_turn)
                eval = game.minimax(depth - 1, False)
                max_eval = max(max_eval, eval)
                game.selected_buttons.clear()
                game.locked_buttons = game.locked_buttons[:-2]
                game.lines.pop()
                game.player_sods = tempPlayerSods
                game.computer_sods = tempCompSods
            return max_eval
        else:
            min_eval = float('inf')
            for move in game.generate_moves():
                game.selected_buttons = list(move)
                game.locked_buttons.extend(list(move))
                tempPlayerSods = game.player_sods
                tempCompSods = game.computer_sods
                game.save_line(move[0], move[1])
                game.check_and_update_penalty(game.current_turn)
                eval = game.minimax(depth - 1, True)
                min_eval = min(min_eval, eval)
                game.selected_buttons.clear()
                game.locked_buttons = game.locked_buttons[:-2]
                game.lines.pop()
                game.player_sods = tempPlayerSods
                game.computer_sods = tempCompSods
            return min_eval

    def get_best_move(game):
        best_score = float('-inf')
        best_move = None
        for move in game.generate_moves():
            game.selected_buttons = list(move)
            game.locked_buttons.extend(list(move))
            eval = game.minimax(3, False)
            if eval > best_score:
                best_score = eval
                best_move = move
            game.selected_buttons.clear()
            game.locked_buttons = game.locked_buttons[:-2]
        print(best_score)
        print(best_move)
        return best_move
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