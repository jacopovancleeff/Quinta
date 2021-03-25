"""

Author: Jacopo Van Cleeff
Date: 19-02-2021

WEB APIs that manage a school library

"""

from flask import Flask,render_template,request,redirect,url_for,jsonify
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def home():
    return "<h1> Biblioteca Online</h1><p>Prototipo di web API</p>"

@app.route('/api/v1/resources/books/all',methods=['GET'])
def api_all():
    return all()

def all():
    conn = sqlite3.connect("static/libreria.db")
    cur= conn.cursor()
    cur.execute("SELECT * FROM Libri ")
    data = cur.fetchone()
    conn.close()

    return jsonify(data) 

def search(parametro,dato):
    conn = sqlite3.connect("static/library.db")
    cur= conn.cursor()
    cur.execute("SELECT * FROM Libri WHERE "+ parametro +"=='" + dato +"'")
    data = cur.fetchall()
    if data is None:
        return "Warning, this "+ parametro + " does not exists"
    conn.close()

    return jsonify(data)  

@app.route('/api/v1/resources/books/id',methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id"

    return search("id",str(id))

@app.route('/api/v1/resources/books/author',methods=['GET'])
def api_author():
    if 'author' in request.args:
        author = request.args['author']
    else:
        return "Error: No author field provided. Please specify an author"

    return search("author",str(author))

@app.route('/api/v1/resources/books/title',methods=['GET'])
def api_title():
    if 'title' in request.args:
        title = request.args['title']
    else:
        return "Error: No title field provided. Please specify an title"
    
    return search("title",str(title))

app.run()