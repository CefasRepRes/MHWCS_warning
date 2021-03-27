import xclim 
from xclim.core.calendar import percentile_doy


########read sea surface temperature data in netcdf format as xarray and clip it

def readXarrayData(pathIn, yearsList, concat_dim, variable, xmin, xmax, ymin, ymax):
    data = []
    for y in yearsList:
        xar_year = xr.open_mfdataset(pathIn+'/{0}/*/*.nc'.format(y), concat_dim=concat_dim)
        print(pathIn+'/{0}/*/*.nc'.format(y))
        sliced = xar_year.where((xar_year.lon >xmin) & (xar_year.lon < xmax) & ( xar_year.lat >ymin) & (xar_year.lat < ymax), drop=True)
        data.append(sliced)
    	
    x_ar = xr.concat(data, dim = concat_dim)
    x_ar = x_ar[variable]

    print("Data successfully imported")
    return x_ar


ostia_sst = readXarrayData(pathIn="dataPath", 
                   yearsList=["2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019"], #10 years of data
                   concat_dim= "time", 
                   variable="analysed_sst", 
                   xmin=-10.4, 
                   xmax=10.4, 
                   ymin=44.8, 
                   ymax=65.6)

####xclim method to calculate percentiles###
ds_qt10 = percentile_doy(ostia_sst, window=1, per=0.1)
print("10th percentile was computed")

ds_qt90 = percentile_doy(ostia_sst, window=1, per=0.9)
print("90th percentile was computed")
