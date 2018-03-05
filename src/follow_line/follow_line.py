from main import ColorSensor
from main import MotorController
from main import MotorMixer

color_setpoint = 380
speed_max = 100
speed_min = -100
base_speed = 50

cs = ColorSensor.ColorSensor()
mc = MotorController.MotorController(0.5, 0.2, 0.05, 20, color_setpoint)
mixer = MotorMixer.MotorMixer(base_speed, speed_min, speed_max)

# this loop should make the robot follow a black line on its right side
while True:
    color_values = cs.get_rgb()     # get color values from color sensor
    rudder = mc.run(color_values)   # calculate rudder from color values
    mixer.run(rudder)               # divide the rudder speed on the motors
    pass
