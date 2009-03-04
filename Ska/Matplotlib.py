"""Provide useful utilities for matplotlib."""


import pylab
import datetime
from matplotlib.dates import (YearLocator, MonthLocator, DayLocator,
                              HourLocator, MinuteLocator, SecondLocator,
                              date2num, DateFormatter)
import Chandra.Time

# Default tick locator and format specification for making nice time axes
TICKLOCS = ((YearLocator, {'base': 5}, '%Y',    YearLocator, {'base': 1}),
            (YearLocator, {'base': 4}, '%Y',    YearLocator, {'base': 1}),
            (YearLocator, {'base': 2}, '%Y',    YearLocator, {'base': 1}),
            (YearLocator, {'base': 1}, '%Y', MonthLocator, {'bymonth': (1, 4, 7, 10)}),
            (MonthLocator, {'bymonth': range(1, 13, 6)}, '%Y-%b', MonthLocator, {}),
            (MonthLocator, {'bymonth': range(1, 13, 4)}, '%Y-%b', MonthLocator, {}),
            (MonthLocator, {'bymonth': range(1, 13, 3)}, '%Y-%b', MonthLocator, {}),
            (MonthLocator, {'bymonth': range(1, 13, 2)}, '%Y-%b', MonthLocator, {}),
            (MonthLocator, {},         '%Y-%b', DayLocator, {'bymonthday': (1, 15)}),

            (DayLocator, {'interval': 10}, '%Y:%j', DayLocator, {}),
            (DayLocator, {'interval': 5}, '%Y:%j', DayLocator, {}),
            (DayLocator, {'interval': 4}, '%Y:%j', DayLocator, {}),
            (DayLocator, {'interval': 2}, '%Y:%j', DayLocator, {}),
            (DayLocator, {'interval': 1}, '%Y:%j', HourLocator, {'byhour': (0, 6, 12, 18)}),

            (HourLocator, {'byhour': range(0, 24, 12)}, '%j:%H:00', HourLocator, {}),
            (HourLocator, {'byhour': range(0, 24, 6)}, '%j:%H:00', HourLocator, {}),
            (HourLocator, {'byhour': range(0, 24, 4)}, '%j:%H:00', HourLocator, {}),
            (HourLocator, {'byhour': range(0, 24, 2)}, '%j:%H:00', HourLocator, {}),
            (HourLocator, {}, '%j:%H:00', MinuteLocator, {'byminute': (0, 15, 30, 45)}),

            (MinuteLocator, {'byminute': (0, 30)}, '%j:%H:%M', MinuteLocator, {'byminute': range(0,60,5)}),
            (MinuteLocator, {'byminute': (0, 15, 30, 45)}, '%j:%H:%M', MinuteLocator, {'byminute': range(0,60,5)}),
            (MinuteLocator, {'byminute': range(0, 60, 10)}, '%j:%H:%M', MinuteLocator, {}),
            (MinuteLocator, {'byminute': range(0, 60, 5)}, '%j:%H:%M', MinuteLocator, {}),
            (MinuteLocator, {'byminute': range(0, 60, 4)}, '%j:%H:%M', MinuteLocator, {}),
            (MinuteLocator, {'byminute': range(0, 60, 2)}, '%j:%H:%M', MinuteLocator, {}),
            (MinuteLocator, {}, '%j:%H:%M', SecondLocator, {'bysecond': (0, 15, 30, 45)}),

            (SecondLocator, {'bysecond': (0, 30)}, '%H:%M:%S', SecondLocator, {'bysecond': range(0,60,5)}),
            (SecondLocator, {'bysecond': (0, 15, 30, 45)}, '%H:%M:%S', SecondLocator, {'bysecond': range(0,60,5)}),
            (SecondLocator, {'bysecond': range(0, 60, 10)}, '%H:%M:%S', SecondLocator, {}),
            (SecondLocator, {'bysecond': range(0, 60, 5)}, '%H:%M:%S', SecondLocator, {}),
            (SecondLocator, {'bysecond': range(0, 60, 4)}, '%H:%M:%S', SecondLocator, {}),
            (SecondLocator, {'bysecond': range(0, 60, 2)}, '%H:%M:%S', SecondLocator, {}),
            (SecondLocator, {}, '%H:%M:%S', SecondLocator, {}),
            )

def set_time_ticks(plt, ticklocs=None):
    """
    Pick nice values to show time ticks in a date plot.

    Example::
    
      x = cxctime2plotdate(numpy.linspace(0, 3e7, 20))
      y = numpy.random.normal(size=len(x))

      fig = pylab.figure()
      plt = fig.add_subplot(1, 1, 1)
      plt.plot_date(x, y, fmt='b-')
      ticklocs = set_time_ticks(plt)

      fig.autofmt_xdate()
      fig.show()

    The returned value of ``ticklocs`` can be used in subsequent date plots to
    force the same major and minor tick locations and formatting.  Note also
    the use of the high-level fig.autofmt_xdate() convenience method to configure
    vertically stacked date plot(s) to be well-formatted.

    :param plt: ``matplotlib.axes.AxesSubplot`` object (from ``pylab.figure.add_subplot``)
    :param ticklocs: list of major/minor tick locators ala the default ``TICKLOCS``
    :rtype: tuple with selected ticklocs as first element
    """
    # def make_outputs(opt, states, times, T_pin, T_dea):

    locs = ticklocs or TICKLOCS

    for majorLoc, major_kwargs, major_fmt, minorLoc, minor_kwargs in locs:
        plt.xaxis.set_major_locator(majorLoc(**major_kwargs))
        plt.xaxis.set_minor_locator(minorLoc(**minor_kwargs))
        plt.xaxis.set_major_formatter(DateFormatter(major_fmt))

        majorticklocs = plt.xaxis.get_ticklocs()
        if len(majorticklocs) >= 5:
            break

    return ((majorLoc, major_kwargs, major_fmt, minorLoc, minor_kwargs), )

def cxctime2plotdate(times):
    """
    Convert input CXC time (sec) to the time base required for the matplotlib
    plot_date function (days since start of year 1).
    
    :param times: iterable list of times
    :rtype: plot_date times
    """
    
    # Find the plotdate of first time and use a relative offset from there
    t0 = Chandra.Time.DateTime(times[0])
    datetime0 = datetime.datetime(*(t0.mxDateTime.tuple()[:7]))
    plotdate0 = date2num(datetime0)

    return [(x - times[0]) / 86400. + plotdate0 for x in times]

def _check_many_sizes():
    """Run through a multiplicative series of x-axis lengths and visually confirm that
    chosen axes are OK."""
    import numpy 
    import time

    dt = 6.
    while True:
        print dt
        t0 = numpy.random.uniform(3e7*10)
        times = numpy.linspace(t0, t0+dt, 20)
        x = cxctime2plotdate(times)
        y = numpy.random.normal(size=len(times))

        pylab.clf()
        fig = pylab.figure(1)
        plt1 = fig.add_subplot(1, 1, 1)
        plt1.plot_date(x, y, fmt='b-')

        locs = set_time_ticks(plt1)

        fig.autofmt_xdate()
        fig.show()
        time.sleep(0.5)
        dt *= 1.1
        if dt > 1e9:
            break
        
if __name__ == '__main__':
    _check_many_sizes()
