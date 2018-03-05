# TODO: implement mixing from battery


class MotorMixer:
    def __init__(self, throttle, minimum, maximum):
        self.throttle = throttle
        self.min = minimum
        self.max = maximum

    def run(self, rudder):
        left = self.throttle + rudder
        right = self.throttle - rudder
        speed = self.compensate(left, right)
        return speed

    def compensate(self, left, right):
        if left > self.max:
            right += self.max - left
        elif left < self.min:
            right += self.min - left
        if right > self.max:
            left += self.max - right
        elif right < self.min:
            left += self.min - right
        left = max(self.min, min(self.max, left))
        right = max(self.min, min(self.max, right))
        return left, right
