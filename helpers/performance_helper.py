import os
def performance_cal(text1):
	if "高" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/performance.txt','a+') as f:
			f.write('高')
	elif "一般" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/performance.txt','a+') as f:
			f.write('中低')
	