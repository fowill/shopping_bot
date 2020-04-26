from aip import AipNlp
import time

def looking_cal(text1):
		
	APP_ID = '18102862'
	API_KEY = 'igU7dumhhWws35yIMUE6wGRL'
	SECRET_KEY = 'hE9QieKEA3nYUrGIbKVbIdrmEZGsUGgS'

	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

	looking_ls = ["轻薄携带小巧精致","商务办公大气公司出差低调沉稳","炫酷帅RGB灯霸气威武"]
	name_ls = ["looking-elegent","looking-business","looking-cool"]


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
