import ev3dev.ev3 as ev3
from main import ColorSensor
from main import MotorController
from main import MotorMixer

color_setpoint = 180
speed_max = 100
speed_min = -100
base_speed = 30

cs = ColorSensor.ColorSensor()
ts1 = ev3.TouchSensor('in2')
ts2 = ev3.TouchSensor('in4')
mc = MotorController.MotorController(0.3, 0.2, 0.1, 40, color_setpoint)
mixer = MotorMixer.MotorMixer(base_speed, speed_min, speed_max)
lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')
lm.command = 'run-direct'
rm.command = 'run-direct'
lm.duty_cycle_sp = 0
rm.duty_cycle_sp = 0
# this loop should make the robot follow a black line on its right side
while not ts1.value() and not ts2.value():
    color_values = cs.get_rgb()  # get color values from color sensor
    print('color: ', color_values[0], color_values[1], color_values[2],
          (color_values[0] + color_values[1] + color_values[2]) / 3)
    rudder = mc.run(color_values)  # calculate rudder from color values
    print('rudder: ', rudder)
    speed = mixer.run(rudder)  # divide the rudder speed on the motors
    lm.duty_cycle_sp = speed[0] / 2
    rm.duty_cycle_sp = speed[1] / 2
    print('speed: ', speed[0], speed[1])
    # time.sleep(1)
    pass
lm.duty_cycle_sp = 0
rm.duty_cycle_sp = 0
