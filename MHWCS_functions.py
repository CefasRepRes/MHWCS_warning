
import xarray as xr
import numpy as np
import pandas as pd

####################STEP 1- Read OSTIA Data as an xarray and perform geographic clipping######################

"""readXarrayData returns an xarray concatenated on the time dimension and clip it to the area of interest
   arguments:
   pathIn= data Input Path, 
   yearsList= list of years, 
   concat_dim= time dimenstion ("time"), 
   variable= netcdf variable, 
   xmin=xmin, 
   xmax=xmax, 
   ymin=ymin, 
   ymax=ymax"""
   
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
   
   


####################STEP 2- Daily flags of abnormally cold or hot water temperatures######################
"""Flagging3D function calculates daily marine heatwaves and cold spells flags using sea surface temperature 
   that is greater or smaller than the 90th and 10th climatological percentile.
   arguments:
   quantile_xar_cold= dayofyear 10th percentile climatology
   quantile_xar_warm = dayofyear 90th percentile climatology
   sst_xar=xarray containing dayofyear dimension and sea surface temperature,
   dayofyear= the day of the year"""


def Flagging3D(quantile_xar_cold, quantile_xar_warm, sst_xar):

    #select only days of year that are in NRT data
    quantile_xar_cold = quantile_xar_cold.where(quantile_xar_cold.time.dt.dayofyear.isin(sst_xar.time.dt.dayofyear), drop=True)
    quantile_xar_warm = quantile_xar_warm.where(quantile_xar_warm.time.dt.dayofyear.isin(sst_xar.time.dt.dayofyear), drop=True)
    #make an array with the flags
    flags_mapped_warm = xr.where(sst_xar['analysed_sst'].values > quantile_xar_warm['analysed_sst'].values,1,np.nan)
    #add the flags to the NRT data
    sst_xar['warm_flags'] = (["time", "lat", "lon"], flags_mapped_warm)
    #make an array with the flags
    flags_mapped_cold = xr.where(sst_xar['analysed_sst'].values < quantile_xar_cold['analysed_sst'].values,1,np.nan)
    #add the flags to the NRT data
    sst_xar['cold_flags'] = (["time", "lat", "lon"], flags_mapped_cold)
    return sst_xar
  
####################STEP 3- Calculate consecutive days in 5 days window#####################################
"""duration5Days returns an xarray with the length of consecutive days in 5 days windows. More describtion of
   this function is included in the READ_ME. 
   arguments:
   endDate = end date of the 5 day window, e.g. '2020-01-05'
   flagged_array = xarray from Flagging3D"""

def duration5Days(endDate, flagged_array):
    #turn nas to 0
    flagged_array = flagged_array.fillna(0)
    #get list of dates ending with input date
    dates = pd.date_range(end = endDate, periods = 5) #get the window 5 
    flagged_array = flagged_array.sel(time = slice(dates[0],dates[4] + pd.Timedelta(hours = 23, minutes = 59, seconds = 59)))
    d1 = flagged_array[0,:,:]
    d2 = flagged_array[1,:,:]
    d3 = flagged_array[2,:,:]
    d4 = flagged_array[3,:,:]
    d5 = flagged_array[4,:,:]
    
    
    #create new empty 2D array that will hold the consecutive days
    rows = flagged_array.shape[1]
    cols = flagged_array.shape[2]
    
    #add an auxialiary empty 2D array at the start and end of the 5 days slice
    con = np.empty((rows,cols))
    
    #note this changes the axis, 0,1,2 (2 is the depth)
    f = np.dstack([con, d1, d2, d3, d4, d5, con]) #sandwich the 3darray with auxialiary arrays of 0
    
    #loop through each cell and find the maximum lenght of the consecutive days (flags with 1)
    for row in range(0,f.shape[0]-1):
        for col in range(0, f.shape[1]-1):
            index = np.where(f[row,col,:]==0) #get an index of where 0s are
            maxConDays = np.max(np.diff(index))-1 #difference of the indices
            if maxConDays == 5:
                con[row,col] = 5
            elif (maxConDays == 4 and f[row,col,1] == 0):
                con[row,col] = 4
            elif (maxConDays == 3 and f[row,col,1] == 0 and f[row,col,2] == 0):
                con[row,col] = 3
            else:
                con[row,col] = 0
                        
    #change 0 to na
    con[con==0] = np.nan
    #create a dataset
    ds = xr.Dataset(
        data_vars=dict(
            condayscount=(["lat", "lon"], con)
        ),
        coords=dict(
            lon=flagged_array['lon'],
            lat=flagged_array['lat']
        ),
    )
    #assign time coordinate from endDayofYear
    ds = ds.assign_coords(time=flagged_array[4,:,:].coords['time'].values)
    ds = ds.expand_dims('time')
    
    return ds
  
  
