import csv
import multiprocessing
import sys
import time
import pynput.mouse
from pynput.mouse import Button, Controller
import pynput.keyboard
import keyboard
import os


mouse_events = []

def record_mouse_events(csvname, q):
    def on_click(x, y, button, pressed):
        if pressed:
            
            click_type = 'Left' if button == Button.left else 'Right'
            mouse_events.append({'x': x, 'y': y, 'event_type': 'Click', 'click_type': click_type, 'scroll_direction': None, 'scroll_amount': None})
            print(f"Mouse click recorded at position ({x}, {y}) - {click_type}")

    def on_scroll(x, y, dx, dy):
        
        mouse_events.append({'x': x, 'y': y, 'event_type': 'Scroll', 'click_type': None, 'scroll_direction': 'Up' if dy > 0 else 'Down', 'scroll_amount': dy})
        print(f"Scroll event recorded: {'Up' if dy > 0 else 'Down'} - Amount: {dy}")

    
    mouse_listener = pynput.mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    
    print("Press the ` key to start recording")
    
   
    keyboard.wait("`")
    
    mouse_listener.start()

    while True:
        if keyboard.is_pressed("esc"):
           
            print('-----------------------------------')
            write_mouse_events_to_csv(csvname)
            for event in mouse_events:
                print(f"Mouse event recorded: {event}")
            q.put("KILL")
            break

def repeat_mouse_events(q):
    # Repeat the recorded mouse events
    for event in mouse_events:
        if event['event_type'] == 'Click':
            pynput.mouse.Controller().position = (event['x'], event['y'])
            pynput.mouse.Controller().click()
        elif event['event_type'] == 'Scroll':
            pynput.mouse.Controller().scroll(0, event['scroll_amount'])

def write_mouse_events_to_csv(csvname):
    
    name = csvname + ".csv"
    events_to_write = list(mouse_events)

    
    file_path = os.path.join("Saved_Macros", name)
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['x', 'y', 'event_type', 'click_type', 'scroll_direction', 'scroll_amount'])
        writer.writeheader()
        writer.writerows(events_to_write)


def main(csvname):
    q = multiprocessing.Queue()

    
    process_record_mouse_events = multiprocessing.Process(target=record_mouse_events, args=(csvname,q,))
    process_repeat_mouse_events = multiprocessing.Process(target=repeat_mouse_events, args=(q,))

    process_record_mouse_events.start()
    process_repeat_mouse_events.start()


    msg = q.get()
    if msg == "KILL":
        
        process_record_mouse_events.terminate()
        process_repeat_mouse_events.terminate()

        

    print("End of program")
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) >= 1:
        slider_value = sys.argv[1]
        main(slider_value)
    else:
        print("No slider value provided.")
