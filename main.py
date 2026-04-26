from core import net
import asyncio
import inspect

Debugging = False

cryptography_command = 'CAN`T ENCRYPT'
isHistory = 1

print("———Settings———")

if Debugging:
    print("Pass")
    selfIP = "192.168.0.170"
    targetIP = "192.168.0.147"
else:
    selfIP = input("Please, write your ip adress: ")
    targetIP = input("Please, write target ip adress: ")

print('\nLocal P2P Messenger Standard-edition v1.3')

def close_app():
    print("Process is down")
    return 0

def credits():
    print("P2P Messenger created by CYBWAAAZ")
    return 1

def settings():
    global cryptography_command, isHistory
    while True:
        print("\n———Advanced settings———")
        print('[0]Return to menu\n[1]Enable/Disable Encryption\n[2]Enable/Disable history\n')

        try:
            command = int(input('> '))
        except ValueError:
            print("Enter the number")
            continue
        if command == 1:
            if cryptography_command != 'CAN`T ENCRYPT' and cryptography_command == 'PASS ENCRYPT':
                cryptography_command = 'DO ENCRYPT'
                print("✅ Encryption has enabled!")
            elif cryptography_command != 'CAN`T ENCRYPT' and cryptography_command == 'DO ENCRYPT':
                cryptography_command = 'PASS ENCRYPT'
                print("🚫 Encryption has disabled!")
            else:
                print("⚠️ Encryption does not work in this version")
        elif command == 2:
            if isHistory:
                isHistory = 0
                print("🚫 History has disabled")
            else:
                isHistory = 1
                print("✅ History has enabled!")
        elif command == 0:
            break

    print('\nLocal P2P Messenger edition v1.2')

def print_options():
   print('[0]Сlose app\n[1]Listen\n[2]Seek\n[3]Credits\n[4]Settings\n')

commands = {
    0: close_app,
    1: lambda: net.listen(selfIP, cryptography_command, isHistory),
    2: lambda: net.seek(targetIP, cryptography_command, isHistory),
    3: credits,
    4: settings
}

live = True

while live:
    print_options()

    try:
        command = int(input('> '))
    except ValueError:
        print("Enter the number")
        continue

    action = commands.get(command)

    if action is None:
        print("Unknown command")
        continue

    result = action()

    if inspect.isawaitable(result):
        live = asyncio.run(result)
    else:
        live = result

    if live != 0:
        live = True



