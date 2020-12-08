from flask import Flask, render_template, request
import socket
import json
import hashlib

ok = "ok"

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
    encoded_password = hashlib.sha1(password.encode('utf-8')).digest()
    message_dict = {"command" : -1, "argument1" : login, "argument2" : encoded_password}
    message = json.dumps(message_dict)

    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = '{"response" : "yes"}'

    decoded = json.loads(reply)

    if decoded["response"] == "yes":
        return render_template("main.html")
    else:
        return render_template("index.html", message = "Incorrent credentials")

@app.route("/create_file", methods = ["POST", "GET"])
def create_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 1, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "some reply"

    return render_template("main.html", create_file_message = reply)

@app.route("/delete_file", methods = ["POST", "GET"])
def delete_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 4, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "file was deleted"

    return render_template("main.html", delete_file_message = reply)

@app.route("/info_file", methods = ["POST", "GET"])
def info_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 5, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "info about file"

    return render_template("main.html", info_file_message = reply)

@app.route("/copy_file", methods = ["POST", "GET"])
def copy_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 6, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "file was copied"

    return render_template("main.html", copy_file_message = reply)

@app.route("/move_file", methods = ["POST", "GET"])
def move_file():
    filename = request.form.getlist('filename')[0]
    dest_dir = request.form.getlist('dest_dir')[0]

    message_dict = {"command" : 7, "argument1" : filename, "argument2" : dest_dir}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "file was moved"

    return render_template("main.html", move_file_message = reply)

@app.route("/open_dir", methods = ["POST", "GET"])
def open_dir():
    dirname = request.form.getlist('target_dir')[0]

    message_dict = {"command" : 8, "argument1" : dirname, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "dir {} is opened".format(dirname)

    return render_template("main.html", open_dir_message = reply)

@app.route("/read_dir", methods = ["POST", "GET"])
def read_dir():
    dirname = request.form.getlist('target_dir')[0]

    message_dict = {"command" : 9, "argument1" : dirname, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "content is: 1) biba 2) boba 3) pupa 4) lupa"

    return render_template("main.html", read_dir_message = reply)

@app.route("/make_dir", methods = ["POST", "GET"])
def make_dir():
    dirname = request.form.getlist('new_dir')[0]

    message_dict = {"command" : 10, "argument1" : dirname, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "directory {} is created".format(dirname)

    return render_template("main.html", make_dir_message = reply)

@app.route("/del_dir", methods = ["POST", "GET"])
def del_dir():
    dirname = request.form.getlist('del_dir')[0]

    message_dict = {"command" : 11, "argument1" : dirname, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "directory {} is deleted (oops)".format(dirname)

    return render_template("main.html", del_dir_message = reply)

@app.route("/write_file", methods = ["POST", "GET"])
def write_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 3, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)
    # reply = send_to_namenode(SERVER_ADDR, message)
    reply = "file successfully uploaded"

    return render_template("main.html", write_file_message = reply)

if __name__ == "__main__":
    my_ip = "10.91.52.97"
    lol = "0.0.0.0"
    app.run(host = my_ip, port = FLASK_PORT)
