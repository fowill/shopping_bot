from aip import AipNlp
import time

def looking_cal(text1):
		
	APP_ID = '18102862'
	API_KEY = 'igU7dumhhWws35yIMUE6wGRL'
	SECRET_KEY = 'hE9QieKEA3nYUrGIbKVbIdrmEZGsUGgS'

	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

	looking_ls = ["轻薄优雅","商务办公大气","炫酷帅","精致高级"]


	""" 调用短文本相似度 """
	best_num = 0
	best_score = 0
	for i in range(len(looking_ls)):
		result = client.simnet(text1, looking_ls[i])
		time.sleep(0.5)
		if result["score"] > best_score:
			best_score = result["score"]
			best_num = i

	return looking_ls[best_num]
