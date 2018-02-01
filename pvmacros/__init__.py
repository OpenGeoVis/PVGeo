__all__ = [
    "export",
    "vis"
]

from paraview.simple import LoadPlugin
import os

os.path.abspath(__file__)
PVPATH = "%s/../plugins/" % os.path.abspath(__file__)
filters = [f for f in os.listdir(PVPATH) if f.endswith(".xml")]
for f in filters:
    LoadPlugin(PVPATH + f, remote=True, ns=globals())
