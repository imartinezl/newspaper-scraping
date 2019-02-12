
data <- read.csv('data.csv', stringsAsFactors = F)

library(dplyr)

data %>% 
  dplyr::distinct(date) %>% 
  # dplyr::mutate(cat = gsub(".*, |\\..*", "", name)) %>% 
  View()

duplicated()
strsplit(data[2,]$url,'/')[[1]][4]
