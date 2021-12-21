import json

f = open('phong_vu_data.json', 'r')
raw_txt = f.read()
f.close()

f = open('phong_vu_data_formated.json', 'w')
f.write("["  + raw_txt.replace("}{", "},{") + "]")
f.close()

f = open('phong_vu_data_formated.json', 'r')
data = json.load(f)
for item in data:
	print(item)
f.close()