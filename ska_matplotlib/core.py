# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Provide useful utilities for matplotlib."""

from matplotlib.dates import (YearLocator, MonthLocator, DayLocator,
                              HourLocator, MinuteLocator, SecondLocator,
                              DateFormatter, date2num)
from matplotlib.ticker import FixedLocator, FixedFormatter
from Chandra.Time import DateTime
from cxotime import CxoTime
import numpy as np

# Default tick locator and format specification for making nice time axes
TICKLOCS = ((YearLocator, {'base': 5}, '%Y',    YearLocator, {'base': 1}),
            (YearLocator, {'base': 4}, '%Y',    YearLocator, {'base': 1}),
            (YearLocator, {'base': 2}, '%Y',    YearLocator, {'base': 1}),
            (YearLocator, {'base': 1}, '%Y', MonthLocator, {'bymonth': (1, 4, 7, 10)}),
            (MonthLocator, {'bymonth': list(range(1, 13, 6))}, '%Y-%b', MonthLocator, {}),
            (MonthLocator, {'bymonth': list(range(1, 13, 4))}, '%Y-%b', MonthLocator, {}),
            (MonthLocator, {'bymonth': list(range(1, 13, 3))}, '%Y-%b', MonthLocator, {}),
            (MonthLocator, {'bymonth': list(range(1, 13, 2))}, '%Y-%b', MonthLocator, {}),
            (MonthLocator, {},         '%Y-%b', DayLocator, {'bymonthday': (1, 15)}),

            (DayLocator, {'interval': 10}, '%Y:%j', DayLocator, {}),
            (DayLocator, {'interval': 5}, '%Y:%j', DayLocator, {}),
            (DayLocator, {'interval': 4}, '%Y:%j', DayLocator, {}),
            (DayLocator, {'interval': 2}, '%Y:%j', DayLocator, {}),
            (DayLocator, {'interval': 1}, '%Y:%j', HourLocator, {'byhour': (0, 6, 12, 18)}),

            (HourLocator, {'byhour': list(range(0, 24, 12))}, '%j:%H:00', HourLocator, {}),
            (HourLocator, {'byhour': list(range(0, 24, 6))}, '%j:%H:00', HourLocator, {}),
            (HourLocator, {'byhour': list(range(0, 24, 4))}, '%j:%H:00', HourLocator, {}),
            (HourLocator, {'byhour': list(range(0, 24, 2))}, '%j:%H:00', HourLocator, {}),
            (HourLocator, {}, '%j:%H:00', MinuteLocator, {'byminute': (0, 15, 30, 45)}),

            (MinuteLocator, {'byminute': (0, 30)}, '%j:%H:%M', MinuteLocator, {'byminute': list(range(0,60,5))}),
            (MinuteLocator, {'byminute': (0, 15, 30, 45)}, '%j:%H:%M', MinuteLocator, {'byminute': list(range(0,60,5))}),
            (MinuteLocator, {'byminute': list(range(0, 60, 10))}, '%j:%H:%M', MinuteLocator, {}),
            (MinuteLocator, {'byminute': list(range(0, 60, 5))}, '%j:%H:%M', MinuteLocator, {}),
            (MinuteLocator, {'byminute': list(range(0, 60, 4))}, '%j:%H:%M', MinuteLocator, {}),
            (MinuteLocator, {'byminute': list(range(0, 60, 2))}, '%j:%H:%M', MinuteLocator, {}),
            (MinuteLocator, {}, '%j:%H:%M', SecondLocator, {'bysecond': (0, 15, 30, 45)}),

            (SecondLocator, {'bysecond': (0, 30)}, '%H:%M:%S', SecondLocator, {'bysecond': list(range(0,60,5))}),
            (SecondLocator, {'bysecond': (0, 15, 30, 45)}, '%H:%M:%S', SecondLocator, {'bysecond': list(range(0,60,5))}),
            (SecondLocator, {'bysecond': list(range(0, 60, 10))}, '%H:%M:%S', SecondLocator, {}),
            (SecondLocator, {'bysecond': list(range(0, 60, 5))}, '%H:%M:%S', SecondLocator, {}),
            (SecondLocator, {'bysecond': list(range(0, 60, 4))}, '%H:%M:%S', SecondLocator, {}),
            (SecondLocator, {'bysecond': list(range(0, 60, 2))}, '%H:%M:%S', SecondLocator, {}),
            (SecondLocator, {}, '%H:%M:%S', SecondLocator, {}),
            )

