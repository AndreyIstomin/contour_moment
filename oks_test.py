from moment_test import MomentTest
from gdal_helper import transform_geom
from moment import Moment
import ogr

if __name__ == '__main__':
    wkt = 'POLYGON((-2 -2, 2 -2, 2 2, -2 2, -2 -2), (-1 -1, 1 -1, 1 1, -1 1, -1 -1))'

    # wkt = 'POLYGON((-2 -2, 2 -2, 2 2, -2 2, -2 -2), (-1 -1, -1 1, 1 1, 1 -1, -1 -1))'

    geom = list()
    response = list()

    geom.append(ogr.CreateGeometryFromWkt((wkt)))
    response.append((0.0, 0.0))

    # geom.append(transform_geom(geom[0], angle=35))
    # response.append((0.0, 0.0))
    #
    # geom.append(transform_geom(geom[0], shift=(2.0, 44.7)))
    # response.append((2.0, 44.7))
    #
    # geom.append(transform_geom(geom[0], scale=3.3))
    # response.append((0.0, 0.0))

    geom.append(transform_geom(geom[0], shift=(1.1, 5.5), angle=45.0))

    response.append((1.1, 5.5))

    for i in range(len(geom)):

        m = Moment(geom[i])

        print(m.compute(1, 0, central=False))

        cm = (m.compute(1, 0, central=False) / m.compute(0, 0, central=False),
              m.compute(0, 1, central=False) / m.compute(0, 0, central=False))

        print(cm[0], response[i][0])
        print(cm[1], response[i][1])
