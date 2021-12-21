import json

f = open('psu.json', 'r', encoding='utf-8')
psu = json.load(f)
f.close()

for i in psu:
	i['price'] = str(i['price'])

f = open('final_psu.json', 'w', encoding='utf-8')
json.dump(psu, f)
f.close()