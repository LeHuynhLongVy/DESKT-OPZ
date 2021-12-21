import json

f = open('phong_vu_case_data.txt', 'r')
raw_txt = f.read()
f.close()

f = open('final_case.json', 'w')
f.write("["  + raw_txt.replace("}{", "},{") + "]")
f.close()

f = open('final_case.json', 'r')
data = json.load(f)
for item in data:
	print(item)
f.close()