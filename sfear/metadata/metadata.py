import xarray as xr
import geopandas as gp
import shapely
from sfear.utils.surface_area import *

def collect_metadata(
        data: xr.Dataset, 
        lon_dim: str,
        lat_dim: str,
        use_polygons: bool = True
    ) -> gp.GeoDataFrame:
    '''
    Gets the stratified group membership of each coordinate.

    Parameters
    ----------
    model_data: xr.Dataset
        A dataset which includes predictions for some set of variables at a set
        of coordinates.
    lon_dim: str
        The name of the dimension that stores the longitude.
    lat_dim: str
        The name of the dimension that stores the latitude.
    use_polygons: bool
        If True, then each coordinate is turned into a polygon rather than a
        Point. All polygons are non-overlapping and generated with a greedy
        algorithm that will draw the borders at the mean of each dimension
        with its neighboring coordinate. The result of using polygons is that
        the prediction the metric calculated at that gridpoint will be
        attributed to every metadata group that the polygon overlaps, rather
        than just the metadata group that the exact coordinate point is at.
        For territory, subregion, and income, the metric will be attributed
        to all of the territories/subregions/income group that overlap with
        the polygon. For landcover, the majority of the landcover type of the
        land it overlaps will be assigned.
    '''

    gdf = gp.read_file('sfear/metadata/gdf_region_income.csv')

    # TODO: add column for lat cell weight
    # TODO: add column for each metadata category, and fill it with the group value
    # TODO: add column for polygon if use_polygon, otherwise turn coords into Point