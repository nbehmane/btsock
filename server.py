import socket
import struct
import message as msg


class Server:
    """
    Server that will send the file or get the file from the client.
    """
    def __init__(self, server_address, port=3, size=1024, backlog=5, msg_handler=None):
        self.address = server_address
        self.remote_address = None
        self.port = port
        self.size = size
        self.backlog = backlog
        self.client = None
        """
        self.socket = socket.socket(
            socket.AF_BLUETOOTH, 
            socket.SOCK_STREAM, 
            socket.BTPROTO_RFCOMM)
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler = msg_handler

    def start_server(self):
        print("Starting server...")
        if self.handler is None:
            self.handler = msg.MessageHandler()
        try:
            self.socket.bind((self.address, self.port))
        except Exception as e:
            print(e)
            exit(0)
        self.socket.listen(self.backlog)

        try:
            self.client, self.remote_address = self.socket.accept()
            self._mainloop()
        except Exception as e:
            print(e)
            print("Quitting...", end='')
            if self.client is not None:
                self.client.close()
            self.socket.close()
            print('okay', end='')
            print()

    def _mainloop(self):
        # Preamble
        self.client.send(bytes("Server Connected.", 'UTF-8'))
        data = self.client.recv(self.size)
        print(data.decode())
        while True:
            # Receive data sent from Server.
            data = self.client.recv(self.size)
            # Unpack the data.
            msg_cmd, msg_length, msg_data = struct.unpack(msg.Message.type_string, data)
            if data:
                # Construct a message object from the unpacked data.
                received_msg = msg.Message.construct(msg_cmd, msg_length, msg_data)
                # Handle the message using the handler.
                self.handler.msg_handler(received_msg)

            ack_msg = msg.Message(msg.CMD_ACK, 0, None)
            self.client.send(ack_msg.pack())


if __name__ == '__main__':
    serverAddress = "38:BA:F8:55:8C:90"
    port = 3
    size = 1024
    backlog = 5
    server = Server(socket.gethostname(), 25565, size, backlog)
    server.start_server()