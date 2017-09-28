suppressMessages(library('plink2R'))
suppressMessages(library("optparse"))

option_list = list(
  make_option("--ref", action="store", default=NA, type='character',
              help="Prefix to reference LD files in binary PLINK format by chromosome [required]"),
  make_option("--chr", action="store", default=NA, type='character',
              help="Chromosome to analyze, currently only single chromosome analyses are performed [required]"),
  make_option("--genos", action="store", default=NA, type='character',
              help="File name to store the genos data (with suffix .csv) [required]"),
  make_option("--alleles", action="store", default=NA, type='character',
              help="File name to store the alleles data (with suffix .csv) [required]")
)

opt = parse_args(OptionParser(option_list=option_list))

chr = as.character(opt$chr)
genos = read_plink(paste(opt$ref,chr,sep=''),impute="avg")

genos$bim = genos$bim[,c(1,2,5,6)]
colnames(genos$bim) = c("chr","SNP","A1", "A2")

write.csv(genos$bed, opt$genos)
write.csv(genos$bim, opt$alleles, row.names = FALSE)

