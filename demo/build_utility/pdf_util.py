from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
import io
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import locale

locale.setlocale( locale.LC_ALL, 'vi_VN.utf8' )
class PcToPdf:

	@staticmethod
	def fix_comp_keys(k):
		if k == "brand":
			k = "Brand"
		elif k == "name":
			k = "Product Name"
		elif k == "link":
			k = "Link To Product"
		elif k == "user_rating":
			k = "User Rating"
		elif k == "value":
			k = "Product Value"
		elif k == "bench":
			k = "Average Bench"
		elif k == "price":
			k = "Product Price"
		elif k == "name1":
			k = "Product Full Name"
		elif k == "processor_number":
			k = "Processor Number"
		elif k == "max_memory_sizer":
			k = "Max Memory Size"
		elif k == "memory_type":
			k = "Memory Type"
		elif k == "socket_supported":
			k = "Socket Supported"
		# Mainboard
		elif k == "socket":
			k = "Socket Supported"
		elif k == "chipset":
			k = "Chipset"
		elif k == "form_factor":
			k = "Form Factor"
		elif k == "ram_slot":
			k = "Ram slot"
		elif k == "max_memory_size":
			k = "Max Memory Size"
		elif k == "ram_bus":
			k = "Ram Bus"
		elif k == "storage_type":
			k = "Storage Type"
		elif k == "supported_m2":
			k = "Supported M.2"
		elif k == "out_put":
			k = "Output"
		elif k == "pci":
			k = "PCI Slots"
		# PSU
		elif k == "efficient rating":
			k = "Efficient Rating"
		elif k == "wattage":
			k = "Wattage"
		elif k == "protection":
			k = "Protection"
		elif k == "modularity":
			k = "Modularity"
		elif k == "form factor":
			k = "Form Factor"
		# Case
		elif k == "case_type":
			k = "Case Type"
		elif k == "board_supported":
			k = "Board Supported"
		# others
		elif k == "ram_cas":
			k = "Ram CAS"
		elif k == "quantity":
			k = "Quantity"
		elif k == "size":
			k = "Ram Size"
		elif k == "capacity":
			k = "Capacity"
		elif k == "unit":
			k = "Storage Unit"
		return k

	@staticmethod
	def create_component_table(i, c, pc_in, data_out, comp_name):
		styleSheet = getSampleStyleSheet()
		styleBH = styleSheet['BodyText']
		styleBH.fontName = 'Verdana'
		tablerows = 0
		if i == 3 or i == 4 or i == 5:
			for k, v in pc_in["item"].items():
				if k != "id" and k != "img" and k != "link1":
					tablerows += 1
					k = PcToPdf.fix_comp_keys(k)
					if k == 'Product Price':
						v = str(locale.currency(int(float(v)), grouping=True)).replace(',00','')
					if isinstance(v, str):
						if v[0] == "\t" or v[0] == " ":
							v = v[1:]
						v = v.replace("\r", "")
						v = v.replace("\t", "")
						v = v.replace("\n", "")
					data_out.append([Paragraph(str(k), styleBH), Paragraph(str(v), styleBH)])
			rowheight = 30
			t = Table(data_out, colWidths=[90, 400], rowHeights=rowheight)
			style = TableStyle([
				('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
				('FONTNAME', (0, 0), (-1, -1), 'Verdana'),
				('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
			])
			t.setStyle(style)
			tableheight = tablerows * rowheight
			# 612, 792
			c.drawString(60, 792 - 60, comp_name)
			t.wrapOn(c, 60, 792 - 60 - tableheight - 10)
			t.drawOn(c, 60, 792 - 60 - tableheight - 10)
			c.showPage()
		else:
			for k, v in pc_in[i].items():
				if k != "id" and k != "img" and k != "link1":
					tablerows += 1
					k = PcToPdf.fix_comp_keys(k)
					if k == 'Product Price':
						v = locale.currency(int(float(v)), grouping=True).replace(',00','')
					if isinstance(v, str):
						if v[0] == "\t" or v[0] == " ":
							v = v[1:]
						v = v.replace("\r", "")
						v = v.replace("\t", "")
						v = v.replace("\n", "")
					data_out.append([Paragraph(str(k), styleBH), Paragraph(str(v), styleBH)])
			rowheight = 30
			t = Table(data_out, colWidths=[90, 400], rowHeights=rowheight)
			style = TableStyle([
				('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
				('FONTNAME', (1, 0), (-1, -1), 'Verdana'),
				('FONTNAME', (0, 0), (0, -1), 'Verdana-Bold'),
				('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
			])
			t.setStyle(style)
			tableheight = tablerows * rowheight
			# 612, 792
			c.drawString(60, 792 - 60, comp_name)
			t.wrapOn(c, 60, 792 - 60 - tableheight - 10)
			t.drawOn(c, 60, 792 - 60 - tableheight - 10)
			c.showPage()

	@staticmethod
	def create_overview_table(c, pc_in, data_out):
		styleSheet = getSampleStyleSheet()
		styleBH = styleSheet['BodyText']
		styleBH.fontName = 'Verdana'
		total_price = 0
		tablerows = 0
		for i in range(8):
			if pc_in[i] is not None:
				if isinstance(pc_in[i], list):
					for comp in pc_in[i]:
						total_price += float(comp["item"]["price"])
				else:
					total_price += float(float(pc_in[i]["price"]))
		for i in range(8):
			if pc_in[i] is not None:
				if i == 0:
					# print(locale.currency(int(locale.currency(int(float(pc_in[i]["price"])), grouping= True)), grouping= True))
					# print(locale.currency(int(float(pc_in[i]["price"])), grouping= True))
					data_out.append(
						[Paragraph("CPU", styleBH), Paragraph(str(pc_in[i]["brand"] + " " + pc_in[i]["name"]), styleBH),
						 1,
						 str(locale.currency(int(float(pc_in[i]["price"])), grouping= True)).replace(',00','')])
					tablerows += 1
				elif i == 1:
					data_out.append(
						[Paragraph("Motherboard", styleBH), Paragraph(str(pc_in[i]["name"]), styleBH), 1,
						 str(locale.currency(int(float(pc_in[i]["price"])), grouping= True)).replace(',00','')])
					tablerows += 1
				elif i == 2:
					data_out.append(
						[Paragraph("GPU", styleBH), Paragraph(str(pc_in[i]["brand"] + " " + pc_in[i]["name"]), styleBH),
						 1,
						 str(locale.currency(int(float(pc_in[i]["price"])), grouping= True)).replace(',00','')])
					tablerows += 1
				elif i == 3:
					for ram in pc_in[i]:
						data_out.append([Paragraph("RAM", styleBH),
						                 Paragraph(str(ram["item"]["brand"] + " " + ram["item"]["name"]), styleBH),
						                 ram["quantity"], str(locale.currency(int(float(ram["item"]["price"])), grouping= True)).replace(',00','')])
						tablerows += 1
				elif i == 4:
					for ssd in pc_in[i]:
						data_out.append([Paragraph("SSD", styleBH),
						                 Paragraph(str(ssd["item"]["brand"] + " " + ssd["item"]["name"]), styleBH),
						                 ssd["quantity"], str(locale.currency(int(float(ssd["item"]["price"])), grouping= True)).replace(',00','')])
						tablerows += 1
				elif i == 5:
					for hdd in pc_in[i]:
						data_out.append([Paragraph("HDD", styleBH),
						                 Paragraph(str(hdd["item"]["brand"] + " " + hdd["item"]["name"]), styleBH),
						                 hdd["quantity"], str(locale.currency(int(float(hdd["item"]["price"])), grouping= True)).replace(',00','')])
						tablerows += 1
				elif i == 6:
					data_out.append(
						[Paragraph("PSU", styleBH), Paragraph(str(pc_in[i]["brand"] + " " + pc_in[i]["name"]), styleBH),
						 1,
						 str(locale.currency(int(float(pc_in[i]["price"])), grouping= True)).replace(',00','')])
					tablerows += 1
				elif i == 7:
					data_out.append(
						[Paragraph("Case", styleBH), Paragraph(str(pc_in[i]["name"]), styleBH), 1,
						 str(locale.currency(int(float(pc_in[i]["price"])), grouping= True)).replace(',00','')])
					tablerows += 1
		data_out.append(["TOTAL PRICE", "", "", str(locale.currency(int(float(total_price)), grouping= True)).replace(',00','')])
		ot = Table(data_out, colWidths=[65, 300, 60, 80], rowHeights=30)
		style = TableStyle([
			('GRID', (0, 0), (-1, -1), 0.5, colors.black),
			('SPAN', (0, tablerows + 1), (2, tablerows + 1)),
			('FONTNAME', (0, 0), (-1, -1), 'Verdana'),
			('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
			('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
			('ALIGN', (0, 0), (-1, 0), 'CENTER'),
			('FONTNAME', (0, 0), (-1, 0), 'Verdana-Bold'),
			('ALIGN', (0, -1), (0, -1), 'CENTER'),
			('FONTNAME', (0, -1), (0, -1), 'Verdana-Bold'),
		])
		ot.setStyle(style)
		otableheight = 30 * (tablerows + 1)
		c.drawCentredString(300, 792 - 60, "PC Build Overview")
		ot.wrapOn(c, 60, 792 - 60 - otableheight - 40)
		ot.drawOn(c, 60, 792 - 60 - otableheight - 40)
		c.showPage()

	@staticmethod
	def pc_to_pdf(request_pc):
		setpc = request_pc
		buf = io.BytesIO()
		c = canvas.Canvas(buf, pagesize=letter)
		pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
		pdfmetrics.registerFont(TTFont('Verdana-Bold', 'VERDANAB.TTF'))
		c.setFont("Verdana", 20)
		fileName = 'your_pc.pdf'

		# Overview Table
		data = [["Component", "Name", "Quantity", "Price"]]
		PcToPdf.create_overview_table(c, setpc, data)

		# The Specification Tables
		for i in range(8):
			if setpc[i] is not None:
				if i == 0:
					cpu_table = []
					c.setFont("Verdana", 14)
					PcToPdf.create_component_table(i, c, setpc, cpu_table, "CPU Specification")
				if i == 1:
					mainboard_table = []
					c.setFont("Verdana", 14)
					PcToPdf.create_component_table(i, c, setpc, mainboard_table, "Motherboard Specification")
				if i == 2:
					gpu_table = []
					c.setFont("Verdana", 14)
					PcToPdf.create_component_table(i, c, setpc, gpu_table, "GPU Specification")
				if i == 3:
					if len(setpc[i]) == 1:
						for each_ram in setpc[i]:
							ram_table = []
							c.setFont("Verdana", 14)
							PcToPdf.create_component_table(i, c, each_ram, ram_table, "Ram Specification")
					else:
						j = 1
						for each_ram in setpc[i]:
							ram_table = []
							c.setFont("Verdana", 14)
							PcToPdf.create_component_table(i, c, each_ram, ram_table, "Ram " + str(j) + " Specification")
							j += 1
				if i == 4:

					if len(setpc[i]) == 1:
						for each_ssd in setpc[i]:
							ssd_table = []
							c.setFont("Verdana", 14)
							PcToPdf.create_component_table(i, c, each_ssd, ssd_table, "SSD Specification")
					else:
						k = 1
						for each_ssd in setpc[i]:
							ssd_table = []
							c.setFont("Verdana", 14)
							PcToPdf.create_component_table(i, c, each_ssd, ssd_table, "SSD " + str(k) + " Specification")
							k += 1
				if i == 5:

					if len(setpc[i]) == 1:
						for each_hdd in setpc[i]:
							hdd_table = []
							c.setFont("Verdana", 14)
							PcToPdf.create_component_table(i, c, each_hdd, hdd_table, "HDD Specification")
					else:
						l = 1
						for each_hdd in setpc[i]:
							hdd_table = []
							c.setFont("Verdana", 14)
							PcToPdf.create_component_table(i, c, each_hdd, hdd_table, "HDD " + str(l) + " Specification")
							l += 1
				if i == 6:
					psu_table = []
					c.setFont("Verdana", 14)
					PcToPdf.create_component_table(i, c, setpc, psu_table, "PSU Specification")
				if i == 7:
					case_table = []
					c.setFont("Verdana", 14)
					PcToPdf.create_component_table(i, c, setpc, case_table, "Case Specification")

		# Save the file
		c.save()
		buf.seek(0)
		return FileResponse(buf, as_attachment=True, filename=fileName)