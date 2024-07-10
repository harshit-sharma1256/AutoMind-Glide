import RPi.GPIO as GPIO
import time

# Pin definitions
EnableL = 5
HighL = 6       # LEFT SIDE MOTOR
LowL = 7

EnableR = 10
HighR = 8       # RIGHT SIDE MOTOR
LowR = 9

D0 = 21       # Raspberry Pi GPIO pin 21    LSB
D1 = 22       # Raspberry Pi GPIO pin 22
D2 = 23       # Raspberry Pi GPIO pin 23
D3 = 24       # Raspberry Pi GPIO pin 24    MSB

# Initialize variables
i = 0
j = 0

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(EnableL, GPIO.OUT)
GPIO.setup(HighL, GPIO.OUT)
GPIO.setup(LowL, GPIO.OUT)

GPIO.setup(EnableR, GPIO.OUT)
GPIO.setup(HighR, GPIO.OUT)
GPIO.setup(LowR, GPIO.OUT)

GPIO.setup(D0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(D1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(D2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(D3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pwmL = GPIO.PWM(EnableL, 1000)
pwmR = GPIO.PWM(EnableR, 1000)
pwmL.start(0)
pwmR.start(0)

def data():
    a = GPIO.input(D0)
    b = GPIO.input(D1)
    c = GPIO.input(D2)
    d = GPIO.input(D3)
    return 8 * d + 4 * c + 2 * b + a

def forward():
    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)

    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmR.ChangeDutyCycle(100)

def backward():
    GPIO.output(HighL, GPIO.HIGH)
    GPIO.output(LowL, GPIO.LOW)
    pwmL.ChangeDutyCycle(100)

    GPIO.output(HighR, GPIO.HIGH)
    GPIO.output(LowR, GPIO.LOW)
    pwmR.ChangeDutyCycle(100)

def stop():
    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    pwmL.ChangeDutyCycle(0)

    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmR.ChangeDutyCycle(0)

def left1():
    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    pwmL.ChangeDutyCycle(63)

    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmR.ChangeDutyCycle(100)

def left2():
    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    pwmL.ChangeDutyCycle(35)

    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmR.ChangeDutyCycle(100)

def left3():
    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    pwmL.ChangeDutyCycle(20)

    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmR.ChangeDutyCycle(100)

def right1():
    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)

    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmR.ChangeDutyCycle(63)

def right2():
    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)

    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmR.ChangeDutyCycle(35)

def right3():
    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)

    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmR.ChangeDutyCycle(20)

def u_turn():
    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(0.4)

    pwmL.ChangeDutyCycle(98)
    pwmR.ChangeDutyCycle(98)
    time.sleep(1)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(0.4)

    GPIO.output(HighL, GPIO.HIGH)
    GPIO.output(LowL, GPIO.LOW)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)
    pwmR.ChangeDutyCycle(100)
    time.sleep(0.7)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(0.4)

    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)
    pwmR.ChangeDutyCycle(100)
    time.sleep(0.9)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(0.4)

    GPIO.output(HighL, GPIO.HIGH)
    GPIO.output(LowL, GPIO.LOW)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)
    pwmR.ChangeDutyCycle(100)
    time.sleep(0.7)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(1)

    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(59)
    pwmR.ChangeDutyCycle(59)
    time.sleep(0.3)

def object_avoidance():
    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(1)

    GPIO.output(HighL, GPIO.HIGH)
    GPIO.output(LowL, GPIO.LOW)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(98)
    pwmR.ChangeDutyCycle(98)
    time.sleep(0.5)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(0.2)

    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)
    pwmR.ChangeDutyCycle(100)
    time.sleep(1)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(0.2)

    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    GPIO.output(HighR, GPIO.HIGH)
    GPIO.output(LowR, GPIO.LOW)
    pwmL.ChangeDutyCycle(100)
    pwmR.ChangeDutyCycle(100)
    time.sleep(0.5)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(1)

    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(59)
    pwmR.ChangeDutyCycle(59)
    time.sleep(0.5)

    global i
    i += 1

def lane_change():
    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(1)

    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    GPIO.output(HighR, GPIO.HIGH)
    GPIO.output(LowR, GPIO.LOW)
    pwmL.ChangeDutyCycle(98)
    pwmR.ChangeDutyCycle(98)
    time.sleep(0.5)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(0.2)

    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)
    pwmR.ChangeDutyCycle(100)
    time.sleep(0.8)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(0.2)

    GPIO.output(HighL, GPIO.HIGH)
    GPIO.output(LowL, GPIO.LOW)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(100)
    pwmR.ChangeDutyCycle(100)
    time.sleep(0.5)

    pwmL.ChangeDutyCycle(0)
    pwmR.ChangeDutyCycle(0)
    time.sleep(1)

    GPIO.output(HighL, GPIO.LOW)
    GPIO.output(LowL, GPIO.HIGH)
    GPIO.output(HighR, GPIO.LOW)
    GPIO.output(LowR, GPIO.HIGH)
    pwmL.ChangeDutyCycle(59)
    pwmR.ChangeDutyCycle(59)
    time.sleep(0.5)

def loop():
    global i, j
    while True:
        if j > 25000:
            lane_change()
            i = 0
            j = 0

        data_value = data()
        if data_value == 0:
            forward()
            if i > 0:
                j += 1
        elif data_value == 1:
            right1()
            if i > 0:
                j += 1
        elif data_value == 2:
            right2()
            if i > 0:
                j += 1
        elif data_value == 3:
            right3()
            if i > 0:
                j += 1
        elif data_value == 4:
            left1()
            if i > 0:
                j += 1
        elif data_value == 5:
            left2()
            if i > 0:
                j += 1
        elif data_value == 6:
            left3()
            if i > 0:
                j += 1
        elif data_value == 7:
            u_turn()
        elif data_value == 8:
            pwmL.ChangeDutyCycle(0)
            pwmR.ChangeDutyCycle(0)
            time.sleep(4)
            pwmL.ChangeDutyCycle(59)
            pwmR.ChangeDutyCycle(59)
            time.sleep(1)
        elif data_value == 9:
            object_avoidance()
        elif data_value == 10:
            pwmL.ChangeDutyCycle(0)
            pwmR.ChangeDutyCycle(0)
            time.sleep(2)
        elif data_value > 10:
            stop()

try:
    loop()
except KeyboardInterrupt:
    pass
finally:
    pwmL.stop()
    pwmR.stop()
    GPIO.cleanup()
