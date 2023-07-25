import fcns as fcn
import tech as tech

version = 1 
for sensor in tech.sens_array: #for-loops to setup each sensor specified
    sensor.sensor_setup()
for actuator in tech.act_array:
    actuator.actuator_setup()

while True:
    toContext = ""
#code for changing policy version######################
    pf = open("/home/yiannis/cyens/txt/policy.txt", "w")
    if fcn.btn_is_pressed(2):
        version += 1
        if version > 4:
            version = 1
    if version == 4:
        with open("/home/yiannis/cyens/txt/policy4.txt", "r") as f1:
            data = f1.read()
        pf.write(data)
        print("Policy version 4 is being used")
    elif version == 3:
        with open("/home/yiannis/cyens/txt/policy3.txt", "r") as f1:
            data = f1.read()
        pf.write(data)
        print("Policy version 3 is being used")
    elif version == 2:
        with open("/home/yiannis/cyens/txt/policy2.txt", "r") as f1:
            data = f1.read()
        pf.write(data)
        print("Policy version 2 is being used")
    elif version == 1:
        with open("/home/yiannis/cyens/txt/policy1.txt", "r") as f1:
            data = f1.read()
        pf.write(data)
        print("Policy version 1 is being used")
    pf.close()
###########################################################
    
    for sensor in tech.sens_array:
        sensor.sensor_action() 
        sensor.data_in_literal()
        if sensor.is_literal_numeric == True:
            toContext += sensor.literal_p
        elif sensor.data == True:
            toContext += sensor.literal_p      
        elif sensor.data == False:
            toContext += sensor.literal_n
        else:
            print("Something else happened")

    # dist = fcn.getDist(17, 18)
    # toContext ="dist("+str(int(dist))+");"
    
    # if fcn.btn_is_held(24):
    #     toContext += "atHome;"
    # else:
    #     toContext += "-atHome;"
            
    with open("/home/yiannis/cyens/txt/context.txt","w") as f:
        f.write(toContext)
    
    conclusions = fcn.subproc()
    #print(conclusions)
    
    if "blinkLED1slow" in conclusions:
        fcn.blinkLEDslow(3)
    elif "blinkLED1fast" in conclusions:
        fcn.blinkLEDfast(3)
    elif "onLED2" in conclusions:
        fcn.onLED(4)
    elif "sysStandby" in conclusions:
        fcn.sysStandby()
    
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
            print('Distance: ' , sensor.data)
            break

