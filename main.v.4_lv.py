import tkinter as tk
import math
from tkinter import *
import random


class player_minmax_game:
    #Klases inicializācijas funkcija, kas tiek izsaukta, izveidojot objektu.
    def __init__(self, master, n):
        self.player_sods = 0
        self.computer_sods = 0
        self.master = master
        self.numberOfPoints = n
        self.arrayButtons = []
        self.arraySelectedButtons = []
        self.arrayLockedButtons = []
        self.arrayLines = []
        
        #Virtuālo pogu un līniju masīvi, lai paātrinātu minimaksa algoritmu.
        #Minimaksas algoritmam darbības laikā jāizvairās no jebkādām grafiskām kanvas objektu darbībām.        self.arrayVirtualLines = []
        self.arrayVirtualLines = []
        self.arrayVirtualButtons = []
        self.minimaxCounter = 0

        self.player_turn = True
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
        #Funkcijas beigas; turpmāk tiks izsaukts notikumu apstrādātājs 'on click', kad tiks nospiesta jebkura no pogām ap apli.


    #Funkcija, kas izveido pogas un izvieto tās ap apli. Leņķis ir proporcionāls pogu skaitam.
    def generate_buttons(self):
        for i in range(self.numberOfPoints):
            angle = i * (360 / self.numberOfPoints)
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150 * math.sin(math.radians(angle))

            button = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white")
            self.arrayButtons.append(button)
            #Pievienot pogas koordinātas atsevišķā masīvā turpmākām aprēķinām.
            virtualButton =(x,y)
            self.arrayVirtualButtons.append(virtualButton)


    def update_score(self):
        txt1 = "player penalty: " + str(self.player_sods)
        txt2 = "computer penalty: " + str(self.computer_sods)
        self.lbl_player_info.config(text=txt1)
        self.lbl_computer_info.config(text=txt2)

    #Nepieciešama papildināšana funkcijā, lai apstrādātu vienkāršu loga aizvēršanu bez pogu nospiešanas.
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
        for button in self.arrayButtons:
            self.canvas.itemconfig(button, fill="white")
        self.player_sods = 0
        self.computer_sods = 0
        self.arrayLockedButtons.clear()
        self.arraySelectedButtons.clear()
        self.lbl_player_info.config(text="player penalty: 0")
        self.lbl_computer_info.config(text="computer penalty: 0")
        self.player_turn = True

    #Funkcija, kas apstrādā apļa formas pogas klikšķi, izvēloties divas pogas vienādai algoritma solim.
    def player_click(self, event):
        #Funkcija darbojas tikai tad, ja spēlētājs ir gājums.
        if self.player_turn == True:
            #pogas objekta iegūšana pēc aptuvenām koordinātām (var noklikšķināt blakus)
            button = self.canvas.find_closest(event.x, event.y)[0]
            #ģenerējot visu atbloķēto pogu sarakstu
            non_locked_buttons = [button for button in self.arrayButtons if button not in self.arrayLockedButtons]
            if button in non_locked_buttons:
                #poga nav bloķēta, pārbaudit, vai ir atlasīta otrā poga
                if len(self.arraySelectedButtons) < 2:
                    #otrā poga nav atlasīta - ievietot šo pogu atlasīto un bloķēto pogu masīvos
                    self.arraySelectedButtons.append(button)
                    self.arrayLockedButtons.append(button)
                    #krāso pogu sarkanā krāsā
                    self.canvas.itemconfig(button, fill="red")
                #pārbaudīt spēles beigas (bloķēto pogu skaits ir vienāds ar kopējo pogu skaitu)
                if len(self.arraySelectedButtons) == 1 and self.numberOfPoints - len(self.arrayLockedButtons) == 0:
                    self.arraySelectedButtons.clear()
                    self.arrayLockedButtons.clear()
                    self.who_won()
                #ja ir atlasītas abas pogas
                if len(self.arraySelectedButtons) == 2:
                    button1, button2 = self.arraySelectedButtons
                    #novelc līniju starp pogām un ievieto to masīvā
                    self.draw_line(button1, button2)
                    self.arraySelectedButtons.clear()
                    #atjaunināt virtuālo pogu (koordinātu) masīvu. masīvā ir tikai brīvas pogas
                    self.update_virtual_buttons()

                    self.player_sods = self.player_sods + self.calculate_score()
                    self.update_score()

