import os
import sys
import platform

def GetInstallationPaths():
    path = os.path.dirname(os.path.dirname(__file__))
    PYTHONPATH = path
    PV_PLUGIN_PATH = '%s/%s' % (path, 'PVPlugins')

    script = 'sudo sh "$(curl -fsl https://raw.github.com/OpenGeoVis/PVGeo/blob/master/installMac.sh)"'

    if 'darwin' in platform.system().lower():
        # Install launch agents
        print('Copy paste the following line(s) to execute in your bash terminal:')
        print('%s %s' % (script, PYTHONPATH))
    else:
        print('Set these environmental variables to use PVGeo in ParaView:')
        print('export PYTHONPATH="%s"' % PYTHONPATH)
        print('export PV_PLUGIN_PATH="%s"' % PV_PLUGIN_PATH)
    return




if __name__ == '__main__':
    from .__tester__ import test
    arg = sys.argv[1]
    if arg.lower() == 'test':
        test(True)
    elif arg.lower() == 'install':
        GetInstallationPaths()
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
