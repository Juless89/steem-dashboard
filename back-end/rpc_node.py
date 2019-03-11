import urllib3
import time
import threading
import json
import database

from datetime import datetime

current_block = None
urllib3.disable_warnings()

# Sorter thread takes in all blocks from the gathering threads, sorts them
# in order and passes them on to be processed
class Sorter(threading.Thread):
    def __init__(self, num, queue, lock, blocks, blocks_lock,
                 blocks_queue, blocks_queue_lock, n, end):
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
        self.workers = []
        self.end = end

    def run(self):
        global current_block

        while True:
            try:
                # as long as there are blocks in the queue, pop each 
                # block from the queue and sort into the buffer
                if len(self.queue) > 0:
                    try:
                        self.lock.acquire()
                        while len(self.queue) > 0:
                            block = self.queue.pop()
                            block_num = block['block_num']
                            data = block['data']

                            self.buffer[block_num] = data
                    except Exception as e:
                        print()
                        print('failed to load data')
                        print(e)
                    finally:
                        self.lock.release()

                # check for blocks in the buffer and the current length of the 
                # blocks queue. If there is room check for the current block
                # to pop from the buffer into the work queue
                if len(self.buffer) > 0:
                    try:
                        loop = 1
                        while loop:
                            if self.num in self.buffer:
                                block = self.buffer[self.num]
                                block['block_num'] = self.num
                                del self.buffer[self.num]

                                try:
                                    self.blocks_queue_lock.acquire()
                                    self.blocks_queue.append(block)
                                    self.num += 1
                                    current_block += 1
                                finally:
                                    self.blocks_queue_lock.release()
                            else:
                                loop = 0
                    except Exception as e:
                        print()
                        print('failed to pop block')
                        print(e)
                        continue
            except Exception as e:
                print()
                print('Sorter failed')
            time.sleep(0.05)


# Block gathering thread
class Blocks(threading.Thread):
    def __init__(self, id, n, base, end, queue, lock):
        threading.Thread.__init__(self)
        self.id = id
        self.queue = queue
        self.lock = lock
        self.n = n
        self.base = base
        self.end = end
        self.num = self.base - 1 + self.id
        self.db = database.Database()
        self.http = urllib3.PoolManager()

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
            r = self.http.request('POST', url, body=json.dumps(PARAMS).encode())

            data = json.loads(r.data.decode())

            # Empty result for blocks that do not exist yet, wait 2 seconds,
            # new block time is 3 seconds.
            if len(data['result']) == 0:
                time.sleep(2)
                return None
            return data
        except Exception:
            return None

    # Add block to the queue, store block number and block data
    def add_block(self, data, block_num):
        loop = 1

        while loop:
            try:
                self.lock.acquire()
                self.queue.append({
                    "block_num": block_num,
                    "data": data['result']['block'],
                })
                loop = 0
            except Exception as e:
                print()
                print('Failed to add block')
                print(e)
            finally:
                self.lock.release()

    # Keep getting blocks as long as the difference in amount of blocks with
    # the slowest thread is not greater than 5, also as long as the total
    # queue length does not exceed 320
    def run(self):
        global current_block
        while self.num <= self.end:
            try:
                if self.num <= current_block + self.n * 10:
                    try:
                        # retrieve block via api
                        data = self.get_block(self.num)
                        try:
                            if data:
                                # add block to queue and update block counter
                                self.add_block(data, self.num)
                                self.num += self.n
                        except Exception as e:
                            print()
                            print('Failed to add block', e)
                        time.sleep(0.20)
                    except Exception as e:
                        print()
                        print('Failed to get block', e)
                        time.sleep(1)
                else:
                    time.sleep(1)
            except Exception as e:
                print()
                print('Worker thread died, get back to work', e)



# Main thread used to manage all block gathering threads and the sorter.
class RPC_node(threading.Thread):
    def __init__(self, start, block_count, blocks_queue, blocks_queue_lock,
                 amount_of_threads=1):
        threading.Thread.__init__(self)
        self.begin = start
        self.end = start + block_count
        self.block_count = block_count
        self.blocks = []
        self.blocks_lock = threading.Lock()
        self.blocks_queue = blocks_queue
        self.blocks_queue_lock = blocks_queue_lock
        self.n = amount_of_threads

    def run(self):
        # shared blocks queue
        lock = threading.Lock()
        queue = []
        threads = []

        global current_block
        current_block = self.begin

        # create, start and store all block gathering threads
        for x in range(1, self.n+1):
            thread = Blocks(
                x, self.n, self.begin, self.end,
                queue, lock)
            thread.start()
            threads.append(thread)

        # create and start the sorter thread
        sorter = Sorter(
            self.begin, queue, lock, self.blocks, self.blocks_lock,
            self.blocks_queue, self.blocks_queue_lock, self.n, self.end)
        sorter.start()

        while True:
            time.sleep(5)
