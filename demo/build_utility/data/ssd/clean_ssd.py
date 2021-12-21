import json

file = open('ssd_info.json', 'r')
ssd_list = json.load(file)
file.close()

final_ssd_list_with_price = []
for i in ssd_list:
	if i['price'][0] == '$':
		name_part = i['name'].split(" ")
		for part in name_part:
			if 'M.2' in part:
				i.update({'M.2': True})
				break
			i.update({'M.2': False})
		for part in name_part:
			if 'GB' in part or 'TB' in part:
				i.update({'capacity': part[:-2], 'unit': part[-2:]})
				final_ssd_list_with_price.append(i)

file = open('final_ssd.json', 'w')
json.dump(final_ssd_list_with_price, file)
file.close()


for item in final_ssd_list_with_price:
	print(item)