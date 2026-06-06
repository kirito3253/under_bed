import cv2
import numpy as np
from gpiozero import Robot
import time

#gpioの設定
robot=Robot(left=(17,18), right=(19,20))
#暴走を止めるためのstop
robot.stop()

def motor(x): #100とsec_pushは要調整
    sp=((320-x)/3200)+0.4
    robot.forward(sp)
    time.sleep(1)
    robot.backward(sp)
    time.sleep(1)
    robot.stop()
