import os
import sys
import platform

def GetInstallationPaths(echo=False):
    path = os.path.dirname(os.path.dirname(__file__))
    PYTHONPATH = path

    if 'darwin' in platform.system().lower():
        # MAC OS INSTALL
        PV_PLUGIN_PATH = '%s/%s' % (path, 'PVPlugins')
        script = 'curl -s  https://raw.githubusercontent.com/OpenGeoVis/PVGeo/master/installMac.sh | sh -s'
        # Install launch agents
        print('Copy paste the following line(s) to execute in your bash terminal:\n')
        print('%s %s' % (script, PYTHONPATH))
        print('\n')
        if echo:
            print('PYTHONPATH=%s' % PYTHONPATH)
            print('PV_PLUGIN_PATH=%s' % PV_PLUGIN_PATH)
            print('\n')
    else:
        # WINDOWS INSTALL
        PV_PLUGIN_PATH = '%s\\%s' % (path, 'PVPlugins')
        print('We are assuming you are on Windows (Linux users beware!):')
        from os.path import expanduser
        path = expanduser("~")

        launcher = '''@ECHO OFF
SET PYTHONPATH=%s
SET PV_PLUGIN_PATH=%s
CALL "bin\paraview.exe"
''' % (PYTHONPATH, PV_PLUGIN_PATH)
        launcher = launcher.replace(r'\n', '\r\n') # Windows Line-Endings
        filename = '%s\\Desktop\\PVGeoLauncher.bat' % path
        if echo:
            print('Contents of `%s`:' % filename)
            print(launcher)
            print('\n')
        else:
            with open(filename, 'w') as f:
                f.write(launcher)
            print('Please follow installation instructions to create a shortcut for the new file: `%s`' % filename)
    return




if __name__ == '__main__':
    arg1 = sys.argv[1]
    echo = False
    if len(sys.argv) == 3 and sys.argv[2].lower() == 'echo':
        echo = True
    if arg1.lower() == 'install':
        GetInstallationPaths(echo=echo)
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
