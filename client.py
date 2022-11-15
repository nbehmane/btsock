import socket
import struct
import message as msg


class Client:
    """
    Client to connect to server.
    """
    def __init__(self, server_address, port=3, size=1024, handler=None):
        self.server_address = server_address
        self.port = port
        self.size = size
        """
        self.socket = socket.socket(
            socket.AF_BLUETOOTH,
            socket.SOCK_STREAM,
            socket.BTPROTO_RFCOMM)
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler = handler

    def start_client(self):
        if self.handler is None:
            self.handler = msg.MessageHandler()
        self.socket.connect((self.server_address, self.port))
        self._mainloop()

    def _mainloop(self):
        # Preamble
        data = self.socket.recv(self.size)
        print(data.decode())
        self.socket.send(bytes("Client connected.", 'UTF-8'))

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
                print("\033[0;31m WARNING:" + "\033[1;37m No acknowledgment sent from server.")
        self.socket.close()


if __name__ == '__main__':
    server_address = "38:BA:F8:55:8C:90"
    port = 3
    size = 1024
    client = Client(socket.gethostname(), 25565, size)
    client.start_client()