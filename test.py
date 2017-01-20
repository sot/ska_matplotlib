from __future__ import print_function, division

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from Ska.Matplotlib import plot_cxctime
from Ska.Matplotlib.lineid_plot import plot_line_ids
import pytest

np.random.seed(1)


dts = 6 * 2 ** np.arange(28)  # Max of about 25 years


@pytest.mark.parametrize('dt', dts)
def test_check_many_sizes(dt):
    """
    Run through a multiplicative series of x-axis lengths and visually
    confirm that chosen axes are OK.
    """
    plt.close(0)
    plt.figure(0)

    t0 = np.random.uniform(3e7 * 10)
    times = np.linspace(t0, t0 + dt, 20)
    y = np.random.normal(size=len(times))
    plot_cxctime(times, y)

    plt.savefig('test-{:09d}.png'.format(dt))


def test_lineid():
    """Minimal test of plotting line IDs.  Note the test of duplicate line labels"""
    plt.figure()
    plot_line_ids(np.arange(100), np.random.uniform(size=100),
                  np.linspace(10, 90, 10),
                  ['line{}'.format(ii) for ii in
                   (0, 0, 0, 1, 1, 2, 3, 4, 5, 6)])
    plt.savefig('test-lineid.png')
