import csv
import time
import keyboard
import pyautogui
import sys
import multiprocessing

def execute_mouse_events_from_csv(file_path, q):

    print("Press ` to start the macro")

    keyboard.wait("`")

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            event_type = row['event_type']
            if event_type == 'Click':
                x = int(row['x'])
                y = int(row['y'])
                click_type = row['click_type']
                delay = 0.2  
                time.sleep(delay)
                pyautogui.moveTo(x, y)
                if click_type == 'Left':
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                elif click_type == 'Right':
                    pyautogui.mouseDown(button='right')
                    pyautogui.mouseUp(button='right')

            elif event_type == 'Scroll':
                x = int(row['x'])
                y = int(row['y'])
                pyautogui.moveTo(x, y)
                scroll_amount = int(row['scroll_amount'])
                delay = 0.01  
                time.sleep(delay)
                pyautogui.scroll(scroll_amount, x=x, y=y)
               

        q.put("KILL EXECUTE")


def keyChecker(q):
    recorded = keyboard.record(until="esc")
    print(recorded)
    if (recorded != None):
        print("Esc pressed")
        print("KILL EXECUTE!!!")
        q.put("KILL EXECUTE")


def main(slider_value):
    
    csv_file_path = 'Saved_Macros/' + slider_value
    
    q = multiprocessing.Queue()
    
    inputFile = str(csv_file_path)

    print("To end the program press esc")
    print("Starting the execution from the file  {}".format(inputFile))

    ProcessJiggle = multiprocessing.Process(
        target=execute_mouse_events_from_csv, args=(inputFile, q,))
    ProcessKeyChecker = multiprocessing.Process(target=keyChecker, args=(q,))

    ProcessKeyChecker.daemon = True

    ProcessJiggle.start()
    ProcessKeyChecker.start()

    while True:
        msg = q.get()

        if msg == "KILL EXECUTE":
            print("Terminating...")

            ProcessJiggle.terminate()
            time.sleep(0.1)

            if not ProcessJiggle.is_alive():
                ProcessJiggle.join(timeout=1.0)
                print("Joined successfully")
                print("Execution process terminated!")
                q.close()
                break

    print("End of Macro Execution :(")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        slider_value = sys.argv[1]
        main(slider_value)
    else:
        print("No slider value provided.")