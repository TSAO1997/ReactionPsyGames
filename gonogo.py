##########################################################
# 作者: 蔡昌廷
##########################################################
import numpy as np
import cv2
import tkinter as tk
import time
import csv
from tkinter import ttk
from PIL import ImageTk, Image

class go_nogo_Game(object):
    def __init__(self, window):
        self.window = window
        self.canvas = tk.Canvas(window, bg='lightgreen', height=600, width=800)
        self.start_time = 0
        self.end_time = 0
        self.zone_size = 150
        self.zone_x = 400
        self.zone_y = 300
        self.strike = 1
        self.ball = 0
        self.error = 0
        self.fp = 0
        self.fn = 0
        self.press = False
        self.btn = None
        self.run_step = 1
        self.curr_step = 1
        self.record_time = []
        self.respond_time = []
        self.table = None
        self.refresh = None

    '''def menu_picture(self):
        self.btn = tk.Button(self.window, text="start", width=20, height=5)
        self.btn.place(x=330, y=230)
        self.btn.config(command=self.tutorial)'''

    def tutorial(self):
        #self.btn.destroy()
        self.canvas.create_text(400, 120, font=("Times New Roman", 28), text='判斷好壞球')
        self.canvas.create_text(400, 200, font=("Times New Roman", 20), text='以下會有一百顆球，若為好球請按空白鍵')
        self.canvas.create_text(400, 250, font=("Times New Roman", 20), text='一百顆球後，將會顯示所有球的反應時間')
        self.canvas.create_text(400, 300, font=("Times New Roman", 20), text='請加油！')
        self.canvas.pack()
        self.btn = tk.Button(self.window, text="開始遊戲", width=15, height=4)
        self.btn.place(x=330, y=400)
        self.btn.config(command=self.main)

    def create_zone(self):
        # zone position : [x:250-550 , y:150-450]
        self.btn.destroy()
        self.canvas.delete("all")
        self.canvas.configure(bg='lightgreen')
        self.canvas.create_rectangle(400-self.zone_size, 300-self.zone_size, 400+self.zone_size, 300+self.zone_size, tags='zone')
        '''
        self.canvas.create_line(250, 250, 550, 250, fill="black", tags='zone')
        self.canvas.create_line(250, 350, 550, 350, fill="black", tags='zone')
        self.canvas.create_line(350, 150, 350, 450, fill="black", tags='zone')
        self.canvas.create_line(450, 150, 450, 450, fill="black", tags='zone')
        '''
        self.canvas.pack()

    def create_circle(self):
        # zone position : [x:250-550 , y:150-450]
        self.press = False
        oval_x = np.random.rand(1)[0] * 400 + 200 # 200 - 600
        oval_y = np.random.rand(1)[0] * 400 + 100 # 100 - 500
        oval_size = 10
        ball_pos = (abs(oval_x - (self.zone_x - self.zone_size)) < 10) or (abs(oval_x - (self.zone_x + self.zone_size)) < 10) or \
            (abs(oval_y - (self.zone_y - self.zone_size)) < 10) or (abs(oval_y - (self.zone_y - self.zone_size)) < 10)
        while ball_pos:
            oval_x = np.random.rand(1)[0] * 400 + 200 # 200 - 600
            oval_y = np.random.rand(1)[0] * 400 + 100 # 100 - 500
            ball_pos = (abs(oval_x - (self.zone_x - self.zone_size)) < 10) or (abs(oval_x - (self.zone_x + self.zone_size)) < 10) or \
                (abs(oval_y - (self.zone_y - self.zone_size)) < 10) or (abs(oval_y - (self.zone_y - self.zone_size)) < 10)
        self.canvas.create_oval(oval_x - oval_size, oval_y - oval_size, oval_x + oval_size, oval_y + oval_size, fill='red', outline = "red", tags='circle') 
        ball_status = self.detect_circle(oval_x, oval_y)
        self.canvas.update()
        self.start_time = time.time()
        self.window.bind("<space>", lambda event:self.press_space(ball_status))
        self.window.after(2000, lambda: self.delete_circle(ball_status))

    def delete_circle(self, ball_status):
        self.canvas.delete('circle')
        self.canvas.update()
        if self.press == False:
            self.end_time = time.time()
            self.record_time.append(self.end_time - self.start_time)
            if ball_status == self.strike:
                self.fn += 1
        if self.curr_step < self.run_step:
            self.curr_step += 1
            self.create_circle()
        else:
            self.show_result()

    def press_space(self, ball_status):
        if self.press == False:
            self.end_time = time.time()
            self.record_time.append(self.end_time - self.start_time)
            self.press = True
            if ball_status == self.ball:
                self.fp += 1
        self.canvas.delete('circle')
        self.canvas.update()
        if ball_status == self.strike:
            self.respond_time.append(self.end_time - self.start_time)

    def detect_circle(self, x, y):
        if x > self.zone_x - self.zone_size and x < self.zone_x + self.zone_size:
            if y > self.zone_y - self.zone_size and y < self.zone_y + self.zone_size:
                return self.strike
            else:
                return self.ball
        else:
            return self.ball

    def show_result(self):
        self.canvas.delete('zone')
        # Respond time
        if len(self.respond_time) > 0:
            response_time_text = '反應時間 : ' + str(round(sum(self.respond_time)/len(self.respond_time), 3)) + ' 秒'
            respond_time = self.canvas.create_text(400, 100, font=("Purisa", 24), text=response_time_text)
        else:
            respond_time = self.canvas.create_text(400, 100, font=("Purisa", 24), text='反應時間 : 0 秒')      
        
        # Respond table
        style = ttk.Style(self.window)
        style.theme_use("clam")
        style.configure("Treeview", background="black", 
                        fieldbackground="lightgreen", foreground="white")
        item = ['編號', '反應時間(秒)']
        self.table = ttk.Treeview(self.window, columns=item, show="headings")
        for i in item:
            self.table.column(i, anchor='center')
            self.table.heading(i, text=i)
        for i in range(len(self.record_time)):
            if (i+1) % 2 == 1:
                self.table.insert('', 'end', values=[str(i+1), str(round(self.record_time[i], 3))], tags=('odd'))
            else:
                self.table.insert('', 'end', values=[str(i+1), str(round(self.record_time[i], 3))], tags=('even'))
        self.table.place(x=200, y=150)

        # Accuracy
        self.canvas.create_text(400, 500, font=("Purisa", 24), text='準確率: {} %'.format(100 * (self.run_step - (self.fp + self.fn)) / self.run_step))
        self.canvas.create_text(400, 550, font=("Purisa", 12), text='按下Esc鍵繼續...')
        self.window.bind("<Escape>", lambda event:self.refresh())

        # save the result
        self.btn = tk.Button(self.window, text="儲存結果", width=10, height=3)
        self.btn.place(x=350, y=400)
        self.btn.config(command=self.save_result)
    
    def save_result(self):
        f = open('好球判斷成績.txt', 'w')
        f.write('編號  反應時間(秒)\n')
        for i in range(len(self.record_time)):
            result = '{}    {}\n'.format(i+1, round(self.record_time[i], 3))
            f.write(result)
            if i == len(self.record_time) - 1:
                f.write('\n')     
        if len(self.respond_time) == 0:
            f.write('整體反應時間 : 0 秒\n')
        else:
            f.write('整體平均反應時間 : {} 秒\n'.format(round(sum(self.respond_time)/len(self.respond_time), 3)))
        f.write('整體錯誤次數 : {} 次\n'.format(self.fn + self.fp))
        f.write('好球沒按到次數 : {} 次\n'.format(self.fn))
        f.write('壞球按錯次數 : {} 次\n'.format(self.fp))

    def main(self):
        self.create_zone()
        self.canvas.update() 
        self.canvas.after(1000)
        self.create_circle()
        
if __name__ == '__main__':
    window=tk.Tk()
    window.title('Go nogo')
    window.geometry('800x600')
    window.configure(background='white')
    canvas = tk.Canvas(window, bg='white', height=600, width=800)
    run_step = 100
    game = go_nogo_Game(window, canvas)
    game.menu_picture()
    window.mainloop()