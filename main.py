import net
import asyncio
import inspect

Debugging = False
print("———Settings———")

if Debugging:
    print("Pass")
    selfIP = "192.168.0.170"
    targetIP = "192.168.0.147"
else:
    selfIP = input("Please, write your ip adress: ")
    targetIP = input("Please, write target ip adress: ")

print('\nLocal P2P Messenger edition v1.1')

def close_app():
    print("Process is down")
    return 0


def credits():
    print("P2P Messenger created by CYBWAAAZ")
    return 1

def print_options():
   print('[0]Сlose app\n[1]Listen\n[2]Seek\n[3]Credits')

commands = {
    0: close_app,
    1: lambda: net.listen(selfIP),
    2: lambda: net.seek(targetIP),
    3: credits
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

    if live is not False:
        live = True



