from src.follow_line import MotorController, MotorMixer, ColorSensor
import ev3dev.ev3 as ev3
import time

# constants
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
lm.duty_cycle_sp = 0
rm.duty_cycle_sp = 0


def run():
    # this loop should make the robot follow a black line on its right side
    mixer = MotorMixer.MotorMixer(base_speed, speed_min, speed_max)
    mc = MotorController.MotorController(0.62, 0.21, 0.25, 40, color_setpoint)
    while not ts1.value() or not ts2.value():
        color_values = cs.get_rgb()     # get color values from color sensor
        rudder = mc.run(color_values)   # calculate rudder from color values
        speed = mixer.run(rudder)       # divide the rudder speed on the motors
        lm.duty_cycle_sp = speed[0]
        rm.duty_cycle_sp = speed[1]
        print('speed: ', speed[0], speed[1])
    # stop motors
    lm.duty_cycle_sp = 0
    rm.duty_cycle_sp = 0
    pass


def learn():
    # use this loop to tune PID factors
    mixer = MotorMixer.MotorMixer(base_speed, speed_min, speed_max)
    mc = MotorController.MotorController(0, 0, 0, 40, color_setpoint)
    # counter
    step = 5e-4
    i = 0
    while i < 3:
        if ts1.value() or ts2.value():
            i += 1
            lm.duty_cycle_sp = 0
            rm.duty_cycle_sp = 0
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
        color_values = cs.get_rgb()     # get color values from color sensor
        rudder = mc.run(color_values)   # calculate rudder from color values
        speed = mixer.run(rudder)       # divide the rudder speed on the motors
        lm.duty_cycle_sp = speed[0]
        rm.duty_cycle_sp = speed[1]
        print('speed: ', speed[0], speed[1])
    # stop motors
    lm.duty_cycle_sp = 0
    rm.duty_cycle_sp = 0
    print(mc.k_p, mc.k_i, mc.k_d)
    pass


if __name__ == '__main__':
    run()
