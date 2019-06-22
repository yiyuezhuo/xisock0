print('start server (websocket)')

import asyncio
import websockets
#from websocket_utils import WebsocketReader,WebsocketWriter

from pprint import pprint

from config import xi_host,xi_port,local_host,local_port,xi_local_host,timeout

#from common import read_request,read_response,parse_request,parse_data

import h11

from utils import parse_request,socket_to_websocket,websocket_to_socket,recv_http_websocket

async def listener(websocket, path):
    print('start server listener:',websocket, path)

    event_list, data = await recv_http_websocket(websocket)
    print('recv_http_websocket:', event_list, data)
    request = parse_request(event_list)

    remote_reader, remote_writer = await asyncio.open_connection(request['host'], request['port'])

    if request['method'] == b'CONNECT':
        await websocket.send(b'HTTP/1.0 200 Connection Established\r\nProxy-agent: Pyx\r\n\r\n')
    else:
        remote_writer.write(data)
        await remote_writer.drain()

    pipe1 = socket_to_websocket(remote_reader, websocket)
    pipe2 = websocket_to_socket(websocket, remote_writer)
    await asyncio.gather(pipe1, pipe2)

print('Serving on:', xi_local_host, xi_port)

start_server = websockets.serve(listener, xi_local_host, xi_port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
