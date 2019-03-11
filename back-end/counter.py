from database import Database


class Counter:
    def __init__(self, **kwargs):
        self.db = Database()

        self.data_hour = {}
        self.data_minute = {}
        self.data_day = {}

        self.hour = None
        self.date = None
        self.minute = None
        self.counter = 0

        self.table_minute = kwargs['minute']
        self.table_hour = kwargs['hour']
        self.table_day = kwargs['day']

    # Increase frequency counter
    def process_transaction(self, string, data, **kwargs):
        string = str(self.date) + ' ' + string

        if string in data:
            for key, value in kwargs.items():
                data[string][key] += value
        else:
            data[string] = kwargs

    # Clear buffers and add to database
    def dump_data(self):
        #self.insert_into_db(self.data_minute, self.table_minute)
        self.insert_into_db(self.data_hour, self.table_hour)
        self.insert_into_db(self.data_day, self.table_day)
        self.data_hour.clear()
        self.data_minute.clear()
        self.data_day.clear()

    # Loop through the data dict and insert each pair into the database
    def insert_into_db(self, data, table):
        for time, data in data.items():
            string = f'{time}'
            self.db.insert_selection(string, data, table)

    # Account for multiple resolutions
    def set_resolutions(self, hour, minute, **kwargs):
        self.process_transaction(f'{hour}:{minute}:00', self.data_minute, **kwargs)
        self.process_transaction(f'{hour}:00:00', self.data_hour, **kwargs)
        self.process_transaction(f'00:00:00', self.data_day, **kwargs)
