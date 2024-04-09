import tkinter as tk
import math
from tkinter import *

class minmax_game:
    #Klases inicializācijas funkcija, kas tiek izsaukta, izveidojot objektu.
    def __init__(self, master, n, first_turn):
        self.player_sods = 0
        self.computer_sods = 0
        self.master = master
        self.numberOfPoints = n
        self.current_turn=first_turn
        self.arrayButtons = []
        self.arraySelectedButtons = []
        self.arrayLockedButtons = []
        self.arrayLines = []
        #Virtuālo pogu un līniju masīvi, lai paātrinātu minimaksa algoritmu.
        self.arrayVirtualLines = []
        self.arrayVirtualButtons = []
        self.AI_Level = 2 #rekursiju skaits, nevis līmeņi

        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.generate_buttons()
        self.canvas.bind("<Button-1>", self.player_click)
        self.lbl_player_info = Label(self.canvas, text="player penalty: 0", fg="red", font=("Arial", 10), anchor="nw")
        self.lbl_player_info.pack()
        self.canvas.create_window(410, 50, window=self.lbl_player_info)
        self.lbl_computer_info = Label(self.canvas, text="computer penalty: 0", fg="blue", font=("Arial", 10), anchor="ne")
        self.lbl_computer_info.pack()
        self.canvas.create_window(90, 50, window=self.lbl_computer_info)
        if first_turn=="computer":
            self.computer_turn()

    def generate_buttons(self):
        for i in range(self.numberOfPoints):
            angle = i * (360 / self.numberOfPoints)
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150 * math.sin(math.radians(angle))
            button = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white")
            self.arrayButtons.append(button)
            #Pievienot pogas koordinātas atsevišķā masīvā turpmākām aprēķinām.
            virtualButton =(button, x - 10, y - 10, False)
            self.arrayVirtualButtons.append(virtualButton)

    def update_score(self):
        txt1 = "player penalty: " + str(self.player_sods)
        txt2 = "computer penalty: " + str(self.computer_sods)
        self.lbl_player_info.config(text=txt1)
        self.lbl_computer_info.config(text=txt2)

    def who_won(self):
        modalWindow = Toplevel()
        modalWindow.title("game over")
        modalWindow.geometry("300x200")
        l2 = Label(modalWindow, text="", font=("Arial", 12))
        l2.pack(pady=20)
        restart_btn = Button(modalWindow, text="Restart", command=lambda: [self.restart_game(), modalWindow.destroy()])
        restart_btn.pack(pady=20)
        exit_btn = Button(modalWindow, text="Exit", command=self.master.quit)
        exit_btn.pack(pady=20)
        if self.player_sods > self.computer_sods:
            l2.config(text="Computer wins")

        elif self.player_sods < self.computer_sods:
            l2.config(text="Player wins")

        elif self.player_sods == self.computer_sods:
            l2.config(text="Draw")

    def restart_game(self):
        for line in self.arrayLines:
            self.canvas.delete(line)
        self.arrayLines.clear()

        self.arrayVirtualLines.clear()
        for i, item in enumerate(self.arrayVirtualButtons):
            buttonId, x, y, locked = item   
            self.arrayVirtualButtons[i] = (buttonId, x, y, False)

        for button in self.arrayButtons:
            self.canvas.itemconfig(button, fill="white")
        self.player_sods = 0
        self.computer_sods = 0
        self.arrayLockedButtons.clear()
        self.arraySelectedButtons.clear()
        self.lbl_player_info.config(text="player penalty: 0")
        self.lbl_computer_info.config(text="computer penalty: 0")
        self.current_turn=first_turn
        if first_turn=="computer":
            self.computer_turn()

    def player_click(self, event):
        if self.current_turn=="player":
            button = self.canvas.find_closest(event.x, event.y)[0]
            non_locked_buttons = [button for button in self.arrayButtons if button not in self.arrayLockedButtons]
            if button in non_locked_buttons:
                if len(self.arraySelectedButtons) < 2:
                    self.arraySelectedButtons.append(button)
                    self.arrayLockedButtons.append(button)
                    self.canvas.itemconfig(button, fill="red")
                if len(self.arraySelectedButtons) == 1 and self.numberOfPoints - len(self.arrayLockedButtons) == 0:
                    self.arraySelectedButtons.clear()
                    self.arrayLockedButtons.clear()
                    self.who_won()
                if len(self.arraySelectedButtons) == 2:
                    button1, button2 = self.arraySelectedButtons
                    self.draw_line(button1, button2)
                    self.arraySelectedButtons.clear()
                    self.lock_virtual_buttons(button1, button2)

                    self.player_sods = self.player_sods + self.calculate_score()
                    self.update_score()
                    if self.numberOfPoints - len(self.arrayLockedButtons) < 2:
                        self.arraySelectedButtons.clear()
                        self.arrayLockedButtons.clear()
                        self.who_won()
                    else:
                        self.current_turn="computer"
                        self.master.after(300, self.computer_turn)

    def computer_turn(self):
        if self.current_turn=="computer":            
            line = self.find_best_line()
            selected_buttons = []
            selected_buttons.append(line[0])
            selected_buttons.append(line[1])

            for button in selected_buttons:
                if len(self.arraySelectedButtons) < 2:
                    self.arraySelectedButtons.append(button)
                    self.arrayLockedButtons.append(button)
                    self.canvas.itemconfig(button, fill="blue")
                if len(self.arraySelectedButtons) == 1 and self.numberOfPoints - len(self.arrayLockedButtons) == 0:
                    self.arraySelectedButtons.clear()
                    self.arrayLockedButtons.clear()
                    self.who_won()
                if len(self.arraySelectedButtons) == 2:
                    button1, button2 = self.arraySelectedButtons
                    self.draw_line(button1, button2)
                    self.arraySelectedButtons.clear()
                    self.lock_virtual_buttons(button1, button2)
                    self.computer_sods = self.computer_sods + self.calculate_score()  
                    self.update_score()                
                    if self.numberOfPoints - len(self.arrayLockedButtons) < 2:
                        self.arraySelectedButtons.clear()
                        self.arrayLockedButtons.clear()
                        self.who_won()
                    else:
                        self.current_turn="player"

    def lock_virtual_buttons(self, button1, button2):
        new_boolean_value = True    
        for i, item in enumerate(self.arrayVirtualButtons):
            if item[0] == button1 or item[0] == button2:
                # Atjaunot vienuma boolean vērtību norādītajā indeksā
                self.arrayVirtualButtons[i] = (item[0], item[1], item[2], new_boolean_value)
    
    #labākā kustību noteikšanas funkcija
    #izmanto virtuālo pogu masivu (2 koordinātes). Lai algoritms darbotos, ir nepieciešamas tikai brīvas pogas
    #pēc katras reālas kustības šis masīvs ir jāatjauno, noņemot aizņemtās pogas (funkcija update_virtual_buttons)
    #izmanto pašreizējo virtuālo līniju masīvu (4 koordinātes), kas tiek atjaunināts funkcijā draw_line
    #sāk cilpu caur visām pogām, kamēr ir brīvas, novelk līniju un izsauc minmax funkciju
    def find_best_line(self):
        #masīvs, kurā pievienosim ģenerētās līnijas, aprēķinot punktus katrai cilpas rindai un saglabājot un atjauninot pozīciju, ja rindā ir maksimālais punktu skaits
        tempArrayButtons = list(filter(lambda x: x[3] == False, self.arrayVirtualButtons))

        tempLines = self.arrayVirtualLines.copy()
        bestMoveWeight = -math.inf
        min_AI_score = math.inf

        #Visu līniju opciju uzskaitījums tiek veikts, noņemot pēdējo pogu
        while len(tempArrayButtons) > 1:
            lastBtn = tempArrayButtons[-1]
            for btn in tempArrayButtons[0:-1]:
                line = (btn[0], lastBtn[0])
                #šajā gadījumā ir jāveic pirmais datora (AI) gājiens uz visām iespējamām pozīcijām un pēc tam jāizsauc minimax, lai novērtētu katru pozīciju
                tempLines.append(line)
                
                AI_score = self.calculate_virtual_score(tempLines)
                recurseArrayButtons = tempArrayButtons.copy()
                recurseArrayButtons.pop()
                recurseArrayButtons.remove(btn)
                #veicam šī virziena rekursīvu novērtējumu
                #noteikt soda punktu starpību ar spēlētāju, ko AI saņems šīs kustības rezultātā (spēlētāja sods - AI sods)
                #AI uzvar, ja starpība ir > 0
                move_weight = self.mini_max(False, 0, recurseArrayButtons, tempLines, AI_score, 0)
                move_weight = move_weight - AI_score

                #izvēl lielāko atšķirību starp punktiem
                #papildu nosacījums - ja dažādos virzienos ir vienāds punktu skaits, priekšroka tiek dota virzienam, kurā AI saņem mazāku sodu
                if ((move_weight > bestMoveWeight) or (((AI_score < min_AI_score) or (AI_score == 0)) and (move_weight == bestMoveWeight))):
                    #ja kustības svars ir lielāks par pašreizējo, atjauninām labāko līniju un punktus
                    bestMoveWeight = move_weight
                    bestLine = line
                    min_AI_score = AI_score
                tempLines.pop()
            tempArrayButtons.pop()
        # print(bestMoveWeight, min_AI_score)

        return bestLine

    #iziet cauri visām atbloķētajām pogām, izmantojot rekursiju
    #AI = true - datora gājiens
    #arrayButtons - atlikušās brīvās pogas šim pagrieziena posmam
    #arrayLines - jau uzbūvētas līnijas šim pārvietošanas posmam
    #funkcija atgriež pozīcijas svaru - starpību starp AI un spēlētāja soda punktiem
    def mini_max(self, AI, recursive_level, arButtons, arLines, AI_score, player_score):
        if ((recursive_level >= self.AI_Level) or (len(arButtons) <= 1)):
            return player_score - AI_score
      
        if (AI == True):
            bestMoveWeight = -math.inf
        else:
            bestMoveWeight = math.inf
            
        while len(arButtons) > 1:
            lastBtn = arButtons[-1]
            for btn in arButtons[0:-1]:
                line = (btn[0], lastBtn[0])
                arLines.append(line)
                AI_calculated_score = 0
                player_calculated_score = 0

                if (AI == True):
                    AI_calculated_score = self.calculate_virtual_score(arLines)
                else:
                    player_calculated_score = self.calculate_virtual_score(arLines)
                                  
                recurseArrayButtons = arButtons.copy()
                recurseArrayButtons.pop()
                recurseArrayButtons.remove(btn)

                #veicam šī virziena rekursīvu novērtējumu
                #funkcija atgriež punktu starpību starp spēlētāju un datoru; > 0 dators uzvar, < 0 spēlētājs uzvar
                move_weight = self.mini_max(not AI, recursive_level + 1, recurseArrayButtons, arLines, AI_score + AI_calculated_score, player_score + player_calculated_score)


                #jāņem vērā, ka spēlētājs izdarīs AI sliktāko gājienu
                if (AI == True):
                    #MAX: ja punktu skaits ir lielāks par pašreizējo, atjauniniet punktus
                    #dators uzvar, ja score_diff ir lielāks par 0 vai augstākais
                    bestMoveWeight = max(bestMoveWeight, move_weight) 
                else:
                    #MIN: spēlētājs vienmēr veiks gājienu, kas palielinās mūsu soda punktus un samazinās viņa soda punktus. tāpēc šajā posmā mēs izvēlamies sliktāko no visiem variantiem
                    #spēlētājs uzvar, ja score_diff ir mazāks par 0 vai mazākais
                    bestMoveWeight = min(bestMoveWeight, move_weight)

                arLines.pop()
            arButtons.pop()
        #visu virzienu pārbaudes cikls ir pabeigts, ciklā ir izvēlēts spēlētājam vai AI labākais gājiens
        #ir jāatgriež rezultāts, vai šis virziens uzvar AI vai nē. Lai to izdarītu, jums jānorāda atšķirība starp AI un atskaņotāja punktiem
        return bestMoveWeight
    
    def draw_line(self, button1, button2):
        x1, y1 = self.canvas.coords(button1)[0:2]
        x2, y2 = self.canvas.coords(button2)[0:2]
        line = self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10, fill="black")
        self.arrayLines.append(line)
       
        virtualLine =(button1, button2)
        self.arrayVirtualLines.append(virtualLine)

    def check_intersections(self, line1, line2):
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        def ccw(a, b, c):
            if (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0]):
                return True
        if ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and ccw((x1, y1), (x2, y2),(x3, y3)) != ccw((x1, y1),(x2, y2),(x4, y4)):
            return True
        
        
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

    def calculate_score(self):
        score = 0
        #atlase no pēdējās pievienotās rindas masīva
        line1 = self.canvas.coords(self.arrayLines[-1])
        for i in self.arrayLines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                #ja vismaz viena līnija krustojas ar pēdējo, pievienojam soda punktu
                score = score + 1
        return score

    #funkcija punktu aprēķināšanai, izmantojot virtuālu līniju masīvu (lai paātrinātu minmax algoritma darbību)
    def calculate_virtual_score(self, lines):
        score = 0
        endLineButtons = lines[-1]
        #izvilkt pogu pēc tās numura
        targetButton1 = next((element for element in self.arrayVirtualButtons if element[0] == endLineButtons[0]), None)
        targetButton2 = next((element for element in self.arrayVirtualButtons if element[0] == endLineButtons[1]), None)
        endLineCoords = (targetButton1[1], targetButton1[2], targetButton2[1], targetButton2[2], )
        
        #cikla pārbaude, ​​vai pēdējā līnija krustojas ar visām pārējām no masīva
        for curLineButtons in lines[0:-1]:
            #izvilkt pogu pēc tās numura
            targetButton1 = next((element for element in self.arrayVirtualButtons if element[0] == curLineButtons[0]), None)
            targetButton2 = next((element for element in self.arrayVirtualButtons if element[0] == curLineButtons[1]), None)
            curLineCoords = (targetButton1[1], targetButton1[2], targetButton2[1], targetButton2[2], )

            if self.check_intersections(endLineCoords, curLineCoords) == True:
                score = score + 1
        return score

