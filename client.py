print("start client 0.3(websocket)")

import asyncio
#from formats import parse,display_parse
#from pprint import pprint
#import sys

#import h11

from config import xi_host,xi_port,local_host,local_port

from utils import socket_to_websocket,websocket_to_socket

import websockets

xi_addr = 'ws://' + xi_host + ':' + str(xi_port) # i.e. 'ws://localhost:8765'

print('target server addr', xi_addr)

async def listener(reader, writer):
    try:
        
        async with websockets.connect(xi_addr) as websocket:
            
            pipe1 = socket_to_websocket(reader, websocket)
            pipe2 = websocket_to_socket(websocket, writer)
            await asyncio.gather(pipe1, pipe2)
    finally:
        print("writer.close()")
        writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(listener, local_host, local_port, loop = loop)
server = loop.run_until_complete(coro)

print('Serving on',server.sockets[0].getsockname())
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()