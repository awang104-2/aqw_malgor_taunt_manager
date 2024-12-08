from tkinter import *
from ImageHandler import *
import os


plans = {
    'AP': [3, 11, 12],
    'LR': [0, 6, 7, 16],
    'SC': [2, 4, 13],
    'LoO': [1, 9, 15, 18]
}

class_name = 'AP'
hwnd = get_aqw_hwnd()
order = ['truth', 'listen', 'red', 'truth', 'listen', 'truth', 'red', 'listen', 'truth', 'truth', 'listen',
         'red', 'truth', 'listen', 'truth', 'red', 'listen', 'truth', 'truth', 'listen']
step = 0
running = False
taunts = {'truth': 0, 'listen': 0, 'red': 0}
condition_paths = {
    'truth': os.path.abspath('taunts/truth.png'),
    'listen': os.path.abspath('taunts/listen.png'),
    'red': os.path.abspath('taunts/red.png')
}

root = Tk()
root.title('Malgor Taunt Manager')
root.geometry('300x100+20+20')
root.attributes('-topmost', True)
for i in range(6):
    root.columnconfigure(i, weight=1)

def is_in_list(element, _list):
    for a in _list:
        if a == element:
            return True
    return False

def check_taunt():
    global step
    if not running:
        return
    condition = order[step]
    img1 = get_screenshot_of_window(hwnd)
    img2 = load_image(condition_paths[condition])
    if is_image_on_screen(img1, img2, confidence=0.7):
        if condition == 'red':
            if is_in_list(step, plans[class_name]):
                lbl.config(text='Stay in', foreground='red')
                lbl.after(2900, check_taunt)
            else:
                lbl.config(text='Stay out', foreground='red')
                lbl.after(2900, check_taunt)
        else:
            if is_in_list(step, plans[class_name]):
                lbl.config(text='Taunt now', foreground='red')
                lbl.after(1900, check_taunt)
            else:
                lbl.config(text='Idle', foreground='black')
                lbl.after(1900, check_taunt)
        step += 1
    else:
        lbl.config(text='Idle', foreground='black')
        lbl.after(100, check_taunt)

def start(name):
    global running, class_name
    running = True
    class_name = name
    forget_all()
    lbl.grid(row=0, column=1, columnspan=4, sticky='nsew')
    Button(command=stop, text='Stop').grid(row=1, column=2, columnspan=2, sticky='nsew')
    check_taunt()

def stop():
    global running, step
    running = False
    step = 0
    forget_all()
    for a in range(4):
        buttons[a].grid(row=1, column=a+1, sticky='nsew')
    lbl.config(text='Choose:')
    lbl.grid(row=0, column=0, columnspan=6, sticky='nsew')

def forget_all():
    widget_list = root.winfo_children()
    for item in widget_list:
        if item.winfo_children():
            widget_list.extend(item.winfo_children())
    for item in widget_list:
        item.grid_forget()

lbl = Label(root, font=('calibri', 40, 'bold'))
lbl.config(text='Choose:')
lbl.grid(row=0, column=0, columnspan=6)
buttons = []
for i in range(4):
    classes = ['AP', 'SC', 'LoO', 'LR']
    class_name = classes[i]
    button = Button(command=lambda: start(class_name), text=class_name)
    button.grid(row=1, column=i+1, sticky="nsew")
    buttons.append(button)
mainloop()
