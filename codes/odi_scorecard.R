library(hashmap)
source('fetchData.R')

year_link_map <- get_yearwise_link()

# table xpath
yearTable_xpath <- "//table[@class='TableLined']"

# scorecard link xpath
scorecard_link_xpath <- "//a[text()='Scorecard']"

# Day/Night xpath
day_night_xpath <- "//td[contains(text(),' Match Conditions:')]/following-sibling::td"
 
# toss outcome xpath
toss_xpath <- "//td[contains(text(),'  Toss:')]/following-sibling::td"
rain_xpath <- "//td[ contains(text(), 'Notes:')]/following-sibling::td"
firstInn_xpath <- "(//td[ contains(text(), 'Total')])[1]/following-sibling::td[2]"
secondInn_xpath <- "(//td[ contains(text(), 'Total')])[2]/following-sibling::td[2]"
wckts_ovrs_rr_xpath <- "(//td[ contains(text(), 'Total')])[1]/following-sibling::td[1]"
extras_xpath <- "(//td[contains(text(), 'Extras')])[1]/following-sibling::td[2]"
firstBat_xpath <- "(//td[contains(text(),'BF')])[1]/preceding-sibling::td[2]"



year_list <- year_link_map$keys()
day_night_list <- NULL
toss_list <- NULL
rain_list <- NULL
firstInn_score_list <- NULL
secondInn_score_list <- NULL
wckts_ovrs_rr_list <- NULL
extras_list <-  NULL
firstBat_list <- NULL

scorecard_base_url <- 'http://www.howstat.com/cricket/Statistics/Matches/'


get_all_scorecard_data <- function(all_scorecard_links){
       print(length(all_scorecard_links))
       total <- length(all_scorecard_links)
       for(i in 1:total){
            
            scorecard_page_data <- all_scorecard_links[i] %>% read_html()
            
            
            day_night_list[i] <<- scorecard_page_data %>%
                                  html_node(xpath = day_night_xpath) %>%
                                  html_text(trim = TRUE)
            
            toss_list[i] <<- scorecard_page_data %>% 
                             html_node(xpath = toss_xpath) %>% 
                             html_text(trim = TRUE)
            
            
            firstInn_score_list[i] <<- scorecard_page_data %>%
                                       html_node(xpath = firstInn_xpath)%>%
                                       html_text(trim = TRUE)
            
            secondInn_score_list[i] <<- scorecard_page_data %>%
                                        html_node(xpath = secondInn_xpath)%>%
                                        html_text(trim = TRUE)
            
            wckts_ovrs_rr_list[i] <<- scorecard_page_data %>%
                                      html_node(xpath = wckts_ovrs_rr_xpath)%>%
                                      html_text(trim = TRUE)
            
            extras_list[i] <<- scorecard_page_data %>%
                               html_node(xpath = extras_xpath)%>%
                               html_text(trim = TRUE)
            
            rain_list[i] <<- scorecard_page_data %>%
                             html_node(xpath = rain_xpath) %>%
                             html_text(trim = TRUE)
            
            firstBat_list[i] <<- scorecard_page_data %>% 
                                        html_node(xpath = firstBat_xpath) %>% 
                                        html_text(trim = TRUE)
            print(i)
            
            scorecard_page_data <- NULL
       }
}


 for(i in 1:length(year_list)){
  
  this_year <- year_list[i]
  #df_name <- paste0('matches_',this_year)
  annual_match_data <- year_link_map$find(this_year) %>% read_html()
  
  
  
  all_scorecard_links <- paste0(scorecard_base_url,
                                annual_match_data %>% html_nodes(xpath= scorecard_link_xpath) %>% html_attr("href")
                               )
  
  
  get_all_scorecard_data(all_scorecard_links)
  
    
  write.csv( assign(df_name, cbind(annual_match_data %>% html_node(xpath= yearTable_xpath) %>% html_table(header = TRUE),
                                    day_night=day_night_list,
                                    toss = toss_list,
                                    firstInn_score=firstInn_score_list, 
                                    secondInn_score=secondInn_score_list,
                                    wckts_ovrs_rr=wckts_ovrs_rr_list,
                                    extras=extras_list,
                                    rain = rain_list
                                 )
                   ),
             file =  paste0('data/',df_name,'.csv'),
             row.names = FALSE
  ) 
  df_name <- paste0('odi_firstbat_',this_year)
  write.csv(assign(df_name,cbind(first_batting=firstBat_list)),file = paste0('data/',df_name,'.csv'),row.names = FALSE)                                 
  firstBat_list <- NULL
  day_night_list <- NULL 
  toss_list <- NULL 
  rain_list <- NULL
  firstInn_score_list <- NULL
  secondInn_score_list <- NULL
  wckts_ovrs_rr_list <- NULL
  extras_list <-  NULL
  
  Sys.sleep(2)
 }

