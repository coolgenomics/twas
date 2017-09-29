# TWAS
## Description
This program recreates the genotype-expression-trait pathway using weights provided by
previous studies. We aim to create an generic importable module that achieves the prediction
given genotyupe data and associated weights.

In our study, we are particularly interested in schizophrenia (the ``scz.txt`` files).

### Genotype-Expression Weights
We use the weights from this article:  
http://gusevlab.org/projects/fusion/

### Expression-Trait Weights
We use the weights from this article:  
https://github.com/bogdanlab/TWAS30

## Python environment setup and running .py files
We are using Python 3.6.1 for this repo.  
I recommend having a look at ``pyenv`` and ``pyenv-virtualenv`` as a good way to
manage multiple python versions.  
Once you have python 3.6.1 (and the associated pip) running the following line
in a bash shell should install all required packages:  
``pip install -r requirements.txt`` (or `pip3 install -r requirements.txt` if that is the
name associated with your python 3.6.1 pip).

## How to run the program
The program consist of two basic components: ``Plink2CSV.R`` and ``twas_predict.py``.

``Plink2CSV.R`` converts the sample genotype data from PLINK format to python-frindly CSV
format. Please make sure you have the LD Reference data directory in the same directory as
``Plink2CSV.R``. The script can be run as:

```Linux
Rscript PlinkToCSV.R \
  --ref <Prefix to reference LD files in binary PLINK format by chromosome [required]> 
  --chr <Chromosome to analyze [required]> \
  --genos <File name to store the genos data (with suffix .csv) [required]> \
  --alleles <File name to store the alleles data (with suffix .csv) [required]>
```

This will produce two csv files. The genos csv file stores the sample genotype data and alleles
csv stores the corresponding SNP alleles summary data.

``twas_predict.py`` contains the main script for performing the prediction. The file takes the
sample data and weights statistics to give a risk prediction for certain phenotypes (schizophrenia 
in our case). The script uses functions in ``parse_weights.py``, ``calc_expr.py`` and ``predict.py``.
It can be run as:

```Linux
python twas_predict.py \
<File path for Transcriptome weight index file> \
<File path for sample alleles data (in csv)> \
<File path for sample genotype data (in csv)> \
<File path for alpha values> \
<File path for saving the output>
```

A sample run is

```Linux
python twas_predict.py \
test/WEIGHTS/GTEx.Whole_Blood.pos \
test/alleles.csv \
test/genos.csv \
test/scz.txt \
test/result.npz
```

A sample result for the 22nd chromosome is included in the ``results`` directory. The
result is in compressed numpy format and contains the 7 following objects (n is sample size, 
m is genotype dimension, k is expression dimension):

|Name|Description|Format|
|----------|---------------------|---------|
|pred|Risk prediction result for the trait|n*1 numpy array|
|all_expr|The calculated expression value for all individual |n*k numpy array|
|sample|The identifier for each individual|n*1 numpy array|
|gen2expr_wgtmat|The weight matrix for genotype to expression|m*k CSR sparse matrix|
|alpha|The weight vector for expression to trait|k*1 numpy array|
|expr2row|Map from expression to row index|map of length k|
|snp2col|Map from SNP to column index|map of length m|


## Development Guidelines / Git Tutorial
See [Git guidelines](documentation/GIT_GUIDELINES.md)
