"""
    Main developer file. This will not be edited in the final product. 
    Here all system functionalities are executed.
"""

import sys_fcns as fcn
from drivers import button as btn
import tech as tech
import threading

#to chage policy level, not used in final version
version = 8
max_policy_num = 9 # + 1 when adding a new policy
x = None

#initalise peripherals
for sensor in tech.sens_array:
    sensor.sensor_setup()

for actuator in tech.act_array:
    actuator.actuator_setup()

print(f"\n--------------START---------------\nStarting with Policy version {version}")

def program():
    global version
    while True:
        toContext = ""

#       change policy version on button press, and simulate user input
        if btn.btn_is_pressed(2):
            version += 1
            print("\nPolicy level " + str(version % max_policy_num) +" is being used. \n\nEnter new rule: ", end="")
        fcn.change_policy_version(version, max_policy_num)


#       if changes are made to the technician file, 
#       pressing this button will re-initalise the devices without turning it off
        if btn.btn_is_pressed(27):
            fcn.sys_restart(tech.sens_array, tech.act_array, module = tech)

#       copy files from DRIVER_USB       
        fcn.copy_from_USB()
    
#       use the sensor, retrieve data, enter it in the literal
        for sensor in tech.sens_array:
            sensor.sensor_action()
            sensor.data_in_literal()
            if sensor.is_literal_numeric == True or sensor.data == True:
                toContext += sensor.literal_p
            elif sensor.data == False:
                toContext += sensor.literal_n
            else:
                print("Error call dev")
                    
#       start a subprocess to interface with Prudens
        print(toContext)
        conclusions = fcn.subproc(toContext)
                
#       check for which conclusion corresponds to an actuator
        for actuator in tech.act_array:
            if actuator.literal in conclusions:
                actuator.actuator_action()

#        Output Prudens conclusions for debugging, also displays sensor outputs          
        print("\nConclusions: ", conclusions)      

def user_input_thread():
    global version, x
    while True:
        x = input("\nEnter new rule: ")
        if any((char in set('abcdefghijklmnopqrstuvwxyz')) for char in x):
            version += 1
            print("Policy level " + str(version % max_policy_num) +" is being used", end="\n")
    

def main():
    try:
        prog_thread = threading.Thread(target=program)
        inp_thread = threading.Thread(target=user_input_thread)

        prog_thread.start()
        inp_thread.start()

        prog_thread.join()
        inp_thread.join()

    except Exception as exc:
        print(exc)
        raise 

    finally:                                         
        print("Exited program")
        fcn.sys_exit()

main()