import tkinter as tk
import tkinter.font as font
import random 
import time

TRIAL_TIMES = 20

class stroop():
    def __init__(self, window):
        self.word_list = ['紅', '黃', '綠', '藍']
        self.color_list = ['red', 'yellow', 'green', 'blue']
        self.correct_ans = ''
        self.trial = 0
        self.spawn_time = 0.0
        self.congruent_time_list = []
        self.fontsize = font.Font(size=24)
        self.incongruent_time_list = []
        self.window = window
        self.canvas = tk.Canvas(window, bg='white', height=600, width=800)
        self.is_congruent = None
        self.btn = None
        self.refresh = None
        
        '''self.window = tk.Tk()
        self.window.title('stroop')
        self.window.geometry('500x500') '''

    def menu_picture(self):
        self.btn = tk.Button(self.window, text="start", width=20, height=5)
        self.btn.place(x=330, y=230)
        self.btn.config(command=self.tutorial)

    def tutorial(self):
        self.btn.destroy()
        self.canvas.create_text(400, 120, font=("Times New Roman", 28), text='判斷文字顏色')
        self.canvas.create_text(400, 200, font=("Times New Roman", 20), text='開始後請依照上方出現的文字顏色作答')
        self.canvas.create_text(400, 250, font=("Times New Roman", 20), text='作答時按鍵盤上對應答案的數字')
        self.canvas.create_text(400, 300, font=("Times New Roman", 20), text='紅  黃  綠  藍')
        self.canvas.create_text(400, 350, font=("Times New Roman", 20), text='1   2   3   4')
        self.canvas.create_text(400, 400, font=("Times New Roman", 20), text='準備好就可以開始！')
        self.canvas.pack()
        self.btn = tk.Button(self.window, text="開始遊戲", width=15, height=4)
        self.btn.place(x=330, y=450)
        self.btn.config(command=self.run)

    def red_trigger(self):
        if self.correct_ans == 'red':
            self.result_label.configure(text='正確!', font=self.fontsize)
            if self.is_congruent == True:
                self.congruent_time_list.append(time.time()-self.spawn_time)
            else:
                self.incongruent_time_list.append(time.time()-self.spawn_time)
        else:
            self.result_label.configure(text='錯誤!', font=self.fontsize)

        self.check_trial()
        self.new_question()

    def yellow_trigger(self):
        if self.correct_ans == 'yellow':
            self.result_label.configure(text='正確!', font=self.fontsize)
            if self.is_congruent == True:
                self.congruent_time_list.append(time.time()-self.spawn_time)
            else:
                self.incongruent_time_list.append(time.time()-self.spawn_time)
        else:
            self.result_label.configure(text='錯誤!', font=self.fontsize)

        self.check_trial()
        self.new_question()
        
    def green_trigger(self):
        if self.correct_ans == 'green':
            self.result_label.configure(text='正確!', font=self.fontsize)
            if self.is_congruent == True:
                self.congruent_time_list.append(time.time()-self.spawn_time)
            else:
                self.incongruent_time_list.append(time.time()-self.spawn_time)
        else:
            self.result_label.configure(text='錯誤!', font=self.fontsize)

        self.check_trial()
        self.new_question()
        
    def blue_trigger(self):
        if self.correct_ans == 'blue':
            self.result_label.configure(text='正確!', font=self.fontsize)
            if self.is_congruent == True:
                self.congruent_time_list.append(time.time()-self.spawn_time)
            else:
                self.incongruent_time_list.append(time.time()-self.spawn_time)
        else:
            self.result_label.configure(text='錯誤!', font=self.fontsize)
            
        self.check_trial()
        self.new_question()
    
    def key_press(self, event):
        if event.char == '1':
            self.red_trigger()
        elif event.char == '2':
            self.yellow_trigger()
        elif event.char == '3':
            self.green_trigger()
        elif event.char == '4':
            self.blue_trigger()
            
    def new_question(self):
        c = random.randint(0, 3)
        w = random.randint(0, 3)
        if c==w:
            self.is_congruent = True
        else:
            self.is_congruent = False
        self.correct_ans = self.color_list[c]
        self.description_label.configure(text=self.word_list[w], font=font.Font(size=36),fg=self.correct_ans, bg='black')
        self.spawn_time = time.time()
        self.trial += 1
        
    def check_trial(self):
        if self.trial == TRIAL_TIMES:
            self.instruction_label.destroy()
            self.description_label.destroy()
            self.result_label.destroy()
            self.label_frame.destroy()
            self.ans_frame.destroy()
            self.key_frame.destroy()
            self.canvas = tk.Canvas(self.window, bg='white', height=600, width=800)
            if len(self.congruent_time_list) != 0:
                congruent_avg = sum(self.congruent_time_list)/len(self.congruent_time_list)
            else:
                congruent_avg = 0.0
            
            if len(self.incongruent_time_list) != 0:
                incongruent_avg = sum(self.incongruent_time_list)/len(self.incongruent_time_list)
            else:
                incongruent_avg = 0.0    

            #print('Congruent: {:.3f}'.format(congruent_avg))
            #print('Incongruent: {:.3f}'.format(incongruent_avg))
            
            self.canvas.create_text(400, 200, font=("Times New Roman", 24), text='在有答對的情況下')
            self.canvas.create_text(400, 250, font=("Times New Roman", 24), text='文字跟顏色一致時你的判斷時間 : {:.3f}'.format(congruent_avg))
            self.canvas.create_text(400, 300, font=("Times New Roman", 24), text='文字跟顏色不一致時你的判斷時間 : {:.3f}'.format(incongruent_avg))
            self.canvas.create_text(400, 350, font=("Times New Roman", 24), text='史楚普效應為後者時間減去前者時間 : {:.3f}'.format(incongruent_avg-congruent_avg))
            self.canvas.create_text(400, 500, font=("Times New Roman", 24), text='按下Esc鍵繼續...')
            self.canvas.pack()
            self.window.bind("<Escape>", lambda event:self.refresh())
            #exit(0)
        
    def run(self):
        self.btn.destroy()
        self.canvas.destroy()

        self.instruction_label = tk.Label(self.window, font=self.fontsize, text='看到下面的有色字 選擇與顏色對應的答案')
        self.instruction_label.pack()
        
        self.btn.destroy()
        self.description_label = tk.Label(self.window, width=6, height=3)
        self.description_label.pack()

        self.result_label = tk.Label(self.window)
        self.result_label.pack()
        

        self.ans_frame = tk.Frame(self.window)
        self.ans_frame.pack(side=tk.TOP)
        
        self.red_label = tk.Label(self.ans_frame, text='紅', font=self.fontsize, width=6, height=2)
        self.red_label.pack(side = tk.LEFT,fill="x", expand=True)

        self.yellow_label = tk.Label(self.ans_frame, text='黃', font=self.fontsize, width=6, height=2)
        self.yellow_label.pack(side = tk.LEFT,fill="x", expand=True)

        self.green_label = tk.Label(self.ans_frame, text='綠', font=self.fontsize, width=6, height=2)
        self.green_label.pack(side = tk.LEFT,fill="x", expand=True)

        self.blue_label = tk.Label(self.ans_frame, text='藍', font=self.fontsize, width=6, height=2)
        self.blue_label.pack(side = tk.LEFT,fill="x", expand=True)
        
        self.label_frame = tk.Frame(self.window)
        self.label_frame.pack(side=tk.TOP)
        
        self.label1 = tk.Label(self.label_frame, text='1', font=self.fontsize, width=6, height=2)
        self.label1.pack(side = tk.LEFT, fill="x", expand=True)

        self.label2 = tk.Label(self.label_frame, text='2', font=self.fontsize, width=6, height=2)
        self.label2.pack(side = tk.LEFT, fill="x", expand=True)

        self.label3 = tk.Label(self.label_frame, text='3', font=self.fontsize, width=6, height=2)
        self.label3.pack(side = tk.LEFT,fill="x", expand=True)

        self.label4 = tk.Label(self.label_frame, text='4', font=self.fontsize, width=6, height=2)
        self.label4.pack(side = tk.LEFT,fill="x", expand=True)
        
        self.key_frame = tk.Frame(self.window)
        self.key_frame.bind("<KeyPress>", self.key_press)
        self.key_frame.pack()
        self.key_frame.focus_set()
        
        self.new_question()

if __name__ == '__main__':
    window = tk.Tk()
    window.geometry('800x600')
    stroop_test = stroop(window)
    stroop_test.menu_picture()
    window.mainloop()