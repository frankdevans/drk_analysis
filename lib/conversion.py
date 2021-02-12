import numpy as np


def make_array(data, field):
	values = [i[field] for i in data]
	output = np.array(values)
	return output

def make_matrix(data, fields):
	values = []
	for field in fields:
		values.append([i[field] for i in data])
	
	output = np.array(values).T
	return output