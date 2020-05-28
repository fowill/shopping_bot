from aip import AipNlp
import time

def pointExtract(text1):
		
	APP_ID = '18102862'
	API_KEY = 'igU7dumhhWws35yIMUE6wGRL'
	SECRET_KEY = 'hE9QieKEA3nYUrGIbKVbIdrmEZGsUGgS'

	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

	looking_ls = ["屏幕大","屏幕小","沉重傻大黑粗累背不动换个轻点的",'性能强一些','用不上性能轻薄些','太贵了，便宜些','太低端要贵一点的']
	name_ls = ["big-screen","small-screen","too-heavy","high-performance","low-performance","too-expensive","to-cheap"]


	""" 调用短文本相似度 """
	score_ls = []
	score_dict = {}
	for i in range(len(looking_ls)):
		time.sleep(0.5)
		result = client.simnet(text1, looking_ls[i])["score"]
		score_ls.append(result)
		score_dict[name_ls[i]] = score_ls[i]

	return score_dict
