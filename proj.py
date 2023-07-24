import setup

version = 1

while True:
#code for changing policy version######################
    pf = open("/home/yiannis/cyens/policy.txt", "w")
    if setup.button2.is_pressed:
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

    dist = setup.getDist()
    toContext ="dist("+str(int(dist*100))+");"
    
    if setup.button1.is_pressed:
        toContext += "atHome;"
    else:
        toContext += "-atHome;"
            
    with open("/home/yiannis/cyens/context.txt","w") as f:
        f.write(toContext)
     
    conclusions = setup.subproc()
    #print(conclusions)
    
    if "blinkLED1slow" in conclusions:
        setup.blinkLEDslow(0)
    elif "blinkLED1fast" in conclusions:
        setup.blinkLEDfast(0)
    elif "onLED2" in conclusions:
        setup.onLED(1)
    elif "sysStandby" in conclusions:
        setup.sysStandby()
        
    print('Distance: ' , dist * 100)
