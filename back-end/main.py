from votes import Votes
from transfers import Transfers
from claim_reward import Claim_rewards

from steem_node import Node
import threading

if __name__ == "__main__":
    arrays = {
        "vote_operation": [],
        "transfer_operation": [],
        "claim_reward_balance_operation": [],
    }
    lock = threading.Lock()
    node = Node(arrays, lock)

    votes = Votes(arrays['vote_operation'], lock)
    transfers = Transfers(arrays['transfer_operation'], lock)
    claim_rewards = Claim_rewards(arrays['claim_reward_balance_operation'], lock)

    node.start()
    votes.start()
    claim_rewards.start()

    transfers.start()