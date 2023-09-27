import sys
import time
import RPi.GPIO as GPIO

usleep = lambda x: time.sleep(x / 1000000.0)

_TIMEOUT1 = 1000
_TIMEOUT2 = 10000


class UltrasonicRanger(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def _get_distance(self):
        # Ensure the pin is set up as an OUTPUT
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, False)
        usleep(2)
        GPIO.output(self.pin, True)
        usleep(10)
        GPIO.output(self.pin, False)

        # Change the pin setup to INPUT
        GPIO.setup(self.pin, GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if GPIO.input(self.pin):
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not GPIO.input(self.pin):
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()

        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2) - 4  # cm

        return distance

    def get_distance(self):
        while True:
            # Ensure the pin is set up as an OUTPUT before calling _get_distance
            GPIO.setup(self.pin, GPIO.OUT)
            dist = self._get_distance()
            if dist:
                return dist


def main():
    sonar = UltrasonicRanger(18)

    print('Detecting distance...')
    # print('{} cm'.format(sonar.get_distance()))
    return sonar.get_distance()


if __name__ == '__main__':
    main()
