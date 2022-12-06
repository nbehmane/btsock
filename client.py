import io
import socket
import struct
import time

import message as msg


def progress_bar(current, total, bar_length=20):
    fraction = current / total

    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'

    print(f'Progress: [{arrow}{padding}] {int(fraction * 100)}%', end=ending)


class Client:
    """
    Client to connect to server.
    """

    def __init__(self, server_address, port=3, size=1024, handler=None):
        self.server_address = server_address
        self.port = port
        self.size = size
        self.socket = socket.socket(
            socket.AF_BLUETOOTH,
            socket.SOCK_STREAM,
            socket.BTPROTO_RFCOMM)
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler = handler

    def start_client(self, send=False, filename=None):
        if self.handler is None:
            self.handler = msg.MessageHandler()
        self.socket.connect((self.server_address, self.port))
        if not send:
            self._mainloop()
        if send:
            self._sendloop(filename)

    def _serverack(self, file=None):
        server_msg = None
        try:
            msg_cmd, msg_length, msg_data = struct.unpack(msg.Message.type_string, self.socket.recv(self.size))
            server_msg = msg.Message.construct(msg_cmd, msg_length, msg_data)
        except Exception as e:
            if file is not None:
                file.close()
            print(e)
            self.socket.close()
        return server_msg

    def _sendloop(self, filename):
        self._preamble()

        file = open(filename, "rb")
        file_size = file.seek(0, io.SEEK_END)
        file.close()
        file = open(filename, "rb")

        new_msg = msg.Message(msg.CMD_OFILE, len(filename), filename)
        self.socket.send(new_msg.pack(encode=True))

        server_msg = self._serverack(file=file)

        if server_msg:
            self.handler.msg_handler(server_msg)
        else:
            print("\033[0;31m WARNING:" + "\033[1;37m No acknowledgment sent from server.")

        done = False
        while True:
            line = file.read(1000)
            if file.tell() == file_size:
                done = True
            new_msg = msg.Message(msg.CMD_FILE, len(line), line)
            self.socket.send(new_msg.pack(encode=False))
            progress_bar(file.tell(), file_size, 20)

            server_msg = self._serverack(file=file)

            if server_msg:
                self.handler.msg_handler(server_msg)
            else:
                msg.print_warn("\033[1;37m No acknowledgment sent from server.")

            if done:
                break

        new_msg = msg.Message(msg.CMD_CFILE, len(filename), filename)
        self.socket.send(new_msg.pack(encode=True))

        file.close()
        self.socket.close()

    def _mainloop(self):
        # Preamble
        self._preamble()

        while True:  # Mainloop
            text = input("$> ").split(" ", 1)
            if text[0] == "debug":
                debug_msg = "This is a debug message"
                new_msg = msg.Message(msg.CMD_DEBUG, len(debug_msg), debug_msg)
            elif text[0] == "send":
                try:
                    data = str(text[1])
                except Exception as e:
                    data = "0xDEADBEEF"
                new_msg = msg.Message(msg.CMD_SND, len(data), data)
            elif text[0] == "quit" or text[0] == "exit":
                break
            else:
                continue
            self.socket.send(new_msg.pack())

            # Receive the ack from the server
            msg_cmd, msg_length, msg_data = struct.unpack(msg.Message.type_string, self.socket.recv(self.size))
            server_msg = msg.Message.construct(msg_cmd, msg_length, msg_data)
            if server_msg:
                self.handler.msg_handler(server_msg)
            else:
                msg.print_warn("\033[1;37m No acknowledgment sent from server.")
        self.socket.close()

    def _preamble(self):
        data = self.socket.recv(self.size)
        print(data.decode())
        self.socket.send(bytes("Client connected.", 'UTF-8'))


if __name__ == '__main__':
    server_address = "38:BA:F8:55:8C:90"
    port = 3
    size = 1024
    client = Client(server_address, port, size)
    client.start_client()