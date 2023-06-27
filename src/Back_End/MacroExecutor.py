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
                delay = 0.2  # Delay in seconds before executing the click event
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
                delay = 0.01  # Delay in seconds before executing the scroll event
                time.sleep(delay)
                pyautogui.scroll(scroll_amount, x=x, y=y)
                # self.mouse.scroll(0, scroll_amount)

        q.put("KILL JIGGLE")


def keyChecker(q):
    recorded = keyboard.record(until="esc")
    print(recorded)
    if (recorded != None):
        print("Esc pressed")
        print("KILL JIGGLE!!!")
        q.put("KILL JIGGLE")


def main(slider_value):
    # Create an instance of MouseEventExecutor
    # Specify the path to the CSV file containing the mouse events
    csv_file_path = 'Saved_Macros/' + slider_value
    
    # Execute the mouse events from the CSV file
    q = multiprocessing.Queue()
    # int(input("Enter the jiggle period in seconds:"))
    inputFile = str(csv_file_path)

    print("To end the program press esc")
    print("Starting to jiggle in {} seconds!".format(inputFile))

    ProcessJiggle = multiprocessing.Process(
        target=execute_mouse_events_from_csv, args=(inputFile, q,))
    ProcessKeyChecker = multiprocessing.Process(target=keyChecker, args=(q,))

    ProcessKeyChecker.daemon = True

    ProcessJiggle.start()
    ProcessKeyChecker.start()

    while True:
        msg = q.get()

        if msg == "KILL JIGGLE":
            print("Terminating...")

            ProcessJiggle.terminate()
            time.sleep(0.1)

            if not ProcessJiggle.is_alive():
                ProcessJiggle.join(timeout=1.0)
                print("Joined successfully")
                print("Jiggle process terminated!")
                q.close()
                break

    print("End of jiggling :(")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        slider_value = sys.argv[1]
        main(slider_value)
    else:
        print("No slider value provided.")