####################STEP 4- Calculate duration of marine heatwaves or cold spells in 10 days window###########
"""duration10Days calculates the duration of marine heatwaves or cold spells, meaning a duration of the water pixels
   that have at least 5 consecutive days flagged as abonrmally warm or cold compared to percentile climatology. More
   infromation in the READ_ME. 
   arguments:
   startDayOfYear= first day of the 10 days window
   endDayofYear = last day of the 10 days window
   flagged_array = xarray from Flagging3D"""

def duration10Days(endDate, flagged_array):
    #turn nas to 0
    flagged_array = flagged_array.fillna(0)
    #get list of dates ending with input date
    dates = pd.date_range(end = endDate, periods = 10) #get the window 10
    flagged_array = flagged_array.sel(time = slice(dates[0],dates[9] + pd.Timedelta(hours = 23, minutes = 59, seconds = 59)))
    d1 = flagged_array[0,:,:]
    d2 = flagged_array[1,:,:]
    d3 = flagged_array[2,:,:]
    d4 = flagged_array[3,:,:]
    d5 = flagged_array[4,:,:]
    d6 = flagged_array[5,:,:]
    d7 = flagged_array[6,:,:]
    d8 = flagged_array[7,:,:]
    d9 = flagged_array[8,:,:]
    d10 = flagged_array[9,:,:]
    
    
    #create new empty 2D array that will hold the consecutive days
    rows = flagged_array.shape[1]
    cols = flagged_array.shape[2]
    
    #add an auxialiary empty 2D array at the start and end of the 5 days slice
    con = np.empty((rows,cols))
    
    
    #note this changes the axis, 0,1,2 (2 is the depth)
    f = np.dstack([con, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, con]) #sandwich the 3darray with auxialiary arrays of 0
    
    for row in range(0,f.shape[0]-1):
        for col in range(0, f.shape[1]-1):
            
            #look at the first 5 days
            days5 = f[row,col,1:6]
            sumdays5 = np.sum(days5) #if value of the first 5 days == 5: onset of a heatwave
            if sumdays5 == 5:
                f5to10 = np.dstack([con, d5, d6, d7, d8, d9, d10, con]) #rearrange the array
                index = np.where(f5to10[row,col,:]==0) #get an index of where 0s are
                maxConDays = np.max(np.diff(index))-1 #difference of the indices
                if maxConDays == 6: #all days are marked
                    con[row,col] = 6
                elif (maxConDays == 5 and f5to10[row,col,6] == 0):
                    con[row,col] = 5
                elif (maxConDays == 4 and f5to10[row,col,6] == 0 and f5to10[row,col,5] == 0):
                    con[row,col] = 4
                elif (maxConDays == 3 and f5to10[row,col,6] == 0 and f5to10[row,col,5] == 0 and f5to10[row,col,4] == 0):
                    con[row,col] = 3
                elif (maxConDays == 2 and f5to10[row,col,6] == 0 and f5to10[row,col,5] == 0 and f5to10[row,col,4] == 0 and f5to10[row,col,3] == 0):
                    con[row,col] = 2
                elif (maxConDays == 1 and f5to10[row,col,6] == 0 and f5to10[row,col,5] == 0 and f5to10[row,col,4] == 0 and f5to10[row,col,3] == 0 and f5to10[row,col,2] == 0):
                    con[row,col] = 1
            else:
                con[row,col] = 0
                        
    #change 0 to na
    con[con==0] = np.nan
    
    #create a dataset
    ds = xr.Dataset(
        data_vars=dict(
            condayscount=(["lat", "lon"], con)
        ),
        coords=dict(
            lon=flagged_array['lon'],
            lat=flagged_array['lat']
        ),
    )
    #assign time coordinate from endDayofYear
    ds = ds.assign_coords(time=flagged_array[9,:,:].coords['time'].values)
    ds = ds.expand_dims('time')
    
    return ds

  ###################STEP 5- applies the duration10Days and duration5Days over 5 and 10 days window#############################

