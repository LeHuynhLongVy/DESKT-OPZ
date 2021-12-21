import json

file = open('hdd_info_formatted.json', 'r')
hdd_list = json.load(file)
file.close()

final_hdd_list_with_price = []
for i in hdd_list:
	if i['price'][0] == '$':
		name_part = i['name'].split(" ")
		for part in name_part:
			if 'GB' in part or 'TB' in part:
				i.update({'capacity': part[:-2], 'unit': part[-2:]})
				final_hdd_list_with_price.append(i)
#
# for item in final_hdd_list_with_price:
# 	print(item)

file = open('final_hdd.json', 'w')
json.dump(final_hdd_list_with_price,file)
file.close()