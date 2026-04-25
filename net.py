import crypt

import asyncio
import datetime

async def ENCRYPT(writer, command):
    writer.write((command + "\n").encode())
    await writer.drain()

    return 1

async def history(message, sender):
    with open("history.txt", "a", encoding="utf-8") as file:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"[{time}] {sender}: {message}\n")

async def chat(reader, writer, cryptography_command,isHistory):
    stop_event = asyncio.Event()

    write_task = asyncio.create_task(writing(writer, stop_event, cryptography_command, isHistory))
    read_task = asyncio.create_task(reading(reader, stop_event, cryptography_command, isHistory))

    await stop_event.wait()

    for task in (write_task, read_task):
        task.cancel()

    await asyncio.gather(write_task, read_task, return_exceptions=True)

    writer.close()
    await writer.wait_closed()


async def reading(reader, stop_event, cryptography_command, isHistory):
    while not stop_event.is_set():
        data = await reader.readline()

        if not data:
            print("\nPeer disconnected, please press ENTER to return menu")
            stop_event.set()
            break
        msg = data.decode().rstrip('\n')
        if msg in ['DO ENCRYPT','CAN`T ENCRYPT','PASS ENCRYPT']: continue
        print(f"\rPeer: {msg}\nYou: ", end="", flush=True)

        if msg == "exit":
            print("\nPeer disconnected, please press ENTER to return menu")
            stop_event.set()
            break

        if isHistory:
            await history(msg, "Peer")

async def writing(writer, stop_event, cryptography_command, isHistory):
    await ENCRYPT(writer, cryptography_command)

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

            if isHistory:
                await history(msg, "You")

    except asyncio.CancelledError:
        pass
    except (ConnectionResetError, BrokenPipeError):
        print("\nConnection lost")
        stop_event.set()

async def listen(selfIP, cryptography_command, isHistory):
    print("Listening..")

    chat_finished = asyncio.Event()

    async def one_client_handler(reader, writer):
        print("Connected!")
        await chat(reader, writer, cryptography_command, isHistory)
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

async def seek(targetIP, cryptography_command, isHistory):
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
    await chat(reader, writer, cryptography_command, isHistory)

    return True
