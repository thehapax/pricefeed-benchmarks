#!/usr/bin/env python
import asyncio
import logging
import time  
import websockets

from websocket import create_connection as wss
import websocket

from json import dumps as json_dumps
from json import loads as json_loads

logger = logging.getLogger(__name__)
is_alive = True
node_url = "wss://api.fr.bitsharesdex.com/ws" 
#url = "wss://echo.websocket.org/"

def wss_handshake(node):
    global ws
    print(node)
    ws = wss(node, timeout=5)


def wss_send(params):
    query = json_dumps(
        {"method": "call", "params": params, "jsonrpc": "2.0", "id": 1}
    )
    print(query)
    return query
#    ws.send(query)


def wss_receive():
    ret = json_loads(ws.recv())
    try:
        return ret["result"]  # if there is result key take it
    except:
        return ret


def wss_send_ticker():
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
    return ret



async def alive():
    while is_alive:
        logger.info('alive')
        print("alive")
        await asyncio.sleep(1) #300


async def async_processing():
    print("inside async websockets")
    while True:
        try:
            start = time.time()
            query = wss_send_ticker()
            ws.send(query)
            message = wss_receive()
            print(message)
            end = time.time()
            print("Total time: {} \n".format(end - start))
        except websocket._exceptions.WebSocketBadStatusException:            
            print('ConnectionClosed')
            is_alive = False
            break
        

async def ticker():
    try:
        wss_handshake(node_url)
        query = wss_send_ticker()
        ws.send(query)
        response =  ws.recv()
        ret = json_loads(response)
        print(ret["result"])
    except Exception as e:
        print(e)
        print('ConnectionClosed')


def loop_test():
    wss_handshake(node_url)
    tasks = [
        asyncio.ensure_future(async_processing())
    ]
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
        

def single_test():
    start = time.time()    
    asyncio.get_event_loop().run_until_complete(ticker())
    end = time.time()
    print("Total time: {}".format(end - start)) 
   

if __name__ == "__main__":

    single_test()
    print("----------------\n")
    loop_test()



