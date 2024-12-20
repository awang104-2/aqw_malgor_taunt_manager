import tkinter as tk

event_ids = None

def say_hello():
    print("Hello, world!")

root = tk.Tk()
label = tk.Label(root, text="Example Label")
label.pack()

# Schedule an event and store the event ID
def action():
    event_id = label.after(2000, say_hello)
    event_ids.append(event_id)
    print(f"Scheduled event ID: {event_id}")

def cancel():
    global event_ids
    # Cancel the event
    for event_id in event_ids:
        label.after_cancel(event_id)
    print("Event canceled before execution.")


root.mainloop()