"""warmspelldur and coldspelldur apply duration5Days and duration10Days functions on a 5 and 10 days rolling window. 
   arguments:
   ds = 3d xarray with flags as variables
   window = 5 or 10 days (otherwise this would throw an error)
   flags = the name of the flag variable. 'cold_flags' or 'warm_flags' (different names if these were used in Flagging3D)"""

def warmspelldur(ds, window = 5, flags = 'warm_flags', fill = 'True'):
    dates = ds.time.values
    if len(dates) < 10:
        print("ERROR: Input dataset must have at least 10 daily timesteps")
    if window == 5:
        rolling_ds = []
        if fill == "True":
            for d in dates[0:4]:
                dummy = ds.where((ds.time == d), drop=True)
                arr = np.empty((dummy[flags].shape[0],dummy[flags].shape[1],dummy[flags].shape[2]))
                arr[:] = np.NaN
                dummy['condayscount'] = (["time", "lat", "lon"], arr)
                con_days2 = dummy.drop(list(dummy.keys())[0:len(list(dummy.keys()))-1])
                rolling_ds.append(con_days2)
        for d in dates[4:len(dates)]:
            con_days = duration5Days(endDate = d, flagged_array = ds[flags])
            rolling_ds.append(con_days)
        rolling_ds = xr.concat(rolling_ds, dim = 'time')
        rolling_ds = rolling_ds.rename({"condayscount": "warmspelldur"})
        return(rolling_ds)    
    elif window == 10:
        rolling_ds = []
        if fill == "True":
            for d in dates[0:9]:
                dummy = ds.where((ds.time == d), drop=True)
                arr = np.empty((dummy[flags].shape[0],dummy[flags].shape[1],dummy[flags].shape[2]))
                arr[:] = np.NaN
                dummy['condayscount'] = (["time", "lat", "lon"], arr)
                con_days2 = dummy.drop(list(dummy.keys())[0:len(list(dummy.keys()))-1])
                rolling_ds.append(con_days2)
        for d in dates[9:len(dates)]:
            con_days = duration10Days(endDate = d, flagged_array = ds[flags])
            rolling_ds.append(con_days)
        rolling_ds = xr.concat(rolling_ds, dim = 'time')
        rolling_ds = rolling_ds.rename({"condayscount": "warmspelldur"})
        return(rolling_ds)
    
    else:
        print("ERROR: Window must be 5 or 10")
        
def coldspelldur(ds, window = 5, flags = 'cold_flags', fill = 'True'):
    dates = ds.time.values
    if len(dates) < 5:
        print("ERROR: Input dataset must have at least 5 daily timesteps")
    if window == 5:
        rolling_ds = []
        if fill == "True":
            for d in dates[0:4]:
                dummy = ds.where((ds.time == d), drop=True)
                arr = np.empty((dummy[flags].shape[0],dummy[flags].shape[1],dummy[flags].shape[2]))
                arr[:] = np.NaN
                dummy['condayscount'] = (["time", "lat", "lon"], arr)
                con_days2 = dummy.drop(list(dummy.keys())[0:len(list(dummy.keys()))-1])
                rolling_ds.append(con_days2)
        for d in dates[4:len(dates)]:
            con_days = duration5Days(endDate = d, flagged_array = ds[flags])
            rolling_ds.append(con_days)
        rolling_ds = xr.concat(rolling_ds, dim = 'time')
        rolling_ds = rolling_ds.rename({"condayscount": "coldspelldur"})
        return(rolling_ds)    
    elif window == 10:
        rolling_ds = []
        if fill == "True":
            for d in dates[0:9]:
                dummy = ds.where((ds.time == d), drop=True)
                arr = np.empty((dummy[flags].shape[0],dummy[flags].shape[1],dummy[flags].shape[2]))
                arr[:] = np.NaN
                dummy['condayscount'] = (["time", "lat", "lon"], arr)
                con_days2 = dummy.drop(list(dummy.keys())[0:len(list(dummy.keys()))-1])
                rolling_ds.append(con_days2)
        for d in dates[9:len(dates)]:   
            con_days = duration10Days(endDate = d, flagged_array = ds[flags])
            rolling_ds.append(con_days)
        rolling_ds = xr.concat(rolling_ds, dim = 'time')
        rolling_ds = rolling_ds.rename({"condayscount": "coldspelldur"})
        return(rolling_ds)
    
    else:
        print("ERROR: Window must be 5 or 10")

