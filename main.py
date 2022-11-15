import argparse
import socket
import server as sv
import client as cl

DEFAULT_PORT = 25565
DEFAULT_BD_ADDR = "38:BA:F8:55:8C:90"
DEFAULT_SIZE = 1024
DEFAULT_BACKLOG = 5


def main():
    parser = argparse.ArgumentParser(
        prog="btsock",
        description="File management via Bluetooth sockets."
    )
    parser.add_argument('--server', action='store_true')
    parser.add_argument('--client', action='store_true')
    parser.add_argument('-p',
                        '--port',
                        metavar='PORT',
                        required=False,
                        default=DEFAULT_PORT)
    parser.add_argument('-a',
                        '--address',
                        metavar='ADDRESS',
                        nargs=1,
                        type=str,
                        default='0xDEADBEEF',
                        required=False)

    args = parser.parse_args()

    if args.server:
        print(f"Address: {socket.gethostname()} | Port: {args.port}.")
        server = sv.Server(socket.gethostname(), args.port, DEFAULT_SIZE, DEFAULT_BACKLOG)
        server.start_server()
    elif args.client:
        address = args.address
        if address == '0xDEADBEEF':
            print(f"Address not given. Using {socket.gethostname()}.")
            address = socket.gethostname()
        print(f"Connecting to {address} on port {args.port}.")
        client = cl.Client(address, args.port, DEFAULT_SIZE)
        client.start_client()
    else:
        print("Server or Client designation required.")


if __name__ == '__main__':
    main()