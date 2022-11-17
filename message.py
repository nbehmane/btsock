import struct

CMD_ACK = 0x00  # Acknowledge msg
CMD_REJ = 0x01  # Reject
CMD_DATA = 0x02  # Data packet
CMD_INFO = 0x03  # Request info
CMD_CMP = 0x04  # Completed
CMD_SND = 0x05  # SEND
CMD_FILE = 0x06  # Sending a file
CMD_OFILE = 0x07  # Open a file to be written to.
CMD_CFILE = 0x08  # Close a file to be written to.
CMD_QUIT = 0xFF  # Quit
CMD_DEBUG = 0xEE  # Debug msg

file = None
filename = None


def cmd_ofile(message):
    global file
    global filename
    filename = 'copy'
    for i in range(0, message.data_length):
        filename += chr(message.data[i])
    print(f"Opening/Creating {filename}")
    file = open(filename, 'ab')


def cmd_cfile(message):
    global file
    global filename
    if file is None:
        print("FILE ALREADY CLOSED!")
    else:
        print(f"Closing {filename}")
        file.close()


def cmd_debug(message):
    for i in range(0, message.data_length):
        print(chr(message.data[i]), end='')
        print()


def cmd_data(message):
    print(message)


def cmd_ack(message):
    # print("\033[1;31m INFO:" + "\033[0;37m Command acknowledged.")
    pass


def cmd_rej(message):
    print(message)


def cmd_info(message):
    print(message)


def cmd_cmp(message):
    print(message)


def cmd_snd(message):
    for i in range(0, message.data_length):
        print(chr(message.data[i]), end='')
    print()


def cmd_file(message):
    global file
    if file is None:
        print("Critical error")
    else:
        file.write(bytes(message.data[:message.data_length]))


def cmd_quit(message):
    for i in range(0, message.data_length):
        print(chr(message.data[i]), end='')


class MessageHandler:
    def __init__(self):
        # Function call backs. these are replaceable.
        self.function_cbs = {
            CMD_ACK: cmd_ack,
            CMD_REJ: cmd_rej,
            CMD_DATA: cmd_data,
            CMD_INFO: cmd_info,
            CMD_CMP: cmd_cmp,
            CMD_SND: cmd_snd,
            CMD_QUIT: cmd_quit,
            CMD_DEBUG: cmd_debug,
            CMD_FILE: cmd_file,
            CMD_OFILE: cmd_ofile,
            CMD_CFILE: cmd_cfile
        }

    def add_cb(self, cmd_type, function):
        self.function_cbs[cmd_type] = function

    def msg_handler(self, message):
        func = self.function_cbs[message.cmd]
        func(message)


class Message:
    """
    A Message class to be sent over RFCOMM socket.
    """
    type_string = ">ii1000s"

    def __init__(self, cmd, data_length=0, data=None):
        self.cmd = cmd
        if data is None:
            self.data = "0xDEADBEEF"
            self.data_length = len(self.data)
        else:
            self.data_length = data_length
            self.data = data

    def pack(self, encode=True):
        if encode:
            return struct.pack(Message.type_string, self.cmd, self.data_length, bytes(self.data, "utf-8"))
        return struct.pack(Message.type_string, self.cmd, len(self.data), self.data)

    def __repr__(self):
        return f"{self.cmd}, {self.data_length}, {self.data}"

    @staticmethod
    def construct(cmd, data_length, data):
        return Message(cmd, data_length=data_length, data=data)