import tkinter as tk
import math
from tkinter import *
class minmax_game: 
    def __init__(self, master, n,first_turn):
        self.player_sods = 0
        self.computer_sods=0
        self.master = master
        self.n = n
        self.current_turn=first_turn
        self.buttons = []
        self.button_coords=[]
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
            self.button_coords.append((x,y))

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
                    b1, b2 = self.selected_buttons
                    index_b1 = self.buttons.index(b1)
                    index_b2 = self.buttons.index(b2)
                    self.save_line(index_b1, index_b2)
                    self.check_player()
                    self.draw_line(index_b1, index_b2)
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




    def minimax(self, depth, max_turn):
        if depth == 0 or self.n - len(self.locked_buttons) <2:
            return self.player_sods-self.computer_sods            
        if max_turn:
            max_eval = -math.inf
            save_computer_sods=self.computer_sods
            for move in self.all_possible_moves():
                b1,b2=move
                index_b1 = self.buttons.index(b1)
                index_b2 = self.buttons.index(b2)
                self.locked_buttons.append(b1)
                self.locked_buttons.append(b2)
                self.save_line(index_b1,index_b2)
                self.check_computer()
                eval = self.minimax(depth-1, False)
                max_eval = max(max_eval, eval)
                self.locked_buttons.pop()
                self.locked_buttons.pop()
                self.lines.pop()
                self.computer_sods=save_computer_sods
            return max_eval
        else:
            min_eval =math.inf
            save_player_sods=self.player_sods
            for move in self.all_possible_moves():
                b1,b2=move
                index_b1 = self.buttons.index(b1)
                index_b2 = self.buttons.index(b2)
                self.locked_buttons.append(b1)
                self.locked_buttons.append(b2)
                self.save_line(index_b1,index_b2)
                self.check_player()
                eval = self.minimax(depth - 1, True)
                min_eval = min(min_eval, eval)
                self.locked_buttons.pop()
                self.locked_buttons.pop()
                self.lines.pop()
                self.player_sods=save_player_sods
            return min_eval
    
    def get_best_move(self):
        best_score = -math.inf
        best_move = None
        save_computer_sods=self.computer_sods
        for move in self.all_possible_moves():
            b1,b2=move
            index_b1 = self.buttons.index(b1)
            index_b2 = self.buttons.index(b2)
            self.locked_buttons.append(b1)
            self.locked_buttons.append(b2)
            self.save_line(index_b1,index_b2)
            self.check_computer()
            eval = self.minimax(3,True)
            if eval > best_score:
                best_score = eval
                best_move = move
            self.locked_buttons.pop()
            self.locked_buttons.pop()
            self.lines.pop()
            self.computer_sods=save_computer_sods
        return best_move
        
    def computer_turn(self):
            if self.current_turn=="computer":
                best_move=self.get_best_move()
                selected_buttons=list(best_move)
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
                        b1, b2 = self.selected_buttons
                        index_b1 = self.buttons.index(b1)
                        index_b2 = self.buttons.index(b2)
                        self.selected_buttons.clear()
                        self.save_line(index_b1,index_b2)
                        self.check_computer()
                        self.draw_line(index_b1,index_b2)
                        self.update_score()
                        if self.n-len(self.locked_buttons)<2:                           
                            self.selected_buttons.clear()
                            self.locked_buttons.clear()
                            self.who_won()
                        else:      
                            self.current_turn="player"           
            
    def draw_line(self,index_button1,index_button2):
        x1, y1 = self.button_coords[index_button1]
        x2, y2 = self.button_coords[index_button2]
        line=self.canvas.create_line(x1,y1,x2,y2,fill="black")
        self.drawn_lines.append(line)

    def save_line(self, index_button1, index_button2):
        x1, y1 = self.button_coords[index_button1]
        x2, y2 = self.button_coords[index_button2]
        line = (x1, y1, x2, y2)
        self.lines.append(line)

    def check_intersections(self,line1,line2):
        x1,y1,x2,y2=line1
        x3,y3,x4,y4=line2
        cross1=(x4-x3)*(y1-y3)-(y4-y3)*(x1-x3)
        cross2=(x4-x3)*(y2-y3)-(y4-y3)*(x2-x3)
        cross3=(x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)
        cross4=(x2-x1)*(y4-y1)-(y2-y1)*(x4-x1)
        if cross1*cross2<0 and cross3*cross4<0:
            return True
        return False
        
    def check_player(self):
        line1 = self.lines[-1]
        for line2 in self.lines[:-1]: 
            if self.check_intersections(line1, line2):
                self.player_sods+=1
                
    def check_computer(self):
        line1 = self.lines[-1]
        for line2 in self.lines[:-1]: 
            if self.check_intersections(line1, line2):
                self.computer_sods+=1 
                   

    

###########################################################################################################
class alphabeta_game: 
    def __init__(self, master, n,first_turn):
        self.player_sods = 0
        self.computer_sods=0
        self.master = master
        self.n = n
        self.current_turn=first_turn
        self.buttons = []
        self.button_coords=[]
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
            self.button_coords.append((x,y))

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
                    b1, b2 = self.selected_buttons
                    index_b1 = self.buttons.index(b1)
                    index_b2 = self.buttons.index(b2)
                    self.save_line(index_b1, index_b2)
                    self.check_player()
                    self.draw_line(index_b1, index_b2)
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
                best_move=self.get_best_move() #te vajg alfabeta
                selected_buttons=list(best_move)
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
                        b1, b2 = self.selected_buttons
                        index_b1 = self.buttons.index(b1)
                        index_b2 = self.buttons.index(b2)
                        self.selected_buttons.clear()
                        self.save_line(index_b1,index_b2)
                        self.check_computer()
                        self.draw_line(index_b1,index_b2)
                        self.update_score()
                        if self.n-len(self.locked_buttons)<2:                           
                            self.selected_buttons.clear()
                            self.locked_buttons.clear()
                            self.who_won()
                        else:      
                            self.current_turn="player"           
            
    def draw_line(self,index_button1,index_button2):
        x1, y1 = self.button_coords[index_button1]
        x2, y2 = self.button_coords[index_button2]
        line=self.canvas.create_line(x1,y1,x2,y2,fill="black")
        self.drawn_lines.append(line)

    def save_line(self, index_button1, index_button2):
        x1, y1 = self.button_coords[index_button1]
        x2, y2 = self.button_coords[index_button2]
        line = (x1, y1, x2, y2)
        self.lines.append(line)

    def check_intersections(self,line1,line2):
        x1,y1,x2,y2=line1
        x3,y3,x4,y4=line2
        cross1=(x4-x3)*(y1-y3)-(y4-y3)*(x1-x3)
        cross2=(x4-x3)*(y2-y3)-(y4-y3)*(x2-x3)
        cross3=(x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)
        cross4=(x2-x1)*(y4-y1)-(y2-y1)*(x4-x1)
        if cross1*cross2<0 and cross3*cross4<0:
            return True
        return False
        
    def check_player(self):
        line1 = self.lines[-1]
        for line2 in self.lines[:-1]: 
            if self.check_intersections(line1, line2):
                self.player_sods+=1
                
    def check_computer(self):
        line1 = self.lines[-1]
        for line2 in self.lines[:-1]: 
            if self.check_intersections(line1, line2):
                self.computer_sods+=1 
                   


    

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