#                    test = self.calculate_virtual_score(self.arrayVirtualLines)
#                    print("score: ", test)

                    self.update_score()

                    #pārbaude spēles beigas - tiek izmantotas visas pogas
                    if self.numberOfPoints - len(self.arrayLockedButtons) < 2:
                        self.arraySelectedButtons.clear()
                        self.arrayLockedButtons.clear()
                        self.who_won()
                    else:
                        self.player_turn = False
                        #veikt datora kustību
                        self.master.after(300, self.computer_turn)

    def computer_turn(self):
        if self.player_turn == False:
          #  non_locked_buttons = [button for button in self.arrayButtons if button not in self.arrayLockedButtons]
            
            #datoram ir jāizvēlas divas pogas
            #selected_buttons = random.sample(non_locked_buttons, 2)  # Te vajag minmax algoritmu

            #aprēķinat labākās līnijas koordinātas
            line = self.find_best_line()
            #pogu objektu iegūšana pēc virtuālajām koordinātām
            selected_buttons = []
            selected_buttons.append(self.canvas.find_closest(line[0], line[1])[0])
            selected_buttons.append(self.canvas.find_closest(line[2], line[3])[0])       
            
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
                    self.update_virtual_buttons()
                    self.computer_sods = self.computer_sods + self.calculate_score()                   
                    if self.numberOfPoints - len(self.arrayLockedButtons) < 2:
                        self.arraySelectedButtons.clear()
                        self.arrayLockedButtons.clear()
                        self.who_won()
                    else:
                        self.player_turn = True


    #atjaunot virtuālo pogu masīvu. izmantotās pogas tiks noņemtas no masīva
    def update_virtual_buttons(self):
        self.arrayVirtualButtons.clear()
        non_locked_buttons = [button for button in self.arrayButtons if button not in self.arrayLockedButtons]
        for curBtn in non_locked_buttons:
            self.arrayVirtualButtons.append(self.canvas.coords(curBtn)[0:2])

        print("Virtual buttons updated, count : ", len(self.arrayVirtualButtons))
    

    #labākā kustību noteikšanas funkcija
    #izmanto virkni virtuālo pogu (2 koordinātes). Lai algoritms darbotos, ir nepieciešamas tikai brīvas pogas
    #pēc katras reālas kustības šis masīvs ir jāatjauno, noņemot aizņemtās pogas (funkcija update_virtual_buttons)
    #izmanto pašreizējo virtuālo līniju masīvu (4 koordinātes), kas tiek atjaunināts funkcijā draw_line
    #sāk cilpu caur visām pogām, kamēr ir brīvas, novelk līniju un izsauc minmax funkciju
    def find_best_line(self):

        #pārbaudīt virtuālās pogas un līnijas
        selected_buttons = random.sample(self.arrayVirtualButtons, 2)
        bestLine = (selected_buttons[0][0], selected_buttons[0][1], selected_buttons[1][0], selected_buttons[1][1])

        #masīvs, kurā pievienosim ģenerētās līnijas, aprēķinot punktus katrai cilpas rindai un saglabājot un atjauninot pozīciju, ja rindā ir maksimālais punktu skaits
        tempLines = self.arrayVirtualLines.copy()
        bestScore = -1
        tempArrayButtons = self.arrayVirtualButtons.copy()
        #pārvietoties pa virtuālajām pogām. iziet visas rindas secībā un katrai izsauciet funkciju mini_max
        #Visu līniju opciju uzskaitījums tiek veikts, noņemot pēdējo pogu
        while len(tempArrayButtons) > 1:
            #veiciet iekšējo cilpu, novelciet līniju no pēdējās pogas līdz visām pārējām un katrai rindai izsaucam minimax, lai iegūtu aprēķinu
            #šī ir pēdējā poga masīvā
            lastBtn = tempArrayButtons[-1]
            for btn in tempArrayButtons[0:-1]:
                line = (btn[0],btn[1],lastBtn[0],lastBtn[1])
                #pievienojam līniju no pašreizējā cilpas punkta līdz pēdējam punktam
                tempLines.append(line)
                
                #veicam šī virziena rekursīvu novērtējumu
