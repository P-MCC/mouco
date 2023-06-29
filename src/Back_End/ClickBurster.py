import multiprocessing
import sys
import time
import keyboard
from pynput.mouse import Button, Controller

def burst(sleepTime):
    mouse = Controller()
    
    # #TODO add a start stop func0.tionality to ` button (it only starts (when ` is pressed) and terminates (when esc is pressed) the program)
    
    recorded = keyboard.record(until="`")
    print(recorded)
    print(type(recorded))
    if (recorded != None):
        while(True):
            mouse.press(Button.left)
            mouse.release(Button.left)
            time.sleep(sleepTime)  
    

def keyChecker(q):
    recorded = keyboard.record(until="esc")
    print(recorded)
    if (recorded != None):
        print("Esc pressed")
        print("KILL BURST!!!")
        q.put("KILL BURST")
    
    
    
    
def main(slider_value):
    q = multiprocessing.Queue()
    sleepTime = float(slider_value)
    
    print("To end the program press esc")
    print("To start the program press `")
    print("Starting to jiggle in {} seconds!".format(sleepTime))
    
    ProcessJiggle = multiprocessing.Process(target=burst, args=(sleepTime,))
    ProcessKeyChecker = multiprocessing.Process(target=keyChecker, args=(q,))
    
    ProcessKeyChecker.daemon = True
    
    ProcessJiggle.start()
    ProcessKeyChecker.start()
    
    while True:
        msg = q.get()
        
        if msg == "KILL BURST":            
            print("Terminating...")
            
            ProcessJiggle.terminate()
            time.sleep(0.1)
            
            if not ProcessJiggle.is_alive():               
                ProcessJiggle.join(timeout=1.0)               
                print("Burst process successfully terminated!")                                              
                q.close()
                break  
    
    print("End of Click Burst :(")
    sys.exit()


if __name__ == "__main__":
    if len(sys.argv) >= 1:
        slider_value = sys.argv[1]
        main(slider_value)
    else:
        print("No slider value provided.")

