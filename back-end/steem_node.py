from beem import Steem
from beem.blockchain import Blockchain
from database import Database
from datetime import datetime

import threading

class Node(threading.Thread):
    def __init__(self, votes_arr, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.arrays = votes_arr
        self.stm = Steem('https://rpc.steemviz.com')
        self.blockchain = Blockchain(self.stm)
        self.db = Database()

    def run(self):
        for block in self.blockchain.blocks(
            start=30515320,
            threading=True,
            thread_num=16,
        ):

            timestamp = datetime.strftime(block.time(), '%Y-%m-%dT%H:%M:%S')
            block_num = block.block_num
            # print(block_num, timestamp)

            try:
                self.lock.acquire()
                header = {
                    "type": "header",
                    "block_num": block_num,
                    "timestamp": timestamp,
                }
                for operation in block.operations:
                    #print(operation['type'])
                    try:
                        # if operation['type'] == 'transfer_operation':
                            # print(operation)
                        if len(self.arrays[operation['type']]) == 0:
                            self.arrays[operation['type']].append(header)
                        self.arrays[operation['type']].append(operation)
                       
                    except:
                        continue

            finally:
                self.lock.release()
                #print(self.arrays['claim_reward_balance_operation'])

            self.db.add_block(block.block_num, timestamp)

