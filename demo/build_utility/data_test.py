import json
from pc import Pc
from utility import utility
import sys, os


file_path = os.path.join(sys.path[0], 'demo', 'build_utility', 'data')

f = open(os.path.join(file_path, 'cpu', 'final_cpu.json'), 'r')
cpu_list = json.load(f)
f.close()

f = open(os.path.join(file_path, 'gpu', 'final_gpu.json'), 'r')
gpu_list = json.load(f)
f.close()

f = open(os.path.join(file_path, 'hdd', 'final_hdd.json'), 'r')
hdd_list = json.load(f)
f.close()

f = open(os.path.join(file_path, 'motherboard', 'phong_vu_data_formated.json'), 'r')
board_list = json.load(f)
f.close()

f = open(os.path.join(file_path, 'psu', 'final_psu.json'), 'r')
psu_list = json.load(f)
f.close()

f = open(os.path.join(file_path, 'ram', 'final_ram.json'), 'r')
ram_list = json.load(f)
f.close()

f = open(os.path.join(file_path, 'ssd', 'final_ssd.json'), 'r')
ssd_list = json.load(f)
f.close()

f = open(os.path.join(file_path, 'case', 'final_case.json'), 'r')
case_list = json.load(f)
f.close()

for i in cpu_list:
	i['price'] = str((float(i['price'][1:].replace(",","")) * 23000))
for i in gpu_list:
	i['price'] = str((float(i['price'][1:].replace(",","")) * 23000))
for i in ssd_list:
	i['price'] = str((float(i['price'][1:].replace(",","")) * 23000))
for i in hdd_list:
	i['price'] = str((float(i['price'][1:].replace(",","")) * 23000))
for i in ram_list:
	i['price'] = str((float(i['price'][1:].replace(",","")) * 23000))

remove_board = []
for i in board_list:
	if i['max_memory_size'] is None:
		remove_board.append(i)
for i in remove_board:
	board_list.remove(i)
