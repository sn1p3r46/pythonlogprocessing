#!/usr/bin/python3.5

import pathBuilder as pb
import websockets
import asyncio

server_address = 'ws://localhost:8888'


async def hello():
    async with websockets.connect(server_address) as websocket:
        for fp in pb.PathBuilder.get_stream_files_paths():
            # for fp in ['/media/andre/HDD/TkData/sorted/filtered_null_and_empty/test_file.txt']:
            with open(fp, 'r') as fd:
                i = 0
                for log in fd:
                    i += 1
                    if i % 1000000 == 0:
                        print("{}".format(i), end='\r')
                    await websocket.send(log)

        websocket.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello())
