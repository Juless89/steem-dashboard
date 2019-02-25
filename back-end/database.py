import mysql.connector
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.readfp(open(r'../front-end/settings.cnf'))


class Database():
    def __init__(self):
        self.db = None
        self.cur = None
        self.debug = False

        # Multi sql statements
        self.buffer = []
        self.query = None

    def connect_to_db(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user=config.get('client', 'user'),
            passwd=config.get('client', 'password'),
            db=config.get('client', 'database'),
        )
        self.cur = self.db.cursor()

    def close_connection(self):
        self.cur.close()
        self.db.close()

    def add_block(self, num, timestamp):
        query = (f"INSERT INTO `api_blocks` (`id`, `number`, `timestamp`) VALUES (NULL, '{num}', '{timestamp}')")
        self.post_data(query, 'api_blocks')

    def add_vote(self, voter, author, permlink, weight, timestamp, value=0):
        self.query = (
            """INSERT INTO `api_votes` (`id`, `voter`, `author` , `permlink` , `weight`, `value` , `timestamp`)
            VALUES (NULL, %s, %s, %s, %s, %s, %s)""")
        self.buffer.append((voter, author, permlink, weight, value, timestamp))        

    def add_transfer(self, sender, receiver, amount, precision, nai, timestamp):
        self.query = (
            """INSERT INTO `api_transfers` (`id`, `sender`, `receiver` , `amount` , `precision`, `nai` , `timestamp`)
            VALUES (NULL, %s, %s, %s, %s, %s, %s)""")
        self.buffer.append((sender, receiver, amount, precision, nai, timestamp))

    def add_claim_reward(self, account, reward_steem, reward_sbd, reward_vests, timestamp):
        self.query = (
            """INSERT INTO `api_claim_rewards` (`id`, `account`, `reward_steem` , `reward_sbd` , `reward_vests` , `timestamp`)
            VALUES (NULL, %s, %s, %s, %s, %s)""")
        self.buffer.append((account, reward_steem, reward_sbd, reward_vests, timestamp))

    def get_block(self, num):
        query = (f"SELECT `*` FROM `api_blocks` WHERE `number` = '{num}'")

        return self.get_data(query)

    def get_votes(self):
        query = f"SELECT `*` FROM `api_votes`"

        return self.get_data(query)

    def get_votes_count(self, table):
        query = (f"SELECT `*` FROM `{table}`")

        return self.get_data(query)


    def update_signal(self, mail_id):
        query = (
            "UPDATE `signals` SET `processed` = 'yes' WHERE " +
            f"`signals`.`mail_id` = {mail_id};")

        self.post_data(query, 'signals')

    # Execute all stored sql queries at once
    def dump(self, table):
        self.post_data(self.query, table, True)
        self.buffer = []

    # Insert date, amount into table 'table'. Look if the record already
    # exists, update if needed else add.
    def post_data(self, query, table, multi=False):
        if self.debug:
            print(query)

        try:
            self.connect_to_db()

            # Lock table
            self.cur.execute(f"LOCK TABLES {table} WRITE;")

            # single or multi statement
            if multi == False:
                self.cur.execute(query)
            else:
                self.cur.executemany(query, self.buffer)

            # Release table
            self.cur.execute(f"UNLOCK TABLES;")                

            # Commite changes made to the db
            self.db.commit()

        except Exception as e:
            print('Error:', e)

        finally:
            # Close connections
            self.close_connection()

    def get_data(self, query):
        if self.debug:
            print(query)

        try:
            # Connect to DB and execute query
            self.connect_to_db()
            self.cur.execute(query)

            # Fetch results
            rows = self.cur.fetchall()

            # Commite changes made to the db
            self.db.commit()
        except Exception as e:
            print('Error:', e)

        finally:
            # Close connections
            self.close_connection()
            return rows

    # Retrieve current amount value, add new and update the record
    def update_record(self, amount, timestamp, table):
        # retrieve current value for amount
        self.cur.execute(f"SELECT `count` FROM `{table}` "
                         f"WHERE `timestamp` = '{timestamp}';")
        total = amount + self.cur.fetchone()[0]

        # update the record
        query = f"UPDATE `{table}` SET `count` = {total} WHERE " \
                f"`{table}`.`timestamp` = '{timestamp}';"
        self.cur.execute(query)

    # Check if query comes back with any results
    def check_if_record_exist(self, timestamp, table):
        self.cur.execute(f"SELECT 1 FROM `{table}` WHERE `timestamp` = '{timestamp}';")

        if len(self.cur.fetchall()) > 0:
            return True

    # Insert date, amount into table 'table'. Look if the record already
    # exists, update if needed else add.
    def insert_selection(self, timestamp, amount, table):
        # sql query used to insert data into the mysql database
        query = f"INSERT INTO `{table}` (`count`, `timestamp`)" \
                " VALUES ('{}', '{}');".format(amount ,timestamp)

        try:
            self.connect_to_db()

            # Lock table
            self.cur.execute(f"LOCK TABLES {table} WRITE;")

            # Check if record exists, update if the case. Else create
            if self.check_if_record_exist(timestamp, table):
                self.update_record(amount, timestamp, table)
            else:
                self.cur.execute(query)

            # Release table
            self.cur.execute(f"UNLOCK TABLES;")

            # Commite changes made to the db
            self.db.commit()

        except Exception as e:
            print('Error:', e)

        finally:
            # Close connections
            self.close_connection()