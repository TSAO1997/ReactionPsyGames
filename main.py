from gonogo import go_nogo_Game
from stroop import stroop
import tkinter as tk

class Manager():
    def __init__(self, window, gonogo, stroop):
        self.window = window
        self.gonogo = gonogo
        self.stroop = stroop
        self.btn1 = None
        self.btn2 = None

    def menu_page(self):
        self.btn1 = tk.Button(self.window, text="判斷好球遊戲", width=30, height=10)
        self.btn1.config(command=self.run_gonogo)
        self.btn1.pack()
        self.btn2 = tk.Button(self.window, text="判斷顏色遊戲", width=30, height=10)
        self.btn2.config(command=self.run_stroop)
        self.btn2.pack()

    def destroy_all_button(self):
        self.btn1.destroy()
        self.btn2.destroy()
    
    def run_gonogo(self):
        self.destroy_all_button()
        self.gonogo.refresh = self.gonogo_refresh
        self.gonogo.menu_picture()

    def run_stroop(self):
        self.destroy_all_button()
        self.stroop.refresh = self.stroop_refresh
        self.stroop.menu_picture()
    
    def gonogo_refresh(self):
        self.gonogo.table.destroy()
        self.gonogo.canvas.destroy()
        self.window.unbind("<Escape>")
        self.gonogo.__init__(self.window)
        self.__init__(self.window,self.gonogo,self.stroop)
        self.menu_page()
    
    def stroop_refresh(self):
        self.stroop.canvas.destroy()
        self.window.unbind("<Escape>")
        self.stroop.__init__(self.window)
        self.__init__(self.window,self.gonogo,self.stroop)
        self.menu_page()

if __name__=='__main__':
    window=tk.Tk()
    window.title('反應測試小遊戲')
    window.geometry('800x600')
    window.configure(background='white')
    window.resizable(0,0)
    gonogo = go_nogo_Game(window)
    stroop = stroop(window)
    manager = Manager(window, gonogo, stroop)
    manager.menu_page()
    window.mainloop()