#                score = self.calculate_virtual_score(tempLines)
                #noņemt pogas, kurām tiek novilkta pašreizējā līnija, no masīva, kuru mēs nosūtām uz mini_max
                recurseArrayButtons = tempArrayButtons.copy()
                del recurseArrayButtons[-1]
                recurseArrayButtons.remove(btn)
                self.minimaxCounter = 0
                score = self.mini_max(recurseArrayButtons, tempLines, 1)

#                print("Line: ", line, "Score:", score)

                #ir jāatlasa vismaz viena opcija un jāinicializē mainīgais (ja nav labu opciju, jāizvēlas vismazāk sliktā)
                if (bestScore == -1):
                    bestScore = score
                    bestLine = line

                if (score < bestScore):
                    #ja punktu skaits ir lielāks par pašreizējo, atjauninām savu labāko līniju un punktus
                    bestScore = score
                    bestLine = line
                #noņemiet šo līniju no masīva, lai tā netraucētu turpmākiem aprēķiniem
                del tempLines[-1]
            #izdzēšam pēdējo pogu, jo visas līnijas tika izveidotas tai
            del tempArrayButtons[-1]

        print ("Best line : ", bestLine)
        return bestLine

    #iziet cauri visām atbloķētajām pogām, izmantojot rekursīvu (zvanu??)
    #player: -1 - datora gājiens, 1 - spēlētāja gājiens
    #arrayButtons - atlikušās brīvās pogas šim pagrieziena posmam
    #arrayLines - jau uzbūvētas līnijas šim pārvietošanas posmam
    #funkcija atgriež punktu skaitu pašreizējai pozīcijai
    def mini_max(self, arButtons, arLines, player):
  
        #1. Aprēķinam pašreizējo punktu skaitu, izmantojot pēdējo novilkto līniju no arrayLines check_intersections
        #2. pārbaudām, vai ir pietiekami daudz punktu, lai novilktu līniju; ja nē, nekavējoties atgriežam punktu skaitu pēc pēdējās linijas
        #3. ja vēl ir punkti, liekam līnijas pēc kārtas visās vietās un katrā gadījumā izsauc min_max
        #4. izvēlamies labāko punktu skaitu, pievienojiet tos sākumā saņemtajam un atgriezieties
        #5. Izvēloties optimālo punktu skaitu, tas ietekmē to, kam mēs veicam gājienu. spēlētājs=1 spēlētājs kustas, spēlētājs=-1 - dators

        ###### ierobežojot meklēšanas koka dziļumu #######################
        if (self.minimaxCounter > 3):
            return 0

#        print("-> MiniMax call: ", self.minimaxCounter)
        self.minimaxCounter = self.minimaxCounter + 1

        currentScore = self.calculate_virtual_score(arLines)
        if (len(arButtons) <= 1):
#            print("<- MiniMax return1: ", self.minimaxCounter)
            self.minimaxCounter = self.minimaxCounter - 1
            return currentScore
        
        bestScore = -1
        while len(arButtons) > 1:
            #veicam iekšējo cilpu, novelkam līniju no pēdējās pogas līdz visām pārējām un katrai rindai izsauciet minimax, lai iegūtu aprēķinu
            #šī ir pēdējā poga mūsu masīvā
            lastBtn = arButtons[-1]
            for btn in arButtons[0:-1]:
                line = (btn[0],btn[1],lastBtn[0],lastBtn[1])
                #pievienojiet līniju no pašreizējā cilpas punkta līdz pēdējam punktam
                #TODO: проблема - мы добавляем ту же самую линию. необходимо при каждом новом вызове алгоритма сдвигать точку
                arLines.append(line)
                
                #veicam šī virziena rekursīvu novērtējumu
                #noņemam pogas, kurām tiek novilkta pašreizējā līnija, no masīva, kuru mēs nosūtām uz mini_max
                recurseArrayButtons = arButtons.copy()
                del recurseArrayButtons[-1]
                recurseArrayButtons.remove(btn)
                score = self.mini_max(recurseArrayButtons, arLines, player*-1)
