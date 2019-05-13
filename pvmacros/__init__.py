"""
We will from now on refer to macros as a set of standard codes that can be used
regardless of data sets or scenes in ParaView. ParaView's sense of macro is not
robust enough for us so that we will be referring to traditional macros in
ParaView as 'scripts' from here on.

*Scripts are used on specific sets of data whereas macros can be used on any
set of data.*

Macros, all of the ``pvmacros`` module, are standard codes that can be used
regardless of data sets or scenes in ParaView. These codes complete tedious or
recurring tasks either in ParaView's GUI or ParaView's batch processing
environment. We will use macros to complete everyday tasks like saving
screenshots of isometric views of a data scene or tedious tasks like making
many slices of a single data set along a line.
"""

from . import export
from . import vis
from .pipeline import *

__author__ = 'Bane Sullivan'
__license__ = 'BSD-3-Clause'
__copyright__ = '2018, Bane Sullivan'
__version__ = '2.0.0'


__displayname__ = 'ParaView Macros'
