import shapely
from typing import List

# TODO: support automatic per-point edge length detection to handle non-equiangularity
def square_polygons_from_points(
        geometry: List[shapely.Point],
        polygon_edge_in_degrees: int,
    ) -> List[shapely.Polygon]:
    '''
    Converts an array of geometry Points to Polygons that are
    polygon_edge_in_degrees x polygon_edge_in_degrees degrees in shape and that
    are centered on the Point.

    Parameters
    ----------
    geometry: List[shapely.Point]
        The array of input Points, which are (lon, lat) coordinates.
    polygon_edge_in_degrees: int
        The edge length of each polygon in degrees.

    Returns
    -------
    List[shapely.Polygon]
        Array of Polygons in the same order.
    '''

    return [point_to_square_polygon(p, polygon_edge_in_degrees) for p in geometry]

def point_to_square_polygon(
        point: shapely.Point,
        polygon_edge_in_degrees: float,
    ) -> shapely.Polygon:
    '''
    Helper function that takes in one Point and gets the square polygon
    including it subject to the constraints of the coordinate system defined
    as longitude ranging from [-180, 180) and latitude [-90, 90].
    '''

    return shapely.box(
        (((point.x-1.5/2 + 180) % 360) - 180), 
        max(min(point.y-1.5/2, 90), -90),
        (((point.x+1.5/2 + 180) % 360) - 180), 
        max(min(point.y+1.5/2, 90), -90),
    )