#                print("Line: ", line, "Score:", score)

                #ir jāatlasa vismaz viena opcija un jāinicializē mainīgais (ja nav labu opciju, jāizvēlas vismazāk sliktā)
                if (bestScore == -1):
                    bestScore = score

                #TODO: необходимо оценивать очки в зависимости от того, чей ход

                if (score < bestScore):
                    #ja punktu skaits ir lielāks par pašreizējo, atjauniniet punktus
                    bestScore = score

                #noņemam šo līniju no masīva, lai tā netraucētu turpmākiem aprēķiniem
                del arLines[-1]
            #izdzēšam pēdējo pogu, jo visas līnijas tika izveidotas tai
            del arButtons[-1]

#        print("<- MiniMax return2: ", self.minimaxCounter)
        self.minimaxCounter = self.minimaxCounter - 1

        return currentScore+bestScore
    
    #funkcija līnijas zīmēšanai un pievienošanai masīvam
    def draw_line(self, button1, button2):
        x1, y1 = self.canvas.coords(button1)[0:2]
        x2, y2 = self.canvas.coords(button2)[0:2]
        line = self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10, fill="black")
        self.arrayLines.append(line)
       
        virtualLine =(x1 + 10, y1 + 10, x2 + 10, y2 + 10)
        self.arrayVirtualLines.append(virtualLine)

        if (self.player_turn):
            print("Player set line: ", virtualLine)
        else:
            print("Computer set line: ", virtualLine)

    #функция проверки пересечения двух линий (изпользует алгоритм CCW), источник StackOverflow.com
    def check_intersections(self, line1, line2):
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        #funkcija, lai pārbaudītu trīs punktu atrašanās vietu telpā pretēji pulksteņrādītāja virzienam (Counter Clock Wise)
        def ccw(a, b, c):
            if (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0]):
                return True

        # A(x1, y1) B(x2, y2)       C(x3, y3) D(x4, y4)
        #два отрезка AB и CD пересекаются тогда и только тогда, когда точки A и B разделены отрезком CD, а точки C и D разделены отрезком AB. 
        #eсли точки A и B разделены отрезком CD, то ACD и BCD должны иметь противоположную ориентацию, 
        #что означает, что либо ACD, либо BCD вращаются против часовой стрелки, но не оба одновременно
        #поэтому расчет пересечения двух отрезков AB и CD осуществляется следующим образом:
        if ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and ccw((x1, y1), (x2, y2),(x3, y3)) != ccw((x1, y1),(x2, y2),(x4, y4)):
            return True


    def calculate_score(self):
        score = 0
        #atlase no pēdējās pievienotās rindas masīva
        line1 = self.canvas.coords(self.arrayLines[-1])
        #cilpa pārbauda, ​​vai pēdējā rinda krustojas ar visām pārējām no masīva
        for i in self.arrayLines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                #ja vismaz viena līnija krustojas ar pēdējo, pievienojam soda punktu
                score = score + 1
        return score

    #funkcija punktu aprēķināšanai, izmantojot virtuālu līniju masīvu (lai paātrinātu minmax algoritma darbību)
    def calculate_virtual_score(self, lines):
        score = 0
        #atlase no pēdējās pievienotās rindas masīva
        endLine = lines[-1]
        #cilpa pārbauda, ​​vai pēdējā rinda krustojas ar visām pārējām no masīva
        for curLine in lines[0:-1]:
            if self.check_intersections(endLine, curLine) == True:
                #ja vismaz viena līnija krustojas ar pēdējo, pievienojam soda punktu
                score = score + 1
        return score

"""
    def calculate_computer_score(self):
        line1 = self.canvas.coords(self.arrayLines[-1])
        for i in self.arrayLines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                self.computer_sods = self.computer_sods + 1
"""

