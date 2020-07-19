import pandas as pd 
import numpy as np 
import json
import os
import fileinput
def adjust(score_dict):
	path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/sources/laptops.xlsx'

	df = pd.read_excel(path)
	#use = {'use-media': 0.267878, 'use-business': 0.0920902, 'use-gaming': 0.644606, 'use-creator': 0.245646, 'use-all': 0.287746}
	#looking = {'looking-elegent': 0.459218, 'looking-business': 0.283294, 'looking-cool': 0.560444}
	with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/log.txt','r+') as f:
		chosen_ls = f.readlines()


	#print(chosen_ls)
	with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/score.txt','r+') as f:
		score_gotten = f.readline()
	score_gotten = score_gotten.split(',')

	with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/priceLog.txt','r+') as f:
		price = eval(f.read())

	price_low = price['low']
	price_high = price['high']

	#print(df.columns)
	#print(df.index)
	score_ls = []

	for i in range(len(df.index)):
	    score = float(score_gotten[i])
	    if df.loc[i,'price']<price_low or df.loc[i,'price']>price_high or (str(i)+'\n') in chosen_ls:
	        score = 0
	    else:
	        for key in list(score_dict.keys()):
	            score += score_dict[key]*df.loc[i,key]
	    score_ls.append(score)

	for line in fileinput.input(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/score.txt',inplace = 1):
		if not fileinput.isfirstline():
			print(line.replace('\n',''))

	for i in range(len(score_ls)):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/score.txt','a+') as f:
			f.write(str(score_ls[i]))
			f.write(",")
	
	index = 0
	big = 0
	for i in range(len(score_ls)):
	    if score_ls[i]>big:
	        index = i
	        big = score_ls[i]

	with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/log.txt','a+') as f:
		f.write(str(index))
		f.write("\n")
	text = f"为您推荐{df.loc[index,'brand']}生产的{df.loc[index,'name']}, 内存为{df.loc[index,'ram']}g, 硬盘为{df.loc[index,'rom']}。cpu为{df.loc[index,'cpu-core']}核{df.loc[index,'cpu-type']}。屏幕为{df.loc[index,'screen-r1']}*{df.loc[index,'screen-r2']}。重量为{df.loc[index,'weight']}kg,续航为{df.loc[index,'battery']}小时，售价{df.loc[index,'price']}元。"

	return (index,text)

        


