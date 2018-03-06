from . import MotorController, MotorMixer, ColorSensor, color_test
import ev3dev.ev3 as ev3
import time
import sys


# helper method
def stop_motors():
    lm.duty_cycle_sp = 0
    rm.duty_cycle_sp = 0


# constants
k_p = 0.62
k_i = 0.05
k_d = 0.3
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
    while not ts1.value() and not ts2.value():
        colors = cs.get_rgb()              # get rgb values from color sensor
        rbd = colors[0] - colors[2]
        # gs = (colors[0] + colors[1] + colors[2]) / 3
        # print('RBD: ' + str(rbd) + '  GS: ' + str(gs))
        # time.sleep(0.2)
        if 90 <= rbd:  # red patch
            stop_motors()
            ev3.Sound.beep()
            time.sleep(1)
            lm.run_to_rel_pos(position_sp=100, speed_sp=180, stop_action="brake")
            rm.run_to_rel_pos(position_sp=100, speed_sp=180, stop_action="brake")
            print('red')
            time.sleep(1)
            lm.command = 'run-direct'
            rm.command = 'run-direct'
        elif rbd <= -65:  # blue patch
            stop_motors()
            ev3.Sound.beep()
            time.sleep(1)
            lm.run_to_rel_pos(position_sp=100, speed_sp=180, stop_action="brake")
            rm.run_to_rel_pos(position_sp=100, speed_sp=180, stop_action="brake")
            print('blue')
            time.sleep(1)
            #  TODO: überdrehen kompensieren
            lm.command = 'run-direct'
            rm.command = 'run-direct'
        rudder = mc.run(colors)            # calculate rudder from rgb mean
        speed = mixer.run(rudder)          # divide the rudder speed on the motors
        lm.duty_cycle_sp = speed[0]
        rm.duty_cycle_sp = speed[1]
        # print(speed)
    stop_motors()
    pass


def check_isc():
    #  TODO: Intersection checken (turn(deg))
    time.sleep(5)
    pass


def turn(degrees):
    # turn by degrees
    p_sp = 2.88 * degrees
    lm.run_to_rel_pos(position_sp=-p_sp, speed_sp=200, stop_action="hold")
    rm.run_to_rel_pos(position_sp=p_sp, speed_sp=200, stop_action="hold")
    # print('Turned ' + str(degrees) + ' degrees.')
    lm.command = 'run-direct'
    rm.command = 'run-direct'


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
