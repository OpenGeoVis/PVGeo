__all__ = [
    'check_numpy',
]

__displayname__ = 'Version Verifier'

try:
    from ._helpers import PVGeoError
except ImportError:
    PVGeoError = RuntimeError

def check_numpy(alert='print'):
    """A method to check the active environment's version of NumPy for
    compatibility with PVGeo.

    Args:
        alert (str): raise a ``'warn'`` (warning) or an ``'error'`` (PVGeoError) if NumPy is not at a satisfactory version.
    """
    import numpy as np
    import warnings
    v = np.array(np.__version__.split('.')[0:2], dtype=int)
    if v[0] >= 1 and v[1] >= 10:
        return True
    msg = 'WARNING: Your version of NumPy is below 1.10.x (you are using %s), please update the NumPy module used in ParaView for performance enhancement. Some filters/readers may be unavailable or crash otherwise.' % np.__version__
    if alert == 'error':
        raise PVGeoError(msg)
    elif alert == 'warn':
        warnings.warn(msg)
    elif alert == 'print':
        print(msg)
    return False
