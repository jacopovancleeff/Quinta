"""
Author: Bruno Luca, Van Cleeff Jacopo , Tommaso Genovese
Date: 23-10-2020
"""

import socket
import threading
import turtle

server_ip = "127.0.0.1"
server_port = 7000

def client():
    t = turtle.Turtle()

    c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    c.connect((server_ip,server_port))
    while True:
        msg = input(">>")
        c.sendall(msg.encode())
        echo_msg = c.recv(4096).decode()

        print(f"ECHO>> {echo_msg}")
        _,path = echo_msg.split(',')

        print(path)

        index = 0
        while index < len(path):
            distance = ''
            if path[index] == 'F':
                index = index + 1
                while index < len(path) and path[index].isnumeric():
                    distance = distance + path[index]
                    index = index + 1
                t.forward(int(distance)/2)

            elif path[index] == 'B':
                index = index + 1
                while index < len(path) and path[index].isnumeric():
                    distance = distance + path[index]
                    index = index + 1
                t.backward(int(distance)/2)

            elif path[index] == 'L':
                index = index + 1
                while index < len(path) and path[index].isnumeric():
                    distance = distance + path[index]
                    index = index + 1
                t.left(int(distance))

            elif path[index] == 'R':
                index = index + 1
                while index < len(path) and path[index].isnumeric():
                    distance = distance + path[index]
                    index = index + 1
                t.right(int(distance))

        if msg == "close":
            break
    c.close()
    print("finito")
    


if __name__ == "__main__":
    client()