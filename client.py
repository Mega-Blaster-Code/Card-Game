import socket
import threading
import time

class Net_Client:
    def __init__(self):
        self.ip = None
        self.port = 44555
        self.conn = None
        self.addr = None

    def send(self, data):
        conn = self.conn
        print(f"sending {data} to {conn}")
        if conn:
            data = data.encode()
            conn.sendall(data)

    def wait_message(self):
        conn = self.conn
        print(f"waiting from {conn}")
        if conn:
            data = conn.recv(1024)
            data = data.decode()
            return data

    def conect(self, ip):
        try:
            self.ip = ip
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.ip,self.port))
            print("conected to server")
            self.conn = client
            return 0
        except:
            print("Fail")
            return -1