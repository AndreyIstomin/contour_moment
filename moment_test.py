import os
import unittest
import ogr
from gdal_helper import transform_geom

from moment import Moment


class MomentTest(unittest.TestCase):

    def setUp(self):

        res_dir = os.path.join(os.path.dirname(__file__), 'test_resources')
        shp_path = os.path.join(res_dir, 'russia_south_village_3857.shp')

        driver = ogr.GetDriverByName('ESRI Shapefile')

        ds = driver.Open(shp_path, 0)

        lay = ds.GetLayer()

        assert lay.GetFeatureCount() == 146303

        self.geometries = []
        for i, feat in enumerate(lay):

            if i >= 100:
                break
            self.geometries.append(feat.GetGeometryRef().Clone())

    def test_translate_invariant(self):

        translations = [(10.0, -200.0), (777, 11), (9001, 17893)]
        moment_indexes = ((i, j) for i in range(7) for j in range(7))

        for geom in self.geometries:

            for shift in translations:

                translated = transform_geom(geom, shift=shift)

                for i, j in moment_indexes:

                    m1 = Moment(geom)
                    m2 = Moment(translated)

                    with self.subTest(shift=shift, i=i, j=j, msg='central'):

                        self.assertAlmostEqual(m1.compute(i, j), m2.compute(i, j))

    def test_rotate_invariant(self):

        angles = [33, -11, 190.1]
        moment_indexes = ((i, j) for i in range(7) for j in range(7))

        for geom in self.geometries:

            for angle in angles:

                translated = transform_geom(geom, angle=angle)

                for i, j in moment_indexes:
                    m1 = Moment(geom)

                    m2 = Moment(translated)

                    with self.subTest(angle=angle, i=i, j=j, msg='central, rotate_inv'):
                        self.assertAlmostEqual(m1.compute(i, j, rotate_inv=True), m2.compute(i, j, rotate_inv=True))

    def test_scale_invariant(self):

        scales = [0.11, 120, 11.1]
        moment_indexes = ((i, j) for i in range(7) for j in range(7))

        for geom in self.geometries:

            for scale in scales:

                translated = transform_geom(geom, scale=scale)

                for i, j in moment_indexes:
                    m1 = Moment(geom)

                    m2 = Moment(translated)

                    with self.subTest(scale=scale, i=i, j=j, msg='central, scale_inv'):
                        self.assertAlmostEqual(m1.compute(i, j, scale_inv=True), m2.compute(i, j, scale_inv=True))

    def test_inequality(self):

        m1 = Moment(self.geometries[0])

        with self.subTest(msg='central moment: must not be equal'):

            m2 = Moment(transform_geom(self.geometries[0], angle=30.0, scale=0.8))
            self.assertNotAlmostEqual(m1.compute(3, 3), m2.compute(3, 3))

        with self.subTest(msg='central, rot. inv.: must not be equal'):

            m2 = Moment(transform_geom(self.geometries[0], angle=30.0, scale=0.8))
            self.assertNotAlmostEqual(m1.compute(3, 3, rotate_inv=True), m2.compute(3, 3, rotate_inv=True))

        with self.subTest(msg='central, scale. inv.: must not be equal'):

            m2 = Moment(transform_geom(self.geometries[0], angle=30.0, scale=0.8))
            self.assertNotAlmostEqual(m1.compute(3, 3, scale_inv=True), m2.compute(3, 3, scale_inv=True))


if __name__ == '__main__':

    unittest.main()





