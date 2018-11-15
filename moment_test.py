import os
import unittest
import ogr
from gdal_helper import transform_geom
from moment import Moment


class MomentTest(unittest.TestCase):

    def setUp(self):

        geom_count = 10

        res_dir = os.path.join(os.path.dirname(__file__), 'test_resources')
        shp_path = os.path.join(res_dir, 'russia_south_village_3857.shp')

        driver = ogr.GetDriverByName('ESRI Shapefile')

        ds = driver.Open(shp_path, 0)

        lay = ds.GetLayer()

        assert lay.GetFeatureCount() == 146303

        self.geometries = []
        for i, feat in enumerate(lay):

            if i >= geom_count:
                break
            self.geometries.append(feat.GetGeometryRef().Clone())

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

            with self.subTest(i=i, msg='center mass'):

                m = Moment(geom[i])

                cm = (m.compute(1, 0, central=False)/m.compute(0, 0, central=False),
                      m.compute(0, 1, central=False)/m.compute(0, 0, central=False))

                self.assertAlmostEqual(cm[0], response[i][0])
                self.assertAlmostEqual(cm[1], response[i][1])

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

    def test_hu_moment(self):

        angles = [33]

        for geom in self.geometries:

            for angle in angles:

                translated = transform_geom(geom, shift=(1.0, 60.0), angle=angle, scale=0.4)

                for i in range(7):
                    m1 = Moment(geom)

                    m2 = Moment(translated)

                    with self.subTest(angle=angle, i=i, msg='hu-moment'):
                        self.assertAlmostEqual(m1.compute_hu(i), m2.compute_hu(i))

    def test_hu_moment_no_scale_inv(self):

        geom = self.geometries[0]

        geom_1 = transform_geom(geom, shift=(1.0, 60.0),  angle=30.0)

        geom_2 = transform_geom(geom, shift=(1.0, 60.0),  angle=30.0, scale=1.7)

        m = Moment(geom)
        m_1 = Moment(geom_1)
        m_2 = Moment(geom_2)

        for i in range(7):

            with self.subTest(i=i, msg='hu-moment (no scale inv), equality expected'):
                self.assertAlmostEqual(m.compute_hu(i, scale_inv=False), m_1.compute_hu(i, scale_inv=False))

            with self.subTest(i=i, msg='hu-moment (no scale inv), equality not expected'):
                self.assertNotAlmostEqual(m.compute_hu(i, scale_inv=False), m_2.compute_hu(i, scale_inv=False))

    def test_inequality(self):

        m1 = Moment(self.geometries[0])

        with self.subTest(msg='central moment: must not be equal'):

            m2 = Moment(transform_geom(self.geometries[0], angle=30.0, scale=0.8))
            self.assertNotAlmostEqual(m1.compute(3, 3), m2.compute(3, 3))

        with self.subTest(msg='central, rot. inv.: must not be equal'):

            m2 = Moment(transform_geom(self.geometries[0], angle=30.0, scale=0.8))
            self.assertNotAlmostEqual(m1.compute_hu(3, scale_inv=False), m2.compute(3, 3, scale_inv=True))

        with self.subTest(msg='central, scale. inv.: must not be equal'):

            m2 = Moment(transform_geom(self.geometries[0], angle=30.0, scale=0.8))
            self.assertNotAlmostEqual(m1.compute(3, 3, scale_inv=True), m2.compute(3, 3, scale_inv=True))

    def test_parallel_to_axes(self):
        pass


if __name__ == '__main__':

    unittest.main()





