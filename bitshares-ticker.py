import asyncio
from bitshares.bitshares import BitShares
from bitshares.market import Market
import time, os


TEST_CONFIG = {
    'node': 'wss://api.fr.bitsharesdex.com/ws'
}
# User needs to put a key in
KEYS = [os.environ['DEXBOT_TEST_WIF']]


async def ticker_test():
    start = time.time()
    bitshares = BitShares(node=TEST_CONFIG['node'], keys=KEYS)

    market = Market('OPEN.BTC:BTS', bitshares_instance=bitshares)
    ticker = market.ticker()
    print(ticker)

    end = time.time()
    print("Total time: {}".format(end - start))

    
def loop_test():
    bitshares = BitShares(node=TEST_CONFIG['node'], keys=KEYS)
    market = Market('OPEN.BTC:BTS', bitshares_instance=bitshares)
    while True:
        try:
            start = time.time()

            ticker = market.ticker()
            print(ticker)

            end = time.time()
            print("Total time: {}".format(end - start))
            
        except Exception as e:
            print(e)
            print('Connection Closed')
            break

        

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(ticker_test())
    single_test()
    print("----------------\n")    
    print("----------------\n")
    loop_test()
