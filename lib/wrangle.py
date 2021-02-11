import csv

def load_data(path):
	data = []
	fields = [
		'title', 'time', 'punchlines', 'laughs', 
		'pct', 'laughs_min', 'punch_min', 'spp', 'experience'
	]
	with open(path, 'r') as f:
		reader = csv.DictReader(f, delimiter = '\t', fieldnames = fields)
		next(reader, None)
		for row in reader: 
			entry = {}
			for (k,v) in row.items():
				entry[k] = float(v) if v.replace('.', '').isnumeric() else v
			
			data.append(entry)

	return data

def validate_datatype_consistency(data):
	fields = {}
	keys = data[0].keys()
	for k in keys:
		values = [i[k] for i in data]
		datatypes = [str(type(v)) for v in values]
		fields[k] = (len(set(datatypes)) == 1)

	output = {'fields': fields, 'overall': all(fields.values())}
	return output

# Interface ----------------------------------------------------------------------------------------

def process(path):
	data = load_data(path)
	is_valid = validate_datatype_consistency(data)
	if not is_valid['overall']:
		raise ValueError("There are datatype inconsistencies, please investigate.")
	return data
