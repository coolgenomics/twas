import numpy as np
import sys
import csv
import parse_weights
import calc_expr
import predict

def prepare_data(g2e_path, alpha_path):
	loaded1 = np.load(g2e_path)
	loaded2 = np.load(alpha_path)
	return (loaded1["gen2expr_wgtmat"].item(), loaded1["expr2row"].item(), loaded1["snp2col"].item(), loaded1["snps"], loaded2["alpha"])

def get_genos_data_from_npz(npz_path):
	loaded = np.load(npz_path)
	return (loaded["sample"], loaded["snps"], loaded["genos"])

def get_genos_data_from_csv(genos_path):
	sample = []
	genos = []
	with open(genos_path) as csvfile:
		csvreader = csv.reader(csvfile)
		snps = next(csvreader)[1:]
		for row in csvreader:
			sample.append(row[0])
			genos.append(np.array(row[1:], dtype=int))
	return (sample, snps, np.array(genos))

def get_freqs(genos):
	return np.array([np.mean(genos[:,i])/2 for i in range(genos.shape[1])], dtype=np.float64);

def simulate_individual(num, freqs):
	num = int(num)
	inds = np.empty([num, len(freqs)])
	for i, p in enumerate(freqs):
		sprobs = [(1-p)*(1-p), 2*p*(1-p), p*p]
		inds[:,i] = np.random.choice(3,size=num,p=sprobs)
	return inds

def get_pred(gen2expr_wgtmat, snp2col, genos, snps, alpha):
	expr = calc_expr.calc_expr_by_data(gen2expr_wgtmat, snp2col, genos, snps)
	pred = expr.dot(alpha)
	return (pred - np.mean(pred))/ np.std(pred)

def get_controls(control_size, freqs, gen2expr_wgtmat, snp2col, snps, alpha, thresh=2):
	control = []
	while(len(control) < control_size):
		inds = simulate_individual(control_size / 5, freqs)
		pred = get_pred(gen2expr_wgtmat, snp2col, inds, snps, alpha)
		for i, v in enumerate(pred):
			if v < thresh:
				control.append(inds[i])
				print("Getting " + str(len(control) - 1) + "th control")
	return np.array(control[0:control_size])
