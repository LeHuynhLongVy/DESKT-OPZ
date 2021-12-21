from pc import Pc
from utility import utility
# import data_test
# from db_utility import GetItemFromDatabase


class BuildStepByStep():
	def __init__(self, builded_pc=None):
		if builded_pc is None:
			self.pc = Pc()
		else:
			self.pc = builded_pc

	# @staticmethod
	# def get_full_cpu_list():
	# 	# return data_test.cpu_list
	# 	return GetItemFromDatabase.get_cpu_list_from_db()
	#
	# @staticmethod
	# def get_full_board_list():
	# 	# return data_test.board_list
	# 	return GetItemFromDatabase.get_board_list_from_db()
	#
	# @staticmethod
	# def get_full_ram_list():
	# 	# return data_test.ram_list
	# 	return GetItemFromDatabase.get_ram_list_from_db()
	#
	# @staticmethod
	# def get_full_ssd_list():
	# 	# return data_test.ssd_list
	# 	return GetItemFromDatabase.get_ssd_list_from_db()
	#
	# @staticmethod
	# def get_full_hdd_list():
	# 	# return data_test.hdd_list
	# 	return GetItemFromDatabase.get_hdd_list_from_db()
	#
	# @staticmethod
	# def get_full_gpu_list():
	# 	info = GetItemFromDatabase.get_gpu_list_from_db()
	# 	# data_test.gpu_list.sort(reverse=True, key=lambda x: float(x['bench']))
	# 	info.sort(reverse=True, key=lambda x: float(x['bench']))
	# 	# return data_test.gpu_list
	# 	return info
	#
	# @staticmethod
	# def get_full_psu_list():
	# 	# return data_test.psu_list
	# 	return GetItemFromDatabase.get_psu_list_from_db()
	#
	# @staticmethod
	# def get_full_case_list():
	# 	# return data_test.case_list
	# 	return GetItemFromDatabase.get_case_list_from_db()

	def get_cpu_list(self, cpu_list, overclock=None, brand=None):
		final_list = []
		# cpu_list = GetItemFromDatabase.get_cpu_list_from_db()
		for cpu in cpu_list:
			if self.pc.board is None:
				if overclock is not None:
					if overclock ^ utility.check_overclock_cpu(cpu):
						continue
				if brand is not None:
					if brand != cpu['brand']:
						continue
				final_list.append(cpu)
			else:
				if brand is not None:
					if self.pc.board['socket'] == ' AM4 ':
						if brand != 'AMD':
							print('current board not support this brand of cpu')
							return []
					else:
						if brand != 'Intel':
							print('current board not support this brand of cpu')
							return []
				if overclock is not None:
					if overclock:
						if not utility.check_overclock_board(self.pc.board):
							print('current board does not support overclocking')
							return []
						else:
							if not utility.check_overclock_cpu(cpu):
								continue
					else:
						if utility.check_overclock_cpu(cpu):
							continue
				if not utility.check_compatible_cpu_board(cpu, self.pc.board):
					continue
				final_list.append(cpu)
		final_list.sort(reverse=True, key=lambda x: float(x['bench']))
		return final_list

	def add_cpu(self, cpu):
		self.pc.cpu = cpu
		return True

	def remove_cpu(self):
		self.pc.cpu = None
		return True

	def get_board_list(self, board_list,cpu_supported=None, overclock=None, form_factor=None):
		final_list = []
		# board_list = GetItemFromDatabase.get_board_list_from_db()
		for board in board_list:
			if self.pc.cpu is None:
				if overclock is not None:
					if overclock ^ utility.check_overclock_board(board):
						continue
				if cpu_supported is not None:
					if cpu_supported != utility.get_supported_cpu(board):
						continue
				if form_factor is not None:
					if form_factor != board['form_factor'].replace(' ', ''):
						continue
				final_list.append(board)
			else:
				if overclock is not None:
					if overclock:
						if not utility.check_overclock_cpu(self.pc.cpu):
							print('Note: the current cpu doesn not support overclocking')
						if not utility.check_overclock_board(board):
							continue
					else:
						if utility.check_overclock_board(board):
							continue
				if cpu_supported is not None:
					if cpu_supported != self.pc.cpu['brand']:
						print("board does not match with the current cpu")
						return []
				if form_factor is not None:
					if form_factor != board['form_factor'].replace(' ', ''):
						continue
				if not utility.check_compatible_cpu_board(self.pc.cpu, board):
					continue
				final_list.append(board)
		final_list.sort(reverse=True, key=lambda x: utility.get_item_price(x))
		return final_list

	def add_board(self, board):
		self.pc.board = board
		self.pc.ram = None
		self.pc.storage_ssd = None
		self.pc.storage_hdd = None
		return True

	def remove_board(self):
		self.pc.board = None
		self.pc.ram = None
		self.pc.storage_ssd = None
		self.pc.storage_hdd = None
		return True

	def get_ram_list(self, ram_list, kit=None, amount=None):
		return_list = []
		# ram_list = GetItemFromDatabase.get_ram_list_from_db()
		for ram in ram_list:
			if kit is not None:
				if kit:
					if int(ram['quantity']) < 2:
						continue
				else:
					if int(ram['quantity']) >= 2:
						continue
			if amount is not None:
				if float(ram['quantity']) * float(ram['size'].replace('GB', '')) != amount:
					continue
			if self.pc.board is not None:
				if not self.pc.board['memory_type'].replace(' ', '') in ram['name']:
					continue
			return_list.append(ram)
		return_list.sort(reverse=True, key=lambda x: float(x['bench']))
		return return_list

	def add_ram(self, ram):
		if self.pc.board is not None:
			ram_slot = int(self.pc.board['ram_slot'][1])
			slot_taken = 0
			if self.pc.ram is not None:
				for r in self.pc.ram:
					slot_taken = slot_taken + int(r['quantity'])
			if ram_slot - slot_taken < int(ram['quantity']):
				print("Current board does not have enough ram slot")
				return {'stat': False, 'mess': "Current board does not have enough ram slot"}
		max_size = self.get_max_memory_size()
		return_mess = {'stat': True, 'mess': ""}
		if max_size is not None:
			if max_size < self.get_current_ram_size() + utility.get_ram_total_size(ram):
				print("note: current ram total size has exceed the maximum supported size")
				return_mess['mess'] = "current ram total size has exceed the maximum supported size"
		if self.pc.ram is None:
			self.pc.ram = [ram]
		else:
			self.pc.ram = self.pc.ram + [ram]
		return return_mess

	def remove_ram(self, pos=None):
		if self.pc.ram is None:
			print("ram is already None")
			return {'stat': True, "mess": "ram is already None"}
		if len(self.pc.ram) == 1:
			self.pc.ram = None
			return {'stat': True, "mess": "successfully remove the last ram"}
		else:
			if pos is None:
				del self.pc.ram[len(self.pc.ram) - 1]
				return {'stat': True, "mess": "successfully remove ram"}
			else:
				try:
					del self.pc.ram[pos]
				except IndexError:
					print("WRONG INDEX!")
					return {'stat': False, "mess": "WRONG INDEX!"}
				return {'stat': True, "mess": "successfully remove ram"}

	def get_max_memory_size(self):
		if self.pc.cpu is not None:
			max_cpu = int(self.pc.cpu['max_memory_sizer'].replace(' ', '').replace('GB', '')) if self.pc.cpu[
				                                                                                     'brand'] == 'Intel' else 128
		else:
			max_cpu = None
		if self.pc.board is not None:

			max_board = int(self.pc.board['max_memory_size'].replace(' ', '').replace('GB', ''))
		else:
			max_board = None
		if max_cpu is None and max_board is None:
			return None
		elif max_cpu is None and max_board is not None:
			return max_cpu
		elif max_cpu is not None and max_board is None:
			return max_board
		else:
			if max_cpu >= max_board:
				return max_board
			else:
				return max_cpu

	def get_current_ram_size(self):
		if self.pc.ram is None:
			return 0
		else:
			size = 0
			for r in self.pc.ram:
				size = size + utility.get_ram_total_size(r)
			return size

	def get_ssd_list(self, ssd_list,amount=None):
		return_list = []
		temp = []
		# ssd_list = GetItemFromDatabase.get_ssd_list_from_db()
		for ssd in ssd_list:
			if self.pc.board is not None:
				if ssd['M.2'] and self.pc.board['supported_m2'] is None:
					continue
			if amount is not None:
				unit = amount[-2:].lower()
				cap = int(amount[:-2])
				ssd_cap = utility.get_a_storage_capacity(ssd)
				if unit == 'tb':
					cap = cap * 1000
				if cap == ssd_cap:
					temp.append(ssd)
					continue
				elif ssd_cap > cap + 250 or ssd_cap < cap - 250:
					continue
			return_list.append(ssd)
		temp.sort(reverse=True, key=lambda x: float(x['bench']))
		return_list.sort(reverse=True, key=lambda x: float(x['bench']))
		return_list = temp + return_list
		return return_list

	def get_hdd_list(self, hdd_list,amount=None):
		return_list = []
		temp = []
		# hdd_list = GetItemFromDatabase.get_hdd_list_from_db()
		for hdd in hdd_list:
			if amount is not None:
				unit = amount[-2:].lower()
				cap = int(amount[:-2])
				hdd_cap = utility.get_a_storage_capacity(hdd)
				if unit == 'tb':
					cap = cap * 1000
				if cap == hdd_cap:
					temp.append(hdd)
					continue
				elif hdd_cap > cap + 250 or hdd_cap < cap - 250:
					continue
			return_list.append(hdd)
		temp.sort(reverse=True, key=lambda x: float(x['bench']))
		return_list.sort(reverse=True, key=lambda x: float(x['bench']))
		return_list = temp + return_list
		return return_list

	def add_ssd(self, ssd):
		if self.pc.board is not None:
			if ssd['M.2']:
				avail = self.get_available_storage_slot()[1]
			else:
				avail = self.get_available_storage_slot()[0]
			if avail > 0:
				if self.pc.storage_ssd is None:
					self.pc.storage_ssd = [ssd]
				else:
					self.pc.storage_ssd = self.pc.storage_ssd + [ssd]
				return {'stat': True, 'mess': ""}
			else:
				print("current board cannot support more ssd")
				return {'stat': False, 'mess': "current board cannot support more ssd"}
		else:
			return {'stat': True, 'mess': "add ssd without board"}

	def add_hdd(self, hdd):
		if self.pc.board is not None:
			if self.get_available_storage_slot()[0] > 0:
				if self.pc.storage_hdd is None:
					self.pc.storage_hdd = [hdd]
				else:
					self.pc.storage_hdd = self.pc.storage_hdd + [hdd]
				return {'stat': True, 'mess': ""}
			else:
				print("current board cannot support more hdd")
				return {'stat': False, 'mess': "current board cannot support more hdd"}
		else:
			return {'stat': True, 'mess': "add hdd without board"}

	def remove_ssd(self, pos=None):
		if self.pc.storage_ssd is None:
			print("ssd is already None")
			return {'stat': True, "mess": "ssd is already None"}
		if len(self.pc.storage_ssd) == 1:
			self.pc.storage_ssd = None
			return {'stat': True, "mess": "successfully remove the last ssd"}
		else:
			if pos is None:
				del self.pc.storage_ssd[len(self.pc.storage_ssd) - 1]
				return {'stat': True, "mess": "successfully remove ssd"}
			else:
				try:
					del self.pc.storage_ssd[pos]
				except IndexError:
					print("WRONG INDEX!")
					return {'stat': False, "mess": "WRONG INDEX!"}
				return {'stat': True, "mess": "successfully remove ssd"}

	def remove_hdd(self, pos=None):
		if self.pc.storage_hdd is None:
			print("hdd is already None")
			return {'stat': True, "mess": "hdd is already None"}
		if len(self.pc.storage_hdd) == 1:
			self.pc.storage_hdd = None
			return {'stat': True, "mess": "successfully remove the last hdd"}
		else:
			if pos is None:
				del self.pc.storage_hdd[len(self.pc.storage_hdd) - 1]
				return {'stat': True, "mess": "successfully remove hdd"}
			else:
				try:
					del self.pc.storage_hdd[pos]
				except IndexError:
					print("WRONG INDEX!")
					return {'stat': False, "mess": "WRONG INDEX!"}
				return {'stat': True, "mess": "successfully remove hdd"}

	def get_available_storage_slot(self):
		if self.pc.board is None:
			print('board is not picked dont care :))')
			return
		else:
			max_slot = utility.get_storage_slot(self.pc.board)
			avail_sata = max_slot['SATA']
			avail_m2 = max_slot['M.2_nvme']
			if self.pc.storage_hdd is not None:
				avail_sata = avail_sata - len(self.pc.storage_hdd)
			if self.pc.storage_ssd is not None:
				for ssd in self.pc.storage_ssd:
					if ssd['M.2']:
						avail_m2 = avail_m2 - 1
					else:
						avail_sata = avail_sata - 1
			return [avail_sata, avail_m2]

	def get_psu_list(self, psu_list,form_factor=None, watt=None):
		return_list = []
		# psu_list = GetItemFromDatabase.get_psu_list_from_db()
		if self.pc.case is None:
			return_list = list(psu_list)
		else:
			return_list = []
			sp_boards = self.pc.case['board_supported'].split(',')
			for psu in psu_list:
				if psu['form factor'] == 'ATX':
					for i in sp_boards:
						if i.replace(' ', '') == 'ATX' or i.replace(' ', '') == 'Extended-ATX':
							return_list.append(psu)
							continue
				elif psu['form factor'] == 'SFX':
					for i in sp_boards:
						if i.replace(' ', '') == 'Mini-ITX' or i.replace(' ', '') == 'Micro-ATX':
							return_list.append(psu)
							continue
				else:
					return_list.append(psu)
		if form_factor is not None:
			temp = []
			for psu in return_list:
				if form_factor in psu['form factor']:
					temp.append(psu)
			return_list = temp
		if watt is not None:
			temp = []
			for psu in return_list:
				if watt - 300 <= psu['wattage'] <= watt + 300:
					temp.append(psu)
			return_list = temp
		return_list.sort(reverse=True, key=lambda x: utility.get_item_price(x))
		return return_list

	def add_psu(self, psu):
		self.pc.psu = psu
		return {'stat': True, 'mess': "0"}

	def remove_psu(self):
		self.pc.psu = None

	def get_case_list(self, case_list, form_factor=None):
		return_list = []
		# if in_case_list is not None:
		# 	case_list = list(in_case_list)
		for case in case_list:
			if self.pc.board is not None:
				if not utility.check_fit_board_case(self.pc.board, case):
					continue
			if self.pc.psu is not None:
				if not utility.check_fit_psu_case(self.pc.psu, case):
					continue
			return_list.append(case)
		if form_factor is not None:
			temp = []
			for case in return_list:
				if not form_factor in case['board_supported']:
					continue
				temp.append(case)
			return_list = temp

		return_list.sort(reverse=True, key=lambda x: utility.get_item_price(x))
		return return_list

	def add_case(self, case):
		self.pc.case = case
		return {'stat': True, 'mess': "0"}

	def remove_case(self):
		self.pc.case = None

	def add_gpu(self, gpu):
		self.pc.gpu = gpu
		return True

	def remove_gpu(self):
		self.pc.gpu = None

	def print(self):
		print(str(self.pc))

	def get_pc(self):
		return self.pc

	def get_score(self, purpose=None):
		if self.pc.cpu is not None:
			if self.pc.board is not None:
				if self.pc.ram is not None:
					if purpose is None:
						return [utility.get_pc_score(self.pc, 'desktop'), utility.get_pc_score(self.pc, 'gaming'), utility.get_pc_score(self.pc, 'workstation')]
					else:
						return utility.get_pc_score(self.pc, purpose)
		return None

