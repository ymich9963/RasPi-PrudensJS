import sys_fcns as fcn
from drivers import button as btn
import tech as tech
import os

for sensor in tech.sens_array: #for-loops to setup each sensor specified
    sensor.sensor_setup()

for actuator in tech.act_array:
    actuator.actuator_setup()

version = 0
print("\n-----------------------------------\nPolicy level " + str(version) +" is being used")

while True:
    #copies driver files found on USB
    if os.path.exists("//media/yiannis/DRIVER_USB/RasPi-PrudensJS/drivers/") and not os.path.exists("~/cyens/drivers/drivers"):
        os.system("cp -r //media/yiannis/DRIVER_USB/RasPi-PrudensJS/drivers ~/cyens/drivers")

    toContext = ""
#code for changing policy version######################
    pf = open("/home/yiannis/cyens/txt/policy.txt", "w")
    if btn.btn_is_pressed(2):
        version += 1
        print("Policy level " + str(version) +" is being used \033[K")
        if version > 4:
            version = 1
    if version == 4:
        with open("/home/yiannis/cyens/txt/policy4.txt", "r") as policy:
            data = policy.read()
        pf.write(data)
    elif version == 3:
        with open("/home/yiannis/cyens/txt/policy3.txt", "r") as policy:
            data = policy.read()
        pf.write(data)
    elif version == 2:
        with open("/home/yiannis/cyens/txt/policy2.txt", "r") as policy:
            data = policy.read()
        pf.write(data)
    elif version == 1:
        with open("/home/yiannis/cyens/txt/policy1.txt", "r") as policy:
            data = policy.read()
        pf.write(data)
    elif version == 0:
        with open("/home/yiannis/cyens/txt/policy0.txt", "r") as policy:
            data = policy.read()
        pf.write(data)
    pf.close()
###########################################################
    
    for sensor in tech.sens_array:
        # if sensor.sensor_id == "BTN1":
        #     print("debug")
        sensor.sensor_action() 
        sensor.data_in_literal()
        if sensor.is_literal_numeric == True:
            toContext += sensor.literal_p
        elif sensor.data == True:
            toContext += sensor.literal_p      
        elif sensor.data == False:
            toContext += sensor.literal_n
        else:
            print("Error call dev")
            
    with open("/home/yiannis/cyens/txt/context.txt","w") as f:
        f.write(toContext)
    
    conclusions = fcn.subproc()
    print("Conclusions: " + str(conclusions), end=' ')
    
    for actuator in tech.act_array:
        if actuator.literal in conclusions:
            actuator.actuator_action()
        else:
            print("(x)" + actuator.literal + ", ", end=' ',)

    print("\033[F")
    
    # for sensor in sensors:
    #     type_of_sensor = typeof(sensor) 
    #     if type_of_sensor == "Button":
    #         # do something
    #         pass
    #     if type_of_sensor == "Dist":
    #         pass
    #     else:
    #         raise TypeError("Sensor type not supported")

    for sensor in tech.sens_array:
        if getattr(sensor, "sensor_id") == "USR1":
            print('\nDistance: ' + str(sensor.data), end='\033[F')
            break
