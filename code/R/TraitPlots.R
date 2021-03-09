library(plyr)
library(dplyr)
library(reshape2)
library(tidyr)
library(ggplot2)
library(sjPlot)
library(car)
library(patchwork)
library(ggcorrplot)

#----
#Make plot of trait predictors for main text and supplement

#Vars to plot?
# alpine plants: seed shed month earliest, number floristic zones
# European plants: temp indicator, seed release height
# Mammals: alt timit, longevity
# Fish: depth, benthopelagic, vulnerability

#----
#read data

setwd("/Volumes/GoogleDrive/My Drive/Buckley/Work/StudentsPostdocs/Cannistra/Traits/data")

mammals= read.csv("mammals01.csv")
plants= read.csv("plants5.csv")
fish= read.csv("west-coast-triennial _species_generaltraits.csv")
eplants= read.csv("rumpf_ShiftsTraitsBuckley_20180418.csv")

#----
#mammals
# Mammals: alt timit, longevity

#update traits to correspond to Angert et al.
mammals$DietBreadth=0
mammals$DietBreadth[mammals$Food=="omni"]=1
mammals$AnnualRhythm=0
mammals$AnnualRhythm[mammals$Annual_rhythm=="fachib"]=1
mammals$DailyRhythm=0
mammals$DailyRhythm[mammals$Daily_rhythm=="both"]=1

#restrict traits
mammals=mammals[,c("Taxon","High_change","Orig_high_limit","Longevity_yrs","Litters_per_yr","Litter_size","Rangesize_km2","Mass_g","DailyRhythm","AnnualRhythm")]
#mammals=mammals[,c("Taxon","High_change","Orig_high_limit","Longevity_yrs","Bio1_std","Litters_per_yr","Young_per_yr","Rangesize_km2","Mass_g","Daily_rhythm_code","Annual_rhythm_code")]
#mammals=mammals[,c("Taxon","High_change","Orig_high_limit","Longevity_yrs")]

#check correlations
r <- cor(mammals[,c(3:10)], use="complete.obs")
ggcorrplot(r)

#to long
mammals.l<- mammals %>%
  gather("trait", "value", 3:ncol(mammals))

## Facet labels
trait.labs <- c("Altitudinal limit (m)","Longevity (yrs)","Litters per yr","Litter size","Range size (km2)","Mass (g)","Daily rhythm","Annual rhythm")
names(trait.labs) <- c("Orig_high_limit","Longevity_yrs","Litters_per_yr","Litter_size","Rangesize_km2","Mass_g","DailyRhythm","AnnualRhythm")

#plot
plot.m= ggplot(mammals.l) + aes(x=value, y = High_change)+geom_point()+
  facet_wrap(~trait, scales="free", labeller = labeller(trait = trait.labs)) + 
  ggtitle('Mammals')+
  theme_bw()+ylab("Elevation shift (m)") #+stat_smooth(method='lm', formula= y~poly(x,2))
#+geom_smooth(se=FALSE) #+scale_x_log10()

#scale
mammals$Orig_high_limit= scale(mammals$Orig_high_limit)
mammals$Rangesize_km2= scale(mammals$Rangesize_km2)
mammals$Mass_g= scale(mammals$Mass_g)
mammals$Young_per_yr= scale(mammals$Young_per_yr)

#mod
mod1= lm(High_change~Orig_high_limit+Longevity_yrs+Bio1_std+Litters_per_yr+Young_per_yr+Rangesize_km2+Mass_g+Daily_rhythm_code+Annual_rhythm_code, data=mammals)
#mod1= lm(High_change~poly(Orig_high_limit)+poly(Longevity_yrs)+poly(Bio1_std)+poly(Litters_per_yr)+poly(Young_per_yr)+poly(Rangesize_km2)+poly(Mass_g)+poly(Daily_rhythm_code)+poly(Annual_rhythm_code), data=mammals)
mod1= lm(High_change~poly(Orig_high_limit)*poly(Longevity_yrs), data=mammals)

#plot model
plot_model(mod1, type="pred", terms=c("Orig_high_limit"), show.data=TRUE)

#----
#alpine plants

#update traits to correspond to Angert et al.
plants$DispersalMode=NA
plants$DispersalMode[plants$dispersal_mode=="gravity"]=0
plants$DispersalMode[plants$dispersal_mode=="wind" | plants$dispersal_mode=="animal" | plants$dispersal_mode=="water" ]=1

#restrict traits
plants=plants[,c("Taxon","migration_m","earliest_seed_shed_mo","seed_shed_dur_mos",
                 "nichebreadth_num_flor_zones", "BreedSysCode",
                 "Ave_seed_shed_ht_m","flwr_dur_mos","DispersalMode",
                 "diaspore_mass_mg","nichebreadth_amplit_ocean","Nbound_lat_GBIF_nosyn")]

