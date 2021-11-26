def round_to_start_of_month(ds, dim):
    """ Return provided array with specified time dimension rounded to the start of 
        the month 
    """
    from xarray.coding.cftime_offsets import MonthBegin
    return ds.assign_coords({dim: ds[dim].dt.floor('D') - MonthBegin()})


def convert_time_to_lead(ds, time_dim='time', init_dim='init', lead_dim='lead'):
    """ Return provided array with time dimension converted to lead time dimension 
        and time added as additional coordinate
    """
    init_date = ds[time_dim].time[0].item()
    lead_time = range(len(ds[time_dim]))
    time_coord = ds[time_dim].rename(
        {time_dim: lead_dim}).assign_coords(
        {lead_dim: lead_time}).expand_dims(
        {init_dim: [init_date]})
    dataset = ds.rename(
        {time_dim: lead_dim}).assign_coords(
        {lead_dim: lead_time,
         init_dim: [init_date]})
    dataset = dataset.assign_coords(
        {time_dim: time_coord})
    return dataset


def truncate_latitudes(ds, dp=10):
    """ Return provided array with latitudes truncated to specified dp.
    
        This is necessary due to precision differences from running forecasts on 
        different systems 
    """
    for dim in ds.dims:
        if 'lat' in dim:
            ds = ds.assign_coords({dim: ds[dim].round(decimals=dp)})
    return ds


def stack_by_init_date(ds, init_dates, n_lead_steps, freq,
                      time_dim='time', init_dim='init', lead_dim='lead'):
    """ Stack timeseries array in inital date / lead time format.
    
        init_dates must be provided in YYYY-MM-DD format

        Stolen and adapted from https://github.com/AusClimateService/unseen/blob/master/unseen
    """
    rounded_times = ds[time_dim].dt.floor(freq).values
    ref_time = init_dates[0]
    ref_calendar = rounded_times[0].calendar
    ref_var = list(ds.keys())[0]
    ref_array = ds[ref_var].sel({time_dim: ref_time}).values    

    time2d = np.empty((len(init_dates), n_lead_steps), 'object')
    init_date_indexes = []
    offset = n_lead_steps - 1
    for ndate, date in enumerate(init_dates):
        date_cf = time_utils.str_to_cftime(date, ref_calendar)
        start_index = np.where(rounded_times == date_cf)[0][0]
        end_index = start_index + n_lead_steps
        time2d[ndate, :] = ds[time_dim][start_index:end_index].values
        init_date_indexes.append(start_index + offset)

    ds = ds.rolling({time_dim: n_lead_steps}, min_periods=1).construct(lead_dim)
    ds = ds.assign_coords({lead_dim: ds[lead_dim].values})
    ds = ds.rename({time_dim: init_dim})
    ds = ds.isel({init_dim: init_date_indexes})
    ds = ds.assign_coords({init_dim: time2d[:, 0]})
    ds = ds.assign_coords({time_dim: ([init_dim, lead_dim], time2d)})
    ds[lead_dim].attrs['units'] = freq

    actual_array = ds[ref_var].sel({init_dim: ref_time, lead_dim: 0}).values
    np.testing.assert_allclose(actual_array[0], ref_array[0])
    
    # TODO: Return nans if requested times lie outside of the available range
    
    return ds