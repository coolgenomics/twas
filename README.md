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

```Bash
Rscript PlinkToCSV.R \
  --ref <Prefix to reference LD files in binary PLINK format by chromosome [required]> 
  --chr <Chromosome to analyze, currently only single chromosome analyses are performed [required]> \
  --genos <File name to store the genos data (with suffix .csv) [required]> \
  --alleles <File name to store the alleles data (with suffix .csv) [required]>
```


## Development Guidelines / Git Tutorial
See [Git guidelines](documentation/GIT_GUIDELINES.md)
