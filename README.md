# RasPi-Prudens 
An implementation of [PrudensJS](https://github.com/VMarkos/prudens-js) on a [Raspberry Pi 400](https://www.raspberrypi.com/products/raspberry-pi-400/) with sensors and actuators. 

## Files

```dev.py``` - main file were all program functionalities are executed.

```tech.py``` - file for a technician to initialise sensors or actuators.

```classes.py``` - containes the classes used by the system.

```sys_fcns.py``` -  functions used by the system that should not be modified.

## Directories

```drivers``` - For a sensor/actuator to run a driver file is required to be placed here and to contain all of its functionality.  

```tests``` - Certain tests to make sure certain components function as inteded.

```txt``` - Contains the text files used by the project.

```prudens-js``` - [PrudensJS](https://github.com/VMarkos/prudens-js)



## Installation
Directories **must** be placed in the same folder as the files. Software will work on any RasPi system with 40 GPIO pins. If issues arise with PrudnsJS check the Issues tab of the GitHub repo.


