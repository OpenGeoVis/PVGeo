import os
import sys
import platform

def GetInstallationPaths(echo=False):
    path = os.path.dirname(os.path.dirname(__file__))
    PYTHONPATH = path

    ###### MAC ######
    if 'darwin' in platform.system().lower():
        # MAC OS INSTALL
        print('We are assuming you are on Mac OS:')
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
    ##### LINUX #####
    elif  'linux' in platform.system().lower():
        print('We are assuming you are on Linux OS:')
        PV_PLUGIN_PATH = '%s/%s' % (path, 'PVPlugins')
        # TODO: only print if echo and run an installation script
        print('\n')
        print('PYTHONPATH=%s' % PYTHONPATH)
        print('PV_PLUGIN_PATH=%s' % PV_PLUGIN_PATH)
        print('\n')
    ##### WINDOWS ######
    elif 'win' in platform.system().lower():
        # WINDOWS INSTALL
        PV_PLUGIN_PATH = '%s\\%s' % (path, 'PVPlugins')
        print('We are assuming you are on Windows OS:')
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
    else:
        print('Unknown operating system. Please post an issues for PVGeo: https://github.com/OpenGeoVis/PVGeo/issues/')
        PV_PLUGIN_PATH = '%s/%s' % (path, 'PVPlugins')
        print('\n')
        print('PYTHONPATH=%s' % PYTHONPATH)
        print('PV_PLUGIN_PATH=%s' % PV_PLUGIN_PATH)
        print('\n')
    return




if __name__ == '__main__':
    arg1 = sys.argv[1]
    echo = False
    if len(sys.argv) == 3 and sys.argv[2].lower() == 'echo':
        echo = True
    if arg1.lower() == 'install':
        GetInstallationPaths(echo=echo)
    elif arg1.lower() == 'test':
        print('testing is now deprecated for deployed versions of PVGeo.')
    elif arg1.lower() == 'which':
        # Telling the user where PVGeo is installed
        print(os.path.dirname(__file__))
    else:
        raise RuntimeError('Unknown argument: %s' % arg)