#plants=plants[,c("Taxon","migration_m","earliest_seed_shed_mo","latest_seed_shed_mo","seed_shed_dur_mos",
"nichebreadth_num_flor_zones", "diaspore_min_len_mm","BreedSysCode",
"MaxAlt","seed_mass_mg","oceanity","Min_seed_shed_ht_m","flwr_mo_end","dispmode01",
"flwr_mo_start","diaspore_mass_mg","nichebreadth_amplit_ocean","StorageOrgan",
"Max_seed_shed_ht_m")]

#check correlations
r <- cor(plants[,c(3:12)], use="complete.obs")
ggcorrplot(r)

#to long
plants.l<- plants %>%
  gather("trait", "value", 3:ncol(plants))
plants.l$value= as.numeric(plants.l$value)

## Facet labels
trait.labs <- c("Earliest seed shed (mo)","Seed shed duration (mo)","Number floristic zones", "Breeding System Code",
                "Seed shed height (m)","Flower duration (mo)","Dispersal mode",
                "Diaspore mass (mg)","Number oceanic zones","Northern Latitude (degrees)")
names(trait.labs) <- c("earliest_seed_shed_mo","seed_shed_dur_mos",
                       "nichebreadth_num_flor_zones", "BreedSysCode",
                       "Ave_seed_shed_ht_m","flwr_dur_mos","DispersalMode",
                       "diaspore_mass_mg","nichebreadth_amplit_ocean","Nbound_lat_GBIF_nosyn")

#plot  
plot.ap= ggplot(plants.l) + aes(x=value, y = migration_m)+geom_point()+
  facet_wrap(~trait, scales="free", labeller = labeller(trait = trait.labs)) +ggtitle('Alpine plants') +
  theme_bw()+ylab("Elevation shift (m)") #+ stat_smooth(method='lm', formula= y~poly(x,2))
#+scale_x_log10()

#mod
#scale
plants$diaspore_ave_len_mm= scale(plants$diaspore_ave_len_mm)
plants$diaspore_min_len_mm = scale(plants$diaspore_min_len_mm)
plants$diaspore_mass_mg = scale(plants$diaspore_mass_mg)
plants$MaxAlt = scale(plants$MaxAlt)
plants$seed_mass_mg = scale(plants$seed_mass_mg)

mod1= lm(migration_m~earliest_seed_shed_mo+latest_seed_shed_mo+seed_shed_dur_mos+nichebreadth_num_flor_zones+             
           diaspore_min_len_mm+BreedSysCode+diaspore_ave_len_mm+MaxAlt+seed_mass_mg+oceanity+Min_seed_shed_ht_m+
           flwr_mo_end+dispmode01+flwr_mo_start+diaspore_mass_mg+nichebreadth_amplit_ocean+  
           StorageOrgan+Max_seed_shed_ht_m, data=plants)

#plot model
plot_model(mod1, type="pred", terms=c("seed_mass_mg"), show.data=TRUE)
plot_model(mod1, type="pred", terms=c("diaspore_mass_mg"), show.data=TRUE)

#----
#fish

#Make salt / fresh variable
fish$WaterType=0
fish$WaterType[fish$Brack== -1]=1
fish$WaterType[fish$Fresh== -1]=2

#compress habitats
#finalize how to code
fish$habitat= as.numeric(factor(fish$DemersPelag, 
                                levels=c("bathydemersal","demersal","benthopelagic","pelagic-oceanic","pelagic-neritic","reef-associated")))

#restrict traits
fish=fish[,c("Species","Latitudinal.Difference","habitat","DepthRangeDeep","Length","WaterType")]
#fish=fish[,c("Species","Latitudinal.Difference","habitat","DepthRangeDeep","Vulnerability", "Length","Fresh")]

#to long
fish.l<- fish %>%
  gather("trait", "value", 3:ncol(fish))

# Facet labels
trait.labs <- c("Habitat","Depth Range (?)","Length (?)","Water Type")
names(trait.labs) <- c("habitat","DepthRangeDeep","Length","WaterType")

#plot
plot.tms= ggplot(fish.l) + aes(x=value, y = Latitudinal.Difference)+geom_point()+
  facet_wrap(~trait, scales="free", labeller = labeller(trait = trait.labs)) +ggtitle('Triennial marine survey') +
  theme_bw()+ylab("Latitudinal shift (°)") #+stat_smooth(method='lm', formula= y~poly(x,2))

#----
#European plants

#to numeric
#eplants$LifeStrategy= as.numeric(as.factor(eplants$LifeStrategy))

#restrict traits
eplants=eplants[,c("speciesname","LeadingEdge","TemperatureIndicator","NutrientIndicator","Dispersal","Persistence")]

#check correlations
#r <- cor(eplants[,c(6:18)], use="complete.obs")
#ggcorrplot(r)

#to long
eplants.l<- eplants %>%
  gather("trait", "value", 3:ncol(eplants))