def set_time_ticks(plt, ticklocs=None):
    """
    Pick nice values to show time ticks in a date plot.

    Example::

      x = cxctime2plotdate(np.linspace(0, 3e7, 20))
      y = np.random.normal(size=len(x))

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

    locs = ticklocs or TICKLOCS

    for majorLoc, major_kwargs, major_fmt, minorLoc, minor_kwargs in locs:
        plt.xaxis.set_major_locator(majorLoc(**major_kwargs))
        plt.xaxis.set_minor_locator(minorLoc(**minor_kwargs))
        plt.xaxis.set_major_formatter(DateFormatter(major_fmt))

        majorticklocs = plt.xaxis.get_ticklocs()
        if len(majorticklocs) >= 5:
            break

    return ((majorLoc, major_kwargs, major_fmt, minorLoc, minor_kwargs), )

def remake_ticks(ax):
    """Remake the date ticks for the current plot if space is pressed.  If '0'
    is pressed then set the date ticks to the maximum possible range.
    """
    ticklocs = set_time_ticks(ax)
    ax.figure.canvas.draw_idle()

def plot_cxctime(times, y, fmt=None, fig=None, ax=None, yerr=None, xerr=None, tz=None,
                 state_codes=None, interactive=True, **kwargs):
    """Make a date plot where the X-axis values are in a CXC time compatible format.  If no ``fig``
    value is supplied then the current figure will be used (and created
    automatically if needed).  If yerr or xerr is supplied, ``errorbar()`` will
    be called and any additional keyword arguments will be passed to it.
    Otherwise any additional keyword arguments (e.g. ``fmt='b-'``) are passed
    through to the ``plot()`` function.  Also see ``errorbar()`` for an
    explanation of the possible forms of *yerr*/*xerr*.

    If the ``state_codes`` keyword argument is provided then the y-axis ticks and
    tick labels will be set accordingly.  The ``state_codes`` value must be a list
    of (raw_count, state_code) tuples, and is normally set to ``msid.state_codes``
    for an MSID object from fetch().

    If the ``interactive`` keyword is True (default) then the plot will be redrawn
    at the end and a GUI callback will be created which allows for on-the-fly
    update of the date tick labels when panning and zooming interactively.  Set
    this to False to improve the speed when making several plots.  This will likely
    require issuing a plt.draw() or fig.canvas.draw() command at the end.

    :param times: CXC time values for x-axis (DateTime compatible format, CxoTime)
    :param y: y values
    :param fmt: plot format (default None)
    :param fig: pyplot figure object (optional)
    :param yerr: error on y values, may be [ scalar | N, Nx1, or 2xN array-like ]
    :param xerr: error on x values in units of DAYS (may be [ scalar | N, Nx1, or 2xN array-like ] )
    :param tz: timezone string
    :param state_codes: list of (raw_count, state_code) tuples
    :param interactive: use plot interactively (default=True, faster if False)
    :param ``**kwargs``: keyword args passed through to ``plot()`` or ``errorbar()``

    :rtype: ticklocs, fig, ax = tick locations, figure, and axes object.
    """
    from matplotlib import pyplot

    if fig is None:
        fig = pyplot.gcf()

    if ax is None:
        ax = fig.gca()

    dates = cxctime2plotdate(times)
    args = () if fmt is None else (fmt,)

    if yerr is not None or xerr is not None:
        ax.errorbar(dates, y, yerr, xerr, *args, **kwargs)
    else:
        ax.plot(dates, y, *args, **kwargs)
    ax.xaxis_date(tz)

    ticklocs = set_time_ticks(ax)
    fig.autofmt_xdate()

    if state_codes is not None:
        counts, codes = zip(*state_codes)
        ax.yaxis.set_major_locator(FixedLocator(counts))
        ax.yaxis.set_major_formatter(FixedFormatter(codes))

    # If plotting interactively then show the figure and enable interactive resizing
    if interactive and hasattr(fig, 'show'):
        fig.canvas.draw_idle()
        ax.callbacks.connect('xlim_changed', remake_ticks)

    return ticklocs, fig, ax


def cxctime2plotdate(times):
    """
    Convert input CXC time (sec) to the time base required for the matplotlib
    plot_date function (days since start of year 1).

    For new code, do not use cxctime2plotdate and instead use the plot_date
    Time format from cxotime.CxoTime with ``CxoTime(times).plot_date``.

    :param times: times (any DateTime compatible format or object)
    :rtype: plot_date times
    """
    # Convert times to float array of CXC seconds
    if isinstance(times, (DateTime, CxoTime)):
        times = times.secs
    else:
        times = np.asarray(times)

        # If not floating point then use CxoTime to convert to seconds
        if times.dtype.kind != 'f':
            times = CxoTime(times).secs

    shape = times.shape

    # Zero-length input gives empty output
    if shape == (0,):
        return np.array([], dtype=np.float64)

    # Find the plotdate of first time and use a relative offset from there
    times = times.ravel()
    plotdate0 = date2num(CxoTime(times[0]).datetime)
    out = (times - times[0]) / 86400. + plotdate0

    return out.reshape(shape)


def pointpair(x, y=None):
    """Interleave and then flatten two arrays ``x`` and ``y``.  This is
    typically useful for making a histogram style plot where ``x`` and ``y``
    are the bin start and stop respectively.  If no value for ``y`` is provided then
    ``x`` is used.

    Example::

      from ska_matplotlib import pointpair
      x = np.arange(1, 100, 5)
      x0 = x[:-1]
      x1 = x[1:]
      y = np.random.uniform(len(x0))
      xpp = pointpair(x0, x1)
      ypp = pointpair(y)
      plot(xpp, ypp)

    :x: left edge value of point pairs
    :y: right edge value of point pairs (optional)
    :rtype: np.array of length 2*len(x) == 2*len(y)
    """
    if y is None:
        y = x
    return np.array([x, y]).reshape(-1, order='F')


def hist_outline(dataIn, *args, **kwargs):
    """
    histOutline from http://www.scipy.org/Cookbook/Matplotlib/UnfilledHistograms

    Make a histogram that can be plotted with plot() so that
    the histogram just has the outline rather than bars as it
    usually does.

    Example Usage:
    binsIn = np.arange(0, 1, 0.1)
    angle = pylab.rand(50)

    (bins, data) = histOutline(binsIn, angle)
    plot(bins, data, 'k-', linewidth=2)

    """

    (histIn, binsIn) = np.histogram(dataIn, *args, **kwargs)

    stepSize = binsIn[1] - binsIn[0]

    bins = np.zeros(len(binsIn)*2 + 2, dtype=float)
    data = np.zeros(len(binsIn)*2 + 2, dtype=float)
    for bb in range(len(binsIn)):
        bins[2*bb + 1] = binsIn[bb]
        bins[2*bb + 2] = binsIn[bb] + stepSize
        if bb < len(histIn):
            data[2*bb + 1] = histIn[bb]
            data[2*bb + 2] = histIn[bb]

    bins[0] = bins[1]
    bins[-1] = bins[-2]
    data[0] = 0
    data[-1] = 0

    return (bins, data)


def set_min_axis_range(ax, min_range, axis='y'):
    """
    Set the minimum range of the y- or x-axis limits of a matplotlib Axes object.

    This is used to prevent the axis limits from being set to a very small range.

    :param ax: matplotlib Axes object
    :param min_range: minimum range of the axis
    :param axis: axis to set (default 'y', also allowed 'x')
    """
    set_lim = getattr(ax, f'set_{axis}lim')
    get_lim = getattr(ax, f'get_{axis}lim')

    lim0, lim1 = get_lim()
    if abs(lim1 - lim0) < min_range:
        lim_mean = (lim0 + lim1) / 2
        sign = 1 if lim1 > lim0 else -1
        set_lim(lim_mean - sign * min_range / 2, lim_mean + sign * min_range / 2)
