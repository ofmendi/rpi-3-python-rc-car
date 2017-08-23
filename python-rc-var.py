import RPi.GPIO as GPIO
import time
import serial

PWMA1 = 6 
PWMA2 = 13
PWMB1 = 20
PWMB2 = 21
D1 = 12 # Sol Teker
D2 = 26 # Sag Teker

PWM = 50

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PWMA1,GPIO.OUT)
GPIO.setup(PWMA2,GPIO.OUT)
GPIO.setup(PWMB1,GPIO.OUT)
GPIO.setup(PWMB2,GPIO.OUT)
GPIO.setup(D1,GPIO.OUT)
GPIO.setup(D2,GPIO.OUT)
p1 = GPIO.PWM(D1,500)
p2 = GPIO.PWM(D2,500)
p1.start(50) # Sol Teker
p2.start(50) # Sag Teker

#Serial itelisim icin gerekli ayarlar yapildi.
ser = serial.Serial (
    port = '/dev/serial0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def set_motor(A1,A2,B1,B2):
    GPIO.output(PWMA1,A1)
    GPIO.output(PWMA2,A2)
    GPIO.output(PWMB1,B1)
    GPIO.output(PWMB2,B2)

def forward():
    set_motor(1,0,1,0)
    
def stop():
    set_motor(0,0,0,0)

def reverse():
    set_motor(0,1,0,1)

def left():
    #set_motor(0,0,1,0)
    pass 
def right():
    #set_motor(1,0,0,0)
    pass

print('Xbee Uzerinden Gelecek Veri Bekleniyor')
stop()

try:
    while True:
        # begin Serial itelsim ile gelen byte turunde olan veri utf-8 formatında str veri tipine donusturuluyor
        key = ser.readline().decode('utf-8')
        # end
        if(key != ''):
            # begin Gelen verinin ilk karakterine gore araca yon veriliyor
            print("Get the key:",key)
            if key[0] == 'W':
                forward()
                p2.ChangeDutyCycle(PWM)
                p1.ChangeDutyCycle(PWM)
                print("forward")
            if key[0] == 'A':
                left()
                p2.ChangeDutyCycle(PWM)
                p1.ChangeDutyCycle(PWM - (PWM/2) )
                print("left")
            if key[0] == 'B':
                stop()
                print("stop")
            if key[0] == 'D':
                right()
                p1.ChangeDutyCycle(PWM)
                p2.ChangeDutyCycle(PWM - (PWM/2) )
                print("right")
            if key[0] == 'S':
                reverse()
                p2.ChangeDutyCycle(PWM)
                p1.ChangeDutyCycle(PWM)
                print("reverse")
            if key[0] == 'E':
                if(PWM + 10 < 101):
                    PWM = PWM + 10
                    p1.ChangeDutyCycle(PWM)
                    p2.ChangeDutyCycle(PWM)
                    ser.write(str(PWM).encode('utf-8'))
                    print(PWM)
            if key[0] == 'Q':
                if(PWM - 10 > -1):
                    PWM = PWM - 10
                    p1.ChangeDutyCycle(PWM)
                    p2.ChangeDutyCycle(PWM)
                    ser.write(str(PWM).encode('utf-8'))
                    print(PWM)
            # end
			
except KeyboardInterrupt:
    GPIO.cleanup();

