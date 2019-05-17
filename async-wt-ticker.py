#!/usr/bin/env python
import cProfile

import asyncio
import logging
import time

from websocket import create_connection as wss
import websocket

from json import dumps as json_dumps
from json import loads as json_loads
from config import MAX_ITER, node_url

logger = logging.getLogger(__name__)
is_alive = True


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
    # not really async because no await
    print("inside websocket")
    count = 1
    while count < MAX_ITER:
        try:
            start = time.time()
            query = wss_send_ticker()
            await ws.send(query)
            message = wss_receive()
            print(message)
            end = time.time()
            print("Total time: {} \n".format(end - start))
            count += 1
        except websocket._exceptions.WebSocketBadStatusException:            
            print('ConnectionClosed')
            is_alive = False
            break
        

async def ticker():
    try:
        wss_handshake(node_url)
        query = wss_send_ticker()
        await ws.send(query)
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
   

def run_tests():
    single_test()
    print("----------------\n")
#    loop_test()
    
    
if __name__ == "__main__":
    cProfile.run('run_tests()', 'websocket-stats')
    



