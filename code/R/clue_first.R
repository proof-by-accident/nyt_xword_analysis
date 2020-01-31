library(dplyr)
library(magrittr)
library(ggplot2)
library(data.table)
library(viridis)

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
                   aes(x=puzzle_day_name, y=pun.mn,colour=as.factor(puzzle_year))) + 
  geom_point() + 
  scale_colour_viridis_d()


p.pun.year = ggplot(clues_pun_summ,aes(x=puzzle_year,
                                       y=pun.mn,
                                       group=puzzle_day_name,
                                       colour=puzzle_day_name)) +
  geom_line() + 
  scale_colour_viridis_d()



clues_cult_summ = clues %>%
  group_by(puzzle_day_name,puzzle_year) %>%
  summarize(cult.mn = mean(is_culture_clue),
            cult.sd = sd(is_culture_clue))

p.cult.day = ggplot(clues_cult_summ,aes(x=puzzle_day_name,
                                        y=cult.mn,colour=as.factor(puzzle_year))) +
  geom_point()+
  scale_colour_viridis_d()
  
p.cult.year = ggplot(clues_cult_summ,aes(x=puzzle_year,
                                       y=cult.mn,
                                       group=puzzle_day_name,
                                       colour=puzzle_day_name)) +
  geom_line() + 
  scale_colour_viridis_d()

