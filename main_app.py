#!/usr/bin/python3.5

import asyncio
import websockets
import logProcessor as lp
import pathBuilder as pb
from datetime import datetime

# async def echo(websocket, path):
#     while True:
#         try:
#             msg = await websocket.recv()
#             LP.log_digest(msg.strip())
#         except Exception:
#             LP.persist()
#             asyncio.get_event_loop().stop()
#
# if __name__ == '__main__':
#
#     LP = lp.LogProcessor(pb.PathBuilder)
#     start_server = websockets.serve(echo, '127.0.0.1', 8888)
#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()

LP = lp.LogProcessor(pb.PathBuilder)
for fp in pb.PathBuilder.get_stream_files_paths():
    t0 = datetime.now()
    with open(fp, 'r') as fd:
        i = 0
        for log in fd:
            i += 1
            if i % 1000000 == 0:
                print("{}".format(i), end='\r')
            LP.log_digest(log.strip())
    t1 = datetime.now()
    print("Elapsed: {}".format(t1-t0))
LP.persist()
