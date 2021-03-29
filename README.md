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



## Cefas Data Cube Viewer 

The above products can be accessed through an online Cefas [Data Cube Viewer](https://eutro-cube.cefas.co.uk/). Apart from marine heatwaves and cold spells warning products, the Cefas Data Cube Viewer contains various environmental data cubes, that can be spatially visualised and interoggated thorugh interactive graphs in the Web browser. Each data layer contains metadata ("i" button in the righ hand corner) and a possibility to play a timeseries or aggregated data through areas of interst. The diagram below shows the Cefas Data Cube Server. Spatial data is stored on a Linux server in data cube format. These can be accessible through a Web service via any devices witht the Internet connection. On the top of that, the data cubes could be access through APIs (Python and R scripts are available here: **scripts (add).**) as dataframes or xarrays directly to the local machine ready for data analysis. This creates a powerful tool for visualisation, query and analysis.


Schematic diagram showing the flow of data:

![image](https://user-images.githubusercontent.com/23084713/112495901-36d01600-8d7c-11eb-9d5c-0f1a9d4f19c3.png)

## Interpretation of MHW and MCS products

**1. Daily cold or warm flags**

Sea surface temperature pixels that are below 90th percentile are flagged as warm flags and below 10th percentile are flagged as cold flags. The value of the flagged pixels is 1. (add a screenshot)

**2. MHW and MCS warning**

MHW and MCS warnings show consecutive days in 5 days window when the sea surface temperature was above or below the percentile climatology threshold. In this method, we focus only on identifying either 1) an onset of a heatwave event or a cold spell (5 consecutive days) 2) Potentially devloping MHW or MCS with 4 consecutive days (including the last day in the window and 3) Potentially devloping MHW or MCS with 3 consecutive days (including the last day of the window). These warnings map the areas where the MHW or MCS started or show were these could be developed, subject to these being followed by another 1 or 2 days of abnormally warm or cold water temperatures respectivelly. Please see a table below that depicts this:

![image](https://user-images.githubusercontent.com/23084713/112399472-2d07cd80-8cfe-11eb-9735-6d27a82b46a2.png)

To note the above table does not show all the possible combinations in 5 days window but servers as an example of the warning method.


**3. MHW and MCS duration**

MHW and MCS duration shows a duration of MHW or MCS in 10 days windows. Firstly an onset of a MHW or MCS in the first 5 days of the window is marked. For these events a duration of the consecutive days is calculated. Therefore a duration can be between 1-6 days. Please see a table below that depicts this:

![image](https://user-images.githubusercontent.com/23084713/112398558-63dce400-8cfc-11eb-8678-9a999192239b.png)


## MHWCS_warning GitHub repository 

**MHWCS_functions.py** - functions that are applied to created MHW and MCCs products 

**Ostia_heatwaves_coldspells.ipynb** - a jupyter notebook that runs the functions from MHWCS_functions.py on the Cefas Data Cube Viewer Server

**climatology_percentile.py** - a script that reads sea surface temperature data and calculates 10th or 90th percentile climatology

**xcube_webapi.R** - an R script to access data from the Cefas Data Cube through API

**xcube_api.ipynb** - an Python script to access data from the Cefas Data Cube through API


## Reference

[Holbrook et al., (2019)](https://www.nature.com/articles/s41467-019-10206-z)

[Oliver et al., (2018)](https://pubmed.ncbi.nlm.nih.gov/29636482/)

[Hobday et al., (2016)](https://www.sciencedirect.com/science/article/pii/S0079661116000057)

von Schuckmann, K., et al. Copernicus Marine Service Ocean State Report, Issue 5, Journal of Operational Oceanography (in prep) 

## Authors
Kate Collingridge (kate.collingridge@cefas.co.uk)

Lenka Fronkova (lenka.fronkova@cefas.co.uk)

## Licence

This source code is licensed under the Open Government Licence v3.0. To view this licence, visit www.nationalarchives.gov.uk/doc/open-government-licence/version/3 or write to the Information Policy Team, The National Archives, Kew, Richmond, Surrey, TW9 4DU.

The Open Government Licence (OGL) Version 3

Copyright (c) 2021 Centre for Environement Fisheries and Aquaculture Science


## Data

Data is not supplied with this repository, however it could be accessed directly through the Copernicus Marine Service website: https://marine.copernicus.eu/. This data is free and open access, but you will need to create your own account and read and agree to the Licence conditions. In the MHWs and MCSs Cefas Data Cube, we used the following products:

1. METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2

- resolution:	0.05°x0.05°	
- units: Daily analysed SST (Kelvin)	
- access: ftp://nrt.cmems-du.eu/Core/SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001/METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2

2. METOFFICE-GLO-SST-L4-NRT-OBS-ANOM-V2*
- resolution:	0.25°x0.25°	
- units: Daily SST Anomaly from pathfinder climatology (Kelvin)	
- access: ftp://nrt.cmems-du.eu/Core/SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001/METOFFICE-GLO-SST-L4-NRT-OBS-ANOM-V2


3. METOFFICE-GLO-SST-L4-REP-OBS-SST*
- resolution:	0.05°x0.05°	
- units: Reprocessed Daily SST (Kelvin)	
- access: ftp://my.cmems-du.eu/Core/SST_GLO_SST_L4_REP_OBSERVATIONS_010_011/METOFFICE-GLO-SST-L4-REP-OBS-SST


 
