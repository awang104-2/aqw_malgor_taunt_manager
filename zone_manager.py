from tkinter import *
from ImageHandler import *
import os
import time


class Manager:

    classes = ['SC', 'LR', 'AP', 'LoO']
    condition_paths = {
        'truth': os.path.abspath('taunts/truth.png'),
        'listen': os.path.abspath('taunts/listen.png'),
        'red': os.path.abspath('taunts/red.png')
    }

    def __init__(self, name, hwnd):
        self.name = name
        self.taunts = {'truth': 0, 'listen': 0, 'red': 0}
        self.hwnd = hwnd

    def __call__(self, msg='red'):
        img1 = get_screenshot_of_window(self.hwnd, (0, 0, 1600, 300))
        img2 = load_image(Manager.condition_paths[msg])
        is_red = is_image_on_screen(img1, img2, confidence=0.7)
        if is_red:
            self.taunts[msg] += 1
        if self.taunts[msg] == 0:
            zone = 0
            class_string = ''
            string = 'Red: ' + str(zone) + class_string
            return string, False
        else:
            zone = (self.taunts[msg] - 1) % 4 + 1
            class_string = ' ' + '(' + Manager.classes[zone - 1] + ')'
            string = 'Red: ' + str(zone) + class_string
            return string, Manager.classes[zone - 1] == self.name


class ZoneManager:

    def __init__(self):
        self.root = Tk()
        self.root.title('Malgor Taunt Manager')
        self.root.geometry('290x120+5+5')
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        for i in range(6):
            self.root.columnconfigure(i, weight=1)
        self.running = False
        self.manager = None
        self.lbl = Label(self.root, font=('calibri', 40, 'bold'))
        self.lbl.config(text='Choose:', foreground='black')
        self.lbl.grid(row=0, column=0, columnspan=6)
        self.spawn_buttons()
        mainloop()

    def spawn_buttons(self):
        for i in range(4):
            classes = ['AP', 'SC', 'LoO', 'LR']
            button = Button(command=lambda name=classes[i]: self.start(name), text=classes[i])
            button.grid(row=1, column=i + 1, sticky="nsew")

    def forget_all(self):
        widget_list = self.root.winfo_children()
        for item in widget_list:
            if item.winfo_children():
                widget_list.extend(item.winfo_children())
        for item in widget_list:
            item.grid_forget()

    def start(self, name):
        self.running = True
        self.forget_all()
        self.lbl.grid(row=0, column=1, columnspan=4, sticky='nsew')
        Button(command=self.stop, text='Stop').grid(row=1, column=2, columnspan=2, sticky='nsew')
        self.lbl.config(text='N/A')
        self.manager = Manager(name=name, hwnd=get_aqw_hwnd())
        self.check_taunt()

    def stop(self):
        self.running = False
        self.forget_all()
        self.spawn_buttons()
        self.lbl.config(text='Choose:', foreground='black')
        self.lbl.grid(row=0, column=0, columnspan=6, sticky='nsew')

    def check_taunt(self):
        if not self.running:
            return
        else:
            string, is_red = self.manager('red')
            if is_red:
                foreground = 'red'
                dt = 2000
            else:
                foreground = 'black'
                dt = 50
            self.lbl.config(text=string, foreground=foreground)
            self.lbl.after(dt, self.check_taunt)


if __name__ == '__main__':
    window = ZoneManager()






