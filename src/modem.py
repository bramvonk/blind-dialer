import serial # https://pythonhosted.org/pyserial/


class modem:
    """
    Abstraction of a modem.
    Will do some basic stuff such as connecting to the serial port,
    and sending specific commands.
    """
    def __init__(self, serial_port):
        self.serial_port = serial_port

    def __enter__(self):
        # open the serial port with default options (9600,8,1,N)
        self.ser = serial.Serial(self.serial_port)
        return self

    def send_command_and_expect_ok(self, command):
        print "Sending command %s" % command
        self.ser.write(b'%s\r\n' % (command.encode('ascii')))
        line = self.ser.readline()
        print "Received answer %s" % line
        if line.startswith("OK"):
            """OK"""
        else:
            raise RuntimeError("Did not receive ok, but %s" % line)

    def __exit__(self, exc_type, exc_value, traceback):
        # close the serial port
        self.ser.close()
