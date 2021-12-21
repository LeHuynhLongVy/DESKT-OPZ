import json


file = open('gpu_info.json', 'r')
gpu_raw = json.load(file)
file.close()

gpu_final_with_price = []
for i in gpu_raw:
	if i['price'][0] == '$':
		gpu_final_with_price.append(i)

file = open('final_gpu.json', 'w')
json.dump(gpu_final_with_price, file)