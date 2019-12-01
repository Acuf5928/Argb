import sys
import glob
import serial

class port:
    def __init__(self):
        self.result = []
        self.argbdevice = []

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.result.append(port)

            except (OSError, serial.SerialException):
                pass

    def identify(self):
        for element in self.result[1:]:
            s = serial.Serial(port = "COM7", baudrate=9600)
            s.write("identifyYourSelf\n".encode('utf-8'))

            print(str(s.readline()))

            if(out.startswith("ARGB Device: ")):
                self.argbdevice.append(element)

    ##https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

if __name__ == "__main__":
    a = port()
    a.serial_ports()
    a.identify()
    print(a.result)
    print(a.argbdevice)