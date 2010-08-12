#!/usr/bin/env python

import numpy as np
from matplotlib import pylab
from Ska.Matplotlib import histOutline

if __name__ == "__main__":
    binsIn = np.arange(0, 1, 0.1)
    angle = pylab.rand(50)

    pylab.subplot(121)
    pylab.hist(angle,binsIn)
    pylab.title("regular histogram")
    pylab.axis(xmax=1.0)

    pylab.subplot(122)

    (bins, data) = histOutline(angle, binsIn)
    pylab.plot(bins, data, 'k-', linewidth=2)
    pylab.title("histOutline Demo")
    pylab.show()


