# -*- coding: utf-8 -*-

import itertools

import scipy
import numpy as np
import scipy.linalg
import scipy.optimize

from base import Minimizer


class ConjugateGradient(Minimizer):
    """
    Linear Conjugate Gradient Method for quadratic function :
    f = 1/2 * xTAx -bx
    fprime = Ax - b
    """

    def __init__(self, wrt, H=None, b=None, f_Hp=None, epsilon=1e-14,
                 logfunc=None, precond = None):
        super(ConjugateGradient, self).__init__(
            wrt, args=None, logfunc=logfunc)
        self.f_Hp = f_Hp if f_Hp is not None else lambda p: np.dot(H, p)
        self.b = b
        self.epsilon = epsilon
        self.precond = precond

    def solve(self, r):
        if self.precond is  None:
            return r
        elif self.precond.ndim == 1:
        #if the preconditioning matrix is diagonal,
        #then it is supposedly given as a vector
            return r / self.precond
        else:
            return scipy.linalg.solve(self.precond, r)

    def __iter__(self):
        grad = self.f_Hp(self.wrt) - self.b
        y = self.solve(grad)
        direction = -y
       
        # If the gradient is exactly zero, we stop. Otherwise, the
        # updates will lead to NaN errors because the direction will
        # be zero.
        if (grad == 0).all():
            self.logfunc({'message': 'gradient is 0'})
            return

        for i in range(self.wrt.size):
            Hp = self.f_Hp(direction)
            ry = np.dot(grad, y)                     
            pHp = np.inner(direction, Hp)
            step_length = ry / pHp
            self.wrt += step_length * direction            

            # We do this every few iterations to compensate for possible
            # numerical errors due to additions.
            if i % 10 == 0:
                grad = self.f_Hp(self.wrt) - self.b
            else:
                grad += step_length * Hp

            y = self.solve(grad)
            beta = np.dot(grad, y) / ry

            direction = - y + beta * direction

            # If we don't bail out here, we will enter regions of numerical
            # instability.
            if (abs(grad) < self.epsilon).all():
                self.logfunc(
                    {'message': 'converged - gradient smaller than epsilon'})
                break

            yield {
                'ry': ry,
                'Hp': Hp,
                'pHp': pHp,
                'step_length': step_length,
                'n_iter': i,
            }
