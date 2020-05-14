library(dplyr)
library(magrittr)
library(ggplot2)
library(ggwordcloud)
library(data.table)
library(tidyr)
library(viridis)

FIG.DIR = '/home/peter/Junkspace/nyt_xword/figures/'
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

clues %>% select(cluster) %>% group_by(cluster) %>% count %>% t %>% write.csv('cluster_size.csv')

# PLOT PUN/CULTURE PERCENT BY CLUSTER
clues_clust_summ = clues %>% group_by(cluster) %>%
  summarize(pun.mn = mean(is_pun_clue),
            pun.sd = sqrt(mean(is_pun_clue)*(1-mean(is_pun_clue))/n()),
            cult.mn = mean(is_culture_clue),
            cult.sd = sqrt(mean(is_culture_clue)*(1-mean(is_culture_clue))/n()))
clues_clust_summ$cluster %<>% as.factor

p.pun.cult = ggplot(clues_clust_summ,aes(x=cluster)) +
  geom_point(aes(y=pun.mn,color='Pun'),size=4) +
  geom_point(aes(y=cult.mn,color='Culture'),size=4) +
  labs(x='Cluster',y='Percent Pun or Culture Clues',color='Clue Type') +
  theme(text=element_text(size=16))
ggsave('cluster_pun_cult.png',p.pun.cult)

# PLOT CLUSTER GROUP TIME SERIES
cluster_group = function(clust) {
  wordplay = c(4,6)
  wordplay10 = c(4,6,10)
  trivia = c(5,7,8,9)
  nickname = c(3)
  simile = c(1)
  abbr = c(2)

  if (clust %in% wordplay10){return('Wordplay')}
  if (clust %in% trivia){return('Trivia')}
  if (clust %in% nickname){return('Nickname')}
  if (clust %in% simile){return('Simile')}
  if (clust %in% abbr){return('Abbr')}
  else {return('Misc')}
}

clues$group = sapply(clues$cluster,cluster_group) %>%
  unlist %>%
  as.character

year_group_summ = clues %>%
  add_count(puzzle_year) %>%
  group_by(puzzle_year,group) %>%
  summarize(usage=n()/mean(n))

plot_shape = c(16,7)
p.group.year = ggplot(year_group_summ %>% filter(group!='Misc'),
                      aes(x=puzzle_year, y=usage, color=as.factor(group),group=group)) +
  geom_line()+
  #scale_colour_viridis_d() +
  labs(x='Day',y='Usage',title='Percent Clues Belonging to Group by Year',color='Group') +
  theme(text=element_text(size=20),
        legend.text=element_text(size=16),
        title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_group_year.png'),p.group.year,width=plot_shape[1],height=plot_shape[2])


day_group_summ = clues %>%
  add_count(puzzle_day_name) %>%
  group_by(puzzle_day_name,group) %>%
  summarize(usage=n()/mean(n))

p.group.day = ggplot(day_group_summ %>% filter(group!='Misc'),
                      aes(x=puzzle_day_name, y=usage, color=as.factor(group),group=group)) +
  geom_line()+
  #scale_colour_viridis_d() +
  labs(x='Day',y='Usage',title='Percent Clues Belonging to Group by Day',color='Group') +
  theme(text=element_text(size=20),
        legend.text=element_text(size=16),
        title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_group_day.png'),p.group.day,width=plot_shape[1],height=plot_shape[2])

library(patchwork)
p.group = p.group.year/p.group.day
ggsave(paste0(FIG.DIR,'plt_group.png'),p.group,width=plot_shape[1],height=2*plot_shape[2])
