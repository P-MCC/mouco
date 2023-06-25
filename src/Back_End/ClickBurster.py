import multiprocessing
import sys
import time
import keyboard
from pynput.mouse import Button, Controller

def burst(sleepTime):
    mouse = Controller()
    
    #TODO add a start stop func0.tionality to ` button (it only starts (when ` is pressed) and terminates (when esc is pressed) the program)
    
    recorded = keyboard.record(until="`")
    print(recorded)
    print(type(recorded))
    if (recorded != None):
        #Clicks the mouse and the sleeps for the specified time
        while(True):
            mouse.press(Button.left)
            mouse.release(Button.left)
            time.sleep(sleepTime)
            


def keyChecker(q):
    recorded = keyboard.record(until="esc")
    print(recorded)
    if (recorded != None):
        print("Esc pressed")
        print("KILL JIGGLE!!!")
        q.put("KILL JIGGLE")
    
    
def main():
    q = multiprocessing.Queue()
    sleepTime = float(input("Enter the click period in seconds (ex. 0.2):"))
    
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
        
        if msg == "KILL JIGGLE":            
            print("Terminating...")
            
            ProcessJiggle.terminate()
            time.sleep(0.1)
            
            if not ProcessJiggle.is_alive():               
                ProcessJiggle.join(timeout=1.0)               
                print("Burst successfully")
                print("Burst process terminated!")                                                 
                q.close()
                break  
    
    print("End of Click Burst :(")
    sys.exit()


if __name__ == "__main__":
    main()

