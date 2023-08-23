from drivers import RGBled as rgb
from time import sleep
import RPi.GPIO as GPIO

rgb.rgb_setup(13,12,6)
rgb.on_yellow(13, 12, 6)

sleep(5)

rgb.off_yellow(13,12,6)
rgb.on_red(13,12,6)

sleep(5)

rgb.off_red(13,12,6)


GPIO.cleanup()