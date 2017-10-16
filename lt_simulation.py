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
