import json


def find_match_intel(cpu):
	if 'i' in cpu['name'] and '-' in cpu['name']:
		pro_id = cpu['name'].split(" ")[1].split("-")
		c_i = pro_id[0]
		gen = pro_id[1]
		intel_info = open('intel_processor_data.txt', 'r', encoding='utf-8')
		while True:
			l = intel_info.readline()
			if l == '':
				intel_info.close()
				return None
			# if l.split(":")[0] == 'Name':
			# 	print(pro_id, "     ", l)
			if c_i in l and gen in l:
				# print("Matched!")
				name = l.split(":")
				if name[0] == 'Name':
					cpu['name1'] = name[1]
				while True:
					l1 = intel_info.readline()
					if l1 == '\n':
						intel_info.close()
						return cpu
					info = l1.split(":")
					if info[0] == 'Processor Number':
						cpu['processor_number'] = info[1]
					elif info[0] == 'Sockets Supported':
						cpu['socket_supported'] = info[1]
					elif info[0] == 'Max Memory Size (dependent on memory type)':
						cpu['max_memory_sizer'] = info[1]
					elif info[0] == 'Memory Types':
						cpu['memory_type'] = info[1]
	else:
		return None


def find_match_amd(cpu):
	if 'Ryzen' in cpu['name']:
		pro_id = cpu['name'].split(" ")[2]
		pro_gen = cpu['name'].split(" ")[1]
		if pro_gen == "TR":
			pro_gen = "Threadripper"
		amd_info = open('amd_processor_data.txt', 'r', encoding='utf-8')
		while True:
			l = amd_info.readline()
			if l == '':
				amd_info.close()
				return None
			if pro_id in l and pro_gen in l:
				name = l.split(":")
				if name[0] == 'Name':
					cpu['name1'] = name[1]
				while True:
					l1 = amd_info.readline()
					if l1 == '\n':
						amd_info.close()
						return cpu
					info = l1.split(":")
					if info[0] == 'Product Line':
						cpu['processor_number'] = info[1]
					elif info[0] == 'CPU Socket':
						cpu['socket_supported'] = info[1]
					elif info[0] == 'System Memory Specification':
						cpu['max_memory_sizer'] = info[1]
					elif info[0] == 'System Memory Type':
						cpu['memory_type'] = info[1]
	else:
		return None


file_cpu_userbenchmark = open('cpu_info.json', 'r')
cpu_userbenchmark = json.load(file_cpu_userbenchmark)

# for i in cpu_userbenchmark:
# 	if i['price'][0] == '$':
# 		print(i)

# final_cpu_list = []
# for cpu in cpu_userbenchmark:
# 	if cpu['brand'] == 'Intel':
# 		final_cpu = find_match_intel(cpu)
# 		if final_cpu is not None:
# 			final_cpu_list.append(final_cpu)
# 	else:
# 		final_cpu = find_match_amd(cpu)
# 		if final_cpu is not None:
# 			final_cpu_list.append(final_cpu)

# for i in final_cpu_list:
# 	print(i)

# final_cpu_list_with_price = []
# for i in final_cpu_list:
# 	if i['price'][0] == '$':
# 		i['price'] == i['price']
# 		final_cpu_list_with_price.append(i)



for i in final_cpu_list_with_price:
	print(i)

# file = open('final_cpu.json', 'w', encoding='utf-8')
# json.dump(final_cpu_list_with_price, file)
# file.close()



# for i in cpu_userbenchmark:
# 	if i['brand'] == "AMD":
# 		if "Ryzen" in i['name'] :
# 			print(i['name'])
#
#

# count = 0
# with open('intel_processor_data.txt', 'r', encoding='utf-8') as f:
# 	for line in f:
# 		if "Name" in line:
# 			count += 1
# print(count)