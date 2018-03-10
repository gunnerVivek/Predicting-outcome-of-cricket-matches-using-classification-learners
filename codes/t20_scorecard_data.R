library(xml2)
library(rvest)


year_list <- 2005:2016
data_read_path <- 'data/t20/'

day_night_xpath <- "//td[contains(text(),' Match Conditions:')]/following-sibling::td"
toss_xpath <- "//td[contains(text(),'  Toss:')]/following-sibling::td"
rain_xpath <- "//td[ contains(text(), 'Notes:')]/following-sibling::td"
firstInn_xpath <- "(//td[ contains(text(), 'Total')])[1]/following-sibling::td[2]"
secondInn_xpath <- "(//td[ contains(text(), 'Total')])[2]/following-sibling::td[2]"
wckts_ovrs_rr_xpath <- "(//td[ contains(text(), 'Total')])[1]/following-sibling::td[1]"
extras_xpath <- "(//td[contains(text(), 'Extras')])[1]/following-sibling::td[2]"
firstBat_xpath <- "(//td[contains(text(),'BF')])[1]/preceding-sibling::td[2]"

twenty_day_night_list <- NULL
twenty_toss_list <- NULL
twenty_rain_list <- NULL
twenty_firstInn_score_list <- NULL
twenty_secondInn_score_list <- NULL
twenty_wckts_ovrs_rr_list <- NULL
twenty_extras_list <-  NULL
twenty_firstBat_list <- NULL


get_twenty_allScorecard_data <- function(scorecard_url_list){
  
  for(k in 1:length(scorecard_url_list)){
    
    scorecard_page_data <- scorecard_url_list[k] %>% read_html()
    
    twenty_day_night_list[k] <<- scorecard_page_data %>%
      html_node(xpath = day_night_xpath) %>%
      html_text(trim = TRUE)
    
    twenty_toss_list[k] <<- scorecard_page_data %>% 
      html_node(xpath = toss_xpath) %>% 
      html_text(trim = TRUE)
    
    twenty_firstInn_score_list[k] <<- scorecard_page_data %>%
      html_node(xpath = firstInn_xpath)%>%
      html_text(trim = TRUE)
    
    twenty_secondInn_score_list[k] <<- scorecard_page_data %>%
      html_node(xpath = secondInn_xpath)%>%
      html_text(trim = TRUE)
    
    twenty_wckts_ovrs_rr_list[k] <<- scorecard_page_data %>%
      html_node(xpath = wckts_ovrs_rr_xpath)%>%
      html_text(trim = TRUE)
    
    twenty_extras_list[k] <<- scorecard_page_data %>%
      html_node(xpath = extras_xpath)%>%
      html_text(trim = TRUE)
    
    twenty_rain_list[k] <<- scorecard_page_data %>%
      html_node(xpath = rain_xpath) %>%
      html_text(trim = TRUE)
    
    twenty_firstBat_list[k] <<- scorecard_page_data %>% 
      html_node(xpath = firstBat_xpath) %>% 
      html_text(trim = TRUE)
    
    scorecard_page_data <- NULL
    
  }
}


for(i  in 1:length(year_list)){
  
  temp_df <- read.csv(file = paste0(data_read_path,'matches_t20_',year_list[i],'.csv'), header = TRUE)
  scorecard_url_list <- as.character(temp_df[ , ncol(temp_df)])
  
  print(paste('Year',year_list[i],length(scorecard_url_list),sep = ":"))
  
  get_twenty_allScorecard_data(scorecard_url_list)
  
  frame_name <- paste0('t20_extra_',year_list[i])
  
  write.csv(assign(frame_name,cbind( day_night=twenty_day_night_list,
                                     toss = twenty_toss_list,
                                     firstInn_score=twenty_firstInn_score_list,
                                     secondInn_score=twenty_secondInn_score_list,
                                     wckts_ovrs_rr=twenty_wckts_ovrs_rr_list,
                                     extras=twenty_extras_list,
                                     rain = twenty_rain_list,
                                     first_batting = twenty_firstBat_list
                               )
          ),
          file = paste0('E:/class/Dissertation/data/',frame_name,'.csv'),
          row.names = FALSE
   )
  
  temp_df <- NULL
  scorecard_url_list <- NULL
  
}

# rm(list = ls())
