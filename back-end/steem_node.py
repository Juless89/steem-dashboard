from database import Database
from rpc_node import RPC_node
from datetime import datetime, timedelta

import threading
import time


# Block processing thread, takes in blocks from the sorter in order,
# extracts all operations and sorts them for processing by each
# operation thread.
class Node(threading.Thread):
    def __init__(self, votes_arr, lock, **kwargs):
        threading.Thread.__init__(self)
        self.block_num = None
        self.scraping = False
        self.lock = lock
        self.arrays = votes_arr
        self.blocks_queue = []
        self.blocks_queue_lock = threading.Lock()
        self.db = Database()
        self.counter = 0
        self.block_counter = 0
        self.n_threads = 2
        self.block_count = 10**9
        self.s_time = datetime.now()
        self.end = None

        # set scraping mode variables
        if len(kwargs) > 0:
            self.scraping = kwargs['scraping']
            self.block_num = kwargs['block_num']
            self.n_threads = kwargs['n_threads']
            self.block_count = kwargs['block_count']
            print(f'Start: {self.block_num}\nBlocks: {self.block_count}\
                \nThreads: {self.n_threads}\nScrape: {self.scraping}\n')

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

        # calculate avg block processing speed
        c_time = datetime.now()
        speed = int(self.counter/(c_time-self.s_time).total_seconds())

        if speed == 0:
            eta = 0
        else:
            eta = int((self.end-block_num)/speed)
        print(block_num, timestamp, f'avg Block/s: {speed} ETA: {str(timedelta(seconds=eta))}      ', end='\r')

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

        # In scarping mode make less block inserts into the db
        if self.scraping:
            self.block_counter += 1
            if self.block_counter % 1000 == 0:
                self.db.add_block(block_num, timestamp)
        else:
            self.db.add_block(block_num, timestamp)

    def run(self):
        # check if block_num is set, else retrieve form db
        if not self.block_num:
            data = self.db.get_last_block()
            if len(data) > 0:
                start_block = data[0][0]
        else:
            start_block = int(self.block_num)

        # main block gathering thread
        rpc = RPC_node(
            start=start_block+1,
            block_count=self.block_count,
            amount_of_threads=self.n_threads,
            blocks_queue=self.blocks_queue,
            blocks_queue_lock=self.blocks_queue_lock,
        )
        rpc.start()

        self.end = start_block + self.block_count

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