# Facet labels
trait.labs <- c("Temperature Indicator","Nutrient Indicator","Dispersal","Persistence")
names(trait.labs) <- c("TemperatureIndicator","NutrientIndicator","Dispersal","Persistence")

#plot
plot.ep= ggplot(eplants.l) + aes(x=value, y = LeadingEdge)+geom_point()+
  facet_wrap(~trait, scales="free", labeller = labeller(trait = trait.labs)) +ggtitle('European plants') +
  theme_bw()+ylab("Elevational shift (m)") #+stat_smooth(method='lm', formula= y~poly(x,2))
#check LeadingEdge, Optimum, RearEdge

mod1= lm(LeadingEdge~RelativeAbundance+TemperatureIndicator+NutrientIndicator+TerminalVelocity+
           RetInFurCattle+RetInFurSheep+GutSurvival+SeedReleaseHeight+Dispersal+
           LifeStrategy+LifeSpan+Dominance+NoOfVegOffspings+Persistence, data=eplants)

Anova(mod1, type=3)

#--------------
#PLOT

# alpine plants: seed shed month earliest, number floristic zones
# European plants: temp indicator, seed release height
# Mammals: alt timit, longevity
# Fish: depth, benthopelagic, vulnerability

#----
# alpine plants: seed shed month earliest, number floristic zones

plot1a= ggplot(plants) + aes(x=earliest_seed_shed_mo, y = migration_m)+geom_point()+
  xlab("Earliest seed shed month")+ylab("Elevation shift (m)")+ 
  ggtitle('A. Alpine plants')+
  theme_bw(base_size=14)

plot1b= ggplot(plants) + aes(x=seed_shed_dur_mos, y = migration_m)+geom_point()+
  xlab("Seed shed duration (mo)")+ylab("Elevation shift (m)")+ 
  ggtitle('A. Alpine plants')+
  theme_bw(base_size=14)

#----
# European plants: temp indicator, seed release height

plot1c= ggplot(eplants) + aes(x=TemperatureIndicator, y = LeadingEdge)+geom_point()+
  xlab("Temperature indicator")+ylab("Elevation shift (m)")+ 
  ggtitle('B. European plants')+
  theme_bw(base_size=14)

plot1d= ggplot(eplants) + aes(x=Dispersal, y = LeadingEdge)+geom_point()+
  xlab("Dispersal")+ylab("Elevation shift (m)")+ 
  ggtitle('B. European plants')+
  theme_bw(base_size=14)

#check units

#----
# Mammals: alt timit, longevity

plot1e= ggplot(mammals) + aes(x=Orig_high_limit, y = High_change)+geom_point()+
  xlab("Original altitude (m)")+ylab("Elevation shift (m)")+ 
  ggtitle('C. Mammals')+
  theme_bw(base_size=14)

plot1f= ggplot(mammals) + aes(x=Longevity_yrs, y = High_change)+geom_point()+
  xlab("Longevity (years)")+ylab("Elevation shift (m)")+ 
  ggtitle('C. Mammals')+
  theme_bw(base_size=14)+
  theme(axis.title.x = element_text(margin = margin(t = -15)))

#----
# Fish: depth, benthopelagic, vulnerability

plot1g= ggplot(fish) + aes(x=DepthRangeDeep, y = Latitudinal.Difference)+geom_point()+
  xlab("Depth range (m)")+ylab("Latitudinal shift (°)")+ 
  ggtitle('D. Triennial marine survey')+
  theme_bw(base_size=14)+
  theme(axis.title.x = element_text(margin = margin(t = -15)))

fish$habitat= factor(fish$DemersPelag, 
                     levels=c("bathydemersal","demersal","benthopelagic","pelagic-oceanic","pelagic-neritic","reef-associated"))

plot1h= ggplot(fish) + aes(x=habitat, y = Latitudinal.Difference)+geom_point()+
  xlab("Habitat")+ylab("Latitudinal shift (°)")+ 
  ggtitle('D. Triennial marine survey')+
  theme_bw(base_size=14)+ 
  theme(axis.text.x = element_text(angle = 45))+
  theme(axis.title.x = element_text(margin = margin(t = -15)))

#----
#combine
#(plot1a | plot1b) / (plot1c | plot1d) / (plot1e | plot1f) / (plot1g | plot1h)

#setwd for figures
setwd("/Volumes/GoogleDrive/My Drive/Buckley/Work/StudentsPostdocs/Cannistra/Traits/figures/")

pdf("Fig0.pdf", height = 8, width = 10)
(plot1b | plot1d) / (plot1f | plot1h)
dev.off()

#supplementary plots
pdf("FigSm.pdf", height = 12, width = 12)
plot.m
dev.off()

pdf("FigStms.pdf", height = 12, width = 12)
plot.tms
dev.off()

pdf("FigSap.pdf", height = 12, width = 12)
plot.ap
dev.off()

pdf("FigSep.pdf", height = 12, width = 12)
plot.ep
dev.off()