###########################################################################################################
class computer_minmax_game:
    def __init__(self, master, n):
        self.player_sods = 0
        self.computer_sods = 0
        self.master = master
        self.n = n
        self.buttons = []
        self.selected_buttons = []
        self.locked_buttons = []
        self.lines = []
        self.player_turn = False
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.generate_buttons()
        self.canvas.bind("<Button-1>", self.player_click)
        self.player_info = Label(self.canvas, text="player penalty: 0", fg="red", font=("Arial", 10), anchor="nw")
        self.player_info.pack()
        self.canvas.create_window(410, 50, window=self.player_info)
        self.computer_info = Label(self.canvas, text="computer penalty: 0", fg="blue", font=("Arial", 10), anchor="ne")
        self.computer_info.pack()
        self.canvas.create_window(90, 50, window=self.computer_info)
        self.computer_turn()

    def generate_buttons(self):
        for i in range(self.n):
            angle = i * (360 / self.n)
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150 * math.sin(math.radians(angle))
            button = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white")
            self.buttons.append(button)

    def update_score(self):
        txt1 = "player penalty: " + str(self.player_sods)
        txt2 = "computer penalty: " + str(self.computer_sods)
        self.player_info.config(text=txt1)
        self.computer_info.config(text=txt2)

    def who_won(self):
        end_logs = Toplevel()
        end_logs.title("game over")
        end_logs.geometry("300x200")
        l2 = Label(end_logs, text="", font=("Arial", 12))
        l2.pack(pady=20)
        restart_btn = Button(end_logs, text="Restart", command=lambda: [self.restart_game(), end_logs.destroy()])
        restart_btn.pack(pady=20)
        exit_btn = Button(end_logs, text="Exit", command=self.master.quit)
        exit_btn.pack(pady=20)
        if self.player_sods > self.computer_sods:
            l2.config(text="Computer wins")

        elif self.player_sods < self.computer_sods:
            l2.config(text="Player wins")

        elif self.player_sods == self.computer_sods:
            l2.config(text="Draw")

    def restart_game(self):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()
        for button in self.buttons:
            self.canvas.itemconfig(button, fill="white")
        self.player_sods = 0
        self.computer_sods = 0
        self.locked_buttons.clear()
        self.selected_buttons.clear()
        self.player_info.config(text="player penalty: 0")
        self.computer_info.config(text="computer penalty: 0")
        self.player_turn = False
        self.master.after(300, self.computer_turn)

    def player_click(self, event):
        if self.player_turn == True:
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
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.check_player()
                    self.update_score()
                    if self.n - len(self.locked_buttons) < 2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    else:
                        self.player_turn = False
                        self.master.after(300, self.computer_turn)

    def computer_turn(self):
        if self.player_turn == False:
            non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
            selected_buttons = random.sample(non_locked_buttons, 2)  # Te vajag minmax algoritmu
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
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.check_computer()
                    self.update_score()
                    if self.n - len(self.locked_buttons) < 2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    else:
                        self.player_turn = True

    def draw_line(self, button1, button2):
        x1, y1 = self.canvas.coords(button1)[0:2]
        x2, y2 = self.canvas.coords(button2)[0:2]
        line = self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10, fill="black")
        self.lines.append(line)

    def check_intersections(self, line1, line2):
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        def ccw(a, b, c):
            if (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0]):
                return True

        if ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and ccw((x1, y1), (x2, y2),
                                                                                          (x3, y3)) != ccw((x1, y1),
                                                                                                           (x2, y2),
                                                                                                           (x4, y4)):
            return True

    def check_player(self):
        line1 = self.canvas.coords(self.lines[-1])
        for i in self.lines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                self.player_sods = self.player_sods + 1

    def check_computer(self):
        line1 = self.canvas.coords(self.lines[-1])
        for i in self.lines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                self.computer_sods = self.computer_sods + 1


