#This script extracts data from a datacube on https://eutro-cube.cefas.co.uk for points as a time series.

#Required packages
library(httr)
library(jsonlite)


#download time series for a point
dataset_name="ostia"
var_name="analysed_sst_c"
lon=3.87335
lat=54.24584
baseurlts = "https://eutro-cube.cefas.co.uk/eutro/ts/"

url = paste0(baseurlts,dataset_name, "/", var_name, "/point?lon=", lon,"&lat=", lat, "&maxValids=-1")

dat = GET(url)
dat <- httr::content(dat, as = "text")
dat <- fromJSON(dat)
dat$results


#get tiles - have not fully tested this part
#baseurltiles = "https://eutro-cube.cefas.co.uk/eutro/datasets/"
#url = paste0(baseurltiles, dataset_name,"/vars/", var_name, "/tiles/1/1/1.png")


#dat = GET(url)
