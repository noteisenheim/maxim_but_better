from flask import Flask, render_template, request
import socket
import json
import hashlib

ok = "ok"

MY_IP = "10.91.52.97"
LOL = "0.0.0.0"

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
    message_dict = {"command" : -1, "argument1" : login, "argument2" : str(encoded_password)}
    message = json.dumps(message_dict)

    print(str(encoded_password))

    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = '{"response" : "yes"}'

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
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "some reply"

    return render_template("main.html", create_file_message = reply)

@app.route("/delete_file", methods = ["POST", "GET"])
def delete_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 4, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "file was deleted"

    return render_template("main.html", delete_file_message = reply)

@app.route("/info_file", methods = ["POST", "GET"])
def info_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 5, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "info about file"

    return render_template("main.html", info_file_message = reply)

@app.route("/copy_file", methods = ["POST", "GET"])
def copy_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 6, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "file was copied"

    return render_template("main.html", copy_file_message = reply)

@app.route("/move_file", methods = ["POST", "GET"])
def move_file():
    filename = request.form.getlist('filename')[0]
    dest_dir = request.form.getlist('dest_dir')[0]

    message_dict = {"command" : 7, "argument1" : filename, "argument2" : dest_dir}
    message = json.dumps(message_dict)
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "file was moved"

    return render_template("main.html", move_file_message = reply)

@app.route("/open_dir", methods = ["POST", "GET"])
def open_dir():
    dirname = request.form.getlist('target_dir')[0]

    message_dict = {"command" : 8, "argument1" : dirname, "argument2" : ""}
    message = json.dumps(message_dict)
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "dir {} is opened".format(dirname)

    return render_template("main.html", open_dir_message = reply)

@app.route("/read_dir", methods = ["POST", "GET"])
def read_dir():
    dirname = request.form.getlist('target_dir')[0]

    message_dict = {"command" : 9, "argument1" : dirname, "argument2" : ""}
    message = json.dumps(message_dict)
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "content is: 1) biba 2) boba 3) pupa 4) lupa"

    return render_template("main.html", read_dir_message = reply)

@app.route("/make_dir", methods = ["POST", "GET"])
def make_dir():
    dirname = request.form.getlist('new_dir')[0]

    message_dict = {"command" : 10, "argument1" : dirname, "argument2" : ""}
    message = json.dumps(message_dict)
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "directory {} is created".format(dirname)

    return render_template("main.html", make_dir_message = reply)

@app.route("/del_dir", methods = ["POST", "GET"])
def del_dir():
    dirname = request.form.getlist('del_dir')[0]

    message_dict = {"command" : 11, "argument1" : dirname, "argument2" : ""}
    message = json.dumps(message_dict)
    reply = send_to_namenode(SERVER_ADDR, message)
    # reply = "directory {} is deleted (oops)".format(dirname)

    return render_template("main.html", del_dir_message = reply)

@app.route("/write_file", methods = ["POST", "GET"])
def write_file():
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 3, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)

    reply = send_to_namenode(SERVER_ADDR, message)
    print(reply)
    # reply = "file successfully uploaded"

    datanodes_data = reply.split('%')
    filename_prefix = datanodes_data[-2]

    ips = [datanodes_data[i] for i in range(1, len(datanodes_data)-2) if i % 2 != 0]
    ports = [datanodes_data[i] for i in range(1, len(datanodes_data)-2) if i % 2 == 0]

    # send FILE
    for i in range(len(ips)):
        try:
            s = socket.socket()

            s.connect((ips[i], int(ports[i])))
            # We can send file sample.txt
            file = open(filename, "rb")
            SendData = file.read(BUFF_SIZE)

            while SendData:
                # Now send the content of sample.txt to server
                s.send(SendData)
                SendData = file.read(BUFF_SIZE)

            # Close the connection from client side
            s.close()
        except:
            return render_template("main.html", write_file_message = "Error occured while uploading file")
    return render_template("main.html", write_file_message = "Successfully uploaded the file!")

@app.route("/read_file", methods = ["POST", "GET"])
def read_file():
    global MY_IP
    filename = request.form.getlist('filename')[0]

    message_dict = {"command" : 2, "argument1" : filename, "argument2" : ""}
    message = json.dumps(message_dict)

    print("waiting for 1st reply")
    reply = send_to_namenode(SERVER_ADDR, message)
    print("got reply {}".format(reply))
    # reply = "file successfully uploaded"

    if reply != "No such file":
        s = socket.socket()
        PORT = 9899
        s.bind((MY_IP, PORT))
        s.listen(10)

        # Now we can establish connection with server
        print("waiting for conn")
        conn, addr = s.accept()
        print("got conn")
        # Open one recv.txt file in write mode
        file = open(filename, "wb")
        while True:
            # Receive any data from client side
            RecvData = conn.recv(BUFF_SIZE)
            while RecvData:
                file.write(RecvData)
                RecvData = conn.recv(BUFF_SIZE)
            # Close the file opened at server side once copy is completed
            file.close()
            # Close connection with client
            conn.close()
            # Come out from the infinite while loop as the file has been copied from client.
            break
        s.close()
        return render_template("main.html", read_file_message = "Successfully downloaded a file!")
    else:
        return render_template("main.html", read_file_message = "No such file exists!")

if __name__ == "__main__":
    app.run(host = MY_IP, port = FLASK_PORT)
