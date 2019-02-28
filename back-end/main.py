from votes import Votes
from transfers import Transfers
from claim_reward import Claim_rewards
from steem_node import Node

import threading
# import time

if __name__ == "__main__":
    # queues for each different operation type
    arrays = {
        "vote_operation": [],
        "transfer_operation": [],
        "claim_reward_balance_operation": [],
    }
    # shared lock between all operation threads
    lock = threading.Lock()

    # STEEM blockchain node api
    node = Node(arrays, lock)

    # processing threads for each operation type
    votes = Votes(arrays['vote_operation'], lock)
    transfers = Transfers(arrays['transfer_operation'], lock)
    claim_rewards = Claim_rewards(
        arrays['claim_reward_balance_operation'], lock,
    )

    # start all threads
    node.start()
    votes.start()
    claim_rewards.start()
    transfers.start()

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
