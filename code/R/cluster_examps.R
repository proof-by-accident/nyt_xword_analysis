library(dplyr)
library(magrittr)
library(ggplot2)
library(ggwordcloud)
library(data.table)
library(tidyr)
library(viridis)

FIG.DIR = '/home/peter/Junkspace/nyt_xword/figures/low_hanging_fruit/'
DATA.DIR = '/home/peter/Junkspace/nyt_xword/data/'
clues = fread(paste0(DATA.DIR,'clues_df_clusts.csv')) %>% select(-'V1')
clues$puzzle_year %<>% as.character %>% as.numeric
clues %<>% filter(puzzle_year>1990)
clues$puzzle_day_name %<>% factor(level=c('Mon',
                                          'Tue',
                                          'Wed',
                                          'Thu',
                                          'Fri',
                                          'Sat',
                                          'Sun',
                                          '0'))

## GET MAX WORDS FOR EACH CLUSTER
max_words_find = function(text,n=5){
  words = strsplit(text,' ')
  words %<>% unlist %>% table %>% sort(decreasing=TRUE)
  return(words%>%head(n))
}

plot_shape = c(16,7)
n = 5
for (c in unique(clues$cluster)){
  clust_text = clues %>% filter(cluster==c) %>% select(clue_text_clean) %>% unlist
  max_words = max_words_find(clust_text,n=n)

  if (c==unique(clues$cluster)[1]){
    clust.df = data.frame(cluster=rep(c,n),
                          word=names(max_words),
                          count=as.numeric(max_words))
  }

  else {
    new.df = data.frame(cluster=rep(c,n),
                        word=names(max_words),
                        count=as.numeric(max_words))

    clust.df %<>% rbind(new.df)
  }
}

clust.exs.df = list()
nexamps = 5
for (c in unique(clues$cluster)){
  examps = sample(clues %>% filter(cluster==c) %>% select(clue_text) %>% unlist,nexamps)
  clust.exs.df[[paste0('cluster.',c)]] = examps
}

clust.exs.df %<>% as.data.frame
rownames(clust.exs.df) = c()
write.table(clust.exs.df,'./cluster_examps.scsv',row.names=FALSE,sep=';')

