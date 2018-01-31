from evaluator import standardize, evaluate
import numpy as np


def test_evaluator():
    vals = [x for x in range(8)]
    mean = np.nanmean(vals)
    stdv = np.nanstd(vals)

    for i in range(8):
        assert evaluate(standardize(i, mean, stdv), 8) == i + 1
