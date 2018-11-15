from contracts import contract
import ogr


class Moment:

    def __init__(self, geom: 'GDAL Polygon'):

        print(geom)
        pass

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

        return 1.0
