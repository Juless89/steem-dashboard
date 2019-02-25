import time
import threading

from database import Database
from datetime import datetime
from counter import Counter

class Claim_rewards(threading.Thread):
    def __init__(self, storage, lock):
        threading.Thread.__init__(self)
        self.storage = storage
        self.lock = lock
        self.timestamp = None
        self.block = None
        self.hour = None
        self.date = None
        self.minute = None

        self.db = Database()
        self.counter = Counter(
            minute="api_claim_rewards_count_minute",
            hour="api_claim_rewards_count_hour",
            day="api_claim_rewards_count_day",
        )

    def process_claim_reward(self, claim_reward):
        if claim_reward['type'] == "header":
            self.timestamp = datetime.strptime(claim_reward['timestamp'], '%Y-%m-%dT%H:%M:%S')
            self.block = claim_reward['block_num']

            # Keep track of the date
            if self.timestamp.date != self.date:
                self.date = self.timestamp.date()
                self.counter.date = self.timestamp.date()

            # For each hour of data processed upload the data into the database
            # and clear the buffers.
            if self.timestamp.minute != self.minute:
                self.counter.dump_data()
                self.db.dump('api_claim_rewards')
                self.minute = self.timestamp.minute
        else:
            account = claim_reward['value']['account']
            reward_steem = claim_reward['value']['reward_steem']['amount']
            reward_sbd = claim_reward['value']['reward_sbd']['amount']
            reward_vests = claim_reward['value']['reward_vests']['amount']
            self.db.add_claim_reward(account, reward_steem, reward_sbd, reward_vests, self.timestamp)

            # Allow for multiple resolutions
            hour = self.timestamp.hour
            minute = self.timestamp.minute
            self.counter.set_resolutions(hour, minute)

    def run(self):
        while True:
            if len(self.storage) > 0:
                try:
                    self.lock.acquire()
                    claim_rewards = self.storage[:]
                finally:
                    self.lock.release()

                    for claim_reward in claim_rewards:
                        self.process_claim_reward(claim_reward)
                    self.storage.clear()

            else:
                time.sleep(0.1)
