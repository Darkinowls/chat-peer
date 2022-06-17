from socket import SocketIO

import socketio
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room
from pandas import DataFrame
from SqliteManager import sqlite_manager

app = Flask(__name__)
socketIO = SocketIO(app, cors_allowed_origins="*")


@app.route('/')
def html_index(error=None):
    table: DataFrame = sqlite_manager.chat_table.set_index('name')
    return render_template('index.html', index='name',
                           table=table, error_message=error)


@app.route('/chat/<name>')
def html_chat(name):
    if sqlite_manager.is_name_in(name):
        return render_template('chat.html', name=name)
    error = 'Error! No such chat!'
    print(error)
    return html_index(error)


@app.route('/create', methods=("POST", "GET"))
def html_create():
    if request.method == "POST":
        try:
            sqlite_manager.insert_row(request.form['name'], request.form['description'])
            return redirect(url_for('html_chat', name=request.form['name']))
        except ValueError as e:
            print(e)
            return render_template('create.html', error_message=e)
    return render_template('create.html')


@socketIO.on('send_message')
def send_message(data):
    print(data['message'], data['name'])
    socketIO.emit('receive_message', data['message'], to=data['name'])


@socketIO.on('join_room')
def handle_join_room(data):
    name = data['name']
    join_room(name)
    socketIO.emit('join_announce', to=name)


if __name__ == '__main__':
    socketIO.run(app)
