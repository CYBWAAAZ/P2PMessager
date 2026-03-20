import socket

s = socket.socket()

print("Welcome to P2PMessenger v0.1")
print("Type a number for use action:")
print("[1]Settings")
print("[2]Listening")
print("[3]Seek")
print("[4]Exit")

targetIP = "192.168.0.208"
targetPORT = 6666

myIP = "192.168.0.170"
myPORT = 6666

def Established(con):
    print("Estabilshed")
    while True:
        message = input("> ")
        if message == "0":
            main()
            break
        con.send(message.encode())
        data = con.recv(1024)  # получаем данные с сервера
        message = data.decode()  # преобразуем байты в строку
        print(f"Client sent: {message}")

def Established_c(con):
    print("Estabilshed")
    while True:
        message = input("> ")
        if int(message) == 0:
            main()
            break
        s.send(message.encode())
        data = s.recv(1024)  # получаем данные с сервера
        print("Server sent: ", data.decode())


def main():
    while True:
        command = int(input("> "))
        if command == 1:
            print("---Settings---")
            targetIP = input("Enter ip: ")
            targetPORT = int(input("Enter port: "))

        elif command == 4:
            print("See you again")
            break
        elif command == 2:
            print("[1]Auto")
            print("[2]Manual")
            command = int(input("> "))
            if command == 1:
                myIP = socket.gethostname()
                myPORT = 6666

            else:
                myIP = input("Enter ip: ")
                myPORT = input("Enter port: ")
            print(myIP)
            s.bind((myIP, int(myPORT)))
            s.listen(1)
            print("Listening...")
            con, addr = s.accept()
            Established(con)
            break
        elif command == 3:
            print("Seeking...")
            s.connect((targetIP,targetPORT))
            Established_c(s)
            break
main()