# A prototype proxy server using websocket and CDN

My ip of bandwagon server running shadowsocks is blocked by GFW.
So I write the tool to connect the server again.

## Usage

* install `h11` and `websockets` modules.
* clone the project into your local and remote server(if ssh is blocked, use command line provided by VPS provider)
* In `config.py`, replace `xi_host = '127.0.0.1'` with `xi_host = 'your_host_name.xyz'`
* `python3 server.py` in remote server
* `python3 client.py` in local.
* config `SwithcyOmega` or global proxy setting in your browser. 