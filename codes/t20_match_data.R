library(xml2)
library(rvest)


twenty_over_years <- 2005:2016
twenty_over_years_links <- c(
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2005010120051231&Range=2005',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2006010120061231&Range=2006',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2007010120071231&Range=2007',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2008010120081231&Range=2008',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2009010120091231&Range=2009',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2010010120101231&Range=2010',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2011010120111231&Range=2011',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2012010120121231&Range=2012',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2013010120131231&Range=2013',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2014010120141231&Range=2014',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2015010120151231&Range=2015',
                            'http://www.howstat.com/cricket/Statistics/Matches/MatchList_T20.asp?Group=2016010120161231&Range=2016'
                            )


scorecard_link_xpath <- "//a[text()='Scorecard']"
yearTable_xpath <- "//table[@class='TableLined']"


scorecard_base_url <- "http://www.howstat.com/cricket/Statistics/Matches/"


get_twenty_allScorecard_data <- function(twenty_all_scorecard_links){
  
  for(i in 1:length(twenty_all_scorecard_links)){
    
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
    
    scorecard_page_data <- NULL
    
  }
}

for(count in 1:length(twenty_over_years_links)){ 
  
 current_year <- twenty_over_years[count] 
 
 dframe_name <- paste0('matches_t20_',current_year)
 
 current_year_data <- twenty_over_years_links[count] %>% read_html()
 
 twenty_all_scorecard_links <- paste0(scorecard_base_url,
                                      current_year_data %>% html_nodes(xpath= scorecard_link_xpath) %>% html_attr("href")
                               )
 
 write.csv(assign(dframe_name,cbind(current_year_data %>% html_node(xpath=yearTable_xpath) %>% html_table(header=TRUE),
                                    scorecard_links = twenty_all_scorecard_links
                              )
           ),
           file = paste0('data/',dframe_name,'.csv'),
           row.names = FALSE
 )
 

 Sys.sleep(3)
 
}
 