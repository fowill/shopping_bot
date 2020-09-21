import os
def brand_cal(text1):	
	if "华为" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("华为")
	if "荣耀" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			 f.write("HONOR")
	if "苹果" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("Apple")
	if "微软" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("Microsoft")
	if "联想" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("Lenovo")
	if "神舟" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("Hasee")
	if "惠普" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("HP")
	if "小米" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("MI")
	if "戴尔" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("DELL")
	if "华硕" in str(text1):
		with open(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/save/brand.txt','a+') as f:
			f.write("ASUS")