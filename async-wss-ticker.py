#!/usr/bin/env python
# original source : https://github.com/aaugustin/websockets/blob/master/example/secure_client.py
# https://github.com/aaugustin/websockets
# the only library to handle backpressure correctly

import asyncio
import pathlib
import ssl
import websockets
from json import dumps as json_dumps
from json import loads as json_loads

import time
from config import MAX_ITER, node_url

ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)

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


def wss_send(params):
    query = json_dumps(
        {"method": "call", "params": params, "jsonrpc": "2.0", "id": 1}
    )
    print(query)
    return query


async def ticker():
    async with websockets.connect(node_url, ssl=ssl_context) as websocket:
        query = wss_send_ticker()
        await websocket.send(query)
        response = await websocket.recv()
        ret = json_loads(response)
        print(ret["result"])


async def ticker_loop():
    async with websockets.connect(node_url, ssl=ssl_context) as websocket:
        count = 1
        total_time = 0
        while count < MAX_ITER:
            try:
                start = time.time()
                query = wss_send_ticker()
                await websocket.send(query)
                response = await websocket.recv()
                ret = json_loads(response)
                print(ret["result"])
                end = time.time()
                runtime = end -start
                print("Total time: {} \n".format(runtime))
                count += 1
                total_time += runtime                
            except Exception as e:
                print('Connection Closed' + e)
                is_alive = False
                break;
        return total_time
    
    
def loop_test():
    total_time = asyncio.get_event_loop().run_until_complete(ticker_loop())
    return total_time

    
def single_test():
    start = time.time()
    asyncio.get_event_loop().run_until_complete(ticker())
    end = time.time()
    print("Total time: {}".format(end - start))
        

    
if __name__ == "__main__":

    single_test()
    print("----------------\n")
    print("----------------\n")
    total_time = loop_test()
    average_time = total_time/MAX_ITER
    print("\n\nAverage Run Time: {} \n".format(average_time))
