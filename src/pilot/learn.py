from src.events.EventRegistry import EventRegistry
from src.pilot.ColorSensor import ColorSensor
from src.pilot.MotorController import MotorController
from src.pilot.MotorMixer import MotorMixer
import ev3dev.ev3 as ev3
import time


# helper method
def stop_motors():
    lm.duty_cycle_sp = 0
    rm.duty_cycle_sp = 0


# constants
i_max = 40
color_setpoint = 330
speed_max = 100
speed_min = -100
base_speed = 30

# init
ts1 = ev3.TouchSensor('in2')
ts2 = ev3.TouchSensor('in3')
lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')

registry = EventRegistry()
cs = ColorSensor(registry)


def run():
    # use this loop to tune PID factors
    mixer = MotorMixer(base_speed, speed_min, speed_max)
    mc = MotorController(0, 0, 0, i_max, color_setpoint)
    # counter
    step = 5e-4
    i = 0
    while i < 3:
        if ts1.value() or ts2.value():
            i += 1
            stop_motors()
            time.sleep(2)
        if i == 0:
            mc.k_p += step
            print('KP: ', mc.k_p)
        elif i == 1:
            mc.k_d += step
            print('KD: ', mc.k_d)
        elif i == 2:
            mc.k_i += step
            print('KI: ', mc.k_i)
        rgb = cs.get_rgb()              # get rgb values from color sensor
        rudder = mc.run(rgb)            # calculate rudder from color values
        speed = mixer.run(rudder)       # divide the rudder speed on the motors
        lm.duty_cycle_sp = speed[0]
        rm.duty_cycle_sp = speed[1]
        # print('speed: ', speed)
    stop_motors()
    print(mc.k_p, mc.k_i, mc.k_d)
    pass
