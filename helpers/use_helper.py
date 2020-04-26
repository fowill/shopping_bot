from aip import AipNlp
import time

def use_cal(text1):
		
	APP_ID = '18102862'
	API_KEY = 'igU7dumhhWws35yIMUE6wGRL'
	SECRET_KEY = 'hE9QieKEA3nYUrGIbKVbIdrmEZGsUGgS'

	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

	use_ls = ["看电影听音乐追剧看番","办公出差商务表格","游戏电竞单机网游","平面设计PS视频剪辑"]
	name_ls = ["影音娱乐","商务差旅","游戏电竞","创意设计"]


	""" 调用短文本相似度 """
	best_num = 0
	best_score = 0
	for i in range(len(use_ls)):
		result = client.simnet(text1, use_ls[i])
		time.sleep(0.5)
		if result["score"] > best_score:
			best_score = result["score"]
			best_num = i

	return name_ls[best_num]
