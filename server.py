import threading
import socket
import time
import pygame

class Net_Server:
    def __init__(self, ip):
        self.ip = ip
        self.port = 44555
        self.close_server = False
        self.conn = None
        self.addr = None

    def wait_message(self):
        conn = self.conn
        print(f"waiting from {conn}")

        if conn:
            data = conn.recv(1014)

            if not data:
                return False
            data = data.decode()
            return data

    def send(self, data):
        conn = self.conn
        print(f"sending {data} to {conn}")
        if conn:

            data = data.encode()
            conn.sendall(data)

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip,self.port))
        server.listen()
        print(f"server started in {self.ip}:{self.port}")
        try:
            conn, addr = server.accept()
            self.addr = addr
            self.conn = conn
        except TypeError as e:
            print(f"error {e}")