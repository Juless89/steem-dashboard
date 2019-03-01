from database import Database
from rpc_node import RPC_node
from datetime import datetime

import threading
import time


# Block processing thread, takes in blocks from the sorter in order,
# extracts all operations and sorts them for processing by each
# operation thread.
class Node(threading.Thread):
    def __init__(self, votes_arr, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.arrays = votes_arr
        self.blocks_queue = []
        self.blocks_queue_lock = threading.Lock()
        self.db = Database()

        self.counter = 0
        self.s_time = datetime.now()

    # To prevent build up with the database check if all previous operations
    # have already been stored.
    def check_buffers(self):
        for array in self.arrays:
            if len(array) > 0:
                return False
        return True

    def process_transactions(self, block):
        # Extract block_num and timestamp.
        timestamp = block['timestamp']
        block_num = block['block_num']
        c_time = datetime.now()
        speed = int(self.counter/(c_time-self.s_time).total_seconds())
        print(block_num, timestamp, f'avg Block/s: {speed}    ', end='\r')

        # Write header for each new block.
        header = {
            "type": "header",
            "block_num": block_num,
            "timestamp": timestamp,
        }

        # Check each transactions for operations
        for transaction in block['transactions']:
            for operation in transaction['operations']:
                # add operation to correct queue
                try:
                    if len(self.arrays[operation['type']]) == 0:
                        self.arrays[operation['type']].append(header)
                    self.arrays[operation['type']].append(operation)
                except Exception:
                    continue

    def run(self):
        # main block gathering thread
        rpc = RPC_node(
            start=30773649, # 2019-01-01 0:00:00
            amount_of_threads=2,
            blocks_queue=self.blocks_queue,
            blocks_queue_lock=self.blocks_queue_lock,
        )
        rpc.start()

        while True:
            # check for new blocks
            if len(self.blocks_queue) > 0:
                try:
                    self.blocks_queue_lock.acquire()
                    # Take out all new blocks at once
                    while (len(self.blocks_queue) > 0):
                        if self.check_buffers:
                            # remove from queue
                            block = self.blocks_queue.pop(0)

                            try:
                                self.lock.acquire()

                                # process all operations
                                self.process_transactions(block)

                            finally:
                                self.lock.release()

                        else:
                            time.sleep(0.1)

                        # blocks per second counter
                        self.counter += 1

                finally:
                    self.blocks_queue_lock.release()

            # wait for new blocks
            time.sleep(0.05)
