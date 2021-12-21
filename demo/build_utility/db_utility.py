import sqlite3
from google.cloud import storage
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import psycopg2
import math
from utility import utility


class GetItemFromDatabase:
	database = psycopg2.connect(host="35.198.200.244", port=5432, database="thesis", user="postgres", password="123")


	@staticmethod
	def get_link(link_list):
		link_dic = {
			'manufacturer': None,
			'gearvn': None,
			'phongvu': None
		}
		if link_list is None:
			return link_dic
		links = link_list.split(' ')
		for link in links:
			if link == '':
				continue
			if 'gearvn.com' in link:
				link_dic['gearvn'] = link
			elif 'phongvu.vn' in link:
				link_dic['phongvu'] = link
			else:
				link_dic['manufacturer'] = link
		return link_dic

	@staticmethod
	def get_cpu_list_from_db(id_list=None):
		cursor = GetItemFromDatabase.database.cursor()
		if id_list is None:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."CPU" 
			"""
		else:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."CPU" 
				WHERE cpu_id IN {tuple(id_list)}
			"""
		cursor.execute(op)
		data_list = cursor.fetchall()
		cursor.close()
		return GetItemFromDatabase.convert_cpu_db_to_dic(data_list)

	@staticmethod
	def convert_cpu_db_to_dic(data_list):
		return_list = []
		for item in data_list:
			return_list.append({
				'id': item[0],
				'brand': item[1],
				'name': item[2],
				'link': item[3],
				'user_rating': item[4],
				'value': item[5],
				'bench': item[6],
				'price': item[7],
				'name1': item[8],
				'processor_number': item[9],
				'max_memory_sizer': item[10],
				'memory_type': item[11],
				'socket_supported': item[12],
				'link1': GetItemFromDatabase.get_link(item[13]),
				'img': item[14]
			})
		return return_list

	@staticmethod
	def get_board_list_from_db(id_list=None):
		cursor = GetItemFromDatabase.database.cursor()
		if id_list is None:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."Motherboard" 
			"""
		else:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."Motherboard" 
				WHERE mb_id IN {tuple(id_list)}
			"""
		cursor.execute(op)
		data_list = cursor.fetchall()
		cursor.close()
		return GetItemFromDatabase.convert_board_db_to_dic(data_list)

	@staticmethod
	def convert_board_db_to_dic(data_list):
		return_list = []
		for item in data_list:
			if item[8] is not None:
				return_list.append({
					'id': item[0],
					'name': item[1],
					'socket': item[2],
					'chipset': item[3],
					'price': item[4],
					'form_factor': item[5],
					'ram_slot': item[6],
					'memory_type': item[7],
					'max_memory_size': item[8],
					'ram_bus': item[9],
					'storage_type': item[10],
					'supported_m2': item[11],
					'out_put': item[12],
					'pci': item[13],
					'link1': GetItemFromDatabase.get_link(item[14]),
					'img': item[15]
				})
		return return_list

	@staticmethod
	def get_gpu_list_from_db(id_list=None):
		cursor = GetItemFromDatabase.database.cursor()
		if id_list is None or len(id_list) == 0:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."GPU" 
			"""
		else:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."GPU" 
				WHERE gpu_id IN {tuple(id_list)}
			"""
		cursor.execute(op)
		data_list = cursor.fetchall()
		cursor.close()
		return GetItemFromDatabase.convert_gpu_db_to_dic(data_list)

	@staticmethod
	def convert_gpu_db_to_dic(data_list):
		return_list = []
		for item in data_list:
			return_list.append({
				'id': item[0],
				'brand': item[1],
				'name': item[2],
				'link': item[3],
				'user_rating': item[4],
				'value': item[5],
				'bench': item[6],
				'price': item[7],
				'link1': GetItemFromDatabase.get_link(item[8]),
				'img': item[9]
			})
		return return_list

	@staticmethod
	def get_ram_list_from_db(id_list=None):
		cursor = GetItemFromDatabase.database.cursor()
		if id_list is None:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."RAM" 
			"""
		else:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."RAM" 
				WHERE ram_id IN {tuple(id_list)}
			"""
		cursor.execute(op)
		data_list = cursor.fetchall()
		cursor.close()
		return GetItemFromDatabase.convert_ram_db_to_dic(data_list)

	@staticmethod
	def convert_ram_db_to_dic(data_list):
		return_list = []
		for item in data_list:
			return_list.append({
				'id': item[0],
				'brand': item[1],
				'name': item[2],
				'link': item[3],
				'user_rating': item[4],
				'value': item[5],
				'bench': item[6],
				'price': item[7],
				'memory_type': item[8],
				'ram_bus': item[9],
				'ram_cas': item[10],
				'quantity': item[11],
				'size': item[12],
				'link1': GetItemFromDatabase.get_link(item[13]),
				'img': item[14]
			})
		return return_list

	@staticmethod
	def get_ssd_list_from_db(id_list=None):
		cursor = GetItemFromDatabase.database.cursor()
		if id_list is None:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."SSD" 
			"""
		else:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."SSD" 
				WHERE ssd_id IN {tuple(id_list)}
			"""
		cursor.execute(op)
		data_list = cursor.fetchall()
		cursor.close()
		return GetItemFromDatabase.convert_ssd_db_to_dic(data_list)

	@staticmethod
	def convert_ssd_db_to_dic(data_list):
		return_list = []
		for item in data_list:
			return_list.append({
				'id': item[0],
				'brand': item[1],
				'name': item[2],
				'link': item[3],
				'user_rating': item[4],
				'value': item[5],
				'bench': item[6],
				'price': item[7],
				'M.2': item[8],
				'capacity': item[9],
				'unit': item[10],
				'link1': GetItemFromDatabase.get_link(item[11]),
				'img': item[12]
			})
		return return_list

	@staticmethod
	def get_hdd_list_from_db(id_list=None):
		cursor = GetItemFromDatabase.database.cursor()
		if id_list is None:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."HDD" 
			"""
		else:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."HDD" 
				WHERE hdd_id IN {tuple(id_list)}
			"""
		cursor.execute(op)
		data_list = cursor.fetchall()
		cursor.close()
		return GetItemFromDatabase.convert_hdd_db_to_dic(data_list)

	@staticmethod
	def convert_hdd_db_to_dic(data_list):
		return_list = []
		for item in data_list:
			return_list.append({
				'id': item[0],
				'brand': item[1],
				'name': item[2],
				'link': item[3],
				'user_rating': item[4],
				'value': item[5],
				'bench': item[6],
				'price': item[7],
				'capacity': item[8],
				'unit': item[9],
				'link1': GetItemFromDatabase.get_link(item[10]),
				'img': item[11]
			})
		return return_list

	@staticmethod
	def get_psu_list_from_db(id_list=None):
		cursor = GetItemFromDatabase.database.cursor()
		if id_list is None:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."PSU" 
			"""
		else:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."PSU" 
				WHERE psu_id IN {tuple(id_list)}
			"""
		cursor.execute(op)
		data_list = cursor.fetchall()
		cursor.close()
		return GetItemFromDatabase.convert_psu_db_to_dic(data_list)

	@staticmethod
	def convert_psu_db_to_dic(data_list):
		return_list = []
		for item in data_list:
			return_list.append({
				'id': item[0],
				'brand': item[1],
				'name': item[2],
				'efficient rating': item[3],
				'wattage': int(item[4]),
				'protection': item[5],
				'modularity': item[6],
				'form factor': item[7],
				'price': item[8],
				'link1': GetItemFromDatabase.get_link(item[9]),
				'img': item[10]
			})
		return return_list

	@staticmethod
	def get_case_list_from_db(id_list=None):
		cursor = GetItemFromDatabase.database.cursor()
		if id_list is None:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."CASE" 
			"""
		else:
			op = f""" 
				SELECT * 
				FROM "PC_Builder"."CASE" 
				WHERE case_id IN {tuple(id_list)}
			"""
		cursor.execute(op)
		data_list = cursor.fetchall()
		cursor.close()
		return GetItemFromDatabase.convert_case_db_to_dic(data_list)

	@staticmethod
	def convert_case_db_to_dic(data_list):
		return_list = []
		for item in data_list:
			return_list.append({
				'id': item[0],
				'name': item[1],
				'case_type': item[2],
				'board_supported': item[3],
				'price': item[4],
				'link1': GetItemFromDatabase.get_link(item[6]),
				'img': item[7]
			})
		return return_list

	# @staticmethod
	# def check_pc_in_pc_usage_table(pc_session_list):
	# 	cursor = GetItemFromDatabase.database.cursor()
	# 	cpu_id = pc_session_list['cpu']['id']
	# 	mb_id = pc_session_list['board']['id']
	# 	gpu_id = pc_session_list['gpu']['id']
	# 	if gpu_id is None:
	# 		gpu_id = "NULL"
	# 		gpu_statement = "gpu_id is NULL"
	# 	else:
	# 		gpu_statement = f"gpu_id = {gpu_id}"
	# 	op1 = f"""
	# 				SELECT * FROM "PC_Builder"."Main_comp"
	# 				WHERE cpu_id = {cpu_id} and mb_id = {mb_id} and {gpu_statement};
	# 			"""
	# 	cursor.execute(op1)
	# 	check = cursor.fetchall()
	# 	if len(check) == 0:
	# 		op2 = f"""
	# 				INSERT INTO "PC_Builder"."Main_comp" ("cpu_id", "mb_id", "gpu_id")
	# 				VALUES ({cpu_id}, {mb_id}, {gpu_id});
	# 			"""
	# 		cursor.execute(op2)
	# 		GetItemFromDatabase.database.commit()
	# 		cursor.execute(op1)
	# 		main_comp_id = cursor.fetchall()[0][0]
	# 		print("successfully insert new main comp with id: ", main_comp_id)
	# 		cursor.close()
	# 		return main_comp_id
	# 	else:
	# 		print("PC already in the table with the id: ", check[0][0])
	# 		cursor.close()
	# 		return check[0][0]

	@staticmethod
	def insert_to_rec_table(pc_session_list,interact_point, point_type):
		cursor = GetItemFromDatabase.database.cursor()
		cpu_id = pc_session_list['cpu']['id']
		mb_id = pc_session_list['board']['id']
		gpu_id = pc_session_list['gpu']['id']
		if interact_point == 0:
			point = 50
		else:
			point = 50 * (1 / (interact_point * (interact_point + 1)))
		if gpu_id is None:
			gpu_id = "NULL"
			gpu_statement = "gpu_id is NULL"
		else:
			gpu_statement = f"gpu_id = {gpu_id}"
		op1 = f"""
			SELECT * FROM "PC_Builder"."Main_comp"
			WHERE cpu_id = {cpu_id} and mb_id = {mb_id} and {gpu_statement};
		"""
		cursor.execute(op1)
		check = cursor.fetchall()
		if len(check) == 0:
			op2 = f"""
					INSERT INTO "PC_Builder"."Main_comp" ("cpu_id", "mb_id", "gpu_id", "{point_type}_score", "{point_type}_usage")
					VALUES ({cpu_id}, {mb_id}, {gpu_id}, {point}, 1);
				"""
			cursor.execute(op2)
			GetItemFromDatabase.database.commit()
			cursor.execute(op1)
			main_comp_id = cursor.fetchall()[0][0]
			print("successfully insert new main comp with id: ", main_comp_id)
		else:
			op3 = f"""
					UPDATE "PC_Builder"."Main_comp" SET "{point_type}_score" =  COALESCE("{point_type}_score", 0) +  {point},
														"{point_type}_usage" =  COALESCE("{point_type}_usage", 0) +  1
					WHERE cpu_id = {cpu_id} and mb_id = {mb_id} and {gpu_statement};
				"""
			cursor.execute(op3)
			GetItemFromDatabase.database.commit()
			main_comp_id = check[0][0]
			print("successfully update main comp")
		for item in pc_session_list['ram']:
			GetItemFromDatabase.insert_ram_usage(item, main_comp_id)
		if pc_session_list['ssd'] is not None:
			for item in pc_session_list['ssd']:
				GetItemFromDatabase.insert_ssd_usage(item, main_comp_id)
		if pc_session_list['hdd'] is not None:
			for item in pc_session_list['hdd']:
				GetItemFromDatabase.insert_hdd_usage(item, main_comp_id)
		GetItemFromDatabase.insert_psu_usage(pc_session_list['psu'], main_comp_id)
		if pc_session_list['case'] is not None:
			GetItemFromDatabase.insert_case_usage(pc_session_list['case'])
		cursor.close()
		return main_comp_id

	@staticmethod
	def update_score(pc_id, interact_point, point_type):
		cursor = GetItemFromDatabase.database.cursor()
		if point_type == 'confirm':
			point = 50
		else:
			point = 50 * (1 / (interact_point * (interact_point + 1)))
		op = f"""
				UPDATE "PC_Builder"."Main_comp" SET "{point_type}_score" =  COALESCE("{point_type}_score", 0) +  {point}
				WHERE main_comp_id = {pc_id}; 
			"""
		cursor.execute(op)
		GetItemFromDatabase.database.commit()
		print("successfully update main comp by id")
		cursor.close()
		return True

	@staticmethod
	# ram_info = {'id': ram_id, 'amount': "8gb"}
	def insert_ram_usage(ram_info, main_comp_id):
		cursor = GetItemFromDatabase.database.cursor()
		op1 = f""" 
				SELECT * FROM "PC_Builder"."RAM_Usage"
				WHERE main_comp_id = {main_comp_id} and ram_id = {ram_info['id']};
			"""
		cursor.execute(op1)
		check = cursor.fetchall()
		if len(check) == 0:
			op2 = f"""
					INSERT INTO "PC_Builder"."RAM_Usage" ("main_comp_id", "ram_id", "{ram_info['amount']}")
					VALUES ({main_comp_id}, {ram_info['id']}, 1);
				"""
			cursor.execute(op2)
			GetItemFromDatabase.database.commit()
			print("successfully insert new ram to ram usage")
		else:
			op3 = f"""
					UPDATE "PC_Builder"."RAM_Usage" 
					SET "{ram_info['amount']}" =  COALESCE("{ram_info['amount']}", 0) + 1
					WHERE main_comp_id = {main_comp_id} and ram_id = {ram_info['id']};
				"""
			cursor.execute(op3)
			GetItemFromDatabase.database.commit()
			print("successfully update ram usage")
		cursor.close()
		return True

	@staticmethod
	# ssd_info = {'id': ssd_id, 'quantity': x} (buy same ssd x quantity of times)
	def insert_ssd_usage(ssd_info, main_comp_id):
		if ssd_info['id'] is None:
			print("no ssd to update")
			return
		cursor = GetItemFromDatabase.database.cursor()
		op1 = f""" 
				SELECT * FROM "PC_Builder"."SSD_Usage"
				WHERE main_comp_id = {main_comp_id} and ssd_id = {ssd_info['id']};
			"""
		cursor.execute(op1)
		check = cursor.fetchall()
		if len(check) == 0:
			op2 = f"""
					INSERT INTO "PC_Builder"."SSD_Usage" ("main_comp_id", "ssd_id", "quantity", "total_usage")
					VALUES ({main_comp_id}, {ssd_info['id']}, {ssd_info['quantity']}, 1);
				"""
			cursor.execute(op2)
			GetItemFromDatabase.database.commit()
			print("successfully insert new ssd to ssd usage")
		else:
			op3 = f"""
					UPDATE "PC_Builder"."SSD_Usage" 
					SET "quantity" = "quantity" + {ssd_info['quantity']},
						"total_usage" = "total_usage" + 1
					WHERE main_comp_id = {main_comp_id} and ssd_id = {ssd_info['id']};
				"""
			cursor.execute(op3)
			GetItemFromDatabase.database.commit()
			print("successfully update ssd usage")
		cursor.close()
		return True

	@staticmethod
	# hdd_info = {'id': hdd_id, 'quantity': x} (buy same hdd x quantity of times)
	def insert_hdd_usage(hdd_info, main_comp_id):
		if hdd_info['id'] is None:
			print("no hdd to update")
			return
		cursor = GetItemFromDatabase.database.cursor()
		op1 = f""" 
				SELECT * FROM "PC_Builder"."HDD_Usage"
				WHERE main_comp_id = {main_comp_id} and hdd_id = {hdd_info['id']};
			"""
		cursor.execute(op1)
		check = cursor.fetchall()
		if len(check) == 0:
			op2 = f"""
					INSERT INTO "PC_Builder"."HDD_Usage" ("main_comp_id", "hdd_id", "quantity", "total_usage")
					VALUES ({main_comp_id}, {hdd_info['id']}, {hdd_info['quantity']}, 1);
				"""
			cursor.execute(op2)
			GetItemFromDatabase.database.commit()
			print("successfully insert new hdd to hdd usage")
		else:
			op3 = f"""
					UPDATE "PC_Builder"."HDD_Usage" 
					SET "quantity" = "quantity" + {hdd_info['quantity']},
						"total_usage" = "total_usage" + 1
					WHERE main_comp_id = {main_comp_id} and hdd_id = {hdd_info['id']};
				"""
			cursor.execute(op3)
			GetItemFromDatabase.database.commit()
			print("successfully update hdd usage")
		cursor.close()
		return True

	@staticmethod
	def insert_psu_usage(psu_id, main_comp_id):
		cursor = GetItemFromDatabase.database.cursor()
		op1 = f""" 
				SELECT * FROM "PC_Builder"."PSU_Usage"
				WHERE main_comp_id = {main_comp_id} and psu_id = {psu_id['id']};
			"""
		cursor.execute(op1)
		check = cursor.fetchall()
		if len(check) == 0:
			op2 = f"""
					INSERT INTO "PC_Builder"."PSU_Usage" ("main_comp_id", "psu_id", "total_usage")
					VALUES ({main_comp_id}, {psu_id['id']}, 1);
				"""
			cursor.execute(op2)
			GetItemFromDatabase.database.commit()
			print("successfully insert new psu to psu usage")
		else:
			op3 = f"""
					UPDATE "PC_Builder"."PSU_Usage" 
					SET "total_usage" = "total_usage" + 1
					WHERE main_comp_id = {main_comp_id} and psu_id = {psu_id['id']};
				"""
			cursor.execute(op3)
			GetItemFromDatabase.database.commit()
			print("successfully update psu usage")
		cursor.close()
		return True

	@staticmethod
	def insert_case_usage(case_id):
		cursor = GetItemFromDatabase.database.cursor()
		op = f"""
			UPDATE "PC_Builder"."CASE"
			SET "total_usage" = COALESCE(total_usage, 0) + 1
			WHERE case_id = {case_id['id']};
		"""
		cursor.execute(op)
		GetItemFromDatabase.database.commit()
		print("successfully update case usage")
		cursor.close()
		return True

	@staticmethod
	def get_pc_for_recommend(limit=None):
		cursor = GetItemFromDatabase.database.cursor()
		if limit is None:
			limit = 100
		op = f"""
			SELECT
				main.main_comp_id, 
					main.cpu_id, main.mb_id, main.gpu_id, main.auto_score, main.custom_score, main.confirm_score,
					main.ram_id, main."4gb", main."8gb", main."16gb", main."32gb", main."64gb", main."128gb", main.total,
					main.ssd_id, main.ssd_quantity, main.ssd_total_usage,
					main.hdd_id, main.hdd_quantity, main.hdd_total_usage,
					psu.psu_id, psu.total_usage AS psu_total_usage
				FROM (
					SELECT 
						main.main_comp_id, 
							main.cpu_id, main.mb_id, main.gpu_id, main.auto_score, main.custom_score, main.confirm_score,
							main.ram_id, main."4gb", main."8gb", main."16gb", main."32gb", main."64gb", main."128gb", main.total,
							main.ssd_id, main.ssd_quantity, main.ssd_total_usage,
							hdd.hdd_id, hdd.quantity AS hdd_quantity, hdd.total_usage AS hdd_total_usage
					FROM (
						SELECT 
							main.main_comp_id, 
								main.cpu_id, main.mb_id, main.gpu_id, main.auto_score, main.custom_score, main.confirm_score,
								main.ram_id, main."4gb", main."8gb", main."16gb", main."32gb", main."64gb", main."128gb", main.total,
								ssd.ssd_id, ssd.quantity AS ssd_quantity, ssd.total_usage AS ssd_total_usage
						FROM (
							SELECT
								main.main_comp_id,
									main.cpu_id, main.mb_id, main.gpu_id, main.auto_score, main.custom_score, main.confirm_score,
									ram.ram_id, ram."4gb", ram."8gb", ram."16gb", ram."32gb", ram."64gb", ram."128gb", ram.total
							FROM (
								SELECT *
								FROM "PC_Builder"."Main_comp"
								GROUP BY main_comp_id
								ORDER BY SUM(COALESCE(auto_score, 0) + COALESCE(custom_score, 0)) DESC
								LIMIT {limit}
							) AS main
							INNER JOIN (
								SELECT DISTINCT ON(b.main_comp_id) b.main_comp_id, b.ram_id, b."4gb", b."8gb", b."16gb", b."32gb", b."64gb", b."128gb", b.total
								FROM "PC_Builder"."RAM_Usage" AS b
								INNER JOIN (
									SELECT a.main_comp_id, MAX(a.total) AS max
									FROM "PC_Builder"."RAM_Usage" AS a
									GROUP BY a.main_comp_id
								) as c
								ON b.main_comp_id = c.main_comp_id AND b.total = c.max
							) AS ram
							ON main.main_comp_id = ram.main_comp_id
						) AS main
						INNER JOIN (
							SELECT DISTINCT ON(b.main_comp_id) b.main_comp_id, b.ssd_id, b.quantity, b.total_usage
							FROM "PC_Builder"."SSD_Usage" AS b
							INNER JOIN (
								SELECT main_comp_id, MAX(total_usage) AS max_total_each_ssd
								FROM "PC_Builder"."SSD_Usage" 
								GROUP BY main_comp_id
							) as a
							ON b.main_comp_id = a.main_comp_id AND b.total_usage = a.max_total_each_ssd
						) AS ssd
						ON main.main_comp_id = ssd.main_comp_id
					) AS main
					LEFT JOIN (
						SELECT DISTINCT ON(b.main_comp_id) b.main_comp_id, b.hdd_id, b.quantity, b.total_usage
							FROM "PC_Builder"."HDD_Usage" AS b
							JOIN (
								SELECT main_comp_id, MAX(total_usage) AS max_total_each_hdd
								FROM "PC_Builder"."HDD_Usage" 
								GROUP BY main_comp_id
							) as a
							ON b.main_comp_id = a.main_comp_id AND b.total_usage = a.max_total_each_hdd
					) AS hdd
					ON main.main_comp_id = hdd.main_comp_id
				) AS main
				INNER JOIN (
					SELECT DISTINCT ON(b.main_comp_id) b.main_comp_id, b.psu_id, b.total_usage
					FROM "PC_Builder"."PSU_Usage" AS b
					INNER JOIN (
						SELECT main_comp_id, MAX(total_usage) AS max_total_each_psu
						FROM "PC_Builder"."PSU_Usage" 
						GROUP BY main_comp_id
					) as a
					ON b.main_comp_id = a.main_comp_id AND b.total_usage = a.max_total_each_psu
				) AS psu
				ON main.main_comp_id = psu.main_comp_id
		"""
		cursor.execute(op)
		data = cursor.fetchall()
		if len(data) == 0:
			return None
		cpu_id_set = set()
		board_id_set = set()
		gpu_id_set = set()
		ram_id_set = set()
		ssd_id_set = set()
		hdd_id_set = set()
		psu_id_set = set()
		for item in data:
			cpu_id_set.add(item[1])
			board_id_set.add(item[2])
			if item[3] is not None:
				gpu_id_set.add(item[3])
			ram_id_set.add(item[7])
			if item[15] is not None:
				ssd_id_set.add(item[15])
			if item[18] is not None:
				hdd_id_set.add(item[18])
			psu_id_set.add(item[21])
		cpu_info = GetItemFromDatabase.get_cpu_list_from_db(cpu_id_set)
		board_info = GetItemFromDatabase.get_board_list_from_db(board_id_set)
		gpu_info = GetItemFromDatabase.get_gpu_list_from_db(gpu_id_set)
		ram_info = GetItemFromDatabase.get_ram_list_from_db(ram_id_set)
		ssd_info = GetItemFromDatabase.get_ssd_list_from_db(ssd_id_set)
		hdd_info = GetItemFromDatabase.get_hdd_list_from_db(hdd_id_set)
		psu_info = GetItemFromDatabase.get_psu_list_from_db(psu_id_set)
		case_info = GetItemFromDatabase.get_case_list_from_db()
		pc_list = []
		for item in data:
			pc = []
			# cpu
			for cpu in cpu_info:
				if cpu['id'] == item[1]:
					pc.append(cpu)
					break
			# board
			for board in board_info:
				if board['id'] == item[2]:
					pc.append(board)
					break
			# gpu
			if item[3] is None:
				pc.append(None)
			else:
				for gpu in gpu_info:
					if gpu['id'] == item[3]:
						pc.append(gpu)
						break
			# ram
			for ram in ram_info:
				if ram['id'] == item[7]:
					amount_list = []
					for i in range(8, 14):
						if item[i] is None:
							amount_list.append(0)
						else:
							amount_list.append(item[i])
					most_used_size_value = max(amount_list)
					most_used_size_index = amount_list.index(most_used_size_value)
					most_used_size = 2 ** (most_used_size_index + 2)
					quantity = int(most_used_size / utility.get_ram_total_size(ram))
					pc.append([{'item': ram, 'quantity': quantity}])
					break
			# ssd
			for ssd in ssd_info:
				if ssd['id'] == item[15]:
					pc.append([{'item': ssd, 'quantity': 1}])
					break
			# hdd
			pc.append(None)
			# psu
			for psu in psu_info:
				if psu['id'] == item[21]:
					pc.append(psu)
					break
			# case
			pc.append(None)
			pc_list.append(pc)
		cursor.close()
		return {'pc_list': pc_list, 'pc_info': data,
				'comp_info': {
					'cpu': cpu_info,
					'board': board_info,
					'gpu': gpu_info,
					'ram': ram_info,
					'ssd': ssd_info,
					'hdd': hdd_info,
					'psu': psu_info,
					'case': case_info
				}}

	@staticmethod
	def shingle(doc, k=2):
		return {doc[i:i + k] for i in range(0, len(doc) - k + 1)}

	@staticmethod
	def norm(a):
		return a.lower().replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")

	@staticmethod
	def jaccard(a, b):
		return 1.0 * len(a.intersection(b)) / len(a.union(b))

	@staticmethod
	def search(txt, datalist, no_brand=False):
		if txt == "":
			return datalist

		else:
			findata = []
			a = GetItemFromDatabase.shingle(GetItemFromDatabase.norm(txt))
			for item in datalist:
				if no_brand:
					b = GetItemFromDatabase.jaccard(a, GetItemFromDatabase.shingle(GetItemFromDatabase.norm(item[1])))
				else:
					b = GetItemFromDatabase.jaccard(a, GetItemFromDatabase.shingle(GetItemFromDatabase.norm(item[2] + " " + item[1])))
				item = list(item)
				if b > 0:
					findata.append(item)
					item.append(b)

			findata.sort(reverse=True, key=lambda x: x[-1])
			for item in findata:
				del item[-1]
				item = tuple(item)
			return findata


	@staticmethod
	def search_dic(txt, datalist, no_brand=False):
		if txt == "":
			return datalist

		else:
			findata = []
			a = GetItemFromDatabase.shingle(GetItemFromDatabase.norm(txt))
			for item in datalist:
				if no_brand:
					b = GetItemFromDatabase.jaccard(a, GetItemFromDatabase.shingle(GetItemFromDatabase.norm(item['name'])))
				else:
					b = GetItemFromDatabase.jaccard(a, GetItemFromDatabase.shingle(GetItemFromDatabase.norm(item['name'] + " " + item['brand'])))
				temp_item = [item]
				if b > 0:
					findata.append(temp_item)
					temp_item.append(b)

			findata.sort(reverse=True, key=lambda x: x[-1])
			for i in range(len(findata)):
				findata[i] = findata[i][0]
			return findata

	@staticmethod
	def search_cpu(series, brand, socket, bench, price):
		cursor = GetItemFromDatabase.database.cursor()
		query = """ SELECT * FROM "PC_Builder"."CPU" WHERE """
		querycheck = query
		check = 0

		if brand:
			ck = 0
			query += """("""
			for i in brand:
				if ck == 1:
					query += """or """
				query += """"Brand" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if series:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in series:
				if ck == 1:
					query += """or """
				query += """"Name" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if socket:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in socket:
				if ck == 1:
					query += """or """
				query += """"Socketed_supported" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if bench[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) >= """ + bench[0] + """ """
			check = 1

		if bench[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) <= """ + bench[1] + """ """
			check = 1

		if price[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) >= """ + price[0] + """ """
			check = 1

		if price[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) <= """ + price[1] + """ """

		if query == querycheck:
			query = """ SELECT * FROM "PC_Builder"."CPU" """
		cursor.execute(query)
		datalist = cursor.fetchall()
		cursor.close()
		return datalist

	@staticmethod
	def search_gpu(brand, bench, price):
		cursor = GetItemFromDatabase.database.cursor()
		query = """ SELECT * FROM "PC_Builder"."GPU" WHERE """
		querycheck = query
		check = 0

		if brand:
			ck = 0
			query += """("""
			for i in brand:
				if ck == 1:
					query += """or """
				query += """"Brand" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if bench[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) >= """ + bench[0] + """ """
			check = 1

		if bench[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) <= """ + bench[1] + """ """
			check = 1

		if price[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) >= """ + price[0] + """ """
			check = 1

		if price[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) <= """ + price[1] + """ """

		if query == querycheck:
			query = """ SELECT * FROM "PC_Builder"."GPU" """
		cursor.execute(query)
		datalist = cursor.fetchall()
		cursor.close()
		return datalist

	@staticmethod
	def search_ram(brand, memtype, rambus, size, quant, bench, price):
		cursor = GetItemFromDatabase.database.cursor()
		query = """ SELECT * FROM "PC_Builder"."RAM" WHERE """
		querycheck = query
		check = 0

		if brand:
			ck = 0
			query += """("""
			for i in brand:
				if ck == 1:
					query += """or """
				query += """"Brand" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if memtype:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in memtype:
				if ck == 1:
					query += """or """
				query += """"Memory_type" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if rambus:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in rambus:
				if ck == 1:
					query += """or """
				query += """"Ram_bus" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if size:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in size:
				if ck == 1:
					query += """or """
				query += """"Size" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if quant:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in quant:
				if ck == 1:
					query += """or """
				query += """"Quantity" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if bench[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) >= """ + bench[0] + """ """
			check = 1

		if bench[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) <= """ + bench[1] + """ """
			check = 1

		if price[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) >= """ + price[0] + """ """
			check = 1

		if price[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) <= """ + price[1] + """ """

		if query == querycheck:
			query = """ SELECT * FROM "PC_Builder"."RAM" """
		cursor.execute(query)
		datalist = cursor.fetchall()
		cursor.close()
		return datalist

	@staticmethod
	def search_psu(brand, eff, watt, modul, form, price):
		cursor = GetItemFromDatabase.database.cursor()
		query = """ SELECT * FROM "PC_Builder"."PSU" WHERE """
		querycheck = query
		check = 0

		if brand:
			ck = 0
			query += """("""
			for i in brand:
				if ck == 1:
					query += """or """
				query += """"Brand" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if eff:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in eff:
				if ck == 1:
					query += """or """
				query += """"Efficient_rating" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if watt:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in watt:
				if ck == 1:
					query += """or """
				query += """"Wattage" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if modul:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in modul:
				if ck == 1:
					query += """or """
				query += """"Modularity" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if form:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in form:
				if ck == 1:
					query += """or """
				query += """"Form_factor" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if price[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) >= """ + price[0] + """ """
			check = 1

		if price[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) <= """ + price[1] + """ """

		if query == querycheck:
			query = """ SELECT * FROM "PC_Builder"."PSU" """
		cursor.execute(query)
		datalist = cursor.fetchall()
		cursor.close()
		return datalist

	@staticmethod
	def search_hdd(brand, comp, bench, price):
		cursor = GetItemFromDatabase.database.cursor()
		query = """ SELECT * FROM "PC_Builder"."HDD" WHERE """
		querycheck = query
		check = 0

		if brand:
			ck = 0
			query += """("""
			for i in brand:
				if ck == 1:
					query += """or """
				query += """"Brand" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if comp:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in comp:
				if ck == 1:
					query += """or """
				query += """("Capacity" = '""" + i[:-2] + """' and "Unit" = '""" + i[-2:] + """') """
				ck = 1
			query += """) """
			check = 1

		if bench[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) >= """ + bench[0] + """ """
			check = 1

		if bench[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) <= """ + bench[1] + """ """
			check = 1

		if price[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) >= """ + price[0] + """ """
			check = 1

		if price[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) <= """ + price[1] + """ """

		if query == querycheck:
			query = """ SELECT * FROM "PC_Builder"."HDD" """
		cursor.execute(query)
		datalist = cursor.fetchall()
		cursor.close()
		return datalist

	@staticmethod
	def search_ssd(brand, comp, bench, price):
		cursor = GetItemFromDatabase.database.cursor()
		query = """ SELECT * FROM "PC_Builder"."SSD" WHERE """
		querycheck = query
		check = 0

		if brand:
			ck = 0
			query += """("""
			for i in brand:
				if ck == 1:
					query += """or """
				query += """"Brand" = '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if comp:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in comp:
				if ck == 1:
					query += """or """
				a = i[:-2]
				if a == "120" or a == "128":
					query += """(("Capacity" = '120' or "Capacity" = '128') and "Unit" = '""" + i[-2:] + """') """
				elif a == "240" or a == "250" or a == "256":
					query += """(("Capacity" = '240' or "Capacity" = '250' or "Capacity" = '256') and "Unit" = '""" + i[
					                                                                                                  -2:] + """') """
				elif a == "480" or a == "500" or a == "512":
					query += """(("Capacity" = '480' or "Capacity" = '500' or "Capacity" = '512') and "Unit" = '""" + i[
					                                                                                                  -2:] + """') """
				else:
					query += """("Capacity" = '""" + a + """' and "Unit" = '""" + i[-2:] + """') """
				ck = 1
			query += """) """
			check = 1

		if bench[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) >= """ + bench[0] + """ """
			check = 1

		if bench[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Bench" AS real) <= """ + bench[1] + """ """
			check = 1

		if price[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) >= """ + price[0] + """ """
			check = 1

		if price[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) <= """ + price[1] + """ """

		if query == querycheck:
			query = """ SELECT * FROM "PC_Builder"."SSD" """
		cursor.execute(query)
		datalist = cursor.fetchall()
		cursor.close()
		return datalist

	@staticmethod
	def search_case(brand, typ, form, price):
		cursor = GetItemFromDatabase.database.cursor()
		query = """ SELECT * FROM "PC_Builder"."CASE" WHERE """
		querycheck = query
		check = 0

		if brand:
			ck = 0
			query += """("""
			for i in brand:
				if ck == 1:
					query += """or """
				if i == "Cooler Master" or i == "CM":
					query += """("Name" ~* 'Cooler Master' or "Name" ~* 'CM')"""
				else:
					query += """"Name" ~* '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if typ:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in typ:
				if ck == 1:
					query += """or """
				query += """"Case_type" ~* '""" + i + """' """
				ck = 1
			query += """) """
			check = 1

		if form:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in form:
				if ck == 1:
					query += """or """
				query += """"Board_supported" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if price[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) >= """ + price[0] + """ """
			check = 1

		if price[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) <= """ + price[1] + """ """

		if query == querycheck:
			query = """ SELECT * FROM "PC_Builder"."CASE" """
		cursor.execute(query)
		datalist = cursor.fetchall()
		cursor.close()
		return datalist

	@staticmethod
	def search_mb(brand, socket, chipset, form, memtype, ramslot, m2, sata, price):
		cursor = GetItemFromDatabase.database.cursor()
		query = """ SELECT * FROM "PC_Builder"."Motherboard" WHERE """
		querycheck = query
		check = 0

		if brand:
			ck = 0
			query += """("""
			for i in brand:
				if ck == 1:
					query += """or """
				query += """"Name" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if socket:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in socket:
				if ck == 1:
					query += """or """
				query += """"Socket" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if form:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in form:
				if ck == 1:
					query += """or """
				query += """"Board_supported" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if memtype:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in memtype:
				if ck == 1:
					query += """or """
				query += """"Memory_type" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if chipset:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in chipset:
				if ck == 1:
					query += """or """
				query += """"Chipset" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if ramslot:
			if check == 1:
				query += """and """
			ck = 0
			query += """("""
			for i in ramslot:
				if ck == 1:
					query += """or """
				query += """"Ram_slot" ~* '(\m""" + i + """\M)' """
				ck = 1
			query += """) """
			check = 1

		if price[0] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) >= """ + price[0] + """ """
			check = 1

		if price[1] != "":
			if check == 1:
				query += """and """
			query += """CAST("Price" AS real) <= """ + price[1] + """ """

		if query == querycheck:
			query = """ SELECT * FROM "PC_Builder"."Motherboard" """
		cursor.execute(query)
		datalist = cursor.fetchall()

		if m2 != [] or sata != []:
			if m2 != []:
				m2 = range(int(m2[0]), int(m2[1]))
			if sata != []:
				sata = range(int(sata[0]), int(sata[1]))
			print(sata)
			finlist = []
			for item in reversed(datalist):
				i = GetItemFromDatabase.norm(item[10])
				temp = i.split(",")
				checkm2 = 0
				checksata = 0
				for a in temp:
					for m in m2:
						if "m.2" in a and a[0] == str(m):
							checkm2 += 1
					for s in sata:
						if "sata" in a and a[0] == str(s) and "m.2" not in a:
							checksata += 1
				if checkm2 > 0 or checksata > 0:
					finlist.append(item)
			datalist = finlist
		cursor.close()
		return datalist

# data = GetItemFromDatabase.get_case_list_from_db()
# for i in data:
# 	print(i)