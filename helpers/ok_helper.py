from aip import AipNlp
import time

def is_ok(text1):
		
	APP_ID = '18102862'
	API_KEY = 'igU7dumhhWws35yIMUE6wGRL'
	SECRET_KEY = 'hE9QieKEA3nYUrGIbKVbIdrmEZGsUGgS'

	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

	result1 = client.simnet(text1, '好的满意没问题嗯嗯可以就它了就这个')["score"]
	result2 = client.simnet(text1, '有的不行不满意再推荐一款换一个有别的吗不好')["score"]


	return result1>result2
