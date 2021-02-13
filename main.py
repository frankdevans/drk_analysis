import json, itertools

from lib import wrangle, conversion

import numpy as np
from sklearn.linear_model import LinearRegression


# Analytic Helpers ---------------------------------------------------------------------------------

def run_corr(x, y):
	res = np.corrcoef(x, y)
	scalar = float(res[0][1])
	return scalar

def run_linear_model(features, labels, intercept, normalize):
	model = LinearRegression(fit_intercept = intercept, normalize = normalize)
	model.fit(X = features, y = labels)

	res = {}
	res['params'] = {
		'intercept': intercept,
		'normalized': normalize,
	}
	res['results'] = {
		'coef_det': model.score(X = features, y = labels),
		'coef': [float(i) for i in model.coef_],
		'intercept': model.intercept_,
		'singular': [float(i) for i in model.singular_],
	}

	return res

# Output Helpers -----------------------------------------------------------------------------------

def text_breakdown_corr(results):
	coll = []
	coll.append('Pearson Correlation Matrix')
	coll.append('')
	for res in results:
		coll.append(f"{res['x']} | {res['y']} : {round(res['corr'], 3)}")
	
	output = '\n'.join(coll)
	return output

def text_breakdown_linear(results):
	coll = []
	for res in results:
		page = []
		int_line = '{x}intercept computed'.format(
			x = ('' if res['params']['intercept'] else 'no ')
		)
		norm_line = 'data {x}normalized'.format(
			x = ('' if res['params']['normalized'] else 'not ')
		)
		page.append(f'Linear Regression - {int_line}, {norm_line}')
		page.append('')

		page.append('Features: {fea} | Labels: {lab}'.format(
			fea = ', '.join(res['selection']['features']),
			lab = res['selection']['labels']
		))
		page.append(f"Number of Data Points (n): {res['selection']['n']}")
		page.append("Coefficient of Determination (R²): {cd}".format(
			cd = round(res['results']['coef_det'], 3)
		))
		page.append("Intercept: {int}".format(
			int = round(res['results']['intercept'], 3)
		))
		page.append('')

		page.append('Feature Coefficients')
		for (f,c) in zip(res['selection']['features'], res['results']['coef']):
			page.append(f'{f}: {round(c, 3)}')


		coll.append('\n'.join(page))

	output = '\n\n-------------------------\n\n'.join(coll)
	return output

def assemble_output(results, datecode):
	with open(f'./data/results_{datecode}.json', 'w') as f: json.dump(results, f)

	pages = []
	pages.append(text_breakdown_corr(results['PearsonCorrelation']))
	pages.append(text_breakdown_linear(results['LinearRegression']))
	
	text = '\n\n-------------------------\n\n'.join(pages)
	with open(f'./data/results_{datecode}.txt', 'w') as f: f.write(text)
	return

# Responders ---------------------------------------------------------------------------------------

def run_correlations(data):
	fields = ['punch_min', 'sec_punch', 'experience_months', 'pct_punch_laughs', 'laughs_min',]

	results = []
	for (x,y) in itertools.combinations(fields, 2):
		corr = run_corr(
			x = conversion.make_array(data, x),
			y = conversion.make_array(data, y)
		)
		results.append({'x': x, 'y': y, 'corr': corr})
	
	return results

def run_linear_models(data):
	dep_fields = ['punch_min', 'sec_punch', 'experience_months']
	ind_fields = ['pct_punch_laughs', 'laughs_min']
	bools = [True, False]

	results = []
	for (label_field, intercept, normalize) in itertools.product(ind_fields, bools, bools):
		output = {}
		output['selection'] = {
			'features': dep_fields,
			'labels': label_field,
			'n': len(data)
		}
		output.update(run_linear_model(
			features = conversion.make_matrix(data, dep_fields),
			labels = conversion.make_array(data, label_field),
			intercept = intercept,
			normalize = normalize
		))
		results.append(output)

	return results

def run_package(datecode):
	path = f'./data/received_{datecode}.txt'
	data = wrangle(path)

	results  ={}
	results['PearsonCorrelation'] = run_correlations(data)
	results['LinearRegression'] = run_linear_models(data)
	
	assemble_output(results, datecode)

	return

# Interface ----------------------------------------------------------------------------------------

datecode = '20210205'
run_package(datecode)
