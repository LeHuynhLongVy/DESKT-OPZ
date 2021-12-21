# from time import sleep
# from db_utility import GetItemFromDatabase
import redis
import json
# from googlesearch import search
# to search
# query = "Intel core i5"
#
# for i in search(query, num=1, stop=1, pause=2):
# 	print(i)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

data = {'1': 1, '2': 'hello', '3': [1,2,3]}

json_data = json.dumps(data)

r.set('data', json_data)

re_data = json.loads(r.get('data'))

print(re_data)

# data = GetItemFromDatabase.get_cpu_list_from_db()
# for i in range(5):

# a = [[1,2], [1,2]]
# for i in range(len(a)):
#
# 	a[i] = a[i][0]
# print(a)