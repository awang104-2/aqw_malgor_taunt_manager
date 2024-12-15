from tkinter import *
from ImageHandler import *
import os


plans = {
    'AP': [3, 11, 12],
    'LR': [0, 6, 7, 16],
    'SC': [2, 4, 13],
    'LoO': [1, 9, 15, 18]
}

class_name = None
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
root.geometry('290x120+5+5')
root.resizable(False, False)
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
    condition = 'red'
    img1 = get_screenshot_of_window(hwnd, (0, 0, 1600, 300))
    img2 = load_image(condition_paths[condition])
    if is_image_on_screen(img1, img2, confidence=0.7):
        taunts['red'] += 1
        zone = (taunts['red'] - 1) % 4 + 1
        if zone == 4:
            message = 'Red: ' + str(zone) + (' (You)')
        else:
            message = 'Red: ' + str(zone)
        lbl.config(text=message)
        lbl.after(4000, check_taunt)
    else:
        lbl.after(5, check_taunt)

def start(name):
    global running, class_name
    running = True
    class_name = name
    forget_all()
    lbl.grid(row=0, column=1, columnspan=4, sticky='nsew')
    Button(command=stop, text='Stop').grid(row=1, column=2, columnspan=2, sticky='nsew')
    lbl.config(text='N/A')
    taunts['red'] = 0
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
    button = Button(command=lambda name=classes[i]: start(name), text=classes[i])
    button.grid(row=1, column=i+1, sticky="nsew")
    buttons.append(button)
mainloop()
