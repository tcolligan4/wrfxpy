from ingest.grib_source import GribError
from ingest.grib_forecast import GribForecast
from datetime import datetime, timedelta
import pytz
import logging
import os.path as osp
from utils import Dict, timedelta_hours, readhead


class HRRR(GribForecast):
    """
    The HRRR (High Resolution Rapid Refresh) grib source as provided by NOMADS.
    """

    def __init__(self, arg):
        super(HRRR, self).__init__(arg)

    def vtables(self):
        """
        Returns the variable tables that must be linked in for use with the HRRR data source.
        :return:
        """
        return {'geogrid_vtable': 'GEOGRID.TBL',
                'ungrib_vtable': 'Vtable.HRRR',
                'metgrid_vtable': 'METGRID.TBL.HRRR'}


    def namelist_keys(self):
        """
        Returns the namelist keys that must be modified in namelist.input with HRRR.

        HRRR requires that ''num_metgrid_soil_levels'' is set to 8.
        """
        return {}

    def file_names(self, cycle_start, fc_list):
        """
        Computes the relative paths of required GRIB2 files.

        HRRR provides 16 GRIB2 files, one per hour and performs a cycle every hour.

        :param cycle_start: UTC time of cycle start
        :param fc_hours: final forecast hour 
        """
        path_tmpl = 'hrrr.%04d%02d%02d/hrrr.t%02dz.wrfprsf%02d.grib2'
        grib_files = [path_tmpl % (cycle_start.year, cycle_start.month, cycle_start.day, cycle_start.hour, x) for x in fc_list]

        return grib_files

    # instance variables
    # remote_url = 'http://www.ftp.ncep.noaa.gov/data/nccf/nonoperational/com/hrrr/prod'
    id = "HRRR"
    remote_url = 'http://nomads.ncep.noaa.gov/pub/data/nccf/com/hrrr/prod/'
    period_hours = 1
    grib_forecast_hours_periods = [{'hours':15,'period':1}]
    cycle_hours = 1
    hours_behind_real_time = 1     # choose forecast cycle at least one hour behind
    
