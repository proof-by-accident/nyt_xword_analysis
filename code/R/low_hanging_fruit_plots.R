library(dplyr)
library(magrittr)
library(ggplot2)
library(data.table)
library(viridis)

FIG.DIR = '/home/peter/Junkspace/nyt_xword/figures/low_hanging_fruit/'
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


plot_shape = c(16,7)

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
ggsave(paste0(FIG.DIR,'plt_pun_day.png'),p.pun.day,width=plot_shape[1],height=plot_shape[2])

p.pun.year = ggplot(clues_pun_summ,aes(x=puzzle_year,
                                       y=pun.mn)) +
  geom_line()+
  scale_colour_viridis_d() +
  labs(x='Day',y='Percent Pun Clues',title='Average Percent Pun Clues by Year')
ggsave(paste0(FIG.DIR,'plt_pun_year_one.png'),p.pun.year,width=plot_shape[1],height=plot_shape[2])

p.pun.year.full = ggplot(clues %>%
                         group_by(puzzle_year) %>%
                         summarize(pun.mn=mean(is_pun_clue),
                                   pun.sd=sd(is_pun_clue)),
                         aes(x=puzzle_year, y=pun.mn)) +
  geom_line()+
  labs(x='Year',y='Percent Pun Clues',title='Average Percent Pun Clues by Year') +
  theme(text=element_text(size=20), title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_pun_year_one.png'),p.pun.year.full,width=plot_shape[1],height=plot_shape[2])

p.pun.day.full = ggplot(clues %>%
                        group_by(puzzle_day_name) %>%
                         summarize(pun.mn=mean(is_pun_clue),
                                   pun.sd=sd(is_pun_clue)),
                         aes(x=puzzle_day_name, y=pun.mn)) +
  geom_point(size=5) +
  labs(x='Day',y='Percent Pun Clues',title='Average Percent Pun Clues by Day') +
  theme(text=element_text(size=20), title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_pun_day_one.png'),p.pun.day.full,width=plot_shape[1],height=plot_shape[2])

p.pun.month.full = ggplot(clues %>%
                        group_by(puzzle_day) %>%
                         summarize(pun.mn=mean(is_pun_clue),
                                   pun.sd=sd(is_pun_clue)),
                         aes(x=puzzle_day, y=pun.mn)) +
  geom_line() +
  labs(x='Day',y='Percent Pun Clues',title='Average Percent Pun Clues by Day of the Month') +
  theme(text=element_text(size=20), title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_pun_month_one.png'),p.pun.month.full,width=plot_shape[1],height=plot_shape[2])

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
ggsave(paste0(FIG.DIR,'plt_culture_day.png'),p.cult.day,width=plot_shape[1],height=plot_shape[2])

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
ggsave(paste0(FIG.DIR,'plt_culture_year.png'),p.cult.year,width=plot_shape[1],height=plot_shape[2])

p.cult.year.full = ggplot(clues %>%
                          group_by(puzzle_year) %>%
                          summarize(cult.mn=mean(is_culture_clue),
                                    cult.sd=sd(is_culture_clue)/n()),
                          aes(x=puzzle_year,y=cult.mn)) +
  geom_line()+
  labs(x='Year',y='Percent Culture Clues',title='Average Percent Culture Clues by Year') +
  theme(text=element_text(size=20), title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_cult_year_one.png'),p.cult.year.full,width=plot_shape[1],height=plot_shape[2])

p.cult.day.full = ggplot(clues %>%
                          group_by(puzzle_day_name) %>%
                          summarize(cult.mn=mean(is_culture_clue),
                                    cult.sd=sd(is_culture_clue)/n()),
                          aes(x=puzzle_day_name,y=cult.mn)) +
  geom_point(size=4)+
  labs(x='Year',y='Percent Culture Clues',title='Average Percent Culture Clues by Day') +
  theme(text=element_text(size=20), title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_cult_day_one.png'),p.cult.day.full,width=plot_shape[1],height=plot_shape[2])

p.cult.month.full = ggplot(clues %>%
                          group_by(puzzle_day) %>%
                          summarize(cult.mn=mean(is_culture_clue),
                                    cult.sd=sd(is_culture_clue)/n()),
                          aes(x=puzzle_day,y=cult.mn)) +
  geom_line()+
  labs(x='Year',y='Percent Culture Clues',title='Average Percent Culture Clues by Day of Month') +
  theme(text=element_text(size=20), title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_cult_month_one.png'),p.cult.month.full,width=plot_shape[1],height=plot_shape[2])

library(patchwork)
p.pun.main = p.pun.day.full/p.pun.year.full
ggsave(paste0(FIG.DIR,'plt_pun_main.png'),p.pun.main,width=plot_shape[1],height=2.5*plot_shape[2])
p.cult.main = p.cult.day.full/p.cult.year.full
ggsave(paste0(FIG.DIR,'plt_cult_main.png'),p.cult.main,width=plot_shape[1],height=2.5*plot_shape[2])
p.month.main = p.cult.month.full/p.pun.month.full
ggsave(paste0(FIG.DIR,'plt_month_main.png'),p.month.main,width=plot_shape[1],height=2.5*plot_shape[2])
p.cult.pun.main = (p.pun.day.full+p.cult.day.full)/(p.pun.year.full+p.cult.year.full)
ggsave(paste0(FIG.DIR,'pun_cult_main.png'),p.cult.pun.main,width=2*plot_shape[1],height=2.5*plot_shape[2])

clues$clue_is_across[clues$clue_is_across]='Across'
clues$clue_is_across[clues$clue_is_across==FALSE]='Down'

p.pun.year.full = ggplot(clues %>%
                         group_by(puzzle_year) %>%
                         summarize(pun.mn=mean(is_pun_clue),
                                   pun.sd=sd(is_pun_clue)),
                         aes(x=puzzle_year, y=pun.mn)) +
  geom_line()+
  labs(x='Year',y='Percent Pun Clues',title='Average Percent Pun Clues by Year') +
  theme(text=element_text(size=20), title=element_text(size=22))
ggsave(paste0(FIG.DIR,'plt_pun_year_one.png'),p.pun.year.full,width=plot_shape[1],height=plot_shape[2])

p.pun.day.full = ggplot(clues %>%
                        group_by(puzzle_day_name,clue_is_across) %>%
                         summarize(pun.mn=mean(is_pun_clue),
                                   pun.sd=sd(is_pun_clue)),
                         aes(x=puzzle_day_name, y=pun.mn,group=clue_is_across,color=clue_is_across)) +
  geom_point(size=5) +
  labs(x='Day',y='Percent Pun Clues',title='Average Percent Pun Clues by Day',color='Across or Down') +
  theme(text=element_text(size=20), title=element_text(size=22),legend.position='None')

p.pun.year.full = ggplot(clues %>%
                         group_by(puzzle_year,clue_is_across) %>%
                         summarize(pun.mn=mean(is_pun_clue),
                                   pun.sd=sd(is_pun_clue)),
                         aes(x=puzzle_year, y=pun.mn,group=clue_is_across,color=clue_is_across)) +
  geom_line()+
  labs(x='Year',y='Percent Pun Clues',title='Average Percent Pun Clues by Year',color='Across or Down') +
  theme(text=element_text(size=20), title=element_text(size=22),legend.position='None')

p.cult.year.full = ggplot(clues %>%
                          group_by(puzzle_year,clue_is_across) %>%
                          summarize(cult.mn=mean(is_culture_clue),
                                    cult.sd=sd(is_culture_clue)/n()),
                          aes(x=puzzle_year,y=cult.mn,group=clue_is_across,color=clue_is_across)) +
  geom_line()+
  labs(x='Year',y='Percent Culture Clues',title='Average Percent Culture Clues by Year',color='Across or Down') +
  theme(text=element_text(size=20), title=element_text(size=22))

p.cult.day.full = ggplot(clues %>%
                          group_by(puzzle_day_name,clue_is_across) %>%
                          summarize(cult.mn=mean(is_culture_clue),
                                    cult.sd=sd(is_culture_clue)/n()),
                          aes(x=puzzle_day_name,y=cult.mn,group=clue_is_across,color=clue_is_across)) +
  geom_point(size=4)+
  labs(x='Year',y='Percent Culture Clues',title='Average Percent Culture Clues by Day',color='Across or Down') +
  theme(text=element_text(size=20), title=element_text(size=22))

p.cult.pun.main = (p.pun.day.full+p.cult.day.full)/(p.pun.year.full+p.cult.year.full)
ggsave(paste0(FIG.DIR,'pun_cult_main_dir.png'),p.cult.pun.main,width=2*plot_shape[1],height=2.5*plot_shape[2])


