from contracts import contract
import ogr
from shapely import wkb, affinity


@contract
def transform_geom(geom, shift=None, angle=None, scale=None):

    """ Comfort transformation of GDAL geometry
    :param geom: ogr.Geometry
    :type geom: *
    :type shift: tuple(float|int, float|int)|None
    :param angle: degrees
    :type angle: float|int|None
    :type scale: (float|int,>0)|None
    :return: ogr.Geometry
    :type: geom: *
    """

    g = wkb.loads(geom.ExportToWkb())

    if shift:

        g = affinity.translate(g, shift[0], shift[1])

    if angle:

        g = affinity.rotate(g, angle)

    if scale:

        g = affinity.scale(g, scale, scale, scale)

    return ogr.CreateGeometryFromWkb(g.wkb)


if __name__ == '__main__':

    import os

    def test_translate_geom():

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

    test_translate_geom()
