import time
import threading

from database import Database
from datetime import datetime
from counter import Counter


class Operation(threading.Thread):
    def __init__(self, table, storage, lock, scraping=False):
        threading.Thread.__init__(self)
        self.storage = storage
        self.lock = lock
        self.timestamp = None
        self.block = None
        self.hour = None
        self.date = None
        self.minute = None
        self.scraping = scraping
        self.table = table

        self.db = Database()

        # buffer used to process and store different resolutions
        self.counter = Counter(
            minute=f"{self.table}_count_minute",
            hour=f"{self.table}_count_hour",
            day=f"{self.table}_count_day",
        )

    # Take in an operation, checks for headers to set new block time.
    # extract and store relevant data.
    def process_header(self, vote):
        # filter for header
        self.timestamp = datetime.strptime(
            vote['timestamp'], '%Y-%m-%dT%H:%M:%S')
        self.block = vote['block_num']

        # Keep track of the date
        if self.timestamp.date != self.date:
            self.date = self.timestamp.date()
            self.counter.date = self.timestamp.date()

        if not self.scraping:
            self.counter.dump_data()
            self.db.dump(self.table)
        else:
            # For each hour of data processed upload the data into the
            # database and clear the buffers.
            if self.timestamp.hour != self.hour:
                self.counter.dump_data()
                self.db.dump(self.table)
                self.hour = self.timestamp.hour

    def process_operation(self, operation):
        pass

    def run(self):
        while True:
            # check the queue for new operations, copy the data and clear
            # the queue.
            if len(self.storage) > 0:
                try:
                    self.lock.acquire()
                    operations = self.storage[:]
                    self.storage.clear()
                finally:
                    self.lock.release()

                    # process each operation
                    for operation in operations:
                        if operation['type'] == "header":
                            self.process_header(operation)
                        else:
                            self.process_operation(operation)
            else:
                time.sleep(0.1)
