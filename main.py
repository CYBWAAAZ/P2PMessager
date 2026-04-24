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

print('\nLocal P2P Messenger edition v1.0')

def close_app():
    print("Process is down")
    return 0


async def chat(reader, writer):
    stop_event = asyncio.Event()

    write_task = asyncio.create_task(writing(writer, stop_event))
    read_task = asyncio.create_task(reading(reader, stop_event))

    await stop_event.wait()

    for task in (write_task, read_task):
        task.cancel()

    await asyncio.gather(write_task, read_task, return_exceptions=True)

    writer.close()
    await writer.wait_closed()


async def reading(reader, stop_event):
    while not stop_event.is_set():
        data = await reader.readline()

        if not data:
            print("\nPeer disconnected, please press ENTER to return menu")
            stop_event.set()
            break

        msg = data.decode().rstrip('\n')
        print(f"\rPeer: {msg}\nYou: ", end="", flush=True)

        if msg == "exit":
            print("\nPeer disconnected, please press ENTER to return menu")
            stop_event.set()
            break


async def writing(writer, stop_event):
    try:
        while not stop_event.is_set():
            msg = await asyncio.to_thread(input, "You: ")

            if stop_event.is_set():
                break

            writer.write((msg + "\n").encode())
            await writer.drain()

            if msg == "exit":
                stop_event.set()
                break

    except asyncio.CancelledError:
        pass
    except (ConnectionResetError, BrokenPipeError):
        print("\nConnection lost")
        stop_event.set()

async def handler(reader, writer):
    print("Connected!")
    await chat(reader, writer)

async def listen():
    print("Listening..")

    chat_finished = asyncio.Event()

    async def one_client_handler(reader, writer):
        print("Connected!")
        await chat(reader, writer)
        chat_finished.set()

    try:
        server = await asyncio.wait_for(
            asyncio.start_server(one_client_handler, selfIP, 48777),
            timeout=5
        )
    except (asyncio.TimeoutError, OSError):
        print("⚠️ Error, please check your settings")
        return True

    async with server:
        await chat_finished.wait()

    return True

async def seek():
    print("Seeking..")
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(targetIP, 48777),
            timeout=5
        )
    except (asyncio.TimeoutError, OSError):
        print("⚠️ Error, please check your settings")
        return True

    print("Connected!")
    await chat(reader, writer)

    return True

def credits():
    print("P2P Messenger created by CYBWAAAZ")
    return 1

def print_options():
   print('[0]Сlose app\n[1]Listen\n[2]Seek\n[3]Credits')

commands = {
    0: close_app,
    1: listen,
    2: seek,
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

    if inspect.iscoroutinefunction(action):
        live = asyncio.run(action())
    else:
        live = action()

    if live is not False and live != 0:
        live = True



