import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import random
import threading
import time

import sys
sys.setrecursionlimit(10000)

var = tk.IntVar
cell_list = []
sub_regions = {'sg1':[], 'sg2':[], 'sg3':[], 'sg4':[], 'sg5':[], 'sg6':[], 'sg7':[], 'sg8':[], 'sg9':[]}
key_code = {49:'1', 50:'2', 51:'3', 52:'4', 53:'5', 54:'6', 55:'7', 56:'8', 57:'9'}



class Cell(tk.Canvas):
    def __init__(self, master, **kwargs):
        tk.Canvas.__init__(self, master, width=40, relief='sunken', bd=2, height=40, bg='white')
        self.row = kwargs['row']
        self.col = kwargs['col']

        self.sub_region = None
        self.locked = False
        self.phantom_number = 0

        self.text = self.create_text(25, 25, fill="black", font="Roboto 20",text="")

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)
        self.wm_iconbitmap('images/scicon2.ico')
        self.title("SAM'S SUDOCU")


        #######  ------------------------     bind     ------------------------ #######
        self.bind('<Left>', self.left)
        self.bind('<Right>', self.right)
        self.bind('<Up>', self.up)
        self.bind('<Down>', self.down)
        self.bind('<Key>', self.insert_number)
        #######  ------------------------     bind     ------------------------ #######


        self.state = 'standby'
        self.timer = 300
        self.row = 0
        self.col = 0


        #######  ------------------------     images     ------------------------ #######
        self.p = PhotoImage(file='images\play2.png')
        self.p_image = self.p.subsample(2, 2)
        # -------------------
        self.s = PhotoImage(file='images\stop2.png')
        self.s_image = self.s.subsample(2, 2)
        # -------------------
        self.rv = PhotoImage(file='images\solution1.png')
        self.rv_image = self.rv.subsample(2, 2)
        # -------------------
        self.r = PhotoImage(file='images/refresh1.png')
        self.r_image = self.r.subsample(2, 2)
        # -------------------
        self.t = PhotoImage(file='images/time1.png')
        self.t_image = self.t.subsample(2, 2)
        #######  ------------------------     images     ------------------------ #######


        #######  ------------------------      GUI       ------------------------ #######
        self.frame = tk.Frame(self)
        self.frame.pack(side='top', pady=10)
        # -------------------
        self.frame_btn = tk.Frame(self.frame)
        self.frame_btn.pack(side='left', padx=50)
        # -------------------
        self.time_label = tk.Label(self.frame, text='05 : 00', font=('Roboto, 20'))
        self.time_label.pack(side='right', pady=5, anchor='ne')
        self.time_label.configure(image=self.t_image, compound='left')
        # -------------------
        self.canvas_frame = tk.Frame(self, relief='raised', bd=5)
        self.canvas_frame.pack(pady=5, padx=5, side='bottom', anchor='s')
        self.canvas = tk.Canvas(self.canvas_frame, relief='groove')
        self.canvas.pack(padx=20, pady=20)
        # -------------------
        self.start_btn = tk.Button(self.frame_btn, text='Start', image=self.p_image, font=('Roboto', 15),
                                   width=50, height=50, command=lambda:self.start())
        self.start_btn.pack(side='left')
        # -------------------
        self.stop_btn = tk.Button(self.frame_btn, text='Stop', image=self.s_image, font=('Roboto', 15),
                                  width=50, height=50, command=lambda: self.stop())
        self.stop_btn.pack(side='left')
        # -------------------
        self.solve_btn = tk.Button(self.frame_btn, text='Solve', image=self.rv_image, font=('Roboto', 15), width=50,
                                   height=50, command=lambda: self.surrender())
        self.solve_btn.pack(side='left')
        #######  ------------------------      GUI       ------------------------ #######


        self.CreateBox()
        self.draw_grid()


    def CreateBox(self):

        ''' Creation of 9x9 boxex '''

        for i in range(9):
            row = []
            for j in range(9):
                self.cell = Cell(self.canvas, row=i, col=j)
                self.cell.grid(row=i, column=j, padx=1, pady=1)

                row.append(self.cell)

                ### assigning boxes to their respective subregions
                if i <= 2:
                    if j <= 2:
                        sub_regions['sg1'].append(self.cell)
                        self.cell.sub_region = 'sg1'
                    if j > 2 and j <= 5:
                        sub_regions['sg2'].append(self.cell)
                        self.cell.sub_region = 'sg2'
                    if j > 5 and j <= 8:
                        sub_regions['sg3'].append(self.cell)
                        self.cell.sub_region = 'sg3'
                if i > 2 and i <=5:
                    if j <= 2:
                        sub_regions['sg4'].append(self.cell)
                        self.cell.sub_region = 'sg4'
                    if j > 2 and j <= 5:
                        sub_regions['sg5'].append(self.cell)
                        self.cell.sub_region = 'sg5'
                    if j > 5 and j <= 8:
                        sub_regions['sg6'].append(self.cell)
                        self.cell.sub_region = 'sg6'
                if i > 5 and i <=8:
                    if j <= 2:
                        sub_regions['sg7'].append(self.cell)
                        self.cell.sub_region = 'sg7'
                    if j > 2 and j <= 5:
                        sub_regions['sg8'].append(self.cell)
                        self.cell.sub_region = 'sg8'
                    if j > 5 and j <= 8:
                        sub_regions['sg9'].append(self.cell)
                        self.cell.sub_region = 'sg9'
            cell_list.append(row)


    def draw_grid(self):

        ''' To draw four line to differentiate the 3x3 box  '''

        y = 150
        x = 150
        for i in range(2):
            self.canvas.create_line(x, 4, x, 447, width=2, fill='black')
            self.canvas.create_line(4, y, 447, y, width=2, fill='black')
            x += 150
            y += 150


    def stop(self):

        ''' stop the game and time of the counter '''

        self.state = 'standby'
        self.time_label.configure(text='05 : 00')
        self.timer = 300
        self.start_btn.configure(image=self.p_image)


    def start(self):

        ''' Activating all the components of the game to star to play '''

        self.timer = 300
        self.start_btn.configure(image=self.r_image)
        self.generate_random_given_numbers()
        cell_list[self.row][self.col].configure(bg='grey')
        cell_list[self.row][self.col].focus_set()
        if self.state != 'playing':
            self.state = 'playing'
            t = threading.Thread(target=self.timing)
            t.start()


    def surrender(self):

        ''' stop the game and show the solution '''

        self.state = 'standby'
        self.time_label.configure(text='05 : 00')
        self.timer = 300
        for i in range(9):
            for j in range(9):
                cell_list[i][j].itemconfigure(cell_list[i][j].text, text=cell_list[i][j].phantom_number)


    def get_time(self, sec):

        ''' convert the seconds/divide the time into minute and seconds '''

        hours = sec // 3600
        sec %= 3600
        mins = sec // 60
        sec %= 60
        s = str(sec) if len(str(sec)) == 2 else '0' + str(sec)
        m = str(mins) if len(str(mins)) == 2 else '0' + str(mins)
        return [str(m), str(s)]


    def timing(self):

        ''' run the time '''

        while self.state == 'playing':
            time.sleep(1)
            clock = self.get_time(self.timer)
            self.time_label.configure(text='{} : {}'.format(clock[0], clock[1]))
            if clock[0] == '00' and clock[1] == '00':
                self.state = 'standby'
                self.timer = 300
                self.time_label.configure(text='05 : 00')
                tk.messagebox.showwarning('Game Over', 'Sorry! Your time is out')
            self.timer -= 1


    def find_empty_box(self):

        ''' function that loop all the boxes and find usually the first empty box '''

        for i in range(9):
            for j in range(9):
                if cell_list[i][j].phantom_number == 0:
                    return (i, j)


    def check_phantom(self, pos, num):

        ''' check the coresponding number of a box that is hedden to the player '''

        for i in range(9):
            if i != pos[1]:
                if cell_list[pos[0]][i].phantom_number == num:
                    return True
            if i != pos[0]:
                if cell_list[i][pos[1]].phantom_number == num:
                    return True
            target = cell_list[pos[0]][pos[1]]
            for l in sub_regions[target.sub_region]:
                if target != l:
                    if num == l.phantom_number:
                        return True


    def solve(self, pos):

        ''' searching the right number of every boxes '''

        if cell_list[pos[0]][pos[1]].locked == False:
            try:
                if pos[0] <= 8 and pos[1] <=  8:
                    x = pos[0]
                    y = pos[1]
                    target = cell_list[x][y]

                    number = target.phantom_number + 1
                    target.phantom_number = number
                    if number <= 9:
                        if self.check_phantom(pos, number):
                            self.solve((x, y))
                        else:
                            self.solve(self.find_empty_box())
                    else:
                        target.phantom_number = 0
                        if y == 0:
                            self.solve((x - 1, 8))
                        else:
                            self.solve((x, y - 1))
            except:
                return
        else:
            if pos[8] == 0:
                self.solve((pos[0] + 1, 0))
            else:
                self.solve((pos[0], pos[1] + 1))



    def generate_random_given_numbers(self):

        ''' Generating random given numbers and inserting them onto the random box '''

        # reseting all phantom numbers to 0 for refresh request
        for i in range(9):
            for j in range(9):
                cell_list[i][j].phantom_number = 0
                cell_list[i][j].locked = False
                cell_list[i][j].itemconfigure(cell_list[i][j].text, text='')

        # generate first 9 in random order on first row:
        # it is necessary to be able to generate unique random given number
        num = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(9):
            number = num.pop(num.index(random.choice(num)))
            cell_list[0][i].phantom_number = number

        # starting to solve every box
        self.solve(self.find_empty_box())

        # selecting random box to be locked
        for i in range(20):
            locked = False
            while locked == False:
                x = random.randint(0, 8)
                y = random.randint(0, 8)
                if cell_list[x][y].locked == False:
                    cell_list[x][y].locked = True
                    locked = True

        # text configuration of locked boxes and emptying unlocked box
        for i in range(9):
            for j in range(9):
                if cell_list[i][j].locked == True:
                    cell_list[i][j].itemconfigure(
                        cell_list[i][j].text, text=cell_list[i][j].phantom_number, font='Roboto 20 bold')


    def left(self, event):

        ''' To move the focus to the left '''

        if self.state == 'playing':
            for i in range(9):
                for j in range(9):

                    cell_list[self.row][self.col].configure(bg='white')

            if self.col > 0:
                self.col -= 1

            elif self.row == 0 and self.col == 0:
                self.row = 8
                self.col = 8
            else:
                self.row -= 1
                self.col = 8
            cell_list[self.row][self.col].focus_set()
            cell_list[self.row][self.col].configure(bg='grey')


    def right(self, event):

        ''' To move the focus to the right '''

        if self.state == 'playing':
            for i in range(9):
                for j in range(9):
                    cell_list[i][j].configure(bg='white')
            if self.col < 8:
                self.col += 1

            elif self.row == 8 and self.col == 8:
                self.row = 0
                self.col = 0
            else:
                self.row += 1
                self.col = 0
            cell_list[self.row][self.col].focus_set()
            cell_list[self.row][self.col].configure(bg='grey')


    def up(self, event):

        ''' To move the focus up '''

        if self.state == 'playing':
            for i in range(9):
                for j in range(9):
                    cell_list[i][j].configure(bg='white')

            if self.row > 0:
                self.row -= 1

            elif self.row == 0 and self.col == 0:
                self.row = 8
                self.col = 8
            else:
                self.row = 8
                self.col -= 1
            cell_list[self.row][self.col].focus_set()
            cell_list[self.row][self.col].configure(bg='grey')


    def down(self, event):

        ''' To move the focus down '''

        if self.state == 'playing':
            for i in range(9):
                for j in range(9):
                    cell_list[i][j].configure(bg='white')
            if self.row < 8:
                self.row += 1

            elif self.row == 8 and self.col == 8:
                self.row = 0
                self.col = 0
            else:
                self.row = 0
                self.col += 1
            cell_list[self.row][self.col].focus_set()
            cell_list[self.row][self.col].configure(bg='grey')


    def insert_number(self, event):

        ''' Inserting the pressed number to the focused box '''

        if self.state == 'playing' and cell_list[self.row][self.col].locked == False:
            if event.keycode in [49, 50, 51, 52, 53, 54, 55, 56, 57]:
                cell_list[self.row][self.col].itemconfigure(
                    cell_list[self.row][self.col].text, text=key_code[event.keycode]
                )
            self.check()


    def check(self):

        ''' Looping all the entry to check if there are same number in the same row, column and group '''

        hit = False
        for i in range(9):
            for j in range(9):
                cell_list[i][j].itemconfigure(cell_list[i][j].text, fill='black')
                target = cell_list[i][j].itemcget(cell_list[i][j].text, 'text')
                for k in range(9):
                    # Checking the column
                    if target != '' and k != cell_list[i][j].col:
                        if target == cell_list[i][k].itemcget(1, 'text'):
                            cell_list[i][j].itemconfigure(cell_list[i][j].text, fill='red')
                            hit = True

                    # Checking the row
                    if target != '' and k != cell_list[i][j].row:
                        if target == cell_list[k][j].itemcget(1, 'text'):
                            cell_list[i][j].itemconfigure(cell_list[i][j].text, fill='red')
                            hit = True

                # checking the group
                for l in sub_regions[cell_list[i][j].sub_region]:
                    if cell_list[i][j] != l and target != '':
                        if target == l.itemcget(l.text, 'text'):
                            cell_list[i][j].itemconfigure(cell_list[i][j].text, fill='red')
                            hit = True

        cell_list[self.row][self.col].focus_set()
        return hit


if __name__ == '__main__':
    app = App()
    app.mainloop()
