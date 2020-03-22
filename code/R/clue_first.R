library(dplyr)
library(magrittr)
library(ggplot2)
library(data.table)
library(viridis)

FIG.DIR = '/home/peter/Junkspace/nyt_xword/figures/'
DATA.DIR = '/home/peter/Junkspace/nyt_xword/data/'
clues = fread(paste0(DATA.DIR,'clues.csv')) %>% select(-'V1')
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


clues_pun_summ = clues %>%
  group_by(puzzle_day_name,puzzle_year) %>%
  summarize(pun.mn = mean(is_pun_clue),
            pun.sd = sd(is_pun_clue))

p.pun.day = ggplot(clues_pun_summ,
                   aes(x=puzzle_day_name,
                       y=pun.mn,
                       group=as.factor(puzzle_year),
                       colour=as.factor(puzzle_year))) + 
  geom_line()+
  scale_colour_viridis_d() +
  labs(x='Day',y='Percent Pun Clues',title='Average Percent Pun Clues over a Week',color='Year') +
  theme(legend.position=c(.15,.70),
        text=element_text(size=20),
        legend.text=element_text(size=16),
        title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_pun_day.png'),p.pun.day,width=16,height=10)

p.pun.year = ggplot(clues_pun_summ,aes(x=puzzle_year,
                                       y=pun.mn,
                                       group=puzzle_day_name,
                                       colour=puzzle_day_name)) +
  geom_line()+
  scale_colour_viridis_d() +
  labs(x='Day',y='Percent Pun Clues',title='Average Percent Pun Clues over Years',color='Day') +
  theme(legend.position=c(.15,.80),
        text=element_text(size=20),
        legend.text=element_text(size=16),
        title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_pun_year.png'),p.pun.year,width=16,height=10)



clues_cult_summ = clues %>%
  group_by(puzzle_day_name,puzzle_year) %>%
  summarize(cult.mn = mean(is_culture_clue),
            cult.sd = sd(is_culture_clue))

p.cult.day = ggplot(clues_cult_summ,aes(x=puzzle_day_name,
                                        y=cult.mn,
                                        group=as.factor(puzzle_year),
                                        colour=as.factor(puzzle_year))) +
  geom_line()+
  scale_colour_viridis_d() +
  labs(x='Day',y='Percent Culture Clues',title='Average Percent Culture Clues over a Week',color='Year') +
  theme(legend.position=c(.82,.80),
        text=element_text(size=20),
        legend.text=element_text(size=16),
        title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_culture_day.png'),p.cult.day,width=16,height=10)

p.cult.year = ggplot(clues_cult_summ,aes(x=puzzle_year,
                                       y=cult.mn,
                                       group=puzzle_day_name,
                                       colour=puzzle_day_name)) +
  geom_line() +
  scale_colour_viridis_d() +
  labs(x='Year',y='Percent Culture Clues',title='Average Percent Culture Clues over Years',color='Day') +
  theme(legend.position=c(.85,.80),
        text=element_text(size=20),
        legend.text=element_text(size=16),
        title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_culture_year.png'),p.cult.year,width=16,height=10)

