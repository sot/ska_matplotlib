from __future__ import print_function, division

import numpy as np
from Ska.Matplotlib import plot_cxctime, cxctime2plotdate, set_time_ticks
import matplotlib.pyplot as plt


def test_non_interactive():
    x = 4e8 + np.arange(1000) / 200.
    y = x - 4e8
    plot_cxctime(x, y)
    plt.savefig('test.png')


def test_check_many_sizes():
    """Run through a multiplicative series of x-axis lengths and visually
    confirm that chosen axes are OK."""
    plt.ion()
    dt = 6
    while True:
        print(dt)
        t0 = np.random.uniform(3e7 * 10)
        times = np.linspace(t0, t0 + dt, 20)
        x = cxctime2plotdate(times)
        y = np.random.normal(size=len(times))

        fig = plt.figure(1)
        fig.clf()
        plt1 = fig.add_subplot(1, 1, 1)
        plt1.plot_date(x, y, fmt='b-')

        set_time_ticks(plt1)

        fig.autofmt_xdate()
        plt.savefig('test-{:09d}.png'.format(dt))
        dt *= 2
        if dt > 1e9:
            break
