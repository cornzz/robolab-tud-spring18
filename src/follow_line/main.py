from . import MotorController, MotorMixer, ColorSensor, color_test
import ev3dev.ev3 as ev3
import time


# helper method
def stop_motors():
    lm.duty_cycle_sp = 0
    rm.duty_cycle_sp = 0


# constants
k_p = 0.62
k_i = 0.15
k_d = 0.20
i_max = 40
color_setpoint = 330
speed_max = 100
speed_min = -100
base_speed = 30

# init
cs = ColorSensor.ColorSensor()
ts1 = ev3.TouchSensor('in2')
ts2 = ev3.TouchSensor('in3')
lm = ev3.LargeMotor('outA')
rm = ev3.LargeMotor('outD')
lm.command = 'run-direct'
rm.command = 'run-direct'
stop_motors()


def run():
    # this loop should make the robot follow a black line on its right side
    mixer = MotorMixer.MotorMixer(base_speed, speed_min, speed_max)
    mc = MotorController.MotorController(k_p, k_i, k_d, i_max, color_setpoint)
    while not ts1.value() or not ts2.value():
        colors = cs.get_all()
        # time.sleep(0.25)
        rgb = colors[0]                 # get rgb values from color sensor
        rudder = mc.run(rgb)            # calculate rudder from rgb mean
        speed = mixer.run(rudder)       # divide the rudder speed on the motors
        lm.duty_cycle_sp = speed[0]
        rm.duty_cycle_sp = speed[1]
        # print('speed: ', speed[0], speed[1])
    stop_motors()
    pass


def learn():
    # use this loop to tune PID factors
    mixer = MotorMixer.MotorMixer(base_speed, speed_min, speed_max)
    mc = MotorController.MotorController(0, 0, 0, i_max, color_setpoint)
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
        colors = cs.get_all()
        rgb = colors[0]  # get rgb values from color sensor
        rudder = mc.run(rgb)  # calculate rudder from color values
        speed = mixer.run(rudder)       # divide the rudder speed on the motors
        lm.duty_cycle_sp = speed[0]
        rm.duty_cycle_sp = speed[1]
        # print('speed: ', speed[0], speed[1])
    stop_motors()
    print(mc.k_p, mc.k_i, mc.k_d)
    pass


if __name__ == '__main__':
    run()
