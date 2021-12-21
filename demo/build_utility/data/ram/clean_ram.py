import json

file = open('ram_info.json', 'r', encoding='utf-8')
ram_list = json.load(file)

first_list = []
for i in ram_list:
	if i['price'][0] == '$' and 'DDR' in i['name'] and 'UDIMM' not in i['name']:
		first_list.append(i)

for i in first_list:
	name_part = i['name'].split(" ")
	amount = name_part[-1].split('x')
	addition = {
		"memory_type": name_part[-4],
		"ram_bus": name_part[-3],
		"ram_cas": name_part[-2],
		"quantity": amount[0],
		'size': amount[1]
	}
	i.update(addition)

file = open('final_ram.json', 'w', encoding='utf-8')
json.dump(first_list, file)
file.close()