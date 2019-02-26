import requests
import time
import threading
import json

from datetime import datetime


class Sorter(threading.Thread):
    def __init__(self, num, queue, lock, blocks, blocks_lock,
                 blocks_queue, blocks_queue_lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock = lock
        self.blocks = blocks
        self.blocks_lock = blocks_lock
        self.blocks_queue = blocks_queue
        self.blocks_queue_lock = blocks_queue_lock
        self.num = num
        self.buffer = {}
        self.counter = 0
        self.s_time = datetime.now()

    def run(self):
        while True:
            # print('buffer: ', len(self.buffer))
            # print('queue: ', len(self.queue))

            if len(self.queue) > 0 and len(self.buffer) < 10:
                try:
                    self.lock.acquire()
                    while len(self.queue) > 0:
                        block = self.queue.pop()
                        block_num = block['block_num']
                        data = block['data']

                        self.buffer[block_num] = data
                finally:
                    self.lock.release()

            if len(self.buffer) > 0:
                try:
                    block = self.buffer.pop(self.num+1, None)
                    while block is not None:
                        try:
                            self.blocks_queue_lock.acquire()
                            block['block_num'] = self.num+1
                            self.blocks_queue.append(block)
                            # print(len(self.blocks))
                            self.counter += 1
                            self.num += 1
                            block = self.buffer.pop(self.num+1, None)
                        finally:
                            self.blocks_queue_lock.release()
                except Exception as e:
                    print(e)
                    continue

            # speed counter
            c_time = datetime.now()
            if (c_time-self.s_time).total_seconds() > 5:
                self.counter = 0
                self.s_time = c_time

            time.sleep(0.05)


class Blocks(threading.Thread):
    def __init__(self, id, n, base, queue, lock, ready):
        threading.Thread.__init__(self)
        self.id = id
        self.queue = queue
        self.lock = lock
        self.n = n
        self.base = base
        self.ready = ready
        # self.end = self.base + 10000
        self.num = self.base + self.id

    def get_block(self, block_num):
        PARAMS = {
            "jsonrpc": "2.0",
            "method": "block_api.get_block",
            "params": {"block_num": block_num},
            "id": 1
        }

        response = requests.post(
            'https://api.steemit.com/',
            data=json.dumps(PARAMS),
        )

        data = response.json()

        # Empty result for blocks that do not exist yet
        try:
            if len(data['result']) == 0:
                time.sleep(2)
                return None
            return data
        except:
            return None

    def add_block(self, data):
        try:
            self.lock.acquire()
            self.queue.append({
                "block_num": self.num,
                "data": data['result']['block'],
            })
        finally:
            self.lock.release()

        if len(self.queue) > 50:
            print('queue too long')
            time.sleep(5)

    def run(self):
        while True:
            if self.ready == [1 for x in range(0, self.n)]:
                for x in range(0, len(self.ready)):
                    self.ready[x] = 0

            if self.ready[self.id-1] == 0:
                try:
                    data = self.get_block(self.num)
                    try:
                        if data:
                            self.add_block(data)
                            self.ready[self.id-1] = 1
                            self.num += self.n
                    except Exception as e:
                        print('add_block', e)
                    time.sleep(0.25)
                except requests.exceptions.RequestException as e:
                    print(e)
                    time.sleep(1)


class RPC_node():
    def __init__(self, start, blocks_queue, blocks_queue_lock,
                 amount_of_threads=1):
        threading.Thread.__init__(self)
        self.start = start
        self.blocks = []
        self.blocks_lock = threading.Lock()
        self.blocks_queue = blocks_queue
        self.blocks_queue_lock = blocks_queue_lock
        self.n = amount_of_threads
        self.ready = [0 for x in range(0, self.n)]
        self.run()

    def run(self):
        lock = threading.Lock()
        queue = []
        threads = []

        for x in range(1, self.n+1):
            thread = Blocks(x, self.n, self.start, queue, lock, self.ready)
            thread.start()
            threads.append(thread)

        sorter = Sorter(
            self.start, queue, lock, self.blocks, self.blocks_lock,
            self.blocks_queue, self.blocks_queue_lock)
        sorter.start()
