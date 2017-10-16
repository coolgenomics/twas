import numpy as np
import sys
import csv

FLIP = {'A':'T','T':'A','C':'G','G':'C'}

def load_gen2expr_wgtmat(filepath):
    loaded = np.load(filepath)
    return (loaded["gen2expr_wgtmat"].item(), loaded["expr2row"].item(), loaded["snp2col"].item(), loaded["snps"])

# check whether the alleles are recorded in different ways. Return 1 if not flipped, -1 if flipped, 0 if uncertain or ambiguous
def flip_stat(a1, a2, b1, b2):
	if (a1=="A" and a2=="T") or (a1=="T" and a2=="A") or (a1=="C" and a2=="G") or (a1=="G" and a2=="C"):
		return 0
	ref1 = FLIP[b1]
	ref2 = FLIP[b2]
	if (a1 == b1 and a2 == b2) or (a1 == b2 and a2 == b1):
		return 1
	if (a1 == ref1 and a2 == ref2) or (a1 == ref2 and a2 == ref1):
		return -1
	return 0

# flips the sign and clears the weight values whenever necessary
def flip_weights(gen2expr_wgtmat, snp2col, expr2row, alleles_path, snps):
	with open(alleles_path) as csvfile:
		csvreader = csv.reader(csvfile)
		# skips header
		next(csvreader)
		for row in csvreader:
			if row[1] in snp2col:
				snp = snps[snp2col[row[1]]]
				stat = flip_stat(row[2], row[3], snp[2], snp[3])
				for i in range(len(expr2row)):
					if not gen2expr_wgtmat[i,snp2col[row[1]]] == 0.0:
						gen2expr_wgtmat[i,snp2col[row[1]]] *= stat
	return gen2expr_wgtmat

def calc_expr(gen2expr_wgtmat, snp2col, genos_path):
	sample = []
	all_expr = []
	with open(genos_path) as csvfile:
		csvreader = csv.reader(csvfile)
		snp_header = next(csvreader)[1:]
		snp_map = {}
		
		for i in range(len(snp_header)):
			if snp_header[i] in snp2col:
				snp_map[snp2col[snp_header[i]]] = i
		for row in csvreader:
			sample.append(row[0])
			row = np.array(row[1:], dtype=int)
			row_vec = np.array([row[snp_map[i]] if i in snp_map else 0 for i in range(gen2expr_wgtmat.shape[1])])
			res = gen2expr_wgtmat.dot(row_vec)
			all_expr.append(res)
	return (np.array(sample), np.array(all_expr))

def calc_expr_by_data(gen2expr_wgtmat, snp2col, genos, snps):
	all_expr = []
	snp_map = {}
	for i in range(len(snps)):
		if snps[i] in snp2col:
			snp_map[snp2col[snps[i]]] = i
	for row in genos:
		row_vec = np.array([row[snp_map[i]] if i in snp_map else 0 for i in range(gen2expr_wgtmat.shape[1])])
		res = gen2expr_wgtmat.dot(row_vec)
		all_expr.append(res)
	return np.array(all_expr)

def save_expr(filepath, sample, all_expr, expr2row):
    np.savez_compressed(filepath, sample=sample, all_expr=all_expr, expr2row=expr2row)

if __name__ == "__main__":
    weight_filepath = sys.argv[1]
    alleles_path = sys.argv[2]
    genos_path = sys.argv[3]
    save_path = sys.argv[4]
    gen2expr_wgtmat, expr2row, snp2col, snps = load_gen2expr_wgtmat(weight_filepath)
    gen2expr_wgtmat = flip_weights(gen2expr_wgtmat, snp2col, expr2row, alleles_path, snps)
    sample, all_expr = calc_expr(gen2expr_wgtmat, snp2col, genos_path)
    save_expr(save_path, sample, all_expr, expr2row)



