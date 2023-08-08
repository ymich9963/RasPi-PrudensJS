import sys_fcns as fcn
from drivers import button as btn
import tech as tech

for sensor in tech.sens_array:
    sensor.sensor_setup()

for actuator in tech.act_array:
    actuator.actuator_setup()

version = 0
max_policy_num = 8
print("\n-----------------------------------")

try:
    while True:
        toContext = ""

########################## code to output policy level in terminal
        pf = open("/home/yiannis/cyens/txt/policy.txt", "w")
        if btn.btn_is_pressed(2):
            version += 1
        print("Policy level " + str(version % max_policy_num) +" is being used \033[K")
        path = "/home/yiannis/cyens/txt/policy"+str(version % max_policy_num)+".txt"
        with open(path, "r") as policy:
            data = policy.read()
        pf.write(data)
        pf.close()
##############################

        if btn.btn_is_pressed(27):
            fcn.sys_restart(tech.sens_array, tech.act_array, module = tech)
        
        fcn.copy_from_USB()
        #fcn.manual_all_adc_sensor_read()
    
        for sensor in tech.sens_array:
            sensor.sensor_action()
            sensor.data_in_literal()
            if sensor.is_literal_numeric == True or sensor.data == True:
                toContext += sensor.literal_p
            elif sensor.data == False:
                toContext += sensor.literal_n
            else:
                print("Error call dev")
                    
        conclusions = fcn.subproc(toContext)
                
        used_literals = ""
        for actuator in tech.act_array:
            if actuator.literal in conclusions:
                actuator.actuator_action()
                        
        for sensor in tech.sens_array: 
            if getattr(sensor, "sensor_id") == "USR1":
                #print('\nDistance: ',sensor.data)
                break

        print("\nConclusions: ", conclusions)
        #fcn.print_adc_readings()

except Exception as exc:
    print(exc)
    raise 

finally:                                         
    print("Exited loop")
    fcn.sys_exit()