###########################################################################################################
class player_alphabeta_game:
    def __init__(self, master, n):
        self.player_sods = 0
        self.computer_sods = 0
        self.master = master
        self.n = n
        self.buttons = []
        self.selected_buttons = []
        self.locked_buttons = []
        self.lines = []
        self.player_turn = True
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.generate_buttons()
        self.canvas.bind("<Button-1>", self.player_click)
        self.player_info = Label(self.canvas, text="player penalty: 0", fg="red", font=("Arial", 10), anchor="nw")
        self.player_info.pack()
        self.canvas.create_window(410, 50, window=self.player_info)
        self.computer_info = Label(self.canvas, text="computer penalty: 0", fg="blue", font=("Arial", 10), anchor="ne")
        self.computer_info.pack()
        self.canvas.create_window(90, 50, window=self.computer_info)

    def generate_buttons(self):
        for i in range(self.n):
            angle = i * (360 / self.n)
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150 * math.sin(math.radians(angle))
            button = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white")
            self.buttons.append(button)

    def update_score(self):
        txt1 = "player penalty: " + str(self.player_sods)
        txt2 = "computer penalty: " + str(self.computer_sods)
        self.player_info.config(text=txt1)
        self.computer_info.config(text=txt2)

    def who_won(self):
        end_logs = Toplevel()
        end_logs.title("game over")
        end_logs.geometry("300x200")
        l2 = Label(end_logs, text="", font=("Arial", 12))
        l2.pack(pady=20)
        restart_btn = Button(end_logs, text="Restart", command=lambda: [self.restart_game(), end_logs.destroy()])
        restart_btn.pack(pady=20)
        exit_btn = Button(end_logs, text="Exit", command=self.master.quit)
        exit_btn.pack(pady=20)
        if self.player_sods > self.computer_sods:
            l2.config(text="Computer wins")

        elif self.player_sods < self.computer_sods:
            l2.config(text="Player wins")

        elif self.player_sods == self.computer_sods:
            l2.config(text="Draw")

    def restart_game(self):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()
        for button in self.buttons:
            self.canvas.itemconfig(button, fill="white")
        self.player_sods = 0
        self.computer_sods = 0
        self.locked_buttons.clear()
        self.selected_buttons.clear()
        self.player_info.config(text="player penalty: 0")
        self.computer_info.config(text="computer penalty: 0")
        self.player_turn = True

    def player_click(self, event):
        if self.player_turn == True:
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
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.check_player()
                    self.update_score()
                    if self.n - len(self.locked_buttons) < 2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    else:
                        self.player_turn = False
                        self.master.after(300, self.computer_turn)

    def computer_turn(self):
        if self.player_turn == False:
            non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
            selected_buttons = random.sample(non_locked_buttons, 2)  # Te vajag alpha beta algoritmu
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
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.check_computer()
                    self.update_score()
                    if self.n - len(self.locked_buttons) < 2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    else:
                        self.player_turn = True

    def draw_line(self, button1, button2):
        x1, y1 = self.canvas.coords(button1)[0:2]
        x2, y2 = self.canvas.coords(button2)[0:2]
        line = self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10, fill="black")
        self.lines.append(line)

    def check_intersections(self, line1, line2):
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        def ccw(a, b, c):
            if (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0]):
                return True

        if ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and ccw((x1, y1), (x2, y2),
                                                                                          (x3, y3)) != ccw((x1, y1),
                                                                                                           (x2, y2),
                                                                                                           (x4, y4)):
            return True

    def check_player(self):
        line1 = self.canvas.coords(self.lines[-1])
        for i in self.lines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                self.player_sods = self.player_sods + 1

    def check_computer(self):
        line1 = self.canvas.coords(self.lines[-1])
        for i in self.lines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                self.computer_sods = self.computer_sods + 1


###########################################################################################################
class computer_alphabeta_game:
    def __init__(self, master, n):
        self.player_sods = 0
        self.computer_sods = 0
        self.master = master
        self.n = n
        self.buttons = []
        self.selected_buttons = []
        self.locked_buttons = []
        self.lines = []
        self.player_turn = False
        self.canvas = tk.Canvas(master, width=500, height=500)
        self.canvas.pack()
        self.generate_buttons()
        self.canvas.bind("<Button-1>", self.player_click)
        self.player_info = Label(self.canvas, text="player penalty: 0", fg="red", font=("Arial", 10), anchor="nw")
        self.player_info.pack()
        self.canvas.create_window(410, 50, window=self.player_info)
        self.computer_info = Label(self.canvas, text="computer penalty: 0", fg="blue", font=("Arial", 10), anchor="ne")
        self.computer_info.pack()
        self.canvas.create_window(90, 50, window=self.computer_info)
        self.computer_turn()

    def generate_buttons(self):
        for i in range(self.n):
            angle = i * (360 / self.n)
            x = 250 + 150 * math.cos(math.radians(angle))
            y = 250 + 150 * math.sin(math.radians(angle))
            button = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="white")
            self.buttons.append(button)

    def update_score(self):
        txt1 = "player penalty: " + str(self.player_sods)
        txt2 = "computer penalty: " + str(self.computer_sods)
        self.player_info.config(text=txt1)
        self.computer_info.config(text=txt2)

    def who_won(self):
        end_logs = Toplevel()
        end_logs.title("game over")
        end_logs.geometry("300x200")
        l2 = Label(end_logs, text="", font=("Arial", 12))
        l2.pack(pady=20)
        restart_btn = Button(end_logs, text="Restart", command=lambda: [self.restart_game(), end_logs.destroy()])
        restart_btn.pack(pady=20)
        exit_btn = Button(end_logs, text="Exit", command=self.master.quit)
        exit_btn.pack(pady=20)
        if self.player_sods > self.computer_sods:
            l2.config(text="Computer wins")

        elif self.player_sods < self.computer_sods:
            l2.config(text="Player wins")

        elif self.player_sods == self.computer_sods:
            l2.config(text="Draw")

    def restart_game(self):
        for line in self.lines:
            self.canvas.delete(line)
        self.lines.clear()
        for button in self.buttons:
            self.canvas.itemconfig(button, fill="white")
        self.player_sods = 0
        self.computer_sods = 0
        self.locked_buttons.clear()
        self.selected_buttons.clear()
        self.player_info.config(text="player penalty: 0")
        self.computer_info.config(text="computer penalty: 0")
        self.player_turn = False
        self.master.after(300, self.computer_turn)

    def player_click(self, event):
        if self.player_turn == True:
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
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.check_player()
                    self.update_score()
                    if self.n - len(self.locked_buttons) < 2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    else:
                        self.player_turn = False
                        self.master.after(300, self.computer_turn)

    def computer_turn(self):
        if self.player_turn == False:
            non_locked_buttons = [button for button in self.buttons if button not in self.locked_buttons]
            selected_buttons = random.sample(non_locked_buttons, 2)  # Te vajag alpha beta algoritmu
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
                    self.draw_line(button1, button2)
                    self.selected_buttons.clear()
                    self.check_computer()
                    self.update_score()
                    if self.n - len(self.locked_buttons) < 2:
                        self.selected_buttons.clear()
                        self.locked_buttons.clear()
                        self.who_won()
                    else:
                        self.player_turn = True

    def draw_line(self, button1, button2):
        x1, y1 = self.canvas.coords(button1)[0:2]
        x2, y2 = self.canvas.coords(button2)[0:2]
        line = self.canvas.create_line(x1 + 10, y1 + 10, x2 + 10, y2 + 10, fill="black")
        self.lines.append(line)

    def check_intersections(self, line1, line2):
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2

        def ccw(a, b, c):
            if (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0]):
                return True

        if ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and ccw((x1, y1), (x2, y2),
                                                                                          (x3, y3)) != ccw((x1, y1),
                                                                                                           (x2, y2),
                                                                                                           (x4, y4)):
            return True

    def check_player(self):
        line1 = self.canvas.coords(self.lines[-1])
        for i in self.lines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                self.player_sods = self.player_sods + 1

    def check_computer(self):
        line1 = self.canvas.coords(self.lines[-1])
        for i in self.lines[0:-1]:
            line2 = self.canvas.coords(i)
            if self.check_intersections(line1, line2) == True:
                self.computer_sods = self.computer_sods + 1


###########################################################################################################

def player_minmax_start():
    l.destroy()
    player_minmax_game(logs, n)


def computer_minmax_start():
    l.destroy()
    computer_minmax_game(logs, n)


def player_alphabeta_start():
    l.destroy()
    player_alphabeta_game(logs, n)


def computer_alphabeta_start():
    l.destroy()
    computer_alphabeta_game(logs, n)


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
logs.title("Game 41 test4lv")
logs.geometry("500x500")
l = Label(logs, text="Choose number of fields", font=("Arial", 12))
l.pack()
slide = Scale(logs, from_=15, to=25, orient=HORIZONTAL)
slide.pack(pady=40)
btn_ok = Button(logs, text="OK", command=click_ok)
btn_ok.pack()

logs.mainloop()