import time, threading

x = None

def main_prog():
    global x
    while x is None:
        print("Main prog is running")
        time.sleep(2)

def user_input_thread():
    while True:
        x = input("Press enter to continue...")
        print(f"User input finished {x}")

def main():
    print("Main fcn")
    
    program_thread = threading.Thread(target=main_prog)
    inp_thread = threading.Thread(target=user_input_thread)

    program_thread.start()
    inp_thread.start()

    program_thread.join()
    inp_thread.join()

main()
