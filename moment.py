from contracts import contract
import ogr


class Moment:

    def __init__(self, geom: 'GDAL Polygon'):

        pass

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

        return 1.0

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

        return 1.0
