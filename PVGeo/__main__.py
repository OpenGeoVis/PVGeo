import os
import sys
import platform

def GetInstallationPaths():
    path = os.path.dirname(os.path.dirname(__file__))
    PYTHONPATH = path
    PV_PLUGIN_PATH = '%s/%s' % (path, 'PVPlugins')

    script = 'curl -s  https://cdn.rawgit.com/OpenGeoVis/PVGeo/be9e9a95/installMac.sh | sh -s'

    if 'darwin' in platform.system().lower():
        # Install launch agents
        print('Copy paste the following line(s) to execute in your bash terminal:\n')
        print('%s %s' % (script, PYTHONPATH))
        print('\n')
    else:
        print('Set these environmental variables to use PVGeo in ParaView:')
        print('\n')
        print('export PYTHONPATH="%s"' % PYTHONPATH)
        print('export PV_PLUGIN_PATH="%s"' % PV_PLUGIN_PATH)
        print('\n')
    return




if __name__ == '__main__':
    from .tester import test
    arg = sys.argv[1]
    if arg.lower() == 'test':
        test(True)
    elif arg.lower() == 'install':
        GetInstallationPaths()
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
