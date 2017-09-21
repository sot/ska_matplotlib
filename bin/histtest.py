#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
from matplotlib import pylab
from Ska.Matplotlib import hist_outline

if __name__ == "__main__":
    binsIn = np.arange(0, 1, 0.1)
    angle = pylab.rand(50)

    pylab.subplot(121)
    pylab.hist(angle,binsIn)
    pylab.title("regular histogram")
    pylab.axis(xmax=1.0)

    pylab.subplot(122)

    (bins, data) = hist_outline(angle, binsIn)
    pylab.plot(bins, data, 'k-', linewidth=2)
    pylab.title("hist_outline Demo")
    pylab.show()


