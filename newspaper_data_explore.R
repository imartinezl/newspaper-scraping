
data <- read.csv('data.csv', stringsAsFactors = F)

library(dplyr)

data %>% 
  dplyr::distinct(date, .keep_all = T) %>% 
  filter(!grepl(pattern = "cookies",x = text)) %>% 
  View()

duplicated()
strsplit(data[2,]$url,'/')[[1]][4]
