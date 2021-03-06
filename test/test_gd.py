import itertools

import nose
import numpy as np

from climin import GradientDescent

from losses import Quadratic, LogisticRegression, Rosenbrock


def test_gd_quadratic():
    obj = Quadratic()
    opt = GradientDescent(
        obj.pars, obj.fprime, steprate=0.01, momentum=.9)
    for i, info in enumerate(opt):
        if i > 500:
            break
    assert obj.solved(), 'did not find solution'


@nose.tools.nottest
def test_gd_rosen():
    obj = Rosenbrock()
    opt = GradientDescent(
        obj.pars, obj.fprime, steprate=0.01, momentum=.9)
    for i, info in enumerate(opt):
        if i > 5000:
            break
    assert ((1 - obj.pars) < 0.01).all(), 'did not find solution'


def test_gd_lr():
    obj = LogisticRegression()
    args = itertools.repeat(((obj.X, obj.Z), {}))
    opt = GradientDescent(
        obj.pars, obj.fprime, steprate=0.01, momentum=.9, args=args)
    for i, info in enumerate(opt):
        if i > 500:
            break
    assert obj.solved(), 'did not find solution'


def test_gd_quadratic_nesterov():
    obj = Quadratic()
    opt = GradientDescent(
        obj.pars, obj.fprime, steprate=0.01, momentum=.9,
        momentum_type='nesterov')
    for i, info in enumerate(opt):
        if i > 500:
            break
    assert obj.solved(), 'did not find solution'


@nose.tools.nottest
def test_gd_rosen_nesterov():
    obj = Rosenbrock()
    opt = GradientDescent(
        obj.pars, obj.fprime, steprate=0.01, momentum=.9,
        momentum_type='nesterov')
    for i, info in enumerate(opt):
        if i > 5000:
            break
    assert ((1 - obj.pars) < 0.01).all(), 'did not find solution'


def test_gd_lr_nesterov():
    obj = LogisticRegression()
    args = itertools.repeat(((obj.X, obj.Z), {}))
    opt = GradientDescent(
        obj.pars, obj.fprime, steprate=0.01, momentum=.9,
        momentum_type='nesterov',
        args=args)
    for i, info in enumerate(opt):
        if i > 500:
            break
    assert obj.solved(), 'did not find solution'
