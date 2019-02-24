from votes import Votes
from steem_node import Node
import threading

if __name__ == "__main__":
    arrays = {
        "vote_operation": []
    }
    lock = threading.Lock()
    node = Node(arrays, lock)
    votes = Votes(arrays['vote_operation'], lock)
    node.start()
    votes.start()