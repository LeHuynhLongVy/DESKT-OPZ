

class Pc:
	def __init__(self, component=None):
		if component is None:
			self.cpu = None
			self.board = None
			self.gpu = None
			self.ram = None
			self.storage_ssd = None
			self.storage_hdd = None
			self.psu = None
			self.case = None
			self.total_price = 0
		elif len(component) == 8:
			self.cpu = component[0]
			self.board = component[1]
			self.gpu = component[2]
			self.ram = component[3]
			self.storage_ssd = component[4]
			self.storage_hdd = component[5]
			self.psu = component[6]
			self.case = component[7]
			self.total_price = 0
			self.update_price()
		else:
			raise ValueError("invalid argument!")

	@staticmethod
	def price(item):
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

	def update_price(self):
		temp = 0
		if self.cpu is not None:
			temp = temp + self.price(self.cpu)
		if self.board is not None:
			temp = temp + self.price(self.board)
		if self.gpu is not None:
			temp = temp + self.price(self.gpu)
		if self.ram is not None:
			temp = temp + self.price(self.ram)
		if self.storage_ssd is not None:
			temp = temp + self.price(self.storage_ssd)
		if self.psu is not None:
			temp = temp + self.price(self.psu)
		if self.case is not None:
			temp = temp + self.price(self.case)
		if self.storage_hdd is not None:
			temp = temp + self.price(self.storage_hdd)
		self.total_price = temp

	def get_total_price(self):
		self.update_price()
		return self.total_price

	def over_budget(self, budget):
		self.update_price()
		if self.total_price > budget:
			# print('over!!!!!!!!!!!!!!!')
			return True
		else:
			return False

	def __str__(self):
		self.update_price()
		return "cpu:" + str(self.cpu) + "\n" + "board:" + str(self.board) + "\n" + "gpu:" + str(self.gpu) + "\n" + "ram:" + str(self.ram) + "\n" + "storage_ssd:" + str(self.storage_ssd) + "\n" +"storage_hdd:" + str(self.storage_hdd) + "\n" + "psu:" + str(self.psu) + "\n" + "case:" + str(self.case) + "\n" + "Price:" + str(self.total_price)

