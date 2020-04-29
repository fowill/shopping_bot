from aip import AipNlp
import time

def use_cal(text1):
		
	APP_ID = '18102862'
	API_KEY = 'igU7dumhhWws35yIMUE6wGRL'
	SECRET_KEY = 'hE9QieKEA3nYUrGIbKVbIdrmEZGsUGgS'

	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

	use_ls = ["看电影听音乐追剧看番","办公出差商务表格","游戏电竞单机网游","平面设计PS视频剪辑","日常全能随便都行"]
	name_ls = ["use-media","use-business","use-gaming","use-creator","use-all"]


	""" 调用短文本相似度 """
	score_ls = []
	score_dict = {}
	for i in range(len(use_ls)):
		time.sleep(0.5)
		result = client.simnet(text1, use_ls[i])["score"]
		score_ls.append(result)
		score_dict[name_ls[i]] = score_ls[i]


	return score_dict
