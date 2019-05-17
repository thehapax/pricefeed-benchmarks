# pricefeed-benchmarks

Here you will find some benchmark speed tests for single and multple price queries to a bitshares
nodes using websocket, websockets, and pybitshares. 

<ul>
Websockets
<li> Source: https://github.com/aaugustin/websockets/tree/master/example

`$python3 async-wss-ticker.py`
</ul>

<ul>
Websocket client
<li> Source: https://github.com/websocket-client/websocket-client

`$python3 async-wt-ticker.py`
</ul>

<ul>
Bitshares module
<li> Source: https://github.com/bitshares/python-bitshares

`$python3 bitshares-ticker.py`
</ul>

<ul>
UV loop module makes asyncio 2-4x faster. appears to be effective the greater the number of requests per second. 
<li> Source: https://github.com/MagicStack/uvloop

`$python3 uvloop-wss.py`
</ul>

<ul>To view stats, Install snakeviz

`$pip install snakeviz`

`$snakeviz <<file generated from running python script>>`


