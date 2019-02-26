from database import Database
from rpc_node import RPC_node

import threading
import time


class Node(threading.Thread):
    def __init__(self, votes_arr, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.arrays = votes_arr
        self.blocks_queue = []
        self.blocks_queue_lock = threading.Lock()
        # self.stm = Steem('https://rpc.steemviz.com')
        # print('test')
        # self.blockchain =
        # print('test2')
        self.db = Database()

    def run(self):
        rpc = RPC_node(
            start=30515320,
            amount_of_threads=8,
            blocks_queue=self.blocks_queue,
            blocks_queue_lock=self.blocks_queue_lock,
        )

        while True:
            # print(len(self.blocks_queue))
            if len(self.blocks_queue) > 0:

                try:
                    self.blocks_queue_lock.acquire()

                    while len(self.blocks_queue) > 0:
                        block = self.blocks_queue.pop(0)
                        timestamp = block['timestamp']
                        block_num = block['block_num']
                        print(block_num, timestamp, end='\r')

                        try:
                            self.lock.acquire()
                            header = {
                                "type": "header",
                                "block_num": block_num,
                                "timestamp": timestamp,
                            }
                            for transaction in block['transactions']:
                                for operation in transaction['operations']:
                                    try:
                                        if len(self.arrays[operation['type']]) == 0:
                                            self.arrays[operation['type']].append(header)
                                        self.arrays[operation['type']].append(operation)
                                    except:
                                        continue
                        finally:
                            self.lock.release()

                        self.db.add_block(block_num, timestamp)
                finally:
                    self.blocks_queue_lock.release()
            time.sleep(0.05)
