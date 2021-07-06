# Least-Squares Fitting of Two 3-D Point Sets
# KS ARUN, TS HUANG & SD BLOSTEIN
# IEEE Transactions on Pattern Analysis and Machine Intelligence
# Vol PAMI-9 #5 Sept. 1987
# This is the same algorithm that is used by AFNI's 3dTagalign
# (orthogonal rotations only).

from math import sqrt, acos, pi
import numpy as np
from .fid import fid, fid_transform

__all__ = ['getfidrot']

def getfidrot(p1, p2):
    """Given two sets of 3D points, stored as ROWS of the arrays p1 and p2,
    compute R (3x3) and T (3x1) such that p2 ~ Rp1 + T. This version assumes
    there are 3 points in each set, representing fiducial locations. The
    rotation angle and translation distance are reported."""

    # Compute a FID basis for the first set of points, and map both
    # sets into that frame.

    q1 = np.zeros_like(p1)
    q2 = np.zeros_like(p2)

    m = fid(p1[0], p1[1], p1[2])    # nasn, lear, rear
    for i in range(3):
        q1[i, :] = fid_transform(m, p1[i])
    for i in range(3):
        q2[i, :] = fid_transform(m, p2[i])

    # Subtract the centroids --- here, the first set is already centered on
    # the origin, so we only need to translate the second set. Also, use
    # the FID origin, not the centroid.

    #c1 = p1.sum(axis = 0) / 3
    #c2 = p2.sum(axis = 0) / 3
    #q1 = p1 - c1
    #q2 = p2 - c2

    c2 = (q2[1] + q2[2]) / 2    # midpoint between lear and rear
    q2 = q2 - c2

    # Compute covariance matrix and SVD.

    h = 0
    for i in range(3):
        h += np.outer(q1[i], q2[i])

    u, d, v = np.linalg.svd(h)

    # Compute an orthogonal rotation matrix.

    r = v.T.dot(u.T)

    # If the determinant is -1, and the smallest singular value is zero,
    # flip the sign of the corresponding vector and try again.

    det = np.linalg.det(r)
    if abs(det) < .01:
        raise RuntimeError("singular matrix")
    if det < 0:
        if abs(d[2]) > .01:
            raise RuntimeError("unable to compute rotation")
        v[2] *= -1
        r = v.T.dot(u.T)
        det = np.linalg.det(r)

    # Compute the translation, using the centroids (origins).

    #t = c2 - r.dot(c1)
    t = c2                  # c1 is zero, so t is just c2

    # Compute the rotation angle and distance translated

    costheta = .5 * sqrt(1. + np.trace(r))
    theta = 2. * acos(costheta) * 180 / pi
    dist = sqrt((t * t).sum())

    print("Total rotation = {:4.2f} degrees, translation = {:4.2f} cm".format(theta, dist))

    #p2new = r.dot(p1.T).T + t  # this transforms p1 towards p2

if __name__ == '__main__':
    p1 = np.array([
        [6.21, 7.25, -24.3],
        [-4.41, 4.86, -25.7],
        [5.39, -3.96, -25.1]])
    p2 = np.array([
        [6.15, 7.13, -24],
        [-4.4, 4.85, -25.7],
        [5.38, -3.98, -25.2]])
    getfidrot(p1, p2)
    # Total rotation = 2.36 degrees, translation = 0.05 cm