###########################################################################################################

###########################################################################################################
class alphabeta_game:
 def __init__(self, master, n, first_turn):
    self.player_sods = 0
    self.computer_sods = 0
    self.master = master
    self.numberOfPoints = n
    self.current_turn=first_turn
    self.arrayButtons = []
    self.arraySelectedButtons = []
    self.arrayLockedButtons = []
    self.arrayLines = []
        #Virtuālo pogu un līniju masīvi, lai paātrinātu minimaksa algoritmu.
    self.arrayVirtualLines = []
    self.arrayVirtualButtons = []
    self.AI_Level = 2 #rekursiju skaits, nevis līmeņi

    self.canvas = tk.Canvas(master, width=500, height=500)
    self.canvas.pack()
    self.generate_buttons()
    self.canvas.bind("<Button-1>", self.player_click)
    self.lbl_player_info = Label(self.canvas, text="player penalty: 0", fg="red", font=("Arial", 10), anchor="nw")
    self.lbl_player_info.pack()
    self.canvas.create_window(410, 50, window=self.lbl_player_info)
    self.lbl_computer_info = Label(self.canvas, text="computer penalty: 0", fg="blue", font=("Arial", 10), anchor="ne")
    self.lbl_computer_info.pack()
    self.canvas.create_window(90, 50, window=self.lbl_computer_info)
    if first_turn=="computer":
        self.computer_turn()
 def generate_buttons(self):
        for i in range(self.numberOfPoints):
            angle = i * (360 / self.numberOfPoints)
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150 * math.sin(math.radians(angle))
            button = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white")
            self.arrayButtons.append(button)
            #Pievienot pogas koordinātas atsevišķā masīvā turpmākām aprēķinām.
            virtualButton =(button, x - 10, y - 10, False)
            self.arrayVirtualButtons.append(virtualButton)

 def update_score(self):
            txt1 = "player penalty: " + str(self.player_sods)
            txt2 = "computer penalty: " + str(self.computer_sods)
            self.lbl_player_info.config(text=txt1)
            self.lbl_computer_info.config(text=txt2)

 def who_won(self):
        modalWindow = Toplevel()
        modalWindow.title("game over")
        modalWindow.geometry("300x200")
        l2 = Label(modalWindow, text="", font=("Arial", 12))
        l2.pack(pady=20)
        restart_btn = Button(modalWindow, text="Restart", command=lambda: [self.restart_game(), modalWindow.destroy()])
        restart_btn.pack(pady=20)
        exit_btn = Button(modalWindow, text="Exit", command=self.master.quit)
        exit_btn.pack(pady=20)
        if self.player_sods > self.computer_sods:
            l2.config(text="Computer wins")

        elif self.player_sods < self.computer_sods:
            l2.config(text="Player wins")

        elif self.player_sods == self.computer_sods:
            l2.config(text="Draw")

 def restart_game(self):
        for line in self.arrayLines:
            self.canvas.delete(line)
        self.arrayLines.clear()

        self.arrayVirtualLines.clear()
        for i, item in enumerate(self.arrayVirtualButtons):
            buttonId, x, y, locked = item   
            self.arrayVirtualButtons[i] = (buttonId, x, y, False)

        for button in self.arrayButtons:
            self.canvas.itemconfig(button, fill="white")
        self.player_sods = 0
        self.computer_sods = 0
        self.arrayLockedButtons.clear()
        self.arraySelectedButtons.clear()
        self.lbl_player_info.config(text="player penalty: 0")
        self.lbl_computer_info.config(text="computer penalty: 0")
        self.current_turn=first_turn
        if first_turn=="computer":
            self.computer_turn()

 def player_click(self, event):
        if self.current_turn=="player":
            button = self.canvas.find_closest(event.x, event.y)[0]
            non_locked_buttons = [button for button in self.arrayButtons if button not in self.arrayLockedButtons]
            if button in non_locked_buttons:
                if len(self.arraySelectedButtons) < 2:
                    self.arraySelectedButtons.append(button)
                    self.arrayLockedButtons.append(button)
                    self.canvas.itemconfig(button, fill="red")
                if len(self.arraySelectedButtons) == 1 and self.numberOfPoints - len(self.arrayLockedButtons) == 0:
                    self.arraySelectedButtons.clear()
                    self.arrayLockedButtons.clear()
                    self.who_won()
                if len(self.arraySelectedButtons) == 2:
                    button1, button2 = self.arraySelectedButtons
                    self.draw_line(button1, button2)
                    self.arraySelectedButtons.clear()
                    self.lock_virtual_buttons(button1, button2)

                    self.player_sods = self.player_sods + self.calculate_score()
                    self.update_score()
                    if self.numberOfPoints - len(self.arrayLockedButtons) < 2:
                        self.arraySelectedButtons.clear()
                        self.arrayLockedButtons.clear()
                        self.who_won()
                    else:
                        self.current_turn="computer"
                        self.master.after(300, self.computer_turn)

 def computer_turn(self):
        if self.current_turn=="computer":            
            line = self.find_best_line()
            selected_buttons = []
            selected_buttons.append(line[0])
            selected_buttons.append(line[1])

            for button in selected_buttons:
                if len(self.arraySelectedButtons) < 2:
                    self.arraySelectedButtons.append(button)
                    self.arrayLockedButtons.append(button)
                    self.canvas.itemconfig(button, fill="blue")
                if len(self.arraySelectedButtons) == 1 and self.numberOfPoints - len(self.arrayLockedButtons) == 0:
                    self.arraySelectedButtons.clear()
                    self.arrayLockedButtons.clear()
                    self.who_won()
                if len(self.arraySelectedButtons) == 2:
                    button1, button2 = self.arraySelectedButtons
                    self.draw_line(button1, button2)
                    self.arraySelectedButtons.clear()
                    self.lock_virtual_buttons(button1, button2)
                    self.computer_sods = self.computer_sods + self.calculate_score()  
                    self.update_score()                
                    if self.numberOfPoints - len(self.arrayLockedButtons) < 2:
                        self.arraySelectedButtons.clear()
                        self.arrayLockedButtons.clear()
                        self.who_won()
                    else:
                        self.current_turn="player"

 def lock_virtual_buttons(self, button1, button2):
        new_boolean_value = True    
        for i, item in enumerate(self.arrayVirtualButtons):
            if item[0] == button1 or item[0] == button2:
                # Atjaunot vienuma boolean vērtību norādītajā indeksā
                self.arrayVirtualButtons[i] = (item[0], item[1], item[2], new_boolean_value)
    
    #labākā kustību noteikšanas funkcija
    #izmanto virtuālo pogu masivu (2 koordinātes). Lai algoritms darbotos, ir nepieciešamas tikai brīvas pogas
    #pēc katras reālas kustības šis masīvs ir jāatjauno, noņemot aizņemtās pogas (funkcija update_virtual_buttons)
    #izmanto pašreizējo virtuālo līniju masīvu (4 koordinātes), kas tiek atjaunināts funkcijā draw_line
    #sāk cilpu caur visām pogām, kamēr ir brīvas, novelk līniju un izsauc minmax funkciju
 def find_best_line(self):
        #masīvs, kurā pievienosim ģenerētās līnijas, aprēķinot punktus katrai cilpas rindai un saglabājot un atjauninot pozīciju, ja rindā ir maksimālais punktu skaits
        tempArrayButtons = list(filter(lambda x: x[3] == False, self.arrayVirtualButtons))

        tempLines = self.arrayVirtualLines.copy()
        bestMoveWeight = -math.inf
        min_AI_score = math.inf

        #Visu līniju opciju uzskaitījums tiek veikts, noņemot pēdējo pogu
        while len(tempArrayButtons) > 1:
            lastBtn = tempArrayButtons[-1]
            for btn in tempArrayButtons[0:-1]:
                line = (btn[0], lastBtn[0])
                #šajā gadījumā ir jāveic pirmais datora (AI) gājiens uz visām iespējamām pozīcijām un pēc tam jāizsauc minimax, lai novērtētu katru pozīciju
                tempLines.append(line)
                
                AI_score = self.calculate_virtual_score(tempLines)
                recurseArrayButtons = tempArrayButtons.copy()
                recurseArrayButtons.pop()
                recurseArrayButtons.remove(btn)
                #veicam šī virziena rekursīvu novērtējumu
                #noteikt soda punktu starpību ar spēlētāju, ko AI saņems šīs kustības rezultātā (spēlētāja sods - AI sods)
                #AI uzvar, ja starpība ir > 0
                move_weight = self.alpha_beta(False, 0, recurseArrayButtons, tempLines, AI_score, 0, -math.inf, math.inf)
                move_weight = move_weight - AI_score

                #izvēl lielāko atšķirību starp punktiem
                #papildu nosacījums - ja dažādos virzienos ir vienāds punktu skaits, priekšroka tiek dota virzienam, kurā AI saņem mazāku sodu
                if ((move_weight > bestMoveWeight) or (((AI_score < min_AI_score) or (AI_score == 0)) and (move_weight == bestMoveWeight))):
                    #ja kustības svars ir lielāks par pašreizējo, atjauninām labāko līniju un punktus
                    bestMoveWeight = move_weight
                    bestLine = line
                    min_AI_score = AI_score
                tempLines.pop()
            tempArrayButtons.pop()
        # print(bestMoveWeight, min_AI_score)
        return bestLine

    #iziet cauri visām atbloķētajām pogām, izmantojot rekursiju
    #AI = true - datora gājiens
    #arrayButtons - atlikušās brīvās pogas šim pagrieziena posmam
    #arrayLines - jau uzbūvētas līnijas šim pārvietošanas posmam
    #funkcija atgriež pozīcijas svaru - starpību starp AI un spēlētāja soda punktiem
 def alpha_beta(self, AI, recursive_level, arButtons, arLines, AI_score, player_score, alpha, beta):
    if recursive_level >= self.AI_Level or len(arButtons) <= 1:
        return player_score - AI_score

    bestMoveWeight = -math.inf if AI else math.inf

    while len(arButtons) > 1:
        lastBtn = arButtons[-1]
        for btn in arButtons[:-1]:
            line = (btn[0], lastBtn[0])
            arLines.append(line)
            AI_calculated_score = self.calculate_virtual_score(arLines) if AI else 0
            player_calculated_score = self.calculate_virtual_score(arLines) if not AI else 0
            recurseArrayButtons = arButtons[:]
            recurseArrayButtons.pop()
            recurseArrayButtons.remove(btn)

            move_weight = self.alpha_beta(not AI, recursive_level + 1, recurseArrayButtons, arLines, AI_score + AI_calculated_score, player_score + player_calculated_score, alpha, beta)
            if AI:
                bestMoveWeight = max(bestMoveWeight, move_weight)
                if (bestMoveWeight >= beta):
                    arLines.pop()
                    break
                alpha = max(alpha, bestMoveWeight)

            else:
                bestMoveWeight = min(bestMoveWeight, move_weight)
                if (bestMoveWeight <= alpha):
                    arLines.pop()
                    break   
                beta = min(beta, bestMoveWeight)

            arLines.pop()
        arButtons.pop()

    return bestMoveWeight
    
 def draw_line(self, button1, button2):
        x1, y1 = self.canvas.coords(button1)[0:2]
        x2, y2 = self.canvas.coords(button2)[0:2]
        line = self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10, fill="black")
        self.arrayLines.append(line)
       
        virtualLine =(button1, button2)
        self.arrayVirtualLines.append(virtualLine)

 def check_intersections(self, line1, line2):
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        def ccw(a, b, c):
            if (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0]):
                return True
        if ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and ccw((x1, y1), (x2, y2),(x3, y3)) != ccw((x1, y1),(x2, y2),(x4, y4)):
            return True

 def calculate_score(self):
        score = 0
        #atlase no pēdējās pievienotās rindas masīva
        line1 = self.canvas.coords(self.arrayLines[-1])
        for i in self.arrayLines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                #ja vismaz viena līnija krustojas ar pēdējo, pievienojam soda punktu
                score = score + 1
        return score

    #funkcija punktu aprēķināšanai, izmantojot virtuālu līniju masīvu (lai paātrinātu minmax algoritma darbību)
 def calculate_virtual_score(self, lines):
        score = 0
        endLineButtons = lines[-1]
        #izvilkt pogu pēc tās numura
        targetButton1 = next((element for element in self.arrayVirtualButtons if element[0] == endLineButtons[0]), None)
        targetButton2 = next((element for element in self.arrayVirtualButtons if element[0] == endLineButtons[1]), None)
        endLineCoords = (targetButton1[1], targetButton1[2], targetButton2[1], targetButton2[2], )
        
        #cikla pārbaude, ​​vai pēdējā līnija krustojas ar visām pārējām no masīva
        for curLineButtons in lines[0:-1]:
            #izvilkt pogu pēc tās numura
            targetButton1 = next((element for element in self.arrayVirtualButtons if element[0] == curLineButtons[0]), None)
            targetButton2 = next((element for element in self.arrayVirtualButtons if element[0] == curLineButtons[1]), None)
            curLineCoords = (targetButton1[1], targetButton1[2], targetButton2[1], targetButton2[2], )

            if self.check_intersections(endLineCoords, curLineCoords) == True:
                score = score + 1
        return score
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
    sk = slide.get()
    global n
    n = sk
    slide.destroy()
    btn_ok.destroy()
    l.config(text="Choose who will start")

    def click_c():
        l.config(text="Choose algorithm")
        button_c.config(text="ALPHA-BETA",
                        command=lambda: [button_c.destroy(), button_p.destroy(), computer_alphabeta_start()])
        button_p.config(text="MIN-MAX",
                        command=lambda: [button_c.destroy(), button_p.destroy(), computer_minmax_start()])

    button_c = Button(logs, text="COMPUTER", command=click_c)
    button_c.pack(side='left', expand=True)

    def click_p():
        l.config(text="Choose algorithm")
        button_c.config(text="ALPHA-BETA",
                        command=lambda: [button_c.destroy(), button_p.destroy(), player_alphabeta_start()])
        button_p.config(text="MIN-MAX", command=lambda: [button_c.destroy(), button_p.destroy(), player_minmax_start()])

    button_p = Button(logs, text="PLAYER", command=click_p)
    button_p.pack(side='right', expand=True)

logs = tk.Tk()
logs.title("Game 41")
logs.geometry("500x500")
l = Label(logs, text="Choose number of fields", font=("Arial", 12))
l.pack()
slide = Scale(logs, from_=15, to=25, orient=HORIZONTAL)
slide.pack(pady=40)
btn_ok = Button(logs, text="OK", command=click_ok)
btn_ok.pack()
logs.mainloop()
