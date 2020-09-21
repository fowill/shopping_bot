from aip import AipNlp
import time
import os
def pointExtract(text1):
	
	APP_ID = '18102862'
	API_KEY = 'igU7dumhhWws35yIMUE6wGRL'
	SECRET_KEY = 'hE9QieKEA3nYUrGIbKVbIdrmEZGsUGgS'

	client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

	adjust_ls = ["内存大点","轻点",'便宜点','贵点']
	name_ls = ["bigger_rom","lighter","cheap","expensive"]

	cpu_list = ['i3','i5','i7','i9','r3','r5','r7']
	for cpu in cpu_list:
		if cpu in text1.lower():
			with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/cpu.txt','a+') as f:
				f.write(str(cpu))
			return {"bigger_rom":0,"light":0,"cheap":0,"expensive":0}
		else:
			with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/cpu.txt','a+') as f:
				f.write('')

	""" 调用短文本相似度 """
	score_ls = []
	score_dict = {}
	score_dict_temp = {}
	for i in range(len(adjust_ls)):
		time.sleep(0.5)
		result = client.simnet(text1, adjust_ls[i])["score"]
		score_ls.append(result)
		score_dict[name_ls[i]] = score_ls[i]

	big = 0
	adjust = ''
	for k,v in score_dict_temp.items():
		if v > big:
			big = v
			adjust = k
	for k in score_dict_temp.keys():
		if k == adjust:
			score_dict[k] = 10
		else:
			score_dict[k] = 0

	return score_dict
