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
	score_ls = []
	score_dict = {}
	score_dict_temp = {}
	for i in range(len(looking_ls)):
		time.sleep(0.5)
		result = client.simnet(text1, looking_ls[i])["score"]
		score_ls.append(result)
		score_dict_temp[name_ls[i]] = score_ls[i]

	big = 0
	looking = ''
	for k,v in score_dict_temp.items():
		if v > big:
			big = v
			looking = k
	for k in score_dict_temp.keys():
		if k == looking:
			score_dict[k] = 10
		else:
			score_dict[k] = 0

	return score_dict
