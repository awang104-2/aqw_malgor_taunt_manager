from tkinter import *
from ImageHandler import *
import os
from time import sleep

classes = ['SC', 'LR', 'AP', 'LoO']


class Manager:

    condition_paths = {
        'truth': os.path.abspath('taunts/truth.png'),
        'listen': os.path.abspath('taunts/listen.png'),
        'red': os.path.abspath('taunts/red.png')
    }

    def __init__(self, name, hwnd):
        self.name = name
        self.taunts = {'truth': 0, 'listen': 0, 'red': 0}
        self.hwnd = hwnd

    def __call__(self):
        is_red = self.check_screen()
        if is_red:
            self.taunts['red'] += 1
            zone = (self.taunts['red'] - 1) % 4 + 1
            string = 'Red: ' + str(zone) + ' (' + classes[zone - 1] + ')'
            your_taunt = classes[zone - 1] == self.name
            print(classes[zone - 1], self.name)
        else:
            string = ''
            your_taunt = False

        return string, is_red, your_taunt

    def check_screen(self):
        img1 = get_screenshot_of_window(self.hwnd, (0, 0, 1600, 300))
        img2 = load_image(Manager.condition_paths['red'])
        return is_image_on_screen(img1, img2, confidence=0.7)


class ZoneManager:

    def __init__(self, name):

        def initialize_fields():
            self.scheduled_events = []
            self.current_events = {'taunt': None, 'color': None}
            self.manager = Manager(name=name, hwnd=get_aqw_hwnd())

        def initialize_window():
            self.root.title('Overlay')
            self.root.attributes('-fullscreen', True)
            self.root.resizable(False, False)
            self.root.attributes('-topmost', True)
            self.root.config(bg='white')
            self.root.attributes("-transparentcolor", "white")

        def initialize_widgets(swidth, sheight):
            w_factor = swidth / 1920
            h_factor = sheight / 1080
            label_width, label_height = (400, 80)
            label_x, label_y = (1920 / 2 - label_width / 2, 1080 * 0.2 - label_height / 2)
            button_width, button_height = (180, 80)
            button_x, button_y = (1920 - (button_width + 10), 1080 - (button_height + 10))

            self.label = Label(text='N/A', foreground='black', background='yellow', font=('Impact', 40, 'bold'))
            self.reset_button = Button(text='Reset', command=self.reset, font=('calibri', 20, 'bold'), borderwidth=5)
            self.label.place(x=int(label_x * w_factor), y=int(label_y * h_factor), width=int(label_width * w_factor), height=int(label_height * h_factor))
            self.reset_button.place(x=int(button_x * w_factor), y=int(button_y * h_factor), width=int(button_width * w_factor), height=int(button_height * h_factor))

        self.root = Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        initialize_fields()
        initialize_window()
        initialize_widgets(screen_width, screen_height)

        self.check_taunt()
        self.root.mainloop()

    def check_taunt(self):
        string, is_red, your_zone = self.manager()
        if self.current_events['taunt']:
            self.remove_event(self.current_events['taunt'])
        if is_red:
            self.change_colors(flash=your_zone)
            self.label.config(text=string)
            dt = 4500
        else:
            dt = 50
        self.current_events['taunt'] = self.label.after(dt, self.check_taunt)
        self.scheduled_events.append(self.current_events['taunt'])

    def change_colors(self, num=0, flash=False, event=None):
        if event:
            self.remove_event(event)
        if flash:
            if num == 6:
                self.label.config(foreground='black')
                return
            elif num % 2 == 0:
                self.label.config(foreground='red')
            else:
                self.label.config(foreground='blue')
            dt = 500
        else:
            if num == 1:
                self.label.config(foreground='black')
                return
            else:
                self.label.config(foreground='green')
            dt = 3000
        self.current_events['taunt'] = self.label.after(dt, lambda: self.change_colors(num + 1, flash))
        self.scheduled_events.append(self.current_events['taunt'])

    def remove_event(self, event):
        if event in self.scheduled_events:
            self.scheduled_events.remove(event)

    def reset(self):
        for event_id in self.scheduled_events:
            self.label.after_cancel(event_id)
        self.root.destroy()
        sleep(2)
        Menu()


class Menu:

    def __init__(self):

        def initialize_window(swidth, sheight):
            w_factor = swidth / 1920
            h_factor = sheight / 1080
            width, height = (540, 150)
            x, y = (1920 / 2 - width / 2, 1080 * 0.3 - height / 2)
            geometry = str(int(width * w_factor)) + 'x' + str(int(height * h_factor)) + '+' + str(int(x * w_factor)) + '+' + str(int(y * h_factor))

            self.root.title('Menu')
            self.root.geometry(geometry)
            self.root.attributes('-topmost', True)
            self.root.resizable(False, False)

        def initialize_widgets(swidth, sheight):
            w_factor = swidth / 1920
            h_factor = sheight / 1080
            self.label = Label(self.root, text='Choose: ', font=('calibri', 40, 'bold'))
            self.label.grid(row=0, column=1, columnspan=2)
            self.buttons = {}
            for i in range(len(classes)):
                name = classes[i]
                self.buttons[name] = Button(self.root, text=name, command=lambda x=name: self.initialize_zone_manager(x), font=('calibri', 20, 'bold'))
                self.buttons[name].grid(row=1, column=i, ipadx=int(30*w_factor), padx=int(10*h_factor))

        self.root = Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        initialize_window(screen_width, screen_height)
        initialize_widgets(screen_width, screen_height)
        self.root.mainloop()

    def initialize_zone_manager(self, name):
        self.root.destroy()
        sleep(2)
        ZoneManager(name)


if __name__ == '__main__':
    menu = Menu()






