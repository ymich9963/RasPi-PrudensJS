# RasPi-Prudens 
An implementation of [PrudensJS](https://github.com/VMarkos/prudens-js) on a [Raspberry Pi 400](https://www.raspberrypi.com/products/raspberry-pi-400/) with sensors and actuators. 

## Files

```dev.py``` - Main file were all program functionalities are executed.

```tech.py``` - File for a technician to initialise sensors or actuators.

```classes.py``` - Containes the classes used by the system.

```sys_fcns.py``` -  Functions used by the system that should not be modified.

```setup.py``` -  To allow the ```drivers``` directory to be a module that can be imported. Useful mainly for component testing.

## Directories

```docs``` - Documentation for the system and device datasheets. 

```blank_system``` - A version of the project software with no peripherals added except the two buttons.

```drivers``` - For a sensor/actuator to run a driver file is required to be placed here and to contain all of its functionality.  

```tests``` - Certain tests to make sure certain components function as inteded. Mainly used for device driver testing

```txt``` - Contains the text files used by the project.

```fan model``` - 3D printed fan files.

```prudens-js``` - [PrudensJS](https://github.com/VMarkos/prudens-js)



## Installation
Directories **must** be placed in the same folder as the files. Software will work on any RasPi system with 40 GPIO pins. If issues arise with PrudnsJS check the Issues tab of the GitHub repo.

Hardware installation, using the system, and a system analysis is shown in the documentation.

