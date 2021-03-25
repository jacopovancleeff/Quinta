from flask import Flask, render_template, redirect, url_for, request, jsonify
import sqlite3
import socket

app = Flask(__name__)  

@app.route("/", methods=["POST"])
def scanip():
    """
    La funzione serve per scansionare le porte dalla minPort alla maxPort ricevute in input dal sito 
    Dalla riga 17 alla 19 prendo attraverso una POST i 3 valori(ip, numero di porta minimo e numero di porta massimo)
    dalla 23 in giù tengo aperto il db per salvare il risultato dello scan sulle porte 
    nel FOR ciclo per tutte le porte e controllo attraverso la c.connect_ex((ip,port)) se sono aperte o chiuse
    successivamente attraverso la cursor.execute inserisco nel db il risultato insieme all'ip e la porta 
    infine chiudo il db
    e faccio il return di Port scan concluded
    
    """
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#IPv4 socket

    ip = request.form["ip"]                           # prendo ip, numero di porte min e massimo e li assegno a delle variabili         
    minPort = int(request.form["minp"])
    maxPort = int(request.form["maxp"])

    with sqlite3.connect("static/dati.db") as conn:   #connessione al DB
        cursor = conn.cursor()                        #creo un cursore

        for port in range(minPort,maxPort+1):         # for per scorrere le porte
            valore = "CHIUSA"                   
            print(f"port = {port}")

            res = c.connect_ex((ip,port))

            if  res == 0:	                          #  if per controllare se la porta è aperta oppure no          
                print(f"{port} availalbe")

                valore = "APERTA"

            cursor.execute(f"INSERT INTO catalogo (ip,porta,valore) VALUES('{ip}',{port},'{valore}');") # inserisco nel db il risutlato
            corrispondance = cursor.fetchall()

        c.close()                                    # chiudo il db

        return "Port scan concluded"

@app.route("/")
def main():
    return render_template("sito.html")             # mostro il sito html

if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
    