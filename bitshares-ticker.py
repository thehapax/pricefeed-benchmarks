from bitshares.bitshares import BitShares
from bitshares.market import Market
import time, os
from config import MAX_ITER, node_url


TEST_CONFIG = {
    'node': node_url
}
# User needs to put a key in
KEYS = [os.environ['DEXBOT_TEST_WIF']]


def ticker_test():
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
    count = 1
    total_time = 0
    while count < MAX_ITER:
        try:
            start = time.time()

            ticker = market.ticker()
            print(ticker)

            end = time.time()
            runtime = end -start
            print("Total time: {}".format(runtime))

            count +=1
            total_time += runtime
        except Exception as e:
            print(e)
            print('Connection Closed')
            break
    return total_time
        

if __name__ == "__main__":
    ticker_test()
    print("----------------\n")    
    print("----------------\n")
    total_time = loop_test()

    average_time = total_time/MAX_ITER
    print("\n\nAverage Run Time: {} \n".format(average_time))
