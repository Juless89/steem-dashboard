import time
import threading

from database import Database
from datetime import datetime
from counter import Counter


class Votes(threading.Thread):
    def __init__(self, storage, lock, scraping=False):
        threading.Thread.__init__(self)
        self.storage = storage
        self.lock = lock
        self.timestamp = None
        self.block = None
        self.hour = None
        self.date = None
        self.minute = None
        self.scraping = scraping

        self.db = Database()

        # buffer used to process and store different resolutions
        self.counter = Counter(
            minute="api_votes_count_minute",
            hour="api_votes_count_hour",
            day="api_votes_count_day",
        )

    # Take in an operation, checks for headers to set new block time.
    # extract and store relevant data.
    def process_vote(self, vote):
        # filter for header
        if vote['type'] == "header":
            self.timestamp = datetime.strptime(
                vote['timestamp'], '%Y-%m-%dT%H:%M:%S')
            self.block = vote['block_num']

            # Keep track of the date
            if self.timestamp.date != self.date:
                self.date = self.timestamp.date()
                self.counter.date = self.timestamp.date()

            if not self.scraping:
                self.counter.dump_data()
                self.db.dump('api_votes')
            else:
                # For each hour of data processed upload the data into the
                # database and clear the buffers.
                if self.timestamp.hour != self.hour:
                    self.counter.dump_data()
                    self.db.dump('api_votes')
                    self.hour = self.timestamp.hour
        # deconstruct operation and prepare for storing
        else:
            voter = vote['value']['voter']
            author = vote['value']['author']
            permlink = vote['value']['permlink']
            weight = vote['value']['weight']
            self.db.add_vote(voter, author, permlink, weight, self.timestamp)

            # Allow for multiple resolutions
            hour = self.timestamp.hour
            minute = self.timestamp.minute
            self.counter.set_resolutions(hour, minute)

    def run(self):
        while True:
            # check the queue for new operations, copy the data and clear
            # the queue.
            if len(self.storage) > 0:
                try:
                    self.lock.acquire()
                    votes = self.storage[:]
                finally:
                    self.storage.clear()
                    self.lock.release()

                    # process each operation
                    for vote in votes:
                        self.process_vote(vote)
            else:
                time.sleep(0.1)
