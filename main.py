import argparse
import socket
import server as sv
import client as cl
import message as msg

DEFAULT_PORT = 3
DEFAULT_BD_ADDR = "38:BA:F8:55:8C:90"
DEFAULT_SIZE = 1024
DEFAULT_BACKLOG = 5


def main():
    parser = argparse.ArgumentParser(
        prog="btsock",
        description="File management via Bluetooth sockets."
    )
    parser.add_argument('--server',
                        action='store_true',
                        help='Server designation.')
    parser.add_argument('--client',
                        action='store_true',
                        help='Client designation.')
    parser.add_argument('-p',
                        '--port',
                        metavar='PORT',
                        required=False,
                        default=DEFAULT_PORT,
                        help=f"Set Bluetooth port. Default port is {DEFAULT_PORT}.")
    parser.add_argument('-a',
                        '--address',
                        metavar='ADDRESS',
                        nargs=1,
                        type=str,
                        default='0xDEADBEEF',
                        required=False,
                        help='Bluetooth address to connect to.')
    parser.add_argument('-sa',
                        '--serverAddress',
                        metavar='SERVER_ADDRESS',
                        nargs=1,
                        type=str,
                        default='0xDEADBEEF',
                        required=False,
                        help='Bluetooth address to start server on.')
    parser.add_argument('-S', '--send',
                        metavar='ABSOLUTE_FILE_PATH',
                        required=False,
                        default='0xDEADBEEF',
                        help='File to send to server.')

    args = parser.parse_args()

    if args.server:
        # Temp for demo
        server_address = None
        if args.serverAddress:
            server_address = args.serverAddress[0]
            print(server_address)
        else:
            print("Server address required.")
            exit(0)
        msg.print_info(f"Address: {server_address} | Port: {args.port}")
        server = sv.Server(server_address, args.port, DEFAULT_SIZE, DEFAULT_BACKLOG)
        server.start_server()
    elif args.client:
        address = args.address[0]
        if address == '0xDEADBEEF':
            msg.print_info(f"Address not given. Using {socket.gethostname()}")
            address = socket.gethostname()
        msg.print_info(f"Connecting to {address} on port {args.port}")
        client = cl.Client(address, port=args.port, size=DEFAULT_SIZE)
        if args.send == '0xDEADBEEF':
            client.start_client()
        else:
            client.start_client(send=True, filename=args.send)
    else:
        print("Server or Client designation required")
        parser.print_help()


if __name__ == '__main__':
    main()
