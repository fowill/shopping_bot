import pandas as pd 
import numpy as np 
import os

def recommend(use,looking,price):
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/sources/laptops_extended.xlsx'

	df = pd.read_excel(path)
	#use = {'use-media': 0.267878, 'use-business': 0.0920902, 'use-gaming': 0.644606, 'use-creator': 0.245646, 'use-all': 0.287746}
	#looking = {'looking-elegent': 0.459218, 'looking-business': 0.283294, 'looking-cool': 0.560444}
	price_low = price['low']
	price_high = price['high']

	with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/performance.txt','r+') as f:
		performance_demand = str(f.readline())
	print('performance_demand = ' + performance_demand)

	with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','r+') as f:
		brand_demand = str(f.readline())
	print('brand_demand = ' + brand_demand)
	#print(df.columns)
	#print(df.index)

	score_ls = []

	for i in range(len(df.index)):
		score = 0
		if df.loc[i,'cpu-performance'] not in performance_demand:
			score_ls.append(score)
			continue
		if df.loc[i,'brand'] not in brand_demand:
			score_ls.append(score)
			continue
		if df.loc[i,'price']<price_low or df.loc[i,'price']>price_high:
			score_ls.append(score)
			continue
		else:
			for key in list(use.keys()):
				score += use[key]*df.loc[i,key]
			for key in list(looking.keys()):
				score += looking[key]*df.loc[i,key]
			print(i)
			score_ls.append(score)

	index = 0
	big = 0
	for i in range(len(score_ls)):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/score.txt','a+') as f:
			f.write(str(score_ls[i]))
			f.write(',')
		if score_ls[i]>big:
			index = i
			big = score_ls[i]
	with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/score.txt','a+') as f:
		f.write('\n')

	text = f"为您推荐{df.loc[index,'brand']}生产的{df.loc[index,'name']}, 内存为{df.loc[index,'rom']}G, cpu为{df.loc[index,'cpu-core']}核{df.loc[index,'cpu-type']}。屏幕为{df.loc[index,'screen-r1']}*{df.loc[index,'screen-r2']}。重量为{df.loc[index,'weight']}kg,售价{df.loc[index,'price']}元。"

	return (index,text)

        


