# Marine heatwaves and cold spells warning
This repository contains functions and explanation on the methods of predicting warning signals and mapping marine heatwaves and cold spells. 

## Introduction

Marine Heatwaves (MHWs) and Marine Cold Spells (MCSs) have been observed on a global scale as anomalously hot or cold-water masses. Despite their devastating impact on the marine life, the scientific understanding of MHWs and MCSs is in their infancy, compared to their atmospheric counterparts (Holbrook et al., 2019). Understanding the occurrence of MHWs and Cold Spells is a key in assessing their impact on marine species that can react on environmental change differently. Overall, the effects of MHWs and MCSs can range from permanent reallocation of certain species, which can lead to changes in the food chain, hence biodiversity and have adverse economic impact on the local communities. Moreover, is is estimated that the occurence of MHWs under the RCP4.5 ICCP scenario could double by the end of the century (Oliver et al., (2018)). For these reasons, it is important to map MHWs and MCSs. The aim of this project is to provide a warning signal of the developement of MHWS and CCS and their duration in near-real-time (5 and 10 days windows).


## Methods
We use high resolution (0.05x0.05 degrees) [NRT OSTIA Level 4 CMEMS](https://resources.marine.copernicus.eu/?option=com_csw&view=details&product_id=SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001) seas surface temperature data and apply the definition of MHWs Hobday et al. (2016) to map MHWs and MCSs.  MHW is an area of abnormally warm water, greater than the 90th percentile climatolyg in five consecutive days (Hobday et al., 2016). MCS is an area of abnormally cold water, smaller than the 10th percentile climatology in five consecutive days (von Schuckmann, K., et al., in prep). According to the above, we followed these steps to produce 1. Daily cold and warm spell flags, 2. MHW and MCS warnings in 5 days window, 3. MHW and MCS duration in 10 days window:

1. Compute 10th and 90th percentile climatology between 2010-2019 OSTIA Reprocessed product. [XClim Python](https://xclim.readthedocs.io/en/stable/api.html) library is used to calculate the percentile climatological baseline.  

2. Flag NRT OSTIA pixels below the 10th percentile climatological baseline (daily cold spells)

3. Flag NRT OSTIA pixels above the 90th percentile climatological baseline (daily warm spells)

4. Computes the number of consecutive flags in 5 day windows (MHW and MCS warning)

6. Computs the number of consecutive flags in 10 days window  (MHW and MCS duration)

7. Visualise this in the XCube Online Viewer



## XCube Viewer 

The above products can be access through an online [XCube Viewer](https://eutro-cube.cefas.co.uk/). Apart from marine heatwaves and cold spells warning products, the XCube Viewer contains various environmental data cubes, that can be spatially visualised and interoggated thorugh interactive graphs. Each data layer contains metadata ("i" button in the righ hand corner) and a possibility to play the timeseries. The data products can be downloaded through the **scripts (add).**

### System infrastructure (add diagram)

## Interpretation of MHW and MCS products

**1. Daily cold or warm flags**

Sea surface temperature pixels that are below 90th percentile are flagged as warm flags and below 10th percentile are flagged as cold flags. The value of the flagged pixels is 1. (add a screenshot)

**2. MHW and MCS warning**

MHW and MCS warnings show consecutive days in 5 days window when the sea surface temperature was above or below the percentile climatology threshold. In this method, we focus only on identifying either 1) an onset of a heatwave event or a cold spell (5 consecutive days) 2) Potentially devloping MHW or MCS with 4 consecutive days (including the last day in the window and 3) Potentially devloping MHW or MCS with 3 consecutive days (including the last day of the window). These warnings map the areas where the MHW or MCS started or show were these could be developed, subject to these being followed by another 1 or 2 days of abnormally warm or cold water temperatures respectivelly. Please see a table below that depicts this:

**Add a table and a screenshot**

**3. MHW and MCS duration**

MHW and MCS duration shows a duration of MHW or MCS in 10 days windows. Firstly an onset of a MHW or MCS in the first 5 days of the window is marked. For these events a duration of the consecutive days is calculated. Therefore a duration can be between 1-6 days. Please see a table below that depicts this:

**Add a table and a screenshot**






## MHWCS_warning GitHub repository (add description when all scripts will be finalised)



## Reference

[Holbrook et al., (2019)](https://www.nature.com/articles/s41467-019-10206-z)

[Oliver et al., (2018)](https://pubmed.ncbi.nlm.nih.gov/29636482/)

[Hobday et al., (2016)](https://www.sciencedirect.com/science/article/pii/S0079661116000057)

von Schuckmann, K., et al. Copernicus Marine Service Ocean State Report, Issue 5, Journal of Operational Oceanography (in prep) 

## Authors
Kate Collingridge (kate.collingridge@cefas.co.uk)

Lenka Fronkova (lenka.fronkova@cefas.co.uk)


 
