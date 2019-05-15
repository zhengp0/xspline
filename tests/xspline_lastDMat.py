# test file for lastDMat function


def xspline_lastDMat():
    import numpy as np
    from xspline.__init__ import xspline

    ok = True
    # setup test problem
    # -------------------------------------------------------------------------
    knots = np.linspace(0.0, 1.0, 5)
    degree = 3

    bs = xspline(knots, degree, l_linear=True, r_linear=True)

    # test lastDMat function
    # -------------------------------------------------------------------------
    my_dmat = bs.lastDMat()

    x = np.array([0.5*(knots[i] + knots[i + 1])
                  for i in range(bs.num_knots - 1)])

    tr_dmat = bs.designDMat(x[1:-1], degree)
    tr_dmat = np.vstack((bs.designDMat(x[0:1], 1),
                         tr_dmat))
    tr_dmat = np.vstack((tr_dmat,
                         bs.designDMat(x[-1:], 1)))

    tol = 1e-10
    ok = ok and np.linalg.norm(my_dmat - tr_dmat) < tol

    return ok
