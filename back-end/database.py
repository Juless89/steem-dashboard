import pymysql
import configparser
import pandas as pd


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

    # retrieve settings from settings.cnf
    def connect_to_db(self):
        self.db = pymysql.connect(
            host="localhost",
            user=config.get('client', 'user'),
            passwd=config.get('client', 'password'),
            db=config.get('client', 'database'),
            autocommit=True,
            local_infile=1
        )

        # create curser
        self.cur = self.db.cursor()

    # close
    def close_connection(self):
        self.cur.close()
        self.db.close()

    # add error
    def add_error(self, table, **kwargs):
        head = f"INSERT INTO `{table}` (`id`"

        columns = ''
        values = ''
        for column, value in kwargs.items():
            columns += f', `{column}`'
            values += f", '{value}'"

        query = head + columns + ') VALUES (NULL' + values + ')'
        self.post_data(query, table)

    # add new block
    def add_block(self, num, timestamp):
        query = (f"INSERT INTO `api_blocks` (`id`, `block_num`, `timestamp`) VALUES (NULL, '{num}', '{timestamp}')")
        self.post_data(query, 'api_blocks')

    # add vote operation
    def add_vote(self, voter, author, permlink, weight, timestamp, value=0):
        #query = (f"INSERT INTO `api_votes` (`id`, `voter`, `author`, `permlink`, `weight`, `value`, `timestamp`) VALUES (NULL, '{voter}', '{author}', '{permlink}', '{weight}', '{value}', '{timestamp}')")
        query = {
            "id": 'NULL',
            "voter": voter,
            "author": author,
            "permlink": permlink,
            "weight": weight,
            "value": value,
            "timestamp": timestamp,
        }
        self.buffer.append(query)

    # add transfer operation
    def add_transfer(self, sender, receiver, amount, precision, nai, timestamp):
        #query = (f"INSERT INTO `api_transfers` (`id`, `sender`, `receiver`, `amount`, `precision`, `nai`, `timestamp`) VALUES (NULL, '{sender}', '{receiver}', '{amount}', '{precision}', '{nai}', '{timestamp}')")
        query = {
            "id": 'NULL',
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "precision": precision,
            "nai": nai,
            "timestamp": timestamp,
        }
        self.buffer.append(query)

    # add claim reward
    def add_claim_reward(self, account, reward_steem, reward_sbd, reward_vests, timestamp):
        query = {
            "id": 'NULL',
            "account": account,
            "reward_steem": reward_steem,
            "reward_sbd": reward_sbd,
            "reward_vests": reward_vests,
            "timestamp": timestamp,
        }
        #query = (f"INSERT INTO `api_claim_rewards` (`id`, `account`, `reward_steem`, `reward_sbd`, `reward_vests`, `timestamp`) VALUES (NULL, '{account}', '{reward_steem}', '{reward_sbd}', '{reward_vests}', '{timestamp}')")
        self.buffer.append(query)

    # get block by number
    def get_block(self, num):
        query = (f"SELECT `*` FROM `api_blocks` WHERE `number` = '{num}'")

        return self.get_data(query)

    # get highest block by number
    def get_last_block(self):
        query = ("SELECT `block_num` FROM api_blocks order by `block_num` desc limit 1;")

        return self.get_data(query)

    # get votes between period start - end
    def get_votes(self, start, end):
        query = f"SELECT `voter`, `author` FROM `api_votes` WHERE `timestamp` BETWEEN '{start}' AND '{end}'"

        return self.get_data(query)

    # count all votes
    def get_votes_count(self, table):
        query = (f"SELECT `*` FROM `{table}`")

        return self.get_data(query)

    # Construct query and add analyses to db
    def add_analyses(self, table, **kwargs):
        head = f"INSERT INTO `{table}` (`id`"

        columns = ''
        values = ''
        for column, value in kwargs.items():
            columns += f', `{column}`'
            values += f", '{value}'"

        query = head + columns + ') VALUES (NULL' + values + ')'
        self.post_data(query, table)

    # Execute all stored sql queries at once
    def dump(self, table):
        path = "/root/steem-dashboard/back-end/temp/" + table + ".csv"
        if table == 'api_votes':
            columns = ['id', 'voter', 'author', 'permlink', 'weight', 'value', 'timestamp']
        elif table == 'api_transfers':
            columns = ['id', 'sender', 'receiver', 'amount', 'precision', 'nai', 'timestamp']
        elif table == 'api_claim_rewards':
            columns = ['id', 'account', 'reward_steem', 'reward_sbd', 'reward_vests', 'timestamp']

        df = pd.DataFrame(self.buffer)
        try:
            df = df[columns]
            df.to_csv(
                path,
                encoding='utf-8',
                header = True,
                doublequote = True,
                sep=',', index=False
            )
            self.insert_file_into_db(path, table)
        except Exception:
            pass

        #print('\n')
        #print(f'Stored: {table}.csv')
        #print('\n')
        #self.post_data(self.buffer, table, True)
        #for query in self.buffer:
            #self.post_data(query, table)
        self.buffer.clear()

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
                for qry in query:
                    cur = self.db.cursor()
                    cur.execute(qry)
                    cur.close()

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
                " VALUES ('{}', '{}');".format(amount, timestamp)

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
        except Exception as e:
            print('Error:', e)

        finally:
            # Close connections
            self.close_connection()

    # upload csv into mysql db
    def csv_to_mysql(self, load_sql):        
        try:
            self.connect_to_db()
            self.cur.execute(load_sql)
        except Exception:
            pass
        finally:
            # clonse connection
            self.close_connection()

    def insert_file_into_db(self, path, table):
        # Load file from path into table
        load_sql = f"LOAD DATA LOCAL INFILE '{path}' INTO TABLE {table} FIELDS TERMINATED BY ',' ENCLOSED BY '\"' IGNORE 1 LINES;"
        self.csv_to_mysql(load_sql)