from websocket import create_connection as wss  # handshake to node
import asyncio
import time
from json import dumps as json_dumps
from json import loads as json_loads

# original source from litepresence, ticker.py
# uses websocket client, not websockets
# https://github.com/websocket-client/websocket-client

def public_nodes():
    # live since core 181127 and known to have market history
    return [
        "wss://altcap.io/wss",
        "wss://api-ru.bts.blckchnd.com/ws",
        "wss://api.bitshares.bhuz.info/wss",
        "wss://api.bitsharesdex.com/ws",
        "wss://api.bts.ai/ws",
        "wss://api.bts.blckchnd.com/wss",
        "wss://api.bts.mobi/wss",
        "wss://api.bts.network/wss",
        "wss://api.btsgo.net/ws",
        "wss://api.btsxchng.com/wss",
        "wss://api.dex.trading/ws",
        "wss://api.fr.bitsharesdex.com/ws"
        ]


def wss_handshake(node):
    global ws
    print(node)
    ws = wss(node, timeout=5)


def wss_send(params):
    query = json_dumps(
        {"method": "call", "params": params, "jsonrpc": "2.0", "id": 1}
    )
    ws.send(query)


def wss_receive():
    ret = json_loads(ws.recv())
    try:
        return ret["result"]  # if there is result key take it
    except:
        return ret


def rpc_ticker():
    ret = wss_send(
        [
            "database",
            "get_ticker",
            [
                "OPEN.BTC",
                "BTS",
                True
            ]
        ]
    )

    
if __name__ == "__main__":
    start = time.time()

    node = public_nodes()[11]
    wss_handshake(node)
    rpc_ticker()
    ticker = wss_receive()
    print(ticker)

    end = time.time()  
    print("Total time: {}".format(end - start))
