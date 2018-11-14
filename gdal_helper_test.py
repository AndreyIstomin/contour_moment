import unittest
import ogr
from gdal_helper import Vec2, transform_geom, center_mass


class GdalHelperTest(unittest.TestCase):

    def test_center_mass(self):

        wkt = 'POLYGON((-2 -2, 2 -2, 2 2, -2 2, -2 -2), (-1 -1, 1 -1, 1 1, -1 1, -1 -1))'

        geom = list()
        response = list()

        geom.append(ogr.CreateGeometryFromWkt((wkt)))
        response.append((0.0, 0.0))

        geom.append(transform_geom(geom[0], angle=35))
        response.append((0.0, 0.0))

        geom.append(transform_geom(geom[0], shift=(2.0, 44.7)))
        response.append((2.0, 44.7))

        geom.append(transform_geom(geom[0], scale=3.3))
        response.append((0.0, 0.0))

        geom.append(transform_geom(geom[0], shift=(1.1, 5.5), angle=45.0))
        response.append((1.1, 5.5))

        for i in range(len(geom)):

            with self.subTest(i=i, msg=geom[i]):

                cm = center_mass(geom[i])

                self.assertAlmostEqual(cm[0], response[i][0])
                self.assertAlmostEqual(cm[1], response[i][1])


if __name__ == '__main__':

    unittest.main()

