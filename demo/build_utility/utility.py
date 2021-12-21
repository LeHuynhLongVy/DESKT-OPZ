

class utility:
	@staticmethod
	def get_item_price(item):
		if item is not None:
			if isinstance(item, list):
				price = 0
				for i in item:
					if i is None:
						price = price + 0
					else:
						price = price + float(i['price'])
				return price
			else:
				return float(item['price'])
		else:
			return 0

	@staticmethod
	def get_cpu_list(cpu_list, total_budget, purpose=None, overclock=None, preference=None):
		c_list = list(cpu_list)
		cpu_price = 0
		avail_cpu = []
		if purpose == 'gaming':
			cpu_price = 0.2
		elif purpose == 'desktop':
			cpu_price = 0.4
		else:
			cpu_price = 0.3
		min_price = 0
		max_price = 0
		if isinstance(total_budget, (int, float, complex)):
			if (cpu_price + 0.1) * total_budget > 50000000:
				max_price = 50000000
				min_price = (50000000 * (cpu_price - 0.1)) / (cpu_price + 0.1)
			else:
				max_price = (cpu_price + 0.1) * total_budget
				min_price = (cpu_price - 0.1) * total_budget
		else:
			max_price = total_budget[1]
		c_list.sort(reverse=True, key=lambda x: float(x['bench']))
		for cpu in c_list:
			if utility.get_item_price(cpu) <= max_price:
				if preference is None:
					if overclock is None:
						avail_cpu.append(cpu)
					else:
						if not (utility.check_overclock_cpu(cpu) ^ overclock):
							avail_cpu.append(cpu)
				else:
					if preference == cpu['brand']:
						if overclock is None:
							avail_cpu.append(cpu)
						else:
							if not (utility.check_overclock_cpu(cpu) ^ overclock):
								avail_cpu.append(cpu)
			if len(avail_cpu) >= 30:
				break
		# avail_cpu.sort(reverse=True, key=lambda x: float(x['bench']))
		# if len(avail_cpu) > 30:
		# 	return avail_cpu[0:30]
		# if len(avail_cpu) == 0:
		# 	c_list.sort(key=lambda x: utility.get_item_price(x))
		# 	return c_list[:10]
		# else:
		return avail_cpu

	@staticmethod
	def get_cpu_and_board(cpu_list, board_list, overclock, form_factor):
		cpu_board_list = []
		suitable_boards = utility.get_board(board_list, overclock, form_factor)
		for cpu in cpu_list:
			count = 0
			for board in suitable_boards:
				if utility.check_compatible_cpu_board(cpu, board):
					count = count + 1
					cpu_board_list.append({'cpu': cpu, 'board': board, 'price': str(utility.get_item_price(cpu) + utility.get_item_price(board))})
					# if count >= 3:
					# 	break
		return cpu_board_list

	@staticmethod
	def check_overclock_board(board):
		if board['socket'].replace(' ', '') == 'AM4':
			if board['chipset'].replace(' ', '')[0] != 'A':
				return True
			else:
				return False
		elif board['chipset'].replace(' ', '')[0] == 'Z':
				return True
		else:
			return False


	@staticmethod
	def get_board(board_list, overclock, form_factor):
		final_board = []
		if overclock:
			temp1 = []
			for board in board_list:
				if utility.check_overclock_board(board):
					temp1.append(board)
			final_board = temp1
		else:
			final_board = board_list
		if form_factor is not None:
			temp2 = []
			for board in final_board:
				if form_factor == 'SFX' and board['form_factor'].replace(' ', '') != 'ATX' and board['form_factor'].replace(' ', '') != 'Extended-ATX':
					temp2.append(board)
				elif form_factor == 'ATX':
					temp2.append(board)
			final_board = temp2
		return final_board

	@staticmethod
	def check_compatible_cpu_board(cpu, board):
		board_socket = board['socket'].replace(" ", "")
		cpu_brand = cpu['brand']
		if cpu_brand == "Intel":
			cpu_gen = cpu['name'].split(" ")[1].split("-")[1]
			cpu_gen_1 = ''
			cpu_gen_2 = ''
			for n in cpu_gen:
				if n.isnumeric():
					cpu_gen_1 = cpu_gen_1 + n
				else:
					cpu_gen_2 = cpu_gen_2 + n
			if board_socket == "1151":
				if 6000 <= float(cpu_gen_1) < 8000:
					return True
				else:
					return False

			elif board_socket == "1151-v2":
				if 8000 <= float(cpu_gen_1) < 10000:
					return True
				else:
					return False

			elif board_socket == "1200":
				if 10000 <= float(cpu_gen_1) < 12000:
					return True
				else:
					return False

			elif board_socket == "2066":
				if cpu_gen_2 == "X" and 7000 <= float(cpu_gen_1):
					return True
				else:
					return False

		else:
			try:
				cpu_socket = cpu['socket_supported'].replace('\t', '').replace('\n', '').replace('\r', '')
				board_socket = board['socket'].replace(" ", "")
				# if cpu_socket == "AM4" and board_socket == "AM4":
				if cpu_socket == board_socket:
					return True
				else:
					return False
			except:
				return False

	@staticmethod
	def check_overclock_cpu(cpu):
		if cpu['brand'] == 'Intel':
			if 'K' in cpu['name']:
				return True
			else:
				return False
		else:
			if 'Ryzen' in cpu['name']:
				return True
			else:
				return False

	@staticmethod
	def get_gpu_list(gpu_list, total_budget, purpose):
		gpu_price = 0
		g_list = list(gpu_list)
		avail_gpu = []
		if purpose == 'gaming':
			gpu_price = 0.4
		elif purpose == 'desktop':
			gpu_price = 0.05
		else:
			gpu_price = 0.3
		if isinstance(total_budget, (int, float, complex)):
			max_price = (gpu_price + 0.1) * total_budget
		else:
			max_price = total_budget[1]
		g_list.sort(reverse=True, key=lambda x: float(x['bench']))
		count = 0
		for gpu in g_list:
			if utility.get_item_price(gpu) <= max_price:
				avail_gpu.append(gpu)
				count = count + 1
			if count >= 10:
				break
		# avail_gpu.sort(reverse=True, key=lambda x: float(x['bench']))
		# if len(avail_gpu) == 0:
		# 	g_list.sort(key=lambda x: utility.get_item_price(x))
		# 	return g_list[0:5]
		# else:
		return avail_gpu

	@staticmethod
	def get_ram_list(ram_list, total_budget, purpose, cpu_board, kit=None):
		ram_price = 0
		avail_ram = []
		r_list = list(ram_list)
		if purpose == 'gaming':
			ram_price = 0.1
		elif purpose == 'desktop':
			ram_price = 0.15
		else:
			ram_price = 0.1
		min_price = 0
		max_price = 0
		if isinstance(total_budget, (int, float, complex)):
			if (ram_price + 0.1) * total_budget > 20000000:
				max_price = 20000000
				min_price = (20000000 * (ram_price - 0.1)) / (ram_price + 0.1)
			else:
				max_price = (ram_price + 0.1) * total_budget
				min_price = (ram_price - 0.1) * total_budget
		else:
			max_price = total_budget[1]
		r_list.sort(reverse=True, key=lambda x: float(x['bench']))
		count = 0
		for ram in r_list:
			if utility.get_item_price(ram) <= max_price:
				if ram['memory_type'] == cpu_board['board']['memory_type'].replace(" ", ""):
					if int(cpu_board['board']['ram_slot'][1]) >= int(ram['quantity']):
						ram_total_size = float(ram['quantity']) * float(ram['size'].replace('GB', ''))
						# if cpu_board['cpu']['max_memory_sizer'].split(' ')[0].replace('\t', '').isnumeric():
						if cpu_board['cpu']['brand'] == 'AMD':
							max_mem = 128
						else:
							max_mem = float(cpu_board['cpu']['max_memory_sizer'].split(' ')[0].replace('\t', ''))
						if max_mem >= ram_total_size:
							if float(cpu_board['board']['max_memory_size'].replace(' ', '').replace('GB',
																									'')) >= ram_total_size:
								avail_ram.append(ram)
								count = count + 1
			if count >= 10:
				break

		temp = []
		if kit is not None:
			for ram in avail_ram:
				if kit:
					if int(ram['quantity']) > 1:
						temp.append(ram)
				else:
					if int(ram['quantity']) == 1:
						temp.append(ram)
			avail_ram = temp

		# avail_ram.sort(reverse=True, key=lambda x: float(x['bench']))
		# if len(avail_ram) == 0:
		# 	r_list.sort(key=lambda x: utility.get_item_price(x))
		# 	return r_list[0:5]
		# else:
		return avail_ram

	@staticmethod
	def get_ssd_list(ssd_list, total_budget, purpose, cpu_board=None, req_capacity=None):
		ssd_price = 0
		s_list = list(ssd_list)
		avail_ssd = []
		if purpose == 'gaming':
			ssd_price = 0.1
		elif purpose == 'desktop':
			ssd_price = 0.15
		else:
			ssd_price = 0.1
		min_price = 0
		max_price = 0
		if isinstance(total_budget, (int, float, complex)):
			if (ssd_price + 0.1) * total_budget > 30000000:
				max_price = 30000000
				min_price = (30000000 * (ssd_price - 0.1)) / (ssd_price + 0.1)
			else:
				max_price = (ssd_price + 0.1) * total_budget
				min_price = (ssd_price - 0.1) * total_budget
		else:
			max_price = total_budget[1]
		s_list.sort(reverse=True, key=lambda x: float(x['bench']))
		count = 0
		req = None
		if req_capacity is not None:
			if req_capacity[-2:].lower() == 'gb':
				req = int(req_capacity[:-2])
			else:
				req = int(req_capacity[:-2]) * 1000
		for ssd in ssd_list:
			if cpu_board['board']['supported_m2'] is not None and ssd['M.2']:
				if utility.get_item_price(ssd) <= max_price:
					if req is not None:
						capacity = utility.get_a_storage_capacity(ssd)
						if capacity > req + 50 or capacity < req - 50:
							continue
					avail_ssd.append(ssd)
					count = count + 1
				if count >= 10:
					break
		# avail_ssd.sort(reverse=True, key=lambda x: float(x['bench']))
		# if len(avail_ssd) == 0:
		# 	s_list.sort(key=lambda x: utility.get_item_price(x))
		# 	return s_list[0:5]
		# else:
		return avail_ssd

	@staticmethod
	def get_psu_list(psu_list, total_budget, modularity, efficiency=None, form_factor=None):
		temp = []
		if isinstance(total_budget, (int, float, complex)):
			budget = total_budget
		else:
			budget = total_budget[1]
		for psu in psu_list:
			if budget < 15000000 and psu['wattage'] <= 450:
				temp.append(psu)
			elif 15000000 <= budget < 30000000 and 450 < psu['wattage'] <= 550:
				temp.append(psu)
			elif 30000000 <= budget < 35000000 and 550 < psu['wattage'] <= 650:
				temp.append(psu)
			elif 35000000 <= budget < 80000000 and 650 < psu['wattage'] <= 750:
				temp.append(psu)
			elif 80000000 <= budget < 115000000 and 750 < psu['wattage'] <= 1000:
				temp.append(psu)
			elif budget >= 115000000 and 1000 < psu['wattage'] == 1200:
				temp.append(psu)

		if modularity is not None:
			temp1 = []
			for psu in temp:
				if modularity == 'Modular' and psu['modularity'] == 'FULL MODULAR':
					temp1.append(psu)
				elif modularity == 'Non-modular' and psu['modularity'] == 'NON MODULAR':
					temp1.append(psu)
			temp = temp1
		if efficiency is not None:
			temp2 = []
			for psu in temp:
				if psu['efficient rating'] == efficiency:
					temp2.append(psu)
			temp = temp2

		if form_factor is not None:
			temp3 = []
			for psu in temp:
				if form_factor == 'ATX':
					if 'ATX' in psu['form factor']:
						temp3.append(psu)
				else:
					if 'SFX' in psu['form factor']:
						temp3.append(psu)
			temp = temp3
		temp.sort(reverse=True, key=lambda x: utility.get_item_price(x))
		# if len(temp) >= 10:
		# 	return temp[0:10]
		# else:
		# 	return temp
		return temp

	@staticmethod
	def get_case_list(case_list, cpu_board=None, psu=None, form_factor=None):
		return_list = []
		temp = ''
		if form_factor is not None:
			if form_factor == 'SFX':
				temp = 'Micro-ATX'
			else:
				temp = 'ATX'
		for case in case_list:
			support_boards = case['board_supported'].split(',')
			if form_factor is None:
				if cpu_board['board']['form_factor'] == ' Extended-ATX ':
					for s_board in support_boards:
						if s_board.replace(' ', '') == 'Extended-ATX':
							return_list.append(case)
				elif cpu_board['board']['form_factor'] == ' ATX ' or psu['form factor'] == 'ATX':
					for s_board in support_boards:
						if s_board.replace(' ', '') == 'ATX':
							return_list.append(case)
				elif cpu_board['board']['form_factor'] == ' Micro-ATX ' and 'SFX' in psu['form factor']:
					for s_board in support_boards:
						if s_board.replace(' ', '') == 'Micro-ATX':
							return_list.append(case)
				elif cpu_board['board']['form_factor'] == ' Mini-ITX ' and 'SFX' in psu['form factor']:
					for s_board in support_boards:
						if s_board.replace(' ', '') == 'Mini-ITX':
							return_list.append(case)
			else:
				for s_board in support_boards:
					if s_board.replace(' ', '') == temp:
						return_list.append(case)
		return_list.sort(reverse=True, key=lambda x: utility.get_item_price(x))
		return return_list

	@staticmethod
	def get_pc_score(pc, purpose):
		cpu_bench = float(pc.cpu['bench'])
		gpu_bench = 0
		if pc.gpu is not None:
			gpu_bench = float(pc.gpu['bench'])
		ssd_bench = 0
		if pc.storage_ssd is not None:
			if isinstance(pc.storage_ssd, list):
				ssd_bench = float(pc.storage_ssd[0]['bench'])
			else:
				ssd_bench = float(pc.storage_ssd['bench'])
		ram_bench = float(pc.ram[0]['bench'])
		if int(pc.ram[0]['quantity']) *  int(pc.ram[0]['size'].replace('GB', '')) < 8:
			ram_bench = ram_bench / 2
		if purpose == 'desktop':
			return cpu_bench * 0.73 + gpu_bench * 0.14 + ssd_bench * 0.1 + ram_bench * 0.03
		elif purpose == 'gaming':
			return cpu_bench * 0.24 + gpu_bench * 0.64 + ssd_bench * 0.55 + ram_bench * 0.07
		elif purpose == 'workstation':
			return cpu_bench * 0.54 + gpu_bench * 0.34 + ssd_bench * 0.05 + ram_bench * 0.07

	@staticmethod
	def get_supported_cpu(board):
		if board['socket'] == ' AM4 ':
			return 'AMD'
		else:
			return 'Intel'

	@staticmethod
	def get_ram_total_size(ram):
		return int(ram['quantity']) *  int(ram['size'].replace('GB', ''))

	@staticmethod
	def get_storage_slot(board):
		slot = {'SATA': 0, 'M.2_sata': 0, 'M.2_nvme': 0}
		parts = board['storage_type'].split(',')
		for part in parts:
			if 'x' in part:
				detail = part.split('x')
				amount = int(detail[0].replace(' ',''))
				if 'M.2' in detail[1]:
					if 'NVMe' in detail[1]:
						slot['M.2_nvme'] = slot['M.2_nvme'] + amount
					else:
						slot['M.2_sata'] = slot['M.2_sata'] + amount
				else:
					slot['SATA'] = slot['SATA'] + amount
		return slot

	@staticmethod
	def check_fit_psu_case(psu, case):
		sp_boards = case['board_supported'].split(',')
		if psu['form factor'] == 'ATX':
			for i in sp_boards:
				if i.replace(' ', '') == 'ATX' or i.replace(' ', '') == 'Extended-ATX':
					return True
			return False
		elif psu['form factor'] == 'SFX':
			for i in sp_boards:
				if i.replace(' ', '') == 'Mini-ITX' or i.replace(' ', '') == 'Micro-ATX':
					return True
			return False
		else:
			return True

	@staticmethod
	def check_fit_board_case(board, case):
		sp_boards = case['board_supported'].split(',')
		b = board['form_factor'].replace(' ', '')
		for sp in sp_boards:
			if b == sp.replace(' ', ''):
				return True
		return False

	@staticmethod
	def get_a_storage_capacity(storage):
		if storage['unit'] == 'GB':
			return int(storage['capacity'])
		elif storage['unit'] == 'TB':
			return int(storage['capacity']) * 1000

	@staticmethod
	def get_recommend_list(current_pc, budget, ssd_list, hdd_list):
		recommend_list = {'ram': None, 'ssd': None, 'hdd': None}
		left_over = budget - current_pc.get_total_price()
		if current_pc.price(current_pc.ram) < left_over:
			recommend_list['ram'] = current_pc.ram[0]

	@staticmethod
	def check_board_and_ram(board, ram_list, new_ram):
		ram_slot = int(board['ram_slot'][1])
		slot_taken = 0
		for r in ram_list:
			slot_taken = slot_taken + int(r['quantity'])
		if ram_slot - slot_taken < int(new_ram['quantity']):
			# print("Current board does not have enough ram slot")
			return False
		else:
			return True

	@staticmethod
	def get_hdd_list(hdd_list, req_capacity):
		return_list = []
		if req_capacity[-2:].lower() == 'gb':
			req = int(req_capacity[:-2])
		else:
			req = int(req_capacity[:-2]) * 1000
		for hdd in hdd_list:
			capacity = utility.get_a_storage_capacity(hdd)
			if capacity > req + 50 or capacity < req - 50:
				continue
			return_list.append(hdd)
		return return_list
