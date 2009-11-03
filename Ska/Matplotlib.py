"""Provide useful utilities for matplotlib."""

import warnings
import datetime
from matplotlib import pyplot
from matplotlib.dates import (YearLocator, MonthLocator, DayLocator,
                              HourLocator, MinuteLocator, SecondLocator,
                              date2num, DateFormatter)
import Chandra.Time
import numpy

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

def set_time_ticks(plt, ticklocs=None, biggest=False):
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
        if len(majorticklocs) >= 5 or biggest:
            break

    return ((majorLoc, major_kwargs, major_fmt, minorLoc, minor_kwargs), )

def remake_ticks(event):
    """Remake the date ticks for the current plot if space is pressed.  If '0'
    is pressed then set the date ticks to the maximum possible range.
    """
    if event.key in (' ', '0'):
        fig = event.canvas.figure
        ax = fig.gca()
        biggest = event.key == '0'
        ticklocs = set_time_ticks(ax, biggest=biggest)
        fig.show()
    
def plot_cxctime(times, y, fmt='-b', fig=None, **kwargs):
    """Make a date plot where the X-axis values are in CXC time.  If no ``fig``
    value is supplied then the current figure will be used (and created
    automatically if needed).  Any additional keyword arguments
    (e.g. ``fmt='b-'``) are passed through to the ``plot_date()`` function.

    :param times: CXC time values for x-axis (date)
    :param y: y values
    :param fmt: plot format (default = '-b')
    :param fig: pyplot figure object (optional)
    :param **kwargs: keyword args passed through to ``plot_date()``

    :rtype: ticklocs, fig, ax = tick locations, figure, and axes object.
    """

    # Version 0.03 took 'fig' as the third argument.  Check for this and
    # issue deprecation warning.  Now the optional 3rd arg is format (which
    # follows the convention for plot()).
    if hasattr(fmt, 'gca'):
        warnings.warn('Fig argument must be passed by keyword now', DeprecationWarning, stacklevel=2)
        fig = fmt
        fmt = '-b'

    if fig is None:
        fig = pyplot.gcf()

    ax = fig.gca()
    ax.plot_date(cxctime2plotdate(times), y, fmt=fmt, **kwargs)
    ticklocs = set_time_ticks(ax)
    fig.autofmt_xdate()

    # If plotting interactively then show the figure and enable interactive resizing
    if hasattr(fig, 'show'):
        fig.show()
        cid = fig.canvas.mpl_connect('key_release_event', remake_ticks)

    return ticklocs, fig, ax

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

    try:
        return (times - times[0]) / 86400. + plotdate0
    except TypeError:
        return (numpy.array(times) - times[0]) / 86400. + plotdate0
        

def pointpair(x, y=None):
    """Interleave and then flatten two arrays ``x`` and ``y``.  This is
    typically useful for making a histogram style plot where ``x`` and ``y``
    are the bin start and stop respectively.  If no value for ``y`` is provided then
    ``x`` is used.

    Example::

      from Ska.Matplotlib import pointpair
      x = numpy.arange(1, 100, 5)
      x0 = x[:-1]
      x1 = x[1:]
      y = numpy.random.uniform(len(x0))
      xpp = pointpair(x0, x1)
      ypp = pointpair(y)
      plot(xpp, ypp)

    :x: left edge value of point pairs
    :y: right edge value of point pairs (optional)
    :rtype: numpy.array of length 2*len(x) == 2*len(y)
    """
    if y is None:
        y = x
    return numpy.array([x, y]).reshape(-1, order='F')

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

        fig = pyplot.figure(1)
        fig.clf()
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
