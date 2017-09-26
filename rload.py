from rpy2.robjects import r, pandas2ri
import numpy as np
import os.path 

ENET_INDEX = 2

def rload(filepath):
    # load relevant info of specified RData file into np arrays
    r["load"](filepath)
    wgtmat = np.array(r["wgt.matrix"])
    wgtmat_rows = np.array(r["rownames"](r["wgt.matrix"]))
    snps = np.array(r["snps"]).T
    
    # construct snp to index dict
    snp2index = {k: v for v, k in enumerate(wgtmat_rows)}
    
    # return stuff
    return (wgtmat, snps, snp2index)
    
def process_index_file(index_file_path):
    dirpath = os.path.dirname(index_file_path)
    expr_id_cache = {}
    snps_so_far = set()
    for row in np.genfromtxt(index_file_path, dtype="str", skip_header=1):
        rdata_relative_filepath, expr_id, chrom, p0, p1 = row
        wgtmat, snps, snp2index = rload(dirpath + "/" + rdata_relative_filepath)
        if expr_id in expr_id_cache:
            raise ValueError("BUG. Expr_id should not have already been processed.")
        nonzero_snps = list(filter(lambda key: abs(wgtmat[snp2index[key], ENET_INDEX]) > 0, snp2index))
        expr_id_cache[expr_id] = {"wgtmat": wgtmat, "snps": snps, "snp2index": snp2index, 
            "chrom": chrom, "p0": p0, "p1": p1, "nonzero_snps": nonzero_snps}
        snps_so_far.update(nonzero_snps) # this lets snps_so_far be the union of snps_so_far and the snps of snp2index.keys() with nonzero effects
    snp2col = {k: v for v, k in enumerate(snps_so_far)}
    expr2row = {k: v for v, k in enumerate(expr_id_cache)}
    gen2expr_wgtmat = np.zeros((len(expr2row), len(snp2col)))
    for expr_id in expr_id_cache:
        for snp in expr_id_cache[expr_id]["nonzero_snps"]:
            gen2expr_wgtmat[expr2row[expr_id], snp2col[snp]] = expr_id_cache[expr_id]["wgtmat"][expr_id_cache[expr_id]["snp2index"][snp], ENET_INDEX]
    return (gen2expr_wgtmat, expr2row, snp2col)

gen2expr_wgtmat, expr2row, snp2col = process_index_file("test/index.pos")
