from votes import Votes
from transfers import Transfers
from claim_reward import Claim_rewards
from steem_node import Node

from database import Database

import threading
import sys
# import time

if __name__ == "__main__":
    scraping = False
    valid = 0
    settings = {}
    if len(sys.argv) == 4:
        block_num = sys.argv[1]
        block_count = sys.argv[2]
        n_threads = sys.argv[3]
        if block_num.isdigit():
            settings['block_num'] = int(block_num)
            settings['block_count'] = int(block_count)
            settings['n_threads'] = int(n_threads)
            settings['scraping'] = True
            scraping = True
            valid = 1
        else:
            print('String')
    elif len(sys.argv) == 1:
        valid = 1
    else:
        print('For scraping: python main.py <start_block> <blocks> <threads>')

    if valid:
        # queues for each different operation type
        arrays = {
            "vote_operation": [],
            "transfer_operation": [],
            "claim_reward_balance_operation": [],
        }
        # shared lock between all operation threads
        lock = threading.Lock()

        # STEEM blockchain node api
        node = Node(arrays, lock, **settings)

        # processing threads for each operation type
        votes = Votes(arrays['vote_operation'], lock, scraping)
        transfers = Transfers(arrays['transfer_operation'], lock, scraping)
        claim_rewards = Claim_rewards(
            arrays['claim_reward_balance_operation'], lock, scraping
        )

        # check for start block
        db = Database()
        data = db.get_last_block()
        if len(data) > 0 or settings.pop('block_num', None):
            # start all threads
            node.start()
            votes.start()
            claim_rewards.start()
            transfers.start()
        else:
            print('Set start block')

    # Track memory usage and difference
    """
    tr = tracker.SummaryTracker()
    while True:
        time.sleep(5)
        sum1 = summary.summarize(muppy.get_objects())
        summary.print_(sum1)
        print('\n\n\n')
        #tr.print_diff()
        #print('\n\n\n')
    """
