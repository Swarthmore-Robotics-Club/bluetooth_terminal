
import serial
import time

#Picks up your garbage: Use Serial1.write(Char[]) to communicate
def main():
    #You have to find your own path for the HC-05...should be in /dev
    ser = serial.Serial("/dev/tty.HC-05-LEADER-DevB", 9600,timeout = None)
    #Very advanced code. Much wow.
    line = ""
    while True:
        ch = ser.read()
        ch = ch.decode("utf-8")

        if ch != "\n":
            line += ch
        else:
            print(line)
            line = ""


if __name__ == main():
    main()
