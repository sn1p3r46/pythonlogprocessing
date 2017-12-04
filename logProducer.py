#!/usr/bin/python3

import pathBuilder as pb
import websockets
import asyncio
import time

server_address = 'ws://localhost:8888'


async def hello():
    async with websockets.connect(server_address) as websocket:
        for fp in pb.PathBuilder.get_stream_files_paths():
            with open(fp, 'r') as fd:
                for log in [fd.readline() for i in range(2)]:
                    print(log.strip())
                    await websocket.send(log)
        websocket.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello())
