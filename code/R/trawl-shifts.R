# script for collecting trait data for pinsky et al centroid movement range shifts
library(dplyr)
library(ggplot2)
library(rfishbase)

PLOT = FALSE

max_difference_numeric <- function(x){
  return(x %>% summarise(diff=max(x[Latitude]) - min(x[param])))
}

max_difference_time <- function(x){
  min_p = (x %>% filter(Year == min(Year)) %>% select(Latitude))$Latitude
  max_p = (x %>% filter(Year == max(Year)) %>% select(Latitude))$Latitude
  std = sd(x$Latitude)
  return(data.frame(diff=max_p - min_p, std=std))
}

#datafile = "../data/marine/pinsky_trawl_west_annual_all.csv"
datafile = "../data/marine/pinsky_trawl_west_triennial_all.csv"
location = "west-coast-annual"

trawl_data = read.csv(datafile)
trawl_data = trawl_data %>% filter(Species != "ALL")

years = trawl_data %>% summarise(min_year = min(Year), 
                         max_year = max(Year))

summary_year = trawl_data %>% group_by(Species) %>% do(max_difference_time(.))

print(nrow(summary_year))


if (PLOT){
  bp = ggplot(summary_year %>% arrange(desc(diff)), aes(x = Species, y = diff)) 
  bp + geom_pointrange(aes(ymin=diff-std, ymax=diff+std)) +
      ylab("Latitudinal Difference over Time (degrees)") +
      xlab("Species") +
      ggtitle(paste("Latitudinal Shifts over time + std deviation (" , location , ", " , years$min_year , "-" , years$max_year , ")")) + 
      theme( axis.text.x=element_blank(),
             axis.ticks.x=element_blank()) +
      ggsave(paste(location, "_diff.png"), width=11, height=8.5, units="in")
}

general_traits = species(summary_year$Species)
#general_ecology = ecology(summary_year$Species)

#alltraits = merge(general_traits, general_ecology, by='sciname')
alltraits = general_traits
col.has.na <- apply(alltraits, 2, function(x){any(is.na(x))})

alltraits_nona = alltraits[!col.has.na]

alldata = merge(summary_year, alltraits_nona, by.x="Species", by.y="sciname")

colnames(alldata)[2] = "Latitudinal Difference"
colnames(alldata)[3] = "Latitudinal Std"

## Choose Columns
print(colnames(alldata))
keep_columns = c("Species",
                 "Latitudinal Difference", 
                 "Latitudinal Std",
                 "FamCode",
                 "GenCode",
                 "Fresh",
                 "Brack",
                 "Saltwater",
                 "DemersPelag",
                 "DepthRangeDeep",
                 "Vulnerability",
                 "Length")
                 

alldata = alldata[, keep_columns]

write.csv(alldata, file=paste(location, "_species_generaltraits.csv"))


