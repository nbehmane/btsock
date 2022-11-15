import struct

CMD_ACK = 0x00  # Acknowledge msg
CMD_REJ = 0x01  # Reject
CMD_DATA = 0x02  # Data packet
CMD_INFO = 0x03  # Request info
CMD_CMP = 0x04  # Completed
CMD_SND = 0x05  # SEND
CMD_QUIT = 0xFF  # Quit
CMD_DEBUG = 0xEE # Debug msg


def cmd_debug(message):
    for i in range(0, message.data_length):
        print(chr(message.data[i]), end='')
        print()


def cmd_data(message):
    print(message)


def cmd_ack(message):
    print("\033[1;31m INFO:" + "\033[0;37m Command acknowledged.")


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
            CMD_DEBUG: cmd_debug
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
    type_string = ">ii255s"

    def __init__(self, cmd, data_length=0, data=None):
        self.cmd = cmd
        if data is None:
            self.data = "0xDEADBEEF"
            self.data_length = len(self.data)
        else:
            self.data_length = data_length
            self.data = data

    def pack(self):
        return struct.pack(Message.type_string, self.cmd, self.data_length, bytes(self.data, "utf-8"))

    def __repr__(self):
        return f"{self.cmd}, {self.data_length}, {self.data}"

    @staticmethod
    def construct(cmd, data_length, data):
        return Message(cmd, data_length=data_length, data=data)