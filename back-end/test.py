from database import Database
from operator import itemgetter
from collections import OrderedDict

db = Database()

data = db.get_votes_count('api_votes_count_minute')

x = []
y = []

for id, count, timestamp in data:
    x.append(str(timestamp))
    y.append(count)

print(x, y)
