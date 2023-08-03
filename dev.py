import sys_fcns as fcn
from drivers import button as btn
import tech as tech

for sensor in tech.sens_array: #for-loops to setup each sensor specified
    sensor.sensor_setup()

for actuator in tech.act_array:
    actuator.actuator_setup()

version = 0
print("\n-----------------------------------\nPolicy level " + str(version) +" is being used")

try:
    while True:
        toContext = ""
###########################
        pf = open("/home/yiannis/cyens/txt/policy.txt", "w")
        if btn.btn_is_pressed(2):
            version += 1
            if version > 7:
                version = 1
        print("Policy level " + str(version) +" is being used \033[K")
        path = "/home/yiannis/cyens/txt/policy"+str(version)+".txt"
        with open(path, "r") as policy:
            data = policy.read()
        pf.write(data)
        pf.close()
##############################

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
                
        with open("/home/yiannis/cyens/txt/context.txt","w") as f:
            f.write(toContext)
        
        conclusions = fcn.subproc()
                
        used_literals = ""
        for actuator in tech.act_array:
            if actuator.literal in conclusions:
                actuator.actuator_action()
            else:
                used_literals = "(x)" + actuator.literal
                pass
        
        for sensor in tech.sens_array:
            if getattr(sensor, "sensor_id") == "USR1":
                #print('\nDistance: ',sensor.data)
                break

        print("\nConclusions: ", conclusions, "\n", used_literals )
        #fcn.print_adc_readings()
except Exception as exc:
    print(exc)
    raise 
finally:                                         
    print("Exited loop")
    fcn.sys_exit()