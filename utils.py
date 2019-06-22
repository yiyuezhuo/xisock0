import asyncio
import h11
from config import timeout

async def recv_http_websocket(websocket):
    data = b''
    event_list = []
    conn = h11.Connection(h11.SERVER)
    while True:
        event = conn.next_event()
        if event is h11.NEED_DATA:
            #dat = await asyncio.wait_for(websocket.recv(2048), timeout=timeout)
            dat = await asyncio.wait_for(websocket.recv(), timeout=timeout)
            data += dat
            conn.receive_data(dat)
        elif event == h11.EndOfMessage():
            break
        elif event == h11.ConnectionClosed():
            print("ConnectionClosed detected")
            break
        else:
            event_list.append(event)

    return event_list, data

def parse_request(event_list):
    '''
Request(method=b'CONNECT', target=b'tiles.services.mozilla.com:443', headers=[(b'user-agent', b'Mozilla/5.0 (Windows NT
10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'), (b'proxy-connection', b'keep-alive'), (b'connection', b'keep-alive'), (b'host', b'tiles.services.mozilla.com:443')], http_version=b'1.1')
NEED_DATA
Request(method=b'GET', target=b'http://detectportal.firefox.com/success.txt', 
headers=[(b'host', b'detectportal.firefox.com'), 
(b'user-agent', b'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'), 
(b'accept', b'*/*'), (b'accept-language', b'en-US,en;q=0.5'), (b'accept-encoding', b'gzip, deflate'), 
(b'cache-control', b'no-cache'), (b'pragma', b'no-cache'), (b'connection', b'keep-alive')], 
http_version=b'1.1')
NEED_DATA
    '''
    request = {'method':None, 'target':None, 'headers':{}, 'data':b'',
                'host':None, 'port':None}
    for event in event_list:

        if hasattr(event, 'method'):
            request['method'] = event.method #event['method']
            request['target'] = event.target #event['target']
            for key,value in event.headers:
                request['headers'][key] = value
        elif isinstance(event, h11.Data):
            request['data'] += bytes(event['data'])
        else:
            print(event)
            #import pdb;pdb.set_trace()
            raise Exception("Unknown event")

        #import pdb;pdb.set_trace()
    
    if request['method'] == b'CONNECT':
        request['host'], request['port'] = request['headers'][b'host'].split(b':')
        request['host'] = request['host'].strip()
        request['port'] = int(request['port'])
    elif request['method'] == b'GET':
        request['host'] = request['request'][b'host'].strip()
        request['port'] = 80
    else:
        raise Exception("Unknown arg")

    return request

async def socket_to_websocket(reader, websocket):
    try:
        while not reader.at_eof():
            data = await reader.read(2048)
            print('browser_to_xi read:', len(data), data[:10])
            await websocket.send(data)
    finally:
        websocket.close()

async def websocket_to_socket(websocket, writer):
    while True:
        data = await websocket.recv() # default size? A pdb.set_trace to check will be useful.
        print('xi_to_browser recv:', len(data), data[:10])
        writer.write(data)
        await writer.drain()
