import time
import threading

from database import Database
from datetime import datetime
from counter import Counter

class Votes(threading.Thread):
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
            minute="api_votes_count_minute",
            hour="api_votes_count_hour",
            day="api_votes_count_day",
        )

    def process_vote(self, vote):
        if vote['type'] == "header":
            self.timestamp = datetime.strptime(vote['timestamp'], '%Y-%m-%dT%H:%M:%S')
            self.block = vote['block_num']

            # Keep track of the date
            if self.timestamp.date != self.date:
                self.date = self.timestamp.date()
                self.counter.date = self.timestamp.date()

            # For each hour of data processed upload the data into the database
            # and clear the buffers.
            if self.timestamp.minute != self.minute:
                self.counter.dump_data()
                self.db.dump('api_votes')
                self.minute = self.timestamp.minute
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
            if len(self.storage) > 0:
                try:
                    self.lock.acquire()
                    votes = self.storage[:]
                finally:
                    self.storage.clear()
                    self.lock.release()

                    for vote in votes:
                        self.process_vote(vote)
                    

            else:
                time.sleep(0.1)
