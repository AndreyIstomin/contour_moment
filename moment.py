from contracts import contract
import ogr
from polynome import Polynome
from gdal_helper import Vec2


class Moment:
    def __init__(self, geom: 'GDAL Polygon'):

        if type(geom) != ogr.Geometry:
            print("Invalid geometry. Geometry type must be ogr.wkbPolygon")
            return
        self.geom = geom
        rings = [geom.GetGeometryRef(i) for i in range(0, geom.GetGeometryCount())]

        segments=[]

        for ring in rings:
            for i in range(1, ring.GetPointCount()):
                v1 = Vec2(ring.GetPoint(i-1)[:-1])
                v2 = Vec2(ring.GetPoint(i)[:-1])
                if v1 != v2:
                    segments.append([v1, v2])

        self.segments = segments

    @contract
    def compute(self, i, j, central=True, scale_inv=False):
        """
        Computes i,j-th moment of contour

        :type i: int,>=0,<7
        :type j: int,>=0,<7
        :type central: bool
        :type scale_inv: bool
        :rtype: float
        """
        if scale_inv:
            central = True

        m_result = 0
        av_x = 0
        av_y = 0

        if (central):
            m00 = self.compute(0, 0, central=False, scale_inv=False)
            m01 = self.compute(0, 1, central=False, scale_inv=False)
            m10 = self.compute(1, 0, central=False, scale_inv=False)
            av_x += -m10 / m00
            av_y += -m01 / m00


        for s in self.segments:
            dx = (s[1].x - s[0].x)
            dy = (s[1].y - s[0].y)

            length = ((s[1] - s[0]).length())
            k1 = dx / length
            k2 = dy / length

            b1 = av_x + s[0].x
            b2 = av_y + s[0].y

            k3 = dx * dy / length**2
            b3 = s[0].y*dx/length

            m = self.compute_segment_moment(i, j, length, k1, b1, k2, b2, k3, b3)

            m_result += m

        if scale_inv:
            m_result = m_result/(m00**((i+j)+1))
        return m_result

    @staticmethod
    def compute_segment_moment(i, j, length, k1, b1, k2, b2, k3, b3):
        a = Polynome.binomial_theorem(x_coef=k1, y_coef=b1, power=i)
        b = Polynome.binomial_theorem(x_coef=k2, y_coef=b2, power=j)
        # c = Polynome.binomial_theorem(x_coef=k3, y_coef=b3, power=1)
        result = a * b
        m = result.compute_integral_x(x_begin=0, x_end=length, y_value=1)
        return m

    @contract
    def compute_hu(self, i, scale_inv=True):
        """
        Computes hu-moments - translation, rotation, scale invariants,
        optionally scale invariance can be omitted
        :param i: invariant index
        :type i: int,>=0,<7
        :param scale_inv: scale invariance
        :type scale_inv: bool
        :rtype: float
        """
        f = lambda ii, jj: self.compute(ii, jj, scale_inv=scale_inv, central=True)

        if i == 0:
            return f(2, 0) + f(0, 2)

        if i == 1:
            return (f(2, 0) - f(0, 2)) ** 2 + 4 * f(1, 1) ** 2

        if i == 2:
            return (f(3, 0) - 3 * f(1, 2)) ** 2 + (3 * f(2, 1) - f(0, 3)) ** 2

        if i ==3:
            return (f(3, 0) + f(1, 2)) ** 2 + (f(2, 1) + f(0, 3)) ** 2

        if i ==4:
            f30 = f(3, 0)
            f12 = f(1, 2)
            f21 = f(2, 1)
            f03 = f(0, 3)
            return ((f30 - 3 * f12) * (f30 + f12) * ((f30 + f12) ** 2 - 3 * (f21 + f03) ** 2)
                             + (f30 - 3 * f12) * (f30+ f12) * ((f30 + f12) ** 2 - 3 * (f21 + f03) ** 2))
        if i == 5:
            f20 = f(2, 0)
            f02 = f(0, 2)
            f30 = f(3, 0)
            f03 = f(0, 3)
            f12 = f(1, 2)
            f21 = f(2, 1)
            f11 = f(1, 1)
            return ((f20 - f02) * ((f30 + f12) ** 2 - (f21 + f03) ** 2)
                             + 4 * f11 * (f30 + f12) * (f21 + f03))
        if i == 6:
            f30 = f(3, 0)
            f03 = f(0, 3)
            f12 = f(1, 2)
            f21 = f(2, 1)
            return ((3 * f21 - f03) * (f30 + f12) * ((f30 + f12) ** 2 - 3 * (f21 + f03) ** 2) -
                             (f30 - 3 * f12) * (f21 + f03) * (3 * (f30 + f12) ** 2 - (f21 + f03) ** 2))



