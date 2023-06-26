import csv
import time
import pynput.mouse
from pynput.mouse import Button, Controller
import sys

class MouseEventExecutor:
    def __init__(self):
        self.mouse = pynput.mouse.Controller()

    def execute_mouse_events_from_csv(self, file_path):
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
                    self.mouse.position = (x, y)
                    if click_type == 'Left':
                        self.mouse.click(Button.left)
                    elif click_type == 'Right':
                        self.mouse.click(Button.right)
                elif event_type == 'Scroll':
                    scroll_amount = int(row['scroll_amount'])
                    delay = 0.2  # Delay in seconds before executing the scroll event
                    time.sleep(delay)
                    self.mouse.scroll(0, scroll_amount)


def main(slider_value):
    # Create an instance of MouseEventExecutor
    executor = MouseEventExecutor()

    # Specify the path to the CSV file containing the mouse events
    csv_file_path = 'Saved_Macros/'+slider_value#'Saved_Macros/mouse_events.csv'

    # Execute the mouse events from the CSV file
    executor.execute_mouse_events_from_csv(csv_file_path)

if __name__ == "__main__":
    if len(sys.argv) >= 1:
        slider_value = sys.argv[1]
        main(slider_value)
    else:
        print("No slider value provided.")

