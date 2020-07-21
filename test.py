# Licensed under a 3-clause BSD style license - see LICENSE.rst

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
from Ska.Matplotlib import plot_cxctime, cxctime2plotdate
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


def test_cxctime2plotdate():
    from cxotime import CxoTime
    from Chandra.Time import DateTime
    ct = CxoTime(np.arange(30) * 10015. + 1e8)
    dt = DateTime(np.arange(30) * 10015. + 1e8)

    plot_dates_ref = dt.plotdate

    plt.figure(0)
    vals = ct.secs - ct.secs[0]
    offset = 0
    for attr in ('secs', 'date', 'greta', None):
        for converter in (list, lambda x: x):
            for t_in in (ct, dt):
                times = converter(getattr(t_in, attr)) if attr else t_in
                plot_dates = cxctime2plotdate(times)
                assert np.allclose(plot_dates, plot_dates_ref, rtol=0, atol=1e-8)

                # Make sure plot_cxctime does not crashi
                plot_cxctime(times, vals + offset, color=None,
                             label=f'{attr} {converter is list} {t_in is ct}')
                offset += 5000

    plt.legend(fontsize='small')
    plt.savefig('test-time-inputs.png')
