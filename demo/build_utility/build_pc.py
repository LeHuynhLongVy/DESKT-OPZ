import json
# import data_test
from db_utility import GetItemFromDatabase
from pc import Pc
from utility import utility


def build(purpose, total_budget, cpu_list, board_list, gpu_list, ram_list, ssd_list, hdd_list, psu_list, case_list,
          overclock=None, req_ram=None, storage_ssd=None, storage_hdd=None, form_factor=None, kit=None, modular=None, psu_eff=None, preference=None):

	if isinstance(total_budget, (int, float, complex)):
		max_budget = total_budget
		budget = total_budget
	else:
		if total_budget[1] - total_budget[0] > 1000000:
			max_budget = total_budget[1]
			budget = total_budget
		else:
			max_budget = total_budget[1]
			budget = total_budget[1]

	# avail_cpu_list = utility.get_cpu_list(GetItemFromDatabase.get_cpu_list_from_db(), budget, purpose, overclock, preference)
	avail_cpu_list = utility.get_cpu_list(cpu_list, budget, purpose, overclock, preference)
	avail_gpu_list = gpu_list

	if purpose == 'desktop':
		avail_gpu_list = [None] + avail_gpu_list

	# avail_psu_list = utility.get_psu_list(GetItemFromDatabase.get_psu_list_from_db(), budget, modular, psu_eff, form_factor)
	avail_psu_list = utility.get_psu_list(psu_list, budget, modular, psu_eff, form_factor)

	avail_hdd_list = [None]
	if storage_hdd is not None:
		# avail_hdd_list = utility.get_hdd_list(GetItemFromDatabase.get_hdd_list_from_db(), storage_hdd)
		avail_hdd_list = utility.get_hdd_list(hdd_list, storage_hdd)
	pc_list = []
	# cpu_bo_list = utility.get_cpu_and_board(avail_cpu_list, GetItemFromDatabase.get_board_list_from_db(), overclock, form_factor)
	cpu_bo_list = utility.get_cpu_and_board(avail_cpu_list, board_list, overclock, form_factor)


	for cpu_bo in cpu_bo_list:
		current_cpu_bo = cpu_bo
		if req_ram is not None:
			if current_cpu_bo['cpu']['brand'] == 'Intel':
				max_mem_cpu = int(current_cpu_bo['cpu']['max_memory_sizer'].replace(' ', '').replace('GB', ''))
			else:
				max_mem_cpu = 128
			max_mem_board = int(current_cpu_bo['board']['max_memory_size'].replace(' ', '').replace('GB', ''))
			if int(req_ram[:-2]) > max_mem_cpu or int(req_ram[:-2]) > max_mem_board:
				continue
		if utility.get_item_price(current_cpu_bo) > max_budget:
			continue

		else:
			# avail_ram_list = utility.get_ram_list(data_test.ram_list, budget, purpose, cpu_bo, kit)
			avail_ram_list = utility.get_ram_list(ram_list, budget, purpose, cpu_bo, kit)
			for ram in avail_ram_list:
				current_ram = [ram]
				if req_ram is not None:
					size = utility.get_ram_total_size(ram)
					amount = int(req_ram[:-2]) - size
					if amount < 0:
						continue
					while (amount > 0):
						if utility.check_board_and_ram(current_cpu_bo['board'], current_ram, ram):
							current_ram = current_ram + [ram]
							amount = amount - size
						else:
							break
					if amount > 0:
						continue
				if (utility.get_item_price(current_cpu_bo) +
				    utility.get_item_price(current_ram)) > max_budget:
					continue

				else:
					# avail_ssd_list = utility.get_ssd_list(data_test.ssd_list, budget, purpose, cpu_bo, storage_ssd)
					avail_ssd_list = utility.get_ssd_list(ssd_list, budget, purpose, cpu_bo, storage_ssd)
					for ssd in avail_ssd_list:
						current_ssd = ssd
						if (utility.get_item_price(current_cpu_bo) +
						    utility.get_item_price(current_ram) +
						    utility.get_item_price(current_ssd)) > max_budget:
							continue

						else:
							for hdd in avail_hdd_list:
								if hdd is None:
									current_hdd = None
								else:
									current_hdd =  hdd
								if (utility.get_item_price(current_cpu_bo) +
								    utility.get_item_price(current_ram) +
								    utility.get_item_price(current_ssd) +
									utility.get_item_price(current_hdd)) > max_budget:
									continue
								else:
									for gpu in avail_gpu_list:
										current_gpu = gpu

										if current_gpu is None and "F" in current_cpu_bo['cpu']['name']:
											continue

										if (utility.get_item_price(current_cpu_bo) +
										    utility.get_item_price(current_ram) +
										    utility.get_item_price(current_ssd) +
											utility.get_item_price(current_hdd) +
										    utility.get_item_price(current_gpu)) > max_budget:
											continue

										else:
											done = False
											for psu in avail_psu_list:
												current_psu = psu
												if (utility.get_item_price(current_cpu_bo) +
												    utility.get_item_price(current_ram) +
												    utility.get_item_price(current_ssd) +
												    utility.get_item_price(current_hdd) +
												    utility.get_item_price(current_gpu) +
												    utility.get_item_price(current_psu)) > max_budget:
													continue
												else:
													# avail_case_list = utility.get_case_list(data_test.case_list, current_cpu_bo, current_psu, form_factor)
													avail_case_list = utility.get_case_list(case_list, current_cpu_bo, current_psu, form_factor)
													for case in avail_case_list:
														if (utility.get_item_price(current_cpu_bo) +
														    utility.get_item_price(current_ram) +
														    utility.get_item_price(current_ssd) +
														    utility.get_item_price(current_hdd) +
														    utility.get_item_price(current_gpu) +
														    utility.get_item_price(current_psu) +
															utility.get_item_price(case)) > max_budget:
															continue
														else:
															pc_list.append(Pc([current_cpu_bo['cpu'], current_cpu_bo['board'], current_gpu, current_ram, current_ssd, current_hdd, current_psu, case]))
															# print(len(pc_list))
															if len(pc_list) >= 10000:
																pc_list.sort(reverse=True, key=lambda x: utility.get_pc_score(x, purpose))
																# pc_list.sort(reverse=True, key=lambda x: float(utility.get_pc_score(x, purpose) / x.get_total_price()))
																return pc_list
															done = True
															break
													if done:
														break
	pc_list.sort(reverse=True, key=lambda x: utility.get_pc_score(x, purpose))
	# pc_list.sort(reverse=True, key=lambda x: float(utility.get_pc_score(x, purpose) / x.get_total_price()))
	return pc_list

def convert_for_web(pc_l, purpose):
	pc_list = []
	for i in pc_l:
		pc = []
		pc.append([{'id': 'cpu'}, i.cpu])
		pc.append([{'id': 'board'}, i.board])
		pc.append([{'id': 'gpu'}, i.gpu])
		pc.append([{'id': 'ram'}, i.ram]) #list
		pc.append([{'id': 'ssd'}, i.storage_ssd]) #item
		pc.append([{'id': 'hdd'}, i.storage_hdd]) #item or none
		pc.append([{'id': 'psu'}, i.psu])
		pc.append([{'id': 'case'}, i.case])
		pc.append([{'id': 'price'}, {'value': i.total_price}])
		pc.append([{'id': 'bench_score'}, {'value': utility.get_pc_score(i, purpose)}])
		pc_list.append(pc)
	return pc_list