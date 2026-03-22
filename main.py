import socket
import threading
import time

print("Welcome to P2P Messenger!")

clientIP = "None"
serverIP = "None"
clientPORT = 0
serverPORT = 0

connected = False

def Response(s):
    while True:
        message = input("> ")
        if message == "3":
            s.close()
            break
        try:
            s.send(message.encode())
        except:
            print("Connection lost")
            break

def Listening(s):
    while True:
        data = s.recv(1024)
        if data:
            message = data.decode()
            print("\nRecived: ", message)
            print("> ", end="", flush=True)
        else:
            break

def get_ip(arg):
    return input(arg)
def get_port():
    while True:
        try:
            PORT = int(input("Enter PORT(0-65535): "))
            if (0 <= PORT <= 65535):
                break
            print("Wrong port range!")
        except:
            print("Not a number!")
    return PORT

while True:
    print("[0]Settings")
    print("[1]Listening")
    print("[2]Seek")
    print("[3]Exit")

    command = input("> ")

    if command == "0":
        print("[0]Client")
        print("[1]Server")
        print("[2]Check Settings")

        command = input("> ")

        if command == "0":
            clientIP = get_ip("Enter IP: ")
            clientPORT = get_port()
        elif command == "1":
            serverIP = get_ip("Enter IP: ")
            serverPORT = get_port()
        elif command == "2":
            print("Client socket: " + clientIP + ":" + str(clientPORT))
            print("Server socket: " + serverIP + ":" + str(serverPORT))
    elif command == "1":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Listening...")
        try:
            s.bind((serverIP, serverPORT))
        except:
            print("Error, please check your server settings")
            continue
        s.listen(1)
        s.settimeout(5)
        try:
            con, addr = s.accept()
        except socket.timeout:
            print("No founded")
            s.close()
            continue
        print("Connected!")

        thread1 = threading.Thread(target=Response, args=(con,))
        thread2 = threading.Thread(target=Listening, args=(con,))
        thread1.start()
        thread2.start()


    elif command == "2":
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connect...")
        try:
            s.connect((clientIP, clientPORT))
        except:
            print("Error, please check your client settings")
            continue
        thread1 = threading.Thread(target=Response,args=(s,))
        thread2 = threading.Thread(target=Listening,args=(s,))
        thread1.start()
        thread2.start()
    elif command == "3":
        break



