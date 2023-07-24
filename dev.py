import tech2 as tech

version = 1

while True:
#code for changing policy version######################
    pf = open("/home/yiannis/cyens/policy.txt", "w")
    #if tech.button2.is_pressed:
    if tech.btn_is_pressed(2):
        print("pressed------------")
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

    dist = tech.getDist(17, 18)
    toContext ="dist("+str(int(dist*100))+");"
    
    #if tech.button1.is_pressed:
    if tech.btn_is_held(24):
        toContext += "atHome;"
    else:
        toContext += "-atHome;"
            
    with open("/home/yiannis/cyens/context.txt","w") as f:
        f.write(toContext)
     
    conclusions = tech.subproc()
    #print(conclusions)
    
    if "blinkLED1slow" in conclusions:
        tech.blinkLEDslow(3)
    elif "blinkLED1fast" in conclusions:
        tech.blinkLEDfast(3)
    elif "onLED2" in conclusions:
        tech.onLED(4)
    elif "sysStandby" in conclusions:
        tech.sysStandby()
    
    # for sensor in sensors:
    #     type_of_sensor = typeof(sensor) 
    #     if type_of_sensor == "Button":
    #         # do something
    #         pass
    #     if type_of_sensor == "Dist":
    #         pass
    #     else:
    #         raise TypeError("Sensor type not supported")

    print('Distance: ' , dist * 100)
