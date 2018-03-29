import pydoc
import os
import sys

module_header = "## `{}` Documentation\n"
class_header = "## Class `{}` \n"
function_header = "### `{}` \n"


def getmarkdown(module):
    output = [module_header.format(module.__name__)]

    if module.__doc__:
        output.append(module.__doc__.replace('\n    ','\n'))

    output.extend(getfunctions(module))
    return "\n".join((str(x) for x in output))



def generatedocs(module):
    try:
        sys.path.append(os.getcwd())
        # Attempt import
        mod = pydoc.safeimport(module)
        if mod is None:
            print("Module not found")

        # Module imported correctly, let's create the docs
        return getmarkdown(mod)
    except pydoc.ErrorDuringImport as e:
        print("Error while trying to import " + module)

if __name__ == '__main__':
    docs = generatedocs(sys.argv[1])
    """with open(sys.argv[2], 'w') as f:
        f.write(docs)"""
    print(docs)
