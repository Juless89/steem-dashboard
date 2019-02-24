import time
import threading

from database import Database
from datetime import datetime

class Votes(threading.Thread):
    def __init__(self, storage, lock):
        threading.Thread.__init__(self)
        self.storage = storage
        self.lock = lock
        self.timestamp = None
        self.block = None
        self.db = Database()

        self.data_hour = {}
        self.data_minute = {}
        self.data_day = {}

        self.hour = None
        self.date = None
        self.minute = None
        self.counter = 0

    # Increase frequency counter
    def process_transaction(self, string, data):
        string = str(self.date) + ' ' + string
        if string in data:
            data[string] += 1
        else:
            data[string] = 1

    def dump_data(self):
        self.insert_into_db(self.data_minute, 'api_votes_count_minute')
        self.insert_into_db(self.data_hour, 'api_votes_count_hour')
        self.insert_into_db(self.data_day, 'api_votes_count_day')

    # Loop through the data dict and insert each pair into the database
    def insert_into_db(self, data, table):
        for time, amount in data.items():
            string = f'{time}'
            self.db.insert_selection(string, amount, table)

    def process_vote(self, vote):
        if vote['type'] == "header":
            self.timestamp = datetime.strptime(vote['timestamp'], '%Y-%m-%dT%H:%M:%S')
            self.block = vote['block_num']

            # Keep track of the date
            if self.timestamp.date != self.date:
                self.date = self.timestamp.date()

            # For each hour of data processed upload the data into the database
            # and clear the buffers.
            if self.timestamp.minute != self.minute:
                self.dump_data()
                self.data_hour = {}
                self.data_minute = {}
                self.data_day = {}
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
            self.process_transaction(f'{hour}:{minute}:00', self.data_minute)
            self.process_transaction(f'{hour}:00:00', self.data_hour)
            self.process_transaction(f'00:00:00', self.data_day)

    def run(self):
        while True:
            if len(self.storage) > 0:
                try:
                    self.lock.acquire()
                    for vote in self.storage:
                        self.process_vote(vote)
                    self.storage.clear()
                finally:
                    self.lock.release()
            else:
                time.sleep(0.05)
