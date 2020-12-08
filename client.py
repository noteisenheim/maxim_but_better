from flask import Flask, render_template, request
import socket
import json

BUFF_SIZE = 1024
SERVER_ADDR = ("10.91.51.111", 2345)

def send_to_namenode(SERVER_ADDR, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)
    client_socket.send(bytes(message, "utf8"))

    msg = ""
    while msg == "":
        msg = client_socket.recv(BUFF_SIZE)
    decoded_msg = str(msg, "utf8")

    client_socket.close()
    return decoded_msg

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
    message_dict = {"command" : -1, "argument1" : login, "argument2" : password}
    message = json.dumps(message_dict)

    reply = send_to_namenode(SERVER_ADDR, message)

    decoded = json.loads(reply)

    if decoded["response"] == "yes":
        return render_template("main.html")
    else:
        return render_template("index.html", message = "Incorrent credentials")

@app.route("/create_file", methods = ["POST", "GET"])
def create_file():

    filename = get_full_name(CUR_DIR, request.form.getlist('filename')[0])

    message = {"command" : 1, "argument1" : filename, "argument2" : ""}

    if response["status"] == "ok":
        return render_template("main.html")
    elif response["status"] == "notok":
        return render_template("main.html", create_file_error = response["args"]["error"])

if __name__ == "__main__":
    my_ip = "10.91.52.97"
    lol = "0.0.0.0"
    app.run(host = my_ip, port = FLASK_PORT)
