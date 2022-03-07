import typing

example_grids = """
arima = {
	'order':[(2,1,0),(0,1,2),(1,1,1)],
	'seasonal_order':[(0,1,1,12),(2,1,0,12)],
	'trend':['n','c','t','ct']
}

elasticnet = {
	'alpha':[i/10 for i in range(1,21)],
	'l1_ratio':[0,0.25,0.5,0.75,1],
	'normalizer':['scale','minmax',None]
}

gbt = {
	'max_depth':[2,3],
	'max_features':['sqrt',None]
}

hwes = {
	'trend':['add','mul'],
	'seasonal':['add','mul']
}

knn = {
	'n_neighbors':range(2,21),
	'weights':['uniform','distance']
}


lightgbm = {
	'max_depth':[2,3]
}

mlp = {
	'activation':['relu','tanh'],
	'hidden_layer_sizes':[(25,),(25,25,)],
	'solver':['lbfgs','adam'],
	'normalizer':['minmax','scale'],
	'random_state':[20]
}

mlr = {
	'normalizer':['scale','minmax',None]
}

prophet = {
	'n_changepoints':range(5)
}

rf = {
	'max_depth':[2,5],
	'n_estimators':[100,500,1000]
}

silverkite = {
	'changepoints':range(5)
}

svr={
	'kernel':['linear'],
	'C':[.5,1,2,3],
	'epsilon':[0.01,0.1,0.5]
}

xgboost = {
	'max_depth':[2,3]
}
"""

empty_grids = """
arima = {}
elasticnet = {}
gbt = {}
hwes = {}
knn = {}
lightgbm = {}
mlp = {}
mlr = {}
prophet = {}
rf = {}
silverkite = {}
svr={}
xgboost = {}
"""

import os

def get_example_grids(overwrite=False):
	""" saves example grids to working directory as Grids.py (does not overwrite by default).

	Args:
		overwrite (bool): whether to overwrite a Grids.py file if one is already in the working directory.

	Returns:
		None
	"""
	if 'Grids.py' in os.listdir('./'):
		if not overwrite:
			return
	
	with open('Grids.py','w') as f:
		f.write(example_grids)

def get_empty_grids(overwrite=False):
	""" saves empty grids to working directory as Grids.py (does not overwrite by default).

	Args:
		overwrite (bool): whether to overwrite a Grids.py file if one is already in the working directory.

	Returns:
		None
	"""
	if 'Grids.py' in os.listdir('./'):
		if not overwrite:
			return
	
	with open('Grids.py','w') as f:
		f.write(empty_grids)