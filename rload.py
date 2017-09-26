from rpy2.robjects import r, pandas2ri
import numpy as np



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
    

    
wgtmat, snps, snp2index = rload("test.RDat")