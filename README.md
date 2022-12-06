# btsock
A Bluetooth socket program to transfer files from one Linux machine to another.

# Usage
1. The computer that will be receiving the file will be known as the server and must be launched first.
  - `python3 main.py --server --serverAddress <bluetooth_address_of_server>`
2. The computer that will be sending the file will be known as a client and must be launched after the server.
  - `python3 main.py --client --send <file_name> --address <server_address>`
3. Once the file has been transferred, both programs will quit.

# Known Issues
1. When using a Raspberry PI with Raspberry PI OS, the server will fail to launch.
2. Eventually, supplying the server address will be unecessary. 
  - Will try to find the BT address of the server controller automatically.
