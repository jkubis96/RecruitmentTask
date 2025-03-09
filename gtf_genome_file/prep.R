
# annotation version used by Archs4


URL <- "https://ftp.ensembl.org/pub/release-107/gtf/homo_sapiens/Homo_sapiens.GRCh38.107.gtf.gz"



file_name <- "Homo_sapiens.GRCh38.107.gtf.gz"  

download.file(URL, file_name, mode = "wb")


library(R.utils)

gunzip(file_name, remove = FALSE) 


# install.packages("https://github.com/jkubis96/GTF-tool/raw/refs/heads/main/packages/GTF.tool_0.1.0.tar.gz", repos = NULL, type = "source")


library(GTF.tool)
library(dplyr)


# load GTF
GTF <- load_annotation('Homo_sapiens.GRCh38.107.gtf')


# check format GTF$X9[1]

# select coding protein (demat data based on coding)
GTF_coding <- GTF %>% filter(grepl("protein_coding", X9))


# extract gene_id / gene_name
GTF2 <- create_GTF_df(GTF_coding, optimize = FALSE)



#create transcript length
GTF2$len <- GTF2$end - GTF2$start



colnames(GTF2)

GTF3 <- GTF2[, c('gene_name', 'gene_id', 'len')]

GTF_id <- GTF2[, c('gene_id', 'len')]
GTF_gn <- GTF2[, c('gene_name', 'len')]

rm(GTF3, GTF2, GTF)


colnames(GTF_id) <- c('id', 'len')
colnames(GTF_gn) <- c('id', 'len')


GTF_full <- rbind(GTF_id, GTF_gn)

GTF_full <- GTF_full[!'' == GTF_full$id, ]


rm(GTF_id, GTF_gn)


GTF3_red <- GTF_full %>%
  select(id, len) %>% 
  group_by(id) %>% 
  slice_max(len, n = 1) %>%  
  ungroup()  


write.table(GTF3_red, file.path('transcript_length.gtf'), quote = F, sep = '\t')

