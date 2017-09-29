import parse_weights
import calc_expr
import predict
import sys
import numpy as np

def save_result(filepath, pred, all_expr, sample, gen2expr_wgtmat, alpha, expr2row, snp2col):
	np.savez_compressed(filepath, pred=pred, all_expr=all_expr, sample=sample, gen2expr_wgtmat=gen2expr_wgtmat, alpha=alpha, expr2row=expr2row, snp2col=snp2col)

if __name__ == "__main__":
	pos_path = sys.argv[1]
	alleles_path = sys.argv[2]
	genos_path = sys.argv[3]
	alpha_path = sys.argv[4]
	save_path = sys.argv[5]
	gen2expr_wgtmat, expr2row, snp2col, snps = parse_weights.process_index_file(pos_path)
	gen2expr_wgtmat = calc_expr.flip_weights(gen2expr_wgtmat, snp2col, expr2row, alleles_path, snps)
	sample, all_expr = calc_expr.calc_expr(gen2expr_wgtmat, snp2col, genos_path)
	alpha = predict.extract_alpha(alpha_path, expr2row)
	pred = all_expr.dot(alpha)
	save_result(save_path, pred, all_expr, sample, gen2expr_wgtmat, alpha, expr2row, snp2col)



