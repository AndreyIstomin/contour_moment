import math
import ogr
from contracts import contract
from shapely import wkb, affinity


class Vec2:

    """
    Class for simple 2d operations
    """

    def __init__(self, point):

        self.x = point[0]
        self.y = point[1]

    def __add__(self, other):
        return Vec2((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vec2((self.x - other.x, self.y - other.y))

    def __mul__(self, other):
        return Vec2((self.x * other, self.y * other))

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __str__(self):
        return 'x={}, y={}'.format(self.x, self.y)


    def __eq__(self, other):
        return (self.x , self.y) == (other.x, other.y)

    def __ne__(self, other):
        return (self.x, self.y) != (other.x, other.y)

    def __lt__(self, other):
        return ((self.x, self.y) < (other.x, other.y))

    def __le__(self, other):
        return ((self.x, self.y) <= (other.x, other.y))

    def __gt__(self, other):
        return ((self.x, self.y) > (other.x, other.y))

    def __ge__(self, other):
        return ((self.x, self.y) >= (other.x, other.y))



@contract
def transform_geom(geom, shift=None, angle=None, origin=None, scale=None):

    """ Comfort transformation of GDAL geometry
    :param geom: ogr.Geometry
    :type geom: *
    :type shift: tuple(float|int, float|int)|None
    :param angle: degrees
    :type angle: float|int|None
    :param origin: rotation origin, default: center mass
    :type origin: tuple(float, float)|None
    :type scale: (float|int,>0)|None
    :return: ogr.Geometry
    :type: geom: *
    """

    g = wkb.loads(geom.ExportToWkb())

    if shift:

        g = affinity.translate(g, shift[0], shift[1])

    if angle:

        if not origin:
            origin = center_mass(geom)

        g = affinity.rotate(g, angle, origin=origin)

    if scale:

        g = affinity.scale(g, scale, scale, scale)

    return ogr.CreateGeometryFromWkb(g.wkb)


def _center_mass_ring(ring):

    center = Vec2((0, 0))
    perimeter = 0.0

    for i in range(ring.GetPointCount() - 1):

        p = Vec2(ring.GetPoint(i + 1)) + Vec2(ring.GetPoint(i))

        l = (Vec2(ring.GetPoint(i + 1)) - Vec2(ring.GetPoint(i))).length()

        perimeter += l

        center += p * 0.5 * l

    return center * (1.0 / perimeter), perimeter


@contract
def center_mass(geom):

    """
    Finds center of the given ogr.Geometry(Polygon)
    :param geom: instance of ogr.Geometry(Polygon)
    :type geom: *
    :rtype tuple(float, float)
    """

    if geom.GetGeometryType() != ogr.wkbPolygon:
        raise TypeError('Input geometry must have polygon type')

    i = 0

    center = Vec2((0, 0))
    mass = 0

    while True:

        ring = geom.GetGeometryRef(i)

        if not ring:
            break

        ring_center, ring_perimeter = _center_mass_ring(ring)

        center += ring_center * ring_perimeter

        mass += ring_perimeter

        i += 1

    res = center * (1.0 / mass)

    return res.x, res.y


if __name__ == '__main__':

    import os


    def translate_geom_test():

        res_dir = os.path.join(os.path.dirname(__file__), 'test_resources')
        shp_path = os.path.join(res_dir, 'russia_south_village_3857.shp')

        in_driver = ogr.GetDriverByName('ESRI Shapefile')

        in_ds = in_driver.Open(shp_path, 0)
        in_lay = in_ds.GetLayer()

        out_driver = ogr.GetDriverByName('ESRI Shapefile')

        shp_path = os.path.join(res_dir, 'transform_result.shp')
        out_ds = out_driver.CreateDataSource(shp_path)
        out_lay = out_ds.CreateLayer('shift', geom_type=ogr.wkbPolygon)

        for i, feat in enumerate(in_lay):

            if i >= 100:
                break

            feat_def = out_lay.GetLayerDefn()

            feature = ogr.Feature(feat_def)
            feature.SetGeometry(feat.GetGeometryRef())
            out_lay.CreateFeature(feature)

            feature = ogr.Feature(feat_def)
            feature.SetGeometry(transform_geom(feat.GetGeometryRef(), shift=(10.0, 10), angle=45, scale=0.5))
            out_lay.CreateFeature(feature)

        in_ds.Destroy()
        out_ds.Destroy()


    translate_geom_test()
