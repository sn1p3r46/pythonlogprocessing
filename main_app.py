#!/usr/bin/python3.5

import asyncio
import websockets
import logProcessor as lp
import pathBuilder as pb


async def echo(websocket, path):
    while True:
        try:
            msg = await websocket.recv()
            LP.log_digest(msg.strip())
        except Exception:
            LP.persist()
            asyncio.get_event_loop().stop()

if __name__ == '__main__':

    LP = lp.LogProcessor(pb.PathBuilder)
    start_server = websockets.serve(echo, '127.0.0.1', 8888)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
