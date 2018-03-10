# include the required libraries

 # library for web scrapping
   library(rvest)
   library(xml2)

 # used to implement a map
   library(hashmap)

#------------Variable declaration-------------------------------

 # Main website url
   howstat <- 'http://www.howstat.com/cricket/Statistics/Matches/MatchListMenu.asp?r=O#odis?data-scroll=false'
    
   base_url <- 'http://www.howstat.com/cricket/Statistics/Matches/'
    
  
   data <- howstat %>% read_html()
    
   year <- 1997:2016
   year_link <- NULL
   link_map <- NULL
#----------------xxxxxxxxxxxxxxxxxxxxx-----------------------------


 buildXpath <- function(year){
   
   xpath <- paste0(".//div[@id='odis']/table//*[not(self::td)][contains(text(),'",year,"')]")
 }


 get_yearwise_link <- function(){
  
    for(i in 1:length(year)){
          xpath <- buildXpath(year[i])
          link <-  data %>% html_node(xpath = xpath) %>% html_attr('href')
          if(is.na(link)){
                link <-  data %>% html_node(xpath = paste0(xpath,'/parent::a')) %>% html_attr('href')
          }
          year_link[i] <- paste0(base_url, link)
    }
    
    link_map <- hashmap(year, year_link)
    return(link_map)
 }
