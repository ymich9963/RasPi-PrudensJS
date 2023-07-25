import fcns as fcn
import tech2 as tech

version = 1 
for sensor in tech.sens_array: #for-loops to setup each sensor specified
    sensor.sensor_config()
    
for actuator in tech.act_array:
    actuator.actuator_config()

while True:
#code for changing policy version######################
    pf = open("/home/yiannis/cyens/policy.txt", "w")
    if fcn.btn_is_pressed(2):
        #print("pressed------------")
        version += 1
        if version > 4:
            version = 1
    if version == 4:
        with open("/home/yiannis/cyens/policy4.txt", "r") as f1:
            data = f1.read()
        pf.write(data)
        print("Policy version 4 is being used")
    elif version == 3:
        with open("/home/yiannis/cyens/policy3.txt", "r") as f1:
            data = f1.read()
        pf.write(data)
        print("Policy version 3 is being used")
    elif version == 2:
        with open("/home/yiannis/cyens/policy2.txt", "r") as f1:
            data = f1.read()
        pf.write(data)
        print("Policy version 2 is being used")
    elif version == 1:
        with open("/home/yiannis/cyens/policy1.txt", "r") as f1:
            data = f1.read()
        pf.write(data)
        print("Policy version 1 is being used")
    pf.close()
###########################################################

    dist = fcn.getDist(17, 18)
    toContext ="dist("+str(int(dist))+");"
    
    if fcn.btn_is_held(24):
        toContext += "atHome;"
    else:
        toContext += "-atHome;"
            
    with open("/home/yiannis/cyens/context.txt","w") as f:
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

    print('Distance: ' , dist)

