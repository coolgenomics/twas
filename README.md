# TWAS
## Goal and description
Trying to recreate genotype-expression-trait pathway using weights provided by
previous studies.  
We are particularly interested in schizophrenia (the ``scz.txt`` files). However,
(unless I misunderstand) the ultimate goal of this repo would be to make an 
importable module that should be pretty generic and work with any of the files.

### Genotype-Expression Weights
We use the weights from this article:  
http://gusevlab.org/projects/fusion/

### Expression-Trait Weights
We use the weights from this article:  
https://github.com/bogdanlab/TWAS30

## Development Guidelines / Git Tutorial
See [Git guidelines](documentation/GIT_GUIDELINES.md)

## Python environment setup and running .py files
We are using Python 3.6.1 for this repo.  
I recommend having a look at ``pyenv`` and ``pyenv-virtualenv`` as a good way to
manage multiple python versions.  
Once you have python 3.6.1 (and the associated pip) running the following line
in a bash shell should install all required packages:  
``pip install -r requirements`` (or `pip3 install -r requirements` if that is the
name associated with your python 3.6.1 pip).