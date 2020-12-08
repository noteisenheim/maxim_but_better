from flask import Flask, render_template, request
import socket
import json

BUFF_SIZE = 1024
SERVER_ADDR = ("10.0.0.11", 2345)

app = Flask(__name__)

FLASK_PORT = 1234

@app.route("/", methods = ["POST", "GET"])
def index():
    return render_template("index.html", message = None)

@app.route("/auth", methods = ["POST", "GET"])
def try_login():
    global SERVER_ADDR

    login = request.form.getlist('login')[0]
    password = request.form.getlist('password')[0]
    message_dict = {"command" : "authorization", "agrs" : {"login" : login, "password" : password}}
    message = json.dumps(message_dict)

    # send message to authorize

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)
    client_socket.send(bytes(message, "utf8"))

    msg = ""
    while msg == "":
        msg = client_socket.recv(BUFF_SIZE)
    decoded_msg = str(msg, "utf8")
    client_socket.close()

    decoded = json.loads(decoded_msg)

    if decoded["answer"] == "yes":
        pass
    else:
        return render_template("index.html", message = "Incorrent credentials")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = FLASK_PORT)
