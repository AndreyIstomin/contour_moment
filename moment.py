from contracts import contract
import ogr
from polynome import Polynome
from gdal_helper import Vec2


class Moment:

    def __init__(self, geom: 'GDAL Polygon'):
        print(geom)
        print(type(geom))
        if type(geom) != ogr.Geometry:
            print("Invalid geometry. Geometry type must be ogr.wkbPolygon")
            return
        self.geom = geom
        rings = [geom.GetGeometryRef(i) for i in range(0, geom.GetGeometryCount())]
        # print([ring.ExportToWkt() for ring in rings])
        segments=[]
        # for ring in rings:
        #     segments.extend([[ring.GetPoint(i-1)[:-1], ring.GetPoint(i)[:-1]] for i in range(1, ring.GetPointCount())])
        segments=[[Vec2(ring.GetPoint(i - 1)[:-1]), Vec2(ring.GetPoint(i)[:-1])] for ring in rings for i in range(1, ring.GetPointCount())]
        # print(segments)
        self.segments = segments

    @contract
    def compute(self, i, j, central=True, scale_inv=False, rotate_inv=True):
        """
        Computes i,j-th moment of contour

        :type i: int,>=0,<7
        :type j: int,>=0,<7
        :type central: bool
        :type scale_inv: bool
        :type rotate_inv: bool
        :rtype: float
        """
        m_result=0
        for s in self.segments:
            length = (s[1]-s[0]).length()
            x_coef1 = (s[1].x-s[0].x)/length
            x_coef2 = (s[1].y-s[0].y)/length
            a = Polynome.binomial_theorem(x_coef=x_coef1, y_coef=s[0].x, power=i)
            b = Polynome.binomial_theorem(x_coef=x_coef2, y_coef=s[0].y, power=j)
            result = a*b
            m = result.compute_integral_x(x_begin=0, x_end=length, y_value=1)
            m_result+=m

        return m_result
