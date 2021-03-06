from rpy2.robjects import r, pandas2ri
import numpy as np
import os.path
from scipy.sparse import csr_matrix
import sys

ENET_INDEX = 2

def rload(filepath):
    # load relevant info of specified RData file into np arrays
    r["load"](filepath)
    wgtmat = np.array(r["wgt.matrix"])
    wgtmat_rows = np.array(r["rownames"](r["wgt.matrix"]))
    snps = np.array(r["snps"]).T
    # construct snp to index dict
    snp2index = {k: v for v, k in enumerate(wgtmat_rows)}
    return (wgtmat, snps, snp2index)

def process_index_file(index_filepath):
    dirpath = os.path.dirname(index_filepath)
    expr_id_cache = {}
    snps_so_far = set()

    for row in np.genfromtxt(index_filepath, dtype="str", skip_header=1):
        rdata_relative_filepath, expr_id, chrom, p0, p1 = row
        wgtmat, snps, snp2index = rload(dirpath + "/" + rdata_relative_filepath)
        if expr_id in expr_id_cache:
            print("Duplicate expr_id, skipping second.")
        else:
            nonzero_snps = list(filter(lambda key: abs(wgtmat[snp2index[key], ENET_INDEX]) > 0, snp2index))
            expr_id_cache[expr_id] = {"wgtmat": wgtmat, "snps": snps, "snp2index": snp2index,
                "chrom": chrom, "p0": p0, "p1": p1, "nonzero_snps": nonzero_snps}
            snps_so_far.update(nonzero_snps) # this lets snps_so_far be the union of snps_so_far and the snps of snp2index.keys() with nonzero effects
    
    snp2col = {k: v for v, k in enumerate(snps_so_far)}
    expr2row = {k: v for v, k in enumerate(expr_id_cache)}
    gen2expr_wgtmat = np.zeros((len(expr2row), len(snp2col)))
    all_snps = np.empty((len(snp2col),), dtype=object)
    for expr_id in expr_id_cache:
        for snp in expr_id_cache[expr_id]["nonzero_snps"]:
            gen2expr_wgtmat[expr2row[expr_id], snp2col[snp]] = expr_id_cache[expr_id]["wgtmat"][expr_id_cache[expr_id]["snp2index"][snp], ENET_INDEX]
            all_snps[snp2col[snp]] = [expr_id_cache[expr_id]["snps"][expr_id_cache[expr_id]["snp2index"][snp]][i] for i in [1,2,4,5]]

    return (csr_matrix(gen2expr_wgtmat), expr2row, snp2col, all_snps)

def process_index_file_chr(index_filepath, c):
    dirpath = os.path.dirname(index_filepath)
    expr_id_cache = {}
    snps_so_far = set()

    for row in np.genfromtxt(index_filepath, dtype="str", skip_header=1):
        rdata_relative_filepath, expr_id, chrom, p0, p1 = row
        if int(chrom) == c:
            wgtmat, snps, snp2index = rload(dirpath + "/" + rdata_relative_filepath)
            if expr_id in expr_id_cache:
                print("Duplicate expr_id, skipping second.")
            else:
                nonzero_snps = list(filter(lambda key: abs(wgtmat[snp2index[key], ENET_INDEX]) > 0, snp2index))
                expr_id_cache[expr_id] = {"wgtmat": wgtmat, "snps": snps, "snp2index": snp2index,
                    "chrom": chrom, "p0": p0, "p1": p1, "nonzero_snps": nonzero_snps}
                # this lets snps_so_far be the union of snps_so_far and the snps of snp2index.keys() with nonzero effects
                snps_so_far.update(nonzero_snps) 
    snp2col = {k: v for v, k in enumerate(snps_so_far)}
    expr2row = {k: v for v, k in enumerate(expr_id_cache)}
    gen2expr_wgtmat = np.zeros((len(expr2row), len(snp2col)))
    all_snps = np.empty((len(snp2col),), dtype=object)
    for expr_id in expr_id_cache:
        for snp in expr_id_cache[expr_id]["nonzero_snps"]:
            gen2expr_wgtmat[expr2row[expr_id], snp2col[snp]] = expr_id_cache[expr_id]["wgtmat"][expr_id_cache[expr_id]["snp2index"][snp], ENET_INDEX]
            all_snps[snp2col[snp]] = [expr_id_cache[expr_id]["snps"][expr_id_cache[expr_id]["snp2index"][snp]][i] for i in [1,2,4,5]]

    return (csr_matrix(gen2expr_wgtmat), expr2row, snp2col, all_snps)

def save_gen2expr_wgtmat(filepath, gen2expr_wgtmat, expr2row, snp2col, snps):
    np.savez_compressed(filepath, gen2expr_wgtmat=gen2expr_wgtmat, expr2row=expr2row, snp2col=snp2col, snps=snps)

if __name__ == "__main__":
    index_filepath = sys.argv[1]
    save_filepath = sys.argv[2]
    gen2expr_wgtmat, expr2row, snp2col, snps = process_index_file(index_filepath)
    save_gen2expr_wgtmat(save_filepath, gen2expr_wgtmat, expr2row, snp2col, snps)
    