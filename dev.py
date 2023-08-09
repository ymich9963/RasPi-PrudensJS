"""
    Main developer file. This will not be edited in the final product. 
    Here all system functionalities are executed.
"""

import sys_fcns as fcn
from drivers import button as btn
import tech as tech

#initalise peripherals
for sensor in tech.sens_array:
    sensor.sensor_setup()

for actuator in tech.act_array:
    actuator.actuator_setup()

#to chage policy version,
#not used in final version
version = 0
max_policy_num = 8
print("\n-----------------------------------")

try:
    while True:

        toContext = ""

#       code to change policy level and output to terminal, 
#       will not be in the final version,
#       temporarily simulates user input
        pf = open("/home/yiannis/cyens/txt/policy.txt", "w")
        if btn.btn_is_pressed(2):
            version += 1
        print("Policy level " + str(version % max_policy_num) +" is being used \033[K")
        path = "/home/yiannis/cyens/txt/policy"+str(version % max_policy_num)+".txt"
        with open(path, "r") as policy:
            data = policy.read()
        pf.write(data)
        pf.close()


#       if changes are made to the technician file, 
#       pressing this button will re-initalise the devices without turning it off
        if btn.btn_is_pressed(27):
            fcn.sys_restart(tech.sens_array, tech.act_array, module = tech)
        
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
        conclusions = fcn.subproc(toContext)
                
#       check for which conclusion corresponds to an actuator
        for actuator in tech.act_array:
            if actuator.literal in conclusions:
                actuator.actuator_action()
                        
        print("\nConclusions: ", conclusions)

except Exception as exc:
    print(exc)
    raise 

finally:                                         
    print("Exited loop")
    fcn.sys_exit()