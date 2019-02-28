import urllib.request
import urllib.parse
import time
import threading
import json


# Sorter thread takes in all blocks from the gathering threads, sorts them
# in order and passes them on to be processed
class Sorter(threading.Thread):
    def __init__(self, num, queue, lock, blocks, blocks_lock,
                blocks_queue, blocks_queue_lock, n):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.blocks = blocks
        self.blocks_lock = blocks_lock
        self.blocks_queue = blocks_queue
        self.blocks_queue_lock = blocks_queue_lock
        self.num = num
        self.n = n
        self.buffer = {}

    def run(self):
        while True:
            if len(self.queue) > 0:
                try:
                    self.lock.acquire()
                    while len(self.queue) > 0:
                        block = self.queue.pop()
                        block_num = block['block_num']
                        data = block['data']

                        self.buffer[block_num] = data
                finally:
                    self.lock.release()

            if len(self.buffer) > 0 and len(self.blocks_queue) <= 5*self.n:
                try:
                    block = self.buffer.pop(self.num+1, None)
                    while block is not None:
                        try:
                            self.blocks_queue_lock.acquire()
                            block['block_num'] = self.num+1
                            self.blocks_queue.append(block)
                            self.num += 1
                            block = self.buffer.pop(self.num+1, None)
                        finally:
                            self.blocks_queue_lock.release()
                except Exception as e:
                    print(e)
                    continue

            time.sleep(0.05)


# Block gathering thread
class Blocks(threading.Thread):
    def __init__(self, id, n, base, queue, lock, ready):
        threading.Thread.__init__(self)
        self.id = id
        self.queue = queue
        self.lock = lock
        self.n = n
        self.base = base
        self.ready = ready
        self.end = self.base + 247462
        self.num = self.base + self.id

    # Perform API call to get block return None for non existing blocks and
    # any exceptions.
    def get_block(self, block_num):
        # API request
        PARAMS = {
            "jsonrpc": "2.0",
            "method": "block_api.get_block",
            "params": {"block_num": block_num},
            "id": 1
        }
        url = 'https://api.steemit.com/'

        try:
            # perform and decode request
            post_response = urllib.request.urlopen(
                url=url,
                data=json.dumps(PARAMS).encode()
            )
            data = json.loads(post_response.read().decode())

            # Empty result for blocks that do not exist yet, wait 2 seconds,
            # new block time is 3 seconds.
            if len(data['result']) == 0:
                time.sleep(2)
                return None
            return data
        except Exception:
            return None

    # Add block to the queue, store block number and block data
    def add_block(self, data):
        try:
            self.lock.acquire()
            self.queue.append({
                "block_num": self.num,
                "data": data['result']['block'],
            })
        finally:
            self.lock.release()

    # Keep getting blocks as long as the difference in amount of blocks with
    # the slowest thread is not greater than 5, also as long as the total
    # queue length does not exceed 320
    def run(self):
        while True:
            if (self.ready[self.id-1] < min(self.ready) + 5 and
                    len(self.queue) <= 5*self.n):
                try:
                    # retrieve block via api
                    data = self.get_block(self.num)
                    try:
                        if data:
                            # add block to queue and update block counter
                            self.add_block(data)
                            self.ready[self.id-1] += 1
                            self.num += self.n
                    except Exception as e:
                        print('add_block', e)
                    time.sleep(0.10)
                except Exception as e:
                    print(e)
                    time.sleep(1)
            else:
                time.sleep(0.1)


# Main thread used to manage all block gathering threads and the sorter.
class RPC_node(threading.Thread):
    def __init__(self, start, blocks_queue, blocks_queue_lock,
                amount_of_threads=1):
        threading.Thread.__init__(self)
        self.begin = start
        self.blocks = []
        self.blocks_lock = threading.Lock()
        self.blocks_queue = blocks_queue
        self.blocks_queue_lock = blocks_queue_lock
        self.n = amount_of_threads
        self.ready = [0 for x in range(0, self.n)]
        self.ready_lock = threading.Lock()

    def run(self):
        # shared blocks queue
        lock = threading.Lock()
        queue = []
        threads = []

        # create, start and store all block gathering threads
        for x in range(1, self.n+1):
            thread = Blocks(x, self.n, self.begin, queue, lock, self.ready)
            thread.start()
            threads.append(thread)

        # create and start the sorter thread
        sorter = Sorter(
            self.begin, queue, lock, self.blocks, self.blocks_lock,
            self.blocks_queue, self.blocks_queue_lock, self.n)
        sorter.start()

        while True:
            time.sleep(5)