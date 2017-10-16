import numpy as np
import sys
import csv

def load_expr(filepath):
    loaded = np.load(filepath)
    return (loaded["sample"], loaded["all_expr"], loaded["expr2row"].item())

def extract_alpha(alpha_path, expr2row):
	alpha = np.zeros(len(expr2row))
	with open(alpha_path) as csvfile:
		csvreader = csv.reader(csvfile, delimiter=' ')
		next(csvreader)
		for row in csvreader:
			if row[1] in expr2row:
				alpha[expr2row[row[1]]] = row[11]
	return alpha

def save_pred(filepath, pred, sample):
	np.savez_compressed(filepath, sample=sample, pred=pred)


if __name__ == "__main__":
	expr_filepath = sys.argv[1]
	alpha_path = sys.argv[2]
	save_path = sys.argv[3]
	sample, all_expr, expr2row = load_expr(expr_filepath)
	alpha = extract_alpha(alpha_path, expr2row)
	pred = all_expr.dot(alpha)
	save_pred(save_path, pred, alpha)
