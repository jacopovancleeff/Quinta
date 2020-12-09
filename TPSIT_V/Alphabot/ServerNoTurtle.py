"""
Author: Bruno Luca, Genovese Tommaso, Van Cleeff Jacopo
"""

import socket
import threading
import sys
import logging as log 
import sqlite3
import os

ip = "127.0.0.1"
port = 7000

connection_table = {}   #store connected end point
active_thread = []      #store running threads

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(BASE_DIR, "percorsi.db")

class ClietThread(threading.Thread):
    def __init__(self,ip,port,connection): #contructor
        threading.Thread.__init__(self)

        self.ip_address = ip
        self.port = port
        self.connection = connection
        self.again = 1


    def run(self):  #codice che esegue il thread
        while self.again:
            msg = self.connection.recv(4096)
            msg = msg.decode()
            log.info(f"{self.ip_address},{self.port} >> {msg}")

            if msg == "close":
                log.info(f"{self.ip_address}:{self.port} >> exit.")
                self.again=0
                delete_connection(self)
                sys.exit()
            else:
                with sqlite3.connect(db_name) as db_conn:
                    self.cursor = db_conn.cursor()

                    path = msg.split(",")
                    if len(path) < 2:
                        log.error("\t[2.1]\t->\tINVALID FORMAT")
                        self.connection.sendall("2.1,INVALID FORMAT".encode())
                    else:
                        log.info(f"{self.ip_address}:{self.port} >> {path}")

                        self.cursor.execute(f"SELECT id FROM luoghi WHERE luoghi.nome = \"{path[0]}\" OR  luoghi.nome = \"{path[1]}\" ")
                        ids = self.cursor.fetchall()
                        log.info(f"{self.ip_address}:{self.port} >> {ids}")

                        if len(ids) < 2:
                            log.error("\t[1.2]\t->\tEND/START NOT FOUND")
                            self.connection.sendall("1.2,END/START NOT FOUND".encode())
                        else:
                            self.cursor.execute(f"SELECT percorso FROM percorsi, inzio_fine WHERE inzio_fine.id_start = {int(ids[0][0])} AND inzio_fine.id_end = {int(ids[1][0])} AND percorsi.id = inzio_fine.id_percorso ")
                            percorso = self.cursor.fetchone()
                            log.info(percorso)
                        
                            if percorso == None:
                                log.error("\t[1.1]\t->\tPATH NOT FOUND")
                                self.connection.sendall("1.1,PATH NOT FOUND".encode())
                            else:
                                self.connection.sendall(("0.0,"+percorso[0]).encode())

def delete_connection(t):
    global connection_table
    global active_thread
    active_thread.pop(active_thread.index(t))
    connection_table.pop(t.connection)
        

def server():
    global connection_table
    global active_thread

    #configuring log message
    log.basicConfig(format = "%(asctime)s: %(message)s", level = log.INFO, datefmt = "%H:%M:%S")
    log.basicConfig(format = "%(asctime)s: %(message)s", level = log.ERROR, datefmt = "%H:%M:%S")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((ip,port))

    while True:
        #new connection
        s.listen()
        log.info("SERVER IS LISTENING...\n")
        conn, add = s.accept()
        log.info("NEW USER CONNECTED!!\n")
        t = ClietThread(add[0],add[1],conn)
        t.start()

        #updating tables
        active_thread.append(t)
        connection_table[conn] = add

if __name__ == "__main__":
    server()