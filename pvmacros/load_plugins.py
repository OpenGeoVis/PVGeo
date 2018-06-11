
def loadPVGeoplugins():
    from paraview.simple import LoadPlugin
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # TODO: need directory not file
    PVPATH = "%s/../plugins/" % dir_path
    filters = [f for f in os.listdir(PVPATH) if f.endswith(".xml")]
    for f in filters:
        LoadPlugin(PVPATH + f, remote=True, ns=